import logging
import asyncio
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_time_interval, async_track_state_change_event
from homeassistant.components import camera
from homeassistant.components.vacuum import VacuumActivity
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_AUGMENTATIONS
from .map_utils import extract_map_from_image, unpack_pixels, approximate_segment

_LOGGER = logging.getLogger(__name__)

INTERVAL_ACTIVE = timedelta(seconds=2)
INTERVAL_IDLE = timedelta(seconds=60)

ACTIVE_STATES = {
    VacuumActivity.CLEANING,
    VacuumActivity.RETURNING,
}


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Valetudo sensors."""
    if config_entry.data.get(CONF_ENTRY_TYPE) != ENTRY_TYPE_AUGMENTATIONS:
        return

    manager = ValetudoSensorManager(hass, async_add_entities, config_entry.entry_id)
    await manager.async_setup()

    # Store manager reference
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][config_entry.entry_id] = manager

    config_entry.async_on_unload(manager.async_unload)


class ValetudoSensorManager:
    """
    Manages creation and removal of sensors for Valetudo devices.
    Watches the registry to handle device lifecycle events (creation/deletion via MQTT).
    """

    def __init__(self, hass: HomeAssistant, async_add_entities: AddEntitiesCallback, config_entry_id: str):
        self.hass = hass
        self.async_add_entities = async_add_entities
        self.config_entry_id = config_entry_id

        # Map device_id -> List of sensor entities
        self._sensors: dict[str, list[SensorEntity]] = {}
        self._listeners = []

    async def async_setup(self):
        self._scan_existing_devices()

        self._listeners.append(self.hass.bus.async_listen(
            dr.EVENT_DEVICE_REGISTRY_UPDATED,
            self._handle_device_registry_update
        ))

        self._listeners.append(self.hass.bus.async_listen(
            er.EVENT_ENTITY_REGISTRY_UPDATED,
            self._handle_entity_registry_update
        ))

    @callback
    def async_unload(self):
        for unsub in self._listeners:
            unsub()
        self._listeners.clear()
        self._sensors.clear()

    def _scan_existing_devices(self):
        dev_reg = dr.async_get(self.hass)
        for device in dev_reg.devices.values():
            if device.manufacturer == "Valetudo":
                self._try_add_sensors(device.id)

    @callback
    def _handle_device_registry_update(self, event: Event):
        """Handle explicit device removal events."""
        action = event.data.get("action")
        device_id = event.data.get("device_id")

        if action == "remove" and device_id in self._sensors:
            _LOGGER.debug(f"Device {device_id} removed. Cleaning up sensors.")
            sensors = self._sensors.pop(device_id)
            for sensor in sensors:
                if sensor.hass:
                    self.hass.async_create_task(sensor.async_remove())
            return

        if action in ("create", "update"):
            dev_reg = dr.async_get(self.hass)
            device = dev_reg.async_get(device_id)
            if device and device.manufacturer == "Valetudo":
                self._try_add_sensors(device_id)

    @callback
    def _handle_entity_registry_update(self, event: Event):
        """Handle entity removal (e.g. MQTT device deletion) to clean up orphaned augmentation devices."""
        action = event.data.get("action")
        entity_id = event.data.get("entity_id")
        ent_reg = er.async_get(self.hass)

        if action == "create":
            entry = ent_reg.async_get(entity_id)
            if entry and entry.device_id:
                self._try_add_sensors(entry.device_id)
            return

        if action == "remove":
            # Check for orphaned devices (Last Man Standing logic)
            # We must check all managed devices as we don't know which device the removed entity belonged to.
            for device_id, sensors in list(self._sensors.items()):
                device_entities = er.async_entries_for_device(ent_reg, device_id)

                # Check if there are any entities belonging to OTHER config entries (e.g. MQTT)
                other_config_entries = False
                for entry in device_entities:
                    if entry.config_entry_id != self.config_entry_id:
                        other_config_entries = True
                        break

                # If NO other config entries exist for this device, it means the
                # original integration (MQTT) is gone.
                if not other_config_entries:
                    # 1. Remove our Sensor Entities
                    for sensor in sensors:
                        if sensor.hass:
                            self.hass.async_create_task(sensor.async_remove())

                    del self._sensors[device_id]

                    # 2. Delete the Device Entry from the Registry
                    # We must perform this cleanup, otherwise the device remains as an empty shell.
                    dev_reg = dr.async_get(self.hass)
                    dev_reg.async_remove_device(device_id)

    def _try_add_sensors(self, device_id: str):
        dev_reg = dr.async_get(self.hass)
        device = dev_reg.async_get(device_id)

        if not device or device.manufacturer != "Valetudo":
            return

        ent_reg = er.async_get(self.hass)
        device_entities = er.async_entries_for_device(ent_reg, device_id)

        map_entity = next(
            (e for e in device_entities
             if e.domain == "camera" and e.entity_id.endswith("_map_data")),
            None
        )
        vacuum_entity = next(
            (e for e in device_entities if e.domain == "vacuum"),
            None
        )

        if not vacuum_entity or not map_entity:
            return

        if device_id not in self._sensors:
            self._sensors[device_id] = []

        sensor_classes = [ValetudoEstimatedSegmentSensor]

        new_entities = []
        for Cls in sensor_classes:
            if any(isinstance(s, Cls) for s in self._sensors[device_id]):
                continue

            _LOGGER.debug(f"Creating {Cls.__name__} for device {device.name}")
            sensor = Cls(self.hass, device, map_entity.entity_id, vacuum_entity.entity_id)
            self._sensors[device_id].append(sensor)
            new_entities.append(sensor)

        if new_entities:
            self.async_add_entities(new_entities)


class ValetudoEstimatedSegmentSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Estimated Segment"
    _attr_icon = "mdi:floor-plan"
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, device: dr.DeviceEntry, map_entity_id: str, vacuum_entity_id: str):
        self.hass = hass
        self._map_entity_id = map_entity_id
        self._vacuum_entity_id = vacuum_entity_id
        self._device_info = device
        self._attr_unique_id = f"{device.id}_estimated_segment"
        self._attr_device_info = {
            "connections": device.connections,
            "identifiers": device.identifiers,
        }
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

        self._attr_available = False

        self._last_nonce = None
        self._process_lock = asyncio.Lock()
        self._timer_unsub = None

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._vacuum_entity_id], self._handle_vacuum_update
            )
        )
        self.async_on_remove(self._stop_timer)

        state_obj = self.hass.states.get(self._vacuum_entity_id)
        initial_state = state_obj.state if state_obj else STATE_UNKNOWN
        self._handle_state_update(initial_state)

    @callback
    def _handle_vacuum_update(self, event):
        new_state = event.data.get("new_state")
        state_str = new_state.state if new_state else STATE_UNKNOWN
        self._handle_state_update(state_str)

    def _handle_state_update(self, state: str):
        if state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            self._attr_available = False
            self._stop_timer()
            self._last_nonce = None
            self.async_write_ha_state()
            return

        was_unavailable = not self._attr_available
        self._attr_available = True

        target_interval = INTERVAL_ACTIVE if state in ACTIVE_STATES else INTERVAL_IDLE
        self._schedule_timer(target_interval)

        if was_unavailable or target_interval == INTERVAL_ACTIVE:
            self.hass.async_create_task(self._check_map_update(None))

    def _schedule_timer(self, interval: timedelta):
        self._stop_timer()
        self._timer_unsub = async_track_time_interval(
            self.hass, self._check_map_update, interval
        )

    def _stop_timer(self):
        if self._timer_unsub:
            self._timer_unsub()
            self._timer_unsub = None

    async def _check_map_update(self, _):
        """Called by timer to check the camera entity for new data."""
        if self._process_lock.locked():
            return

        async with self._process_lock:
            try:
                image_obj = await camera.async_get_image(self.hass, self._map_entity_id)
                image_bytes = image_obj.content
            except Exception:
                return

            try:
                raw_map_data = await self.hass.async_add_executor_job(
                    extract_map_from_image,
                    image_bytes
                )
            except Exception:
                return

            if not raw_map_data:
                return

            current_nonce = raw_map_data.get("metaData", {}).get("nonce")
            if current_nonce and current_nonce == self._last_nonce:
                return

            self._last_nonce = current_nonce

            try:
                segment_info = await self.hass.async_add_executor_job(
                    self._approximate_segment,
                    raw_map_data
                )

                if segment_info:
                    self._attr_native_value = segment_info.get("name") or f"Segment {segment_info.get('id')}"
                    self._attr_extra_state_attributes = {
                        "segment_id": segment_info.get("id"),
                    }
                else:
                    self._attr_native_value = "Unknown"
                    self._attr_extra_state_attributes = {}

                self.async_write_ha_state()

            except Exception:
                return

    def _approximate_segment(self, map_data: dict) -> dict | None:
        unpacked_pixels = unpack_pixels(map_data)
        approximated_segment = approximate_segment(unpacked_pixels)

        return approximated_segment

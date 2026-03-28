"""
Options flow handler for MQTT Vacuum Camera integration.
Last Updated on version: 2026.2.0
"""

from copy import deepcopy
from typing import Any, Dict, Optional

from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlow
from homeassistant.exceptions import ConfigEntryError, ConfigEntryNotReady
from homeassistant.helpers import floor_registry as fr
from valetudo_map_parser.config.types import RoomStore

from .common import create_floor_data, extract_file_name, update_options
from .const import (
    ALPHA_BACKGROUND,
    ALPHA_CARPET,
    ALPHA_CHARGER,
    ALPHA_GO_TO,
    ALPHA_MATERIAL_TILE,
    ALPHA_MATERIAL_WOOD,
    ALPHA_MOP_MOVE,
    ALPHA_MOVE,
    ALPHA_NO_GO,
    ALPHA_ROBOT,
    ALPHA_ROOM_0,
    ALPHA_TEXT,
    ALPHA_WALL,
    ALPHA_ZONE_CLEAN,
    ATTR_MARGINS,
    ATTR_ROTATE,
    COLOR_BACKGROUND,
    COLOR_CARPET,
    COLOR_CHARGER,
    COLOR_GO_TO,
    COLOR_MATERIAL_TILE,
    COLOR_MATERIAL_WOOD,
    COLOR_MOP_MOVE,
    COLOR_MOVE,
    COLOR_NO_GO,
    COLOR_ROBOT,
    COLOR_ROOM_0,
    COLOR_TEXT,
    COLOR_WALL,
    COLOR_ZONE_CLEAN,
    CONF_ASPECT_RATIO,
    CONF_AUTO_ZOOM,
    CONF_CURRENT_FLOOR,
    CONF_DISABLE_CARPETS,
    CONF_DISABLE_MATERIAL_OVERLAY,
    CONF_DEF_CONTEXT_TYPE,
    CONF_FLOOR_NAME,
    CONF_FLOORS_DATA,
    CONF_MAP_NAME,
    CONF_MOP_PATH_WIDTH,
    CONF_OBSTACLE_LINK_IP,
    CONF_OBSTACLE_LINK_PORT,
    CONF_OBSTACLE_LINK_PROTOCOL,
    CONF_ROBOT_SIZE,
    CONF_TRIM_DOWN,
    CONF_TRIM_LEFT,
    CONF_TRIM_RIGHT,
    CONF_TRIM_UP,
    CONF_VAC_STAT,
    CONF_VAC_STAT_FONT,
    CONF_VAC_STAT_POS,
    CONF_VAC_STAT_SIZE,
    CONF_ZOOM_LOCK_RATIO,
    DEFAULT_ROOMS,
    DEFAULT_ROOMS_NAMES,
    DOMAIN,
    DRAW_FLAGS,
    IS_ALPHA,
    IS_ALPHA_R1,
    IS_ALPHA_R2,
    LOGGER,
    ROOM_FLAGS,
)
from .utils.options import OptionsSchemas


# noinspection PyTypeChecker
class MQTTCameraOptionsFlowHandler(OptionsFlow):
    """Options flow handler for MQTT Vacuum Camera integration."""

    def __init__(self, config_entry: ConfigEntry):
        """Initialize options flow."""
        if not config_entry:
            raise ConfigEntryError("Config entry is required.")
        self.camera_config = config_entry
        self.unique_id = self.camera_config.unique_id
        self.camera_options: dict[str, Any] = {}
        self.backup_options = deepcopy(dict(self.camera_config.options))
        self.file_name = extract_file_name(self.unique_id or "")
        self.is_alpha_enabled = False
        self.number_of_rooms = DEFAULT_ROOMS
        self.rooms_placeholders = DEFAULT_ROOMS_NAMES
        self.floors_data = dict(self.camera_config.options.get("floors_data", {}))
        self.current_floor = self.camera_config.options.get("current_floor", "floor_0")
        self.selected_floor: Optional[str] = None
        # Initialize schemas using dataclass
        self._schemas = OptionsSchemas(
            config_entry=config_entry, is_alpha_enabled=self.is_alpha_enabled
        )

    def _get_ha_floors(self) -> list[dict[str, str]]:
        """Get list of floors with both ID and display name.

        Returns:
            List of dicts with 'floor_id' and 'name' keys
        """
        try:
            floor_reg = fr.async_get(self.hass)
            floors = list(floor_reg.async_list_floors())
            return (
                [{"floor_id": floor.floor_id, "name": floor.name} for floor in floors]
                if floors
                else []
            )
        except (AttributeError, ValueError, KeyError) as e:
            LOGGER.warning("Failed to get HA floors: %s", e)
            return []

    def _get_floor_dropdown_options(
        self, filter_configured: bool = False, use_configured: bool = False
    ) -> list[dict[str, str]]:
        """Get floor options for dropdowns with display names.

        Args:
            filter_configured: If True, exclude already configured floors (for add_floor)
            use_configured: If True, use floors_data keys instead of HA floors (for edit/delete)

        Returns:
            List of dicts with 'label' and 'value' keys for SelectSelector
        """
        # Get HA floors
        ha_floors = self._get_ha_floors()

        if not ha_floors:
            # No HA floors configured, use floor_0
            return [{"label": "Floor 0", "value": "floor_0"}]

        # Build list of floor options
        floor_options = []
        for floor in ha_floors:
            floor_id = floor["floor_id"]
            floor_name = floor["name"]

            # Skip already configured floors if filtering
            if filter_configured and floor_id in self.floors_data:
                continue

            # Skip floors not in floors_data if use_configured is True
            if use_configured and floor_id not in self.floors_data:
                continue

            floor_options.append({"label": floor_name, "value": floor_id})

        return floor_options

    async def async_step_init(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> ConfigFlowResult:
        """Start the options menu configuration."""
        rooms_data = RoomStore(self.file_name)
        self.number_of_rooms = rooms_data.get_rooms_count()
        self.rooms_placeholders = (
            rooms_data.room_names if rooms_data.room_names else DEFAULT_ROOMS_NAMES
        )
        if (
            not isinstance(self.number_of_rooms, int)
            or self.number_of_rooms < DEFAULT_ROOMS
        ):
            LOGGER.error("No rooms found in the configuration. Aborting.")
            return self.async_abort(reason="no_rooms")

        return self.async_show_menu(
            step_id="init",
            menu_options=["image_opt", "colours", "materials", "save_options"],
        )

    async def async_step_main_menu(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> ConfigFlowResult:
        """Return to main menu."""
        return await self.async_step_init()

    async def async_step_image_opt(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> ConfigFlowResult:
        """Handle image options menu."""
        return self.async_show_menu(
            step_id="image_opt",
            menu_options=[
                "image_basic_opt",
                "status_text",
                "draw_elements",
                "floor_management",
                "obstacle_link_config",
                "main_menu",
            ],
        )

    async def async_step_draw_elements(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> ConfigFlowResult:
        """Handle draw elements menu."""
        return self.async_show_menu(
            step_id="draw_elements",
            menu_options=[
                "map_elements",
                "segments_visibility",
                "main_menu",
            ],
        )

    async def async_step_colours(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> ConfigFlowResult:
        """Handle colours menu."""
        menu_options = ["base_colours"]

        match self.number_of_rooms:
            case 1:
                menu_options.append("floor_only")
            case n if 1 < n <= 8:
                menu_options.extend(["rooms_colours_1"])
            case _:
                menu_options.extend(["rooms_colours_1", "rooms_colours_2"])

        if self.is_alpha_enabled:
            menu_options.append("transparency")

        menu_options.append("main_menu")

        return self.async_show_menu(
            step_id="colours",
            menu_options=menu_options,
        )

    async def async_step_transparency(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> ConfigFlowResult:
        """Handle transparency menu"""

        menu_options = ["alpha_1"]

        if self.number_of_rooms == 1:
            menu_options.append("alpha_floor")
        elif self.number_of_rooms <= 8:
            menu_options.append("alpha_2")
        else:
            menu_options.extend(["alpha_2", "alpha_3"])

        menu_options.append("main_menu")

        return self.async_show_menu(
            step_id="transparency",
            menu_options=menu_options,
        )

    async def async_step_materials(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Handle materials configuration."""
        if user_input is not None:
            self.camera_options.update(
                {
                    "disable_material_overlay": user_input.get(
                        CONF_DISABLE_MATERIAL_OVERLAY
                    ),
                    "disable_carpets": user_input.get(CONF_DISABLE_CARPETS),
                    "color_carpet": user_input.get(COLOR_CARPET),
                    "color_material_wood": user_input.get(COLOR_MATERIAL_WOOD),
                    "color_material_tile": user_input.get(COLOR_MATERIAL_TILE),
                    "alpha_carpet": user_input.get(ALPHA_CARPET),
                    "alpha_material_wood": user_input.get(ALPHA_MATERIAL_WOOD),
                    "alpha_material_tile": user_input.get(ALPHA_MATERIAL_TILE),
                }
            )
            return await self.async_step_init()

        return self.async_show_form(
            step_id="materials",
            data_schema=self._schemas.materials_schema,
        )

    # Image Settings Steps
    async def async_step_image_basic_opt(
        self, user_input: Optional[Dict[str, Any]] = None
    ):
        """Handle basic image settings."""
        if user_input is not None:
            self.camera_options.update(
                {
                    "rotate_image": user_input.get(ATTR_ROTATE),
                    "margins": user_input.get(ATTR_MARGINS),
                    "aspect_ratio": user_input.get(CONF_ASPECT_RATIO),
                    "zoom_lock_ratio": user_input.get(CONF_ZOOM_LOCK_RATIO),
                    "auto_zoom": user_input.get(CONF_AUTO_ZOOM),
                    "robot_size": user_input.get(CONF_ROBOT_SIZE),
                    "mop_path_width": user_input.get(CONF_MOP_PATH_WIDTH),
                    "def_context_type": user_input.get(CONF_DEF_CONTEXT_TYPE),
                }
            )
            return await self.async_step_image_opt()

        return self.async_show_form(
            step_id="image_basic_opt",
            data_schema=self._schemas.image_schema,
        )

    async def async_step_floor_management(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> ConfigFlowResult:
        """Handle floor management menu."""
        return self.async_show_menu(
            step_id="floor_management",
            menu_options=[
                "select_floor",
                "add_floor",
                "edit_floor",
                "delete_floor",
                "update_floor_data",
                "main_menu",
            ],
        )

    async def async_step_status_text(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle status text settings."""
        if user_input is not None:
            self.camera_options.update(
                {
                    "show_vac_status": user_input.get(CONF_VAC_STAT),
                    "vac_status_font": user_input.get(CONF_VAC_STAT_FONT),
                    "vac_status_size": user_input.get(CONF_VAC_STAT_SIZE),
                    "vac_status_position": user_input.get(CONF_VAC_STAT_POS),
                    "color_text": user_input.get(COLOR_TEXT),
                }
            )
            return await self.async_step_image_opt()

        return self.async_show_form(
            step_id="status_text",
            data_schema=self._schemas.status_text_options,
        )

    async def async_step_obstacle_link_config(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Handle obstacle image link configuration."""
        if user_input is not None:
            self.camera_options.update(
                {
                    CONF_OBSTACLE_LINK_PROTOCOL: user_input.get(
                        CONF_OBSTACLE_LINK_PROTOCOL
                    ),
                    CONF_OBSTACLE_LINK_PORT: user_input.get(CONF_OBSTACLE_LINK_PORT),
                    CONF_OBSTACLE_LINK_IP: user_input.get(CONF_OBSTACLE_LINK_IP),
                }
            )
            return await self.async_step_image_opt()

        # Get vacuum IP from coordinator to use as default
        vacuum_ip = ""
        try:
            hass_data = self.hass.data.get(DOMAIN, {}).get(self.camera_config.entry_id)
            if hass_data and "coordinator" in hass_data:
                coordinator = hass_data["coordinator"]
                if hasattr(coordinator, "context") and hasattr(
                    coordinator.context, "shared"
                ):
                    vacuum_ip = coordinator.context.shared.vacuum_ips or ""
        except (AttributeError, KeyError):
            # If we can't get the vacuum IP, use empty string
            pass

        return self.async_show_form(
            step_id="obstacle_link_config",
            data_schema=self._schemas.obstacle_link_schema(vacuum_ip),
        )

    async def async_step_map_elements(
        self, user_input: Optional[Dict[str, Any]] = None
    ):
        """Handle map elements visibility configuration."""
        if user_input is not None:
            # Update options based on user input using DRAW_FLAGS
            self.camera_options.update(
                {flag: user_input.get(flag, False) for flag in DRAW_FLAGS}
            )
            return await self.async_step_draw_elements()

        return self.async_show_form(
            step_id="map_elements",
            data_schema=self._schemas.map_elements_schema,
        )

    async def async_step_segments_visibility(
        self, user_input: Optional[Dict[str, Any]] = None
    ):
        """Handle segments (rooms) visibility configuration."""

        # Limit to the number of rooms that exist
        room_limit = min(self.number_of_rooms, 15)

        if user_input is not None:
            # Update options based on user input using ROOM_FLAGS
            self.camera_options.update(
                {flag: user_input.get(flag, False) for flag in ROOM_FLAGS[:room_limit]}
            )
            return await self.async_step_draw_elements()

        return self.async_show_form(
            step_id="segments_visibility",
            data_schema=self._schemas.segments_visibility_schema(room_limit),
            description_placeholders=self.rooms_placeholders,
        )

    async def async_step_base_colours(
        self, user_input: Optional[Dict[str, Any]] = None
    ):
        """Base Colours Configuration."""
        if user_input is not None:
            self.camera_options.update(
                {
                    "color_charger": user_input.get(COLOR_CHARGER),
                    "color_move": user_input.get(COLOR_MOVE),
                    "color_mop_move": user_input.get(COLOR_MOP_MOVE),
                    "color_wall": user_input.get(COLOR_WALL),
                    "color_robot": user_input.get(COLOR_ROBOT),
                    "color_go_to": user_input.get(COLOR_GO_TO),
                    "color_no_go": user_input.get(COLOR_NO_GO),
                    "color_zone_clean": user_input.get(COLOR_ZONE_CLEAN),
                    "color_background": user_input.get(COLOR_BACKGROUND),
                }
            )
            self.is_alpha_enabled = bool(user_input.get(IS_ALPHA))
            if self.is_alpha_enabled:
                self.is_alpha_enabled = False
                return await self.async_step_alpha_1()
            return await self.async_step_colours()

        return self.async_show_form(
            step_id="base_colours",
            data_schema=self._schemas.colors_base_schema,
        )

    async def async_step_alpha_1(self, user_input: Optional[Dict[str, Any]] = None):
        """Transparency Configuration for the Base Colours."""
        if user_input is not None:
            self.camera_options.update(
                {
                    "alpha_charger": user_input.get(ALPHA_CHARGER),
                    "alpha_move": user_input.get(ALPHA_MOVE),
                    "alpha_mop_move": user_input.get(ALPHA_MOP_MOVE),
                    "alpha_wall": user_input.get(ALPHA_WALL),
                    "alpha_robot": user_input.get(ALPHA_ROBOT),
                    "alpha_go_to": user_input.get(ALPHA_GO_TO),
                    "alpha_no_go": user_input.get(ALPHA_NO_GO),
                    "alpha_zone_clean": user_input.get(ALPHA_ZONE_CLEAN),
                    "alpha_background": user_input.get(ALPHA_BACKGROUND),
                    "alpha_text": user_input.get(ALPHA_TEXT),
                }
            )
            return await self.async_step_transparency()

        return self.async_show_form(
            step_id="alpha_1",
            data_schema=self._schemas.colors_alpha_1_schema,
        )

    async def async_step_floor_only(self, user_input: Optional[Dict[str, Any]] = None):
        """Floor colours configuration step based on one room only."""
        if user_input is not None:
            # Update options based on user input
            self.camera_options.update({"color_room_0": user_input.get(COLOR_ROOM_0)})
            self.is_alpha_enabled = user_input.get(IS_ALPHA_R1, False)
            if self.is_alpha_enabled:
                return await self.async_step_alpha_floor()
            return await self.async_step_colours()

        return self.async_show_form(
            step_id="floor_only",
            data_schema=self._schemas.floor_only_schema(self.is_alpha_enabled),
        )

    async def async_step_rooms_colours_1(
        self, user_input: Optional[Dict[str, Any]] = None
    ):
        """Dynamically generate rooms colours configuration step based on the number of rooms."""
        rooms_count = 1
        if self.number_of_rooms > 8:
            rooms_count = 8
        elif (self.number_of_rooms <= 8) and (self.number_of_rooms != 0):
            rooms_count = self.number_of_rooms

        if user_input is not None:
            # Update options based on user input
            self.camera_options.update(
                {
                    f"color_room_{i}": user_input.get(f"color_room_{i}")
                    for i in range(rooms_count)
                }
            )
            self.is_alpha_enabled = user_input.get(IS_ALPHA_R1, False)

            if self.is_alpha_enabled:
                return await self.async_step_alpha_2()
            return await self.async_step_colours()

        return self.async_show_form(
            step_id="rooms_colours_1",
            data_schema=self._schemas.rooms_colours_schema(
                0, rooms_count, self.is_alpha_enabled, IS_ALPHA_R1
            ),
            description_placeholders=self.rooms_placeholders,
        )

    async def async_step_rooms_colours_2(
        self, user_input: Optional[Dict[str, Any]] = None
    ):
        """Dynamically generate rooms colours configuration step based on the number of rooms."""
        end_room = min(self.number_of_rooms, 16)

        if user_input is not None:
            # Update options based on user input
            self.camera_options.update(
                {
                    f"color_room_{i}": user_input.get(f"color_room_{i}")
                    for i in range(8, end_room)
                }
            )
            self.is_alpha_enabled = user_input.get(IS_ALPHA_R2, False)

            if self.is_alpha_enabled:
                return await self.async_step_alpha_3()
            return await self.async_step_colours()

        return self.async_show_form(
            step_id="rooms_colours_2",
            data_schema=self._schemas.rooms_colours_schema(
                8, end_room, self.is_alpha_enabled, IS_ALPHA_R2
            ),
            description_placeholders=self.rooms_placeholders,
        )

    async def async_step_alpha_floor(self, user_input: Optional[Dict[str, Any]] = None):
        """Floor alpha configuration step based on one room only."""
        if user_input is not None:
            # Update options based on user input
            self.camera_options.update({"alpha_room_0": user_input.get(ALPHA_ROOM_0)})
            return await self.async_step_transparency()

        return self.async_show_form(
            step_id="alpha_floor",
            data_schema=self._schemas.alpha_floor_schema(),
        )

    async def async_step_alpha_2(self, user_input: Optional[Dict[str, Any]] = None):
        """Dynamically generate rooms colours configuration step based on the number of rooms."""
        rooms_count = 1
        if self.number_of_rooms > 8:
            rooms_count = 8
        elif (self.number_of_rooms <= 8) and (self.number_of_rooms != 0):
            rooms_count = self.number_of_rooms

        if user_input is not None:
            # Update options based on user input
            self.camera_options.update(
                {
                    f"alpha_room_{i}": user_input.get(f"alpha_room_{i}")
                    for i in range(rooms_count)
                }
            )
            return await self.async_step_transparency()

        return self.async_show_form(
            step_id="alpha_2",
            data_schema=self._schemas.rooms_alpha_schema(0, rooms_count),
            description_placeholders=self.rooms_placeholders,
        )

    async def async_step_alpha_3(self, user_input: Optional[Dict[str, Any]] = None):
        """Dynamically generate rooms colours configuration step based on the number of rooms."""
        end_room = min(self.number_of_rooms, 16)

        if user_input is not None:
            # Update options based on user input
            self.camera_options.update(
                {
                    f"alpha_room_{i}": user_input.get(f"alpha_room_{i}")
                    for i in range(8, end_room)
                }
            )
            return await self.async_step_transparency()

        return self.async_show_form(
            step_id="alpha_3",
            data_schema=self._schemas.rooms_alpha_schema(8, end_room),
            description_placeholders=self.rooms_placeholders,
        )

    # Floor Management Steps

    async def async_step_update_floor_data(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ):
        """Update floor data with current trims."""
        entry = self.camera_config.entry_id
        coordinator = self.hass.data[DOMAIN][entry]["coordinator"]

        # If multi-floor is enabled, update the current floor's FloorData
        if self.floors_data and self.current_floor:
            # Get existing floor data
            floor_data_dict = self.floors_data.get(self.current_floor, {})

            # Get current auto-calculated trims from coordinator.context.shared
            current_trims = coordinator.context.shared.trims
            current_trims_dict = current_trims.to_dict()

            # Get trim values from coordinator's shared data (current auto-calculated trims)
            trim_up = current_trims_dict.get("trim_up", 0)
            trim_left = current_trims_dict.get("trim_left", 0)
            trim_down = current_trims_dict.get("trim_down", 0)
            trim_right = current_trims_dict.get("trim_right", 0)

            # Get current rotation from camera options or config
            current_rotation = int(
                self.camera_options.get(
                    "rotate_image", self.camera_config.options.get("rotate_image", "0")
                )
            )

            # Create updated FloorData using common helper function
            updated_floor = create_floor_data(
                floor_name=self.current_floor,
                trim_up=trim_up,
                trim_down=trim_down,
                trim_left=trim_left,
                trim_right=trim_right,
                map_name=floor_data_dict.get("map_name", ""),
                rotation=current_rotation,
            )

            # Update floors_data
            updated_floors = dict(self.floors_data)
            updated_floors[self.current_floor] = updated_floor.to_dict()
            self.floors_data = updated_floors

            # Update trims_data (legacy single-floor support)
            self.camera_options.update(
                {
                    "trims_data": updated_floor.trims.to_dict(),
                    "floors_data": self.floors_data,
                    "current_floor": self.current_floor,
                }
            )

        return await self.async_step_edit_floor()

    async def async_step_select_floor(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Select the current active floor."""
        if user_input is not None:
            selected_floor_id = user_input.get(CONF_CURRENT_FLOOR)

            # Update instance variable
            self.current_floor = selected_floor_id

            # Update camera_options using .update() to preserve other options
            self.camera_options.update(
                {
                    CONF_CURRENT_FLOOR: selected_floor_id,
                }
            )
            return await self.async_step_floor_management()

        # Get floor options with display names
        floor_options = self._get_floor_dropdown_options()

        return self.async_show_form(
            step_id="select_floor",
            data_schema=self._schemas.select_floor_schema(
                floor_options, self.current_floor
            ),
            description_placeholders={"current_floor": self.current_floor},
        )

    async def async_step_add_floor(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Add a new floor with trim settings."""
        if user_input is not None:
            floor_id = str(user_input.get(CONF_FLOOR_NAME, ""))
            map_name = user_input.get(CONF_MAP_NAME, "")

            # Use existing trims_data as default for first floor if no floors exist yet
            if not self.floors_data:
                existing_trims = self.camera_config.options.get("trims_data", {})
                trim_up = existing_trims.get("trim_up", 0)
                trim_down = existing_trims.get("trim_down", 0)
                trim_left = existing_trims.get("trim_left", 0)
                trim_right = existing_trims.get("trim_right", 0)
            else:
                trim_up = user_input.get(CONF_TRIM_UP, 0)
                trim_down = user_input.get(CONF_TRIM_DOWN, 0)
                trim_left = user_input.get(CONF_TRIM_LEFT, 0)
                trim_right = user_input.get(CONF_TRIM_RIGHT, 0)

            # Create new floor data using common helper function
            new_floor = create_floor_data(
                floor_name=floor_id,
                trim_up=trim_up,
                trim_down=trim_down,
                trim_left=trim_left,
                trim_right=trim_right,
                map_name=map_name,
            )

            # Update floors_data - store FloorData.to_dict() format
            updated_floors = dict(self.floors_data)
            updated_floors[floor_id] = new_floor.to_dict()

            # Update instance variables
            self.floors_data = updated_floors
            self.current_floor = floor_id

            # Update camera_options using .update()
            # to preserve other options
            self.camera_options.update(
                {
                    CONF_FLOORS_DATA: updated_floors,
                    CONF_CURRENT_FLOOR: floor_id,
                }
            )
            return await self.async_step_floor_management()

        # Get floor options with display names, filtered for available floors
        floor_options = self._get_floor_dropdown_options(filter_configured=True)

        description = "Add a new floor. "
        if not self.floors_data:
            description += "Existing auto-calculated trim values will be used for this first floor."
        else:
            description += (
                "Enter trim values or leave at 0 to auto-calculate "
                "when you use 'Save Map Trims'."
            )

        return self.async_show_form(
            step_id="add_floor",
            data_schema=self._schemas.add_floor_schema(
                floor_options, bool(self.floors_data)
            ),
            description_placeholders={"info": description},
        )

    async def async_step_edit_floor(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Edit map name for an existing floor."""
        if user_input is not None:
            if self.selected_floor is None:
                # First step: select which floor to edit
                self.selected_floor = user_input.get(CONF_FLOOR_NAME)
                return await self.async_step_edit_floor()

            # Second step: update map_name and trim values
            map_name = user_input.get(CONF_MAP_NAME, "")
            trim_up = user_input.get(CONF_TRIM_UP, 0)
            trim_down = user_input.get(CONF_TRIM_DOWN, 0)
            trim_left = user_input.get(CONF_TRIM_LEFT, 0)
            trim_right = user_input.get(CONF_TRIM_RIGHT, 0)

            # Create updated floor data using common helper function
            # Note: rotation is not stored in floor data - library uses global rotate_image setting
            updated_floor = create_floor_data(
                floor_name=self.selected_floor,
                trim_up=trim_up,
                trim_down=trim_down,
                trim_left=trim_left,
                trim_right=trim_right,
                map_name=map_name,
                rotation=None,
            )

            # Update floors_data - store FloorData.to_dict() format
            updated_floors = dict(self.floors_data)
            updated_floors[self.selected_floor] = updated_floor.to_dict()

            # Update instance variables
            self.floors_data = updated_floors

            # Update camera_options using .update() to preserve other options
            self.camera_options.update(
                {
                    CONF_FLOORS_DATA: updated_floors,
                }
            )
            self.selected_floor = None
            return await self.async_step_floor_management()

        # First step: select floor to edit
        if self.selected_floor is None:
            if not self.floors_data:
                LOGGER.warning("No floors available to edit")
                return self.async_abort(reason="no_floors")

            # Get floor options from configured floors
            floor_options = self._get_floor_dropdown_options(use_configured=True)

            return self.async_show_form(
                step_id="edit_floor",
                data_schema=self._schemas.edit_floor_select_schema(floor_options),
                description_placeholders={
                    "floor_name": "",
                    "trim_info": "",
                },
            )

        # Second step: edit the selected floor (map_name and trim values)
        floor_data = self.floors_data.get(self.selected_floor, {})
        trims_data = floor_data.get("trims", {})

        return self.async_show_form(
            step_id="edit_floor",
            data_schema=self._schemas.edit_floor_data_schema(floor_data),
            description_placeholders={
                "floor_name": self.selected_floor,
                "trim_info": (
                    f"Current trims: {trims_data.get('trim_up', 0)}, "
                    f"{trims_data.get('trim_left', 0)}, "
                    f"{trims_data.get('trim_down', 0)}, "
                    f"{trims_data.get('trim_right', 0)}"
                ),
            },
        )

    async def async_step_delete_floor(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Delete a floor from the configuration."""
        if user_input is not None:
            floor_to_delete = user_input.get(CONF_FLOOR_NAME)

            updated_floors = dict(self.floors_data)
            if floor_to_delete in updated_floors:
                del updated_floors[floor_to_delete]

                # If we deleted the current floor, select a new one
                new_current_floor = self.current_floor
                if floor_to_delete == self.current_floor:
                    # Get remaining floors after deletion
                    remaining_floors = list(updated_floors.keys())

                    if remaining_floors:
                        # Use first remaining floor
                        new_current_floor = remaining_floors[0]
                    else:
                        # No floors left in floors_data, check HA floors
                        ha_floors = self._get_ha_floors()
                        new_current_floor = (
                            ha_floors[0]["floor_id"] if ha_floors else "floor_0"
                        )

                # Update instance variables
                self.floors_data = updated_floors
                self.current_floor = new_current_floor

                # Update camera_options using .update() to preserve other options
                self.camera_options.update(
                    {
                        CONF_FLOORS_DATA: updated_floors,
                        CONF_CURRENT_FLOOR: new_current_floor,
                    }
                )
                return await self.async_step_floor_management()

        if not self.floors_data:
            LOGGER.warning("No floors available to delete")
            return self.async_abort(reason="no_floors")

        # Get floor options from configured floors
        floor_options = self._get_floor_dropdown_options(use_configured=True)

        return self.async_show_form(
            step_id="delete_floor",
            data_schema=self._schemas.edit_floor_select_schema(floor_options),
        )

    async def async_step_save_options(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ):
        """Save the options in a sorted way. It stores all the options."""
        try:
            opt_update = await update_options(self.backup_options, self.camera_options)
            LOGGER.debug("updated options:%s", dict(opt_update))

            return self.async_create_entry(
                title="",
                data=opt_update,
            )
        except ConfigEntryError as e:
            LOGGER.error(
                "Configuration error while storing options: %s", e, exc_info=True
            )
            return self.async_abort(reason="config_error")
        except ConfigEntryNotReady as e:
            LOGGER.error("System not ready while storing options: %s", e, exc_info=True)
            return self.async_abort(reason="not_ready")

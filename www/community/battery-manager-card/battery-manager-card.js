// Version: v1.3.5
console.info(
  `%c BATTERY-MANAGER-CARD %c v1.3.5`,
  'color: white; background: #34c759; font-weight: 700;',
  'color: #34c759; background: white; font-weight: 700;'
);

const translations = {
  en: {
    title_default: "Battery Status",
    tab_all: "OVERVIEW",
    tab_attention: "ATTENTION",
    tab_type: "TYPE",
    tab_drain: "DRAIN",
    tab_maintenance: "MAINTENANCE",
    all_title: "All Batteries Overview",
    attention_title: "Attention Required",
    type_title: "Battery Type Analytics",
    drain_title: "Highest Discharge Rates",
    maintenance_title: "Update Date (HA Battery Notes)",
    reset_date: "Update replacement/charging date",
    search_placeholder: "Search devices, areas or types...",
    no_connection: "Offline",
    drain_rate: "Drain: ~{0}%/day",
    attention_req: "⚠️ Attention required",
    offline_count: "❔ <b>{0}</b> offline device(s)",
    stale_count: "⏳ <b>{0}</b> device(s) not reporting",
    charge_count: "🔌 <b>{0}</b> batt. to charge",
    replace_note: "🛒 Replacements needed (see Type)",
    all_good: "✅ All devices are good",
    no_problems: "No problem devices found",
    no_buys: "✅ No charging or buying needed",
    need_charge: "🔌 Charging required (<{0}%)",
    need_buy: "🛒 Buy urgently (<{0}%)",
    pcs: "pcs",
    days: "d.",
    in_use: "In use (Inventory)",
    drain_speed: "Discharge rate",
    no_drain_data: "Not enough replacement data",
    total_devices: "Total devices: {0}",
    // Editor Translations
    editor_title: "Card title",
    editor_title_ph: "Leave empty for default",
    editor_charge: "🔌 Rechargeable threshold (%)",
    editor_bat: "🔋 Battery threshold (%)",
    editor_drain: "📉 Devices on 'Drain' tab",
    editor_stale: "⏳ Days without reports (stale, 0=disable)",
    editor_name_size: "🔤 Name font size (px)",
    editor_level_size: "🔢 Level font size (px)",
    editor_default_tab: "Default tab",
    editor_tab_all: "Overview",
    editor_tab_attention: "Attention",
    editor_tab_type: "Type",
    editor_tab_drain: "Drain",
    editor_hide_good: "Hide card if all devices are good"
  },
  ru: {
    title_default: "Элементы питания",
    tab_all: "ОБЗОР",
    tab_attention: "ВНИМАНИЕ",
    tab_type: "ТИП",
    tab_drain: "РАСХОД",
    tab_maintenance: "ОБСЛУЖИВАНИЕ",
    all_title: "Обзор всех элементов питания",
    attention_title: "Устройства, требующие внимания",
    type_title: "Аналитика по типам батареек",
    drain_title: "Наивысшая скорость разряда",
    maintenance_title: "Обновление даты (HA Battery Notes)",
    reset_date: "Обновить дату замены/зарядки",
    search_placeholder: "Поиск (имя, комната, тип)...",
    no_connection: "Нет связи",
    drain_rate: "Расход: ~{0}% в день",
    attention_req: "⚠️ Требуется внимание",
    offline_count: "❔ <b>{0}</b> устройств(а) не на связи",
    stale_count: "⏳ <b>{0}</b> устройств(а) не обновлялись",
    charge_count: "🔌 <b>{0}</b> аккум. на зарядку",
    replace_note: "🛒 Есть элементы под замену (см. Тип)",
    all_good: "✅ Все устройства в норме",
    no_problems: "Проблемных устройств не найдено",
    no_buys: "✅ Зарядка и закупки не требуются",
    need_charge: "🔌 Требуется зарядка (<{0}%)",
    need_buy: "🛒 Срочно купить (<{0}%)",
    pcs: "шт.",
    days: "дн.",
    in_use: "Используется в доме",
    drain_speed: "Скорость разряда",
    no_drain_data: "Недостаточно данных о заменах",
    total_devices: "Всего устройств: {0}",
    // Editor Translations
    editor_title: "Название карточки",
    editor_title_ph: "Оставьте пустым для стандарта",
    editor_charge: "🔌 Порог заряда аккумуляторов (%)",
    editor_bat: "🔋 Порог заряда батареек (%)",
    editor_drain: "📉 Устройств на вкладке 'Расход'",
    editor_stale: "⏳ Дней без обновлений (оффлайн, 0=выкл)",
    editor_name_size: "🔤 Размер шрифта для названий (px)",
    editor_level_size: "🔢 Размер шрифта для заряда (px)",
    editor_default_tab: "Вкладка по умолчанию",
    editor_tab_all: "Обзор",
    editor_tab_attention: "Внимание",
    editor_tab_type: "Тип",
    editor_tab_drain: "Расход",
    editor_hide_good: "Скрыть карточку, если всё в норме"
  },
  de: {
    title_default: "Batteriestatus",
    tab_all: "ÜBERSICHT",
    tab_attention: "ACHTUNG",
    tab_type: "TYP",
    tab_drain: "VERBRAUCH",
    tab_maintenance: "WARTUNG",
    all_title: "Übersicht aller Batterien",
    attention_title: "Geräte, die Aufmerksamkeit erfordern",
    type_title: "Batterietyp-Analyse",
    drain_title: "Höchste Entladungsraten",
    maintenance_title: "Datum aktualisieren (HA Battery Notes)",
    reset_date: "Wechsel-/Ladedatum aktualisieren",
    search_placeholder: "Suchen (Name, Raum, Typ)...",
    no_connection: "Offline",
    drain_rate: "Verbrauch: ~{0}%/Tag",
    attention_req: "⚠️ Achtung erforderlich",
    offline_count: "❔ <b>{0}</b> Gerät(e) offline",
    stale_count: "⏳ <b>{0}</b> Gerät(e) ohne Meldung",
    charge_count: "🔌 <b>{0}</b> Akku(s) laden",
    replace_note: "🛒 Ersatz benötigt (siehe Typ)",
    all_good: "✅ Alle Geräte in Ordnung",
    no_problems: "Keine problematischen Geräte gefunden",
    no_buys: "✅ Kein Laden oder Kaufen nötig",
    need_charge: "🔌 Laden erforderlich (<{0}%)",
    need_buy: "🛒 Dringend kaufen (<{0}%)",
    pcs: "Stk.",
    days: "T.",
    in_use: "Im Einsatz (Bestand)",
    drain_speed: "Entladegeschwindigkeit",
    no_drain_data: "Nicht genug Ersatzdaten",
    total_devices: "Geräte gesamt: {0}",
    // Editor Translations
    editor_title: "Kartentitel",
    editor_title_ph: "Leer lassen für Standard",
    editor_charge: "🔌 Schwellenwert Akkus (%)",
    editor_bat: "🔋 Schwellenwert Batterien (%)",
    editor_drain: "📉 Geräte im 'Verbrauch'-Tab",
    editor_stale: "⏳ Tage ohne Meldung (offline, 0=aus)",
    editor_name_size: "🔤 Schriftgröße Name (px)",
    editor_level_size: "🔢 Schriftgröße Ladestand (px)",
    editor_default_tab: "Standard-Tab",
    editor_tab_all: "Übersicht",
    editor_tab_attention: "Achtung",
    editor_tab_type: "Typ",
    editor_tab_drain: "Verbrauch",
    editor_hide_good: "Karte ausblenden, wenn alles in Ordnung ist"
  },
  es: {
    title_default: "Estado de Baterías",
    tab_all: "RESUMEN",
    tab_attention: "ATENCIÓN",
    tab_type: "TIPO",
    tab_drain: "DESCARGA",
    tab_maintenance: "MANTENIMIENTO",
    all_title: "Resumen de todas las baterías",
    attention_title: "Dispositivos que requieren atención",
    type_title: "Análisis por tipo de batería",
    drain_title: "Mayores tasas de descarga",
    maintenance_title: "Actualizar fecha (HA Battery Notes)",
    reset_date: "Actualizar fecha de cambio/carga",
    search_placeholder: "Buscar (nombre, área, tipo)...",
    no_connection: "Sin conexión",
    drain_rate: "Descarga: ~{0}%/día",
    attention_req: "⚠️ Atención requerida",
    offline_count: "❔ <b>{0}</b> disp. sin conexión",
    stale_count: "⏳ <b>{0}</b> disp. sin reportarse",
    charge_count: "🔌 <b>{0}</b> bat. a cargar",
    replace_note: "🛒 Reemplazos necesarios (ver Tipo)",
    all_good: "✅ Todos los dispositivos bien",
    no_problems: "No se encontraron problemas",
    no_buys: "✅ No se necesita cargar ni comprar",
    need_charge: "🔌 Requiere carga (<{0}%)",
    need_buy: "🛒 Comprar urgente (<{0}%)",
    pcs: "un.",
    days: "d.",
    in_use: "En uso (Inventario)",
    drain_speed: "Tasa de descarga",
    no_drain_data: "Faltan datos de reemplazo",
    total_devices: "Total de dispositivos: {0}",
    // Editor Translations
    editor_title: "Título de la tarjeta",
    editor_title_ph: "Dejar en blanco para predeterminado",
    editor_charge: "🔌 Umbral para recargables (%)",
    editor_bat: "🔋 Umbral para baterías (%)",
    editor_drain: "📉 Dispositivos en pestaña 'Descarga'",
    editor_stale: "⏳ Días sin reportarse (offline, 0=apagado)",
    editor_name_size: "🔤 Tamaño fuente del nombre (px)",
    editor_level_size: "🔢 Tamaño fuente del nivel (px)",
    editor_default_tab: "Pestaña predeterminada",
    editor_tab_all: "Resumen",
    editor_tab_attention: "Atención",
    editor_tab_type: "Tipo",
    editor_tab_drain: "Descarga",
    editor_hide_good: "Ocultar tarjeta si todo está bien"
  },
  fr: {
    title_default: "État des Batteries",
    tab_all: "APERÇU",
    tab_attention: "ATTENTION",
    tab_type: "TYPE",
    tab_drain: "DÉCHARGE",
    tab_maintenance: "ENTRETIEN",
    all_title: "Aperçu de toutes les piles",
    attention_title: "Appareils nécessitant une attention",
    type_title: "Analyse par type de pile",
    drain_title: "Taux de décharge les plus élevés",
    maintenance_title: "Mettre à jour la date (HA Battery Notes)",
    reset_date: "Mettre à jour la date de remplacement/charge",
    search_placeholder: "Recherche (nom, pièce, type)...",
    no_connection: "Hors ligne",
    drain_rate: "Décharge : ~{0}%/jour",
    attention_req: "⚠️ Attention requise",
    offline_count: "❔ <b>{0}</b> appareil(s) hors ligne",
    stale_count: "⏳ <b>{0}</b> appareil(s) sans rapport",
    charge_count: "🔌 <b>{0}</b> bat. à charger",
    replace_note: "🛒 Remplacements nécessaires (voir Type)",
    all_good: "✅ Tous les appareils sont bons",
    no_problems: "Aucun appareil défectueux",
    no_buys: "✅ Aucun chargement ou achat nécessaire",
    need_charge: "🔌 Chargement requis (<{0}%)",
    need_buy: "🛒 Acheter d'urgence (<{0}%)",
    pcs: "pcs",
    days: "j.",
    in_use: "En cours d'utilisation",
    drain_speed: "Taux de décharge",
    no_drain_data: "Pas assez de données de remplacement",
    total_devices: "Total des appareils : {0}",
    // Editor Translations
    editor_title: "Titre de la carte",
    editor_title_ph: "Laisser vide par défaut",
    editor_charge: "🔌 Seuil pour rechargeables (%)",
    editor_bat: "🔋 Seuil pour piles (%)",
    editor_drain: "📉 Appareils dans l'onglet 'Décharge'",
    editor_stale: "⏳ Jours sans rapport (hors ligne, 0=désactivé)",
    editor_name_size: "🔤 Taille de police du nom (px)",
    editor_level_size: "🔢 Taille de police du niveau (px)",
    editor_default_tab: "Onglet par défaut",
    editor_tab_all: "Aperçu",
    editor_tab_attention: "Attention",
    editor_tab_type: "Type",
    editor_tab_drain: "Décharge",
    editor_hide_good: "Masquer la carte si tout va bien"
  }
};

class BatteryManagerCard extends HTMLElement {
  static getConfigElement() { return document.createElement("battery-manager-card-editor"); }

  static getStubConfig() {
    return {
      type: "custom:battery-manager-card", default_tab: "all", hide_if_all_good: false,
      charge_threshold: 15, threshold: 20, drain_count: 10, stale_days: 5, name_font_size: 17, level_font_size: 20
    };
  }

  setConfig(config) {
    this.config = {
      default_tab: config.default_tab || "all",
      hide_if_all_good: config.hide_if_all_good !== undefined ? config.hide_if_all_good : false,
      threshold: config.threshold !== undefined ? config.threshold : 20, 
      charge_threshold: config.charge_threshold !== undefined ? config.charge_threshold : 15, 
      warning_threshold: config.warning_threshold !== undefined ? config.warning_threshold : 40, 
      drain_count: config.drain_count !== undefined ? config.drain_count : 10, 
      stale_days: config.stale_days !== undefined ? config.stale_days : 5,
      name_font_size: config.name_font_size !== undefined ? config.name_font_size : 17,
      level_font_size: config.level_font_size !== undefined ? config.level_font_size : 20,
      ...config
    };
    if (!this.activeTab) this.activeTab = this.config.default_tab;
    if (this.searchQuery === undefined) this.searchQuery = "";
    this._lastStateHash = null;
  }

  localize(key, replaceVal = '') {
    const lang = (this._hass && this._hass.language) ? this._hass.language.substring(0, 2) : 'en';
    let translated = translations[lang] ? translations[lang][key] : translations['en'][key];
    if (!translated) translated = translations['en'][key];
    if (replaceVal !== '') translated = translated.replace('{0}', replaceVal);
    return translated;
  }

  getBatteryIcon(level, isAvailable) {
    if (!isAvailable) return 'mdi:battery-off-outline';
    if (isNaN(level)) return 'mdi:battery-unknown';
    const rounded = Math.round(level / 10) * 10;
    if (rounded >= 100) return 'mdi:battery';
    if (rounded <= 0) return 'mdi:battery-outline';
    return `mdi:battery-${rounded}`;
  }

  set hass(hass) {
    this._hass = hass;
    if (!this.content) {
      this.attachShadow({ mode: 'open' });
      this.shadowRoot.innerHTML = `<ha-card><div class="card-header"></div><div class="card-content" id="content"></div></ha-card>`;
      this.content = this.shadowRoot.querySelector('#content');
      this.header = this.shadowRoot.querySelector('.card-header');
      this.addStyles();
    }
    this.header.innerText = this.config.title !== undefined && this.config.title !== "" ? this.config.title : this.localize('title_default');
    this.style.setProperty('--name-font-size', `${this.config.name_font_size}px`);
    this.style.setProperty('--level-font-size', `${this.config.level_font_size}px`);
    
    let batteries = [];
    let typesToBuy = {}; let typesToCharge = {}; let allTypesInventory = {}; 
    let lowCount = 0; let needChargeCount = 0; let unavailableCount = 0; let staleCount = 0;

    Object.values(hass.states).forEach(state => {
      if (state.entity_id.startsWith('sensor.') && state.attributes.device_class === 'battery' && state.attributes.battery_type !== undefined) {
        const isAvailable = state.state !== 'unknown' && state.state !== 'unavailable';
        const level = isAvailable ? parseFloat(state.state) : NaN;
        const batteryType = state.attributes.battery_type;
        const batteryQuantity = state.attributes.battery_quantity || 1;
        const isRechargeable = batteryType.toLowerCase().includes('rechargeable');

        const iconState = state.attributes.icon || '';
        const isCharging = state.attributes.battery_state === 'charging' || 
                           state.attributes.battery_state === 'Charging' || 
                           state.attributes.is_charging === true || 
                           state.attributes.status === 'Charging' ||
                           iconState.includes('charging');

        let typeStr = state.attributes.battery_type_and_quantity || batteryType;
        if (!typeStr.includes('×') && !typeStr.includes('x')) typeStr = `${batteryQuantity}× ${batteryType}`;

        let drainRate = 0;
        if (isAvailable && state.attributes.battery_last_replaced) {
          const daysPassed = (new Date() - new Date(state.attributes.battery_last_replaced)) / (1000 * 86400);
          if (daysPassed > 1) drainRate = (100 - level) / daysPassed;
        }

        let isStale = false;
        let daysSinceReport = 0;
        if (isAvailable && state.attributes.battery_last_reported) {
          daysSinceReport = Math.floor((new Date() - new Date(state.attributes.battery_last_reported)) / (1000 * 86400));
          if (this.config.stale_days > 0 && daysSinceReport >= this.config.stale_days) {
            isStale = true; staleCount++;
          }
        }

        // Поиск Пространства (Area) через реестры Home Assistant
        let areaName = "";
        if (hass.entities && hass.entities[state.entity_id]) {
            const ent = hass.entities[state.entity_id];
            let aId = ent.area_id;
            if (!aId && ent.device_id && hass.devices && hass.devices[ent.device_id]) {
                aId = hass.devices[ent.device_id].area_id;
            }
            if (aId && hass.areas && hass.areas[aId]) {
                areaName = hass.areas[aId].name;
            }
        }

        batteries.push({
          entity_id: state.entity_id,
          name: state.attributes.friendly_name.replace(' Батарея+', '').trim(),
          level, isAvailable, type: batteryType, isRechargeable, type_str: typeStr,
          last_replaced: isAvailable ? this.formatDate(state.attributes.battery_last_replaced) : null,
          isStale, days_since_report: daysSinceReport,
          drain_rate: drainRate, icon: this.getBatteryIcon(level, isAvailable),
          isCharging, area: areaName 
        });

        allTypesInventory[batteryType] = (allTypesInventory[batteryType] || 0) + batteryQuantity;
        if (!isAvailable) unavailableCount++;
        else if (isRechargeable && level < this.config.charge_threshold) { needChargeCount++; typesToCharge[batteryType] = (typesToCharge[batteryType] || 0) + batteryQuantity; }
        else if (!isRechargeable && level < this.config.threshold) { lowCount++; typesToBuy[batteryType] = (typesToBuy[batteryType] || 0) + batteryQuantity; }
      }
    });

    batteries.sort((a, b) => {
      const aBad = !a.isAvailable || a.isStale;
      const bBad = !b.isAvailable || b.isStale;
      if (aBad && !bBad) return 1;
      if (!aBad && bBad) return -1;
      return a.level - b.level;
    });

    const totalProblems = lowCount + needChargeCount + unavailableCount + staleCount;
    if (this.config.hide_if_all_good && totalProblems === 0) {
      this.style.display = 'none'; this._lastStateHash = null; return;
    } else {
      this.style.display = 'block';
    }

    const stateHash = batteries.map(b => `${b.entity_id}:${b.level}:${b.isAvailable}:${b.isStale}:${b.isCharging}`).join('|') + `|${this.activeTab}`;
    if (this._lastStateHash === stateHash) return;
    this._lastStateHash = stateHash;

    this.render(batteries, typesToBuy, typesToCharge, allTypesInventory, lowCount, needChargeCount, unavailableCount, staleCount, totalProblems);
  }

  formatDate(rawDate) {
    if (!rawDate) return null;
    const lang = (this._hass && this._hass.language) ? this._hass.language : 'en';
    return new Date(rawDate).toLocaleDateString(lang, { month: 'short', day: 'numeric', year: 'numeric' });
  }

  render(batteries, typesToBuy, typesToCharge, allTypesInventory, lowCount, needChargeCount, unavailableCount, staleCount, totalProblems) {
    let html = `<div class="tabs-wrapper"><div class="tabs">`;
    const tabsList = [
      { id: 'all', icon: 'mdi:view-dashboard-outline' },
      { id: 'attention', icon: 'mdi:alert-circle-outline' },
      { id: 'type', icon: 'mdi:tag-outline' },
      { id: 'drain', icon: 'mdi:trending-down' },
      { id: 'maintenance', icon: 'mdi:wrench-outline' }
    ];
    
    tabsList.forEach(t => {
      let badge = ''; let countText = '';
      if (t.id === 'all') countText = `<span class="tab-count">${batteries.length}</span>`;
      if (t.id === 'attention' && totalProblems > 0) badge = `<div class="tab-badge">${totalProblems}</div>`;
      html += `<div class="tab ${this.activeTab === t.id ? 'active' : ''}" data-tab="${t.id}" title="${this.localize('tab_'+t.id)}">
                 <ha-icon icon="${t.icon}"></ha-icon>${countText}${badge}
               </div>`;
    });
    html += `</div></div><div class="tab-content">`;

    // Search bar
    if (this.activeTab !== 'type') {
      html += `<div class="search-bar">
                 <ha-icon icon="mdi:magnify"></ha-icon>
                 <input type="text" id="searchInput" placeholder="${this.localize('search_placeholder')}" value="${this.searchQuery}">
                 <ha-icon icon="mdi:close-circle" id="searchClear" style="display: ${this.searchQuery ? 'block' : 'none'};"></ha-icon>
               </div>`;
    }

    const renderRow = (bat, showDrain = false, isMaintenance = false) => {
      let lClass = (!bat.isAvailable || bat.isStale) ? 'problem' : bat.level < (bat.isRechargeable ? this.config.charge_threshold : this.config.threshold) ? 'critical' : bat.level < this.config.warning_threshold ? 'warning' : 'good';
      let meta = bat.type_str;
      let levelContent = '—';
      let iconClass = lClass;
      
      if (bat.isCharging) iconClass += ' charging';
      
      // Добавляем Пространство (Area) в meta, если оно есть
      if (bat.area) {
        meta += ` • ${bat.area}`;
      }

      if (!bat.isAvailable) {
        meta += ` • ${this.localize('no_connection')}`;
      } else if (bat.isStale) {
        meta += ` • ⏳ ${bat.days_since_report} ${this.localize('days')}`;
        levelContent = `${bat.level}%`;
      } else if (showDrain && bat.drain_rate > 0) {
        meta += ` • 🔋 ${bat.level}%`;
        levelContent = `~${bat.drain_rate.toFixed(1)}<span style="font-size: 14px; font-weight: normal; opacity: 0.8">%</span>`;
      } else {
        meta += (bat.last_replaced ? ` • ${bat.last_replaced}` : '');
        levelContent = `${bat.level}%`;
      }

      if (isMaintenance) {
        levelContent = `<div class="reset-btn" data-entity="${bat.entity_id}" title="${this.localize('reset_date')}">
                          <ha-icon icon="mdi:battery-sync"></ha-icon>
                        </div>`;
      }

      const q = this.searchQuery.toLowerCase();
      const matchName = bat.name.toLowerCase().includes(q);
      const matchEntity = bat.entity_id.toLowerCase().includes(q);
      const matchMeta = meta.toLowerCase().includes(q);
      const displayStyle = (!q || matchName || matchEntity || matchMeta) ? '' : 'style="display: none;"';

      return `<div class="battery-row ${lClass}" data-entity="${bat.entity_id}" ${displayStyle}>
                <div class="icon-wrapper ${iconClass}"><ha-icon icon="${bat.icon}"></ha-icon></div>
                <div class="name-col"><div class="name">${bat.name}</div><div class="meta">${meta}</div></div>
                <div class="level-col"><span class="level ${lClass}">${levelContent}</span></div>
              </div>`;
    };

    if (this.activeTab === 'all') {
      html += `<div class="list-title">${this.localize('all_title')}</div><div class="battery-list">`; batteries.forEach(b => html += renderRow(b)); html += `</div>`;
    } else if (this.activeTab === 'attention') {
      html += `<div class="list-title">${this.localize('attention_title')}</div><div class="rec-box ${totalProblems > 0 ? 'warning' : 'ok'}"><div class="rec-title">${totalProblems > 0 ? this.localize('attention_req') : this.localize('all_good')}</div><div class="rec-status-list">`;
      if (unavailableCount > 0) html += `<div class="rec-stat-item">${this.localize('offline_count', unavailableCount)}</div>`;
      if (staleCount > 0) html += `<div class="rec-stat-item">${this.localize('stale_count', staleCount)}</div>`;
      if (needChargeCount > 0) html += `<div class="rec-stat-item">${this.localize('charge_count', needChargeCount)}</div>`;
      if (lowCount > 0) html += `<div class="rec-stat-item">${this.localize('replace_note')}</div>`;
      html += `</div></div><div class="battery-list">`;
      const att = batteries.filter(b => !b.isAvailable || b.isStale || b.level < (b.isRechargeable ? this.config.charge_threshold : this.config.threshold));
      att.length ? att.forEach(b => html += renderRow(b)) : html += `<div class="meta" style="text-align:center">${this.localize('no_problems')}</div>`;
      html += `</div>`;
    } else if (this.activeTab === 'type') {
      html += `<div class="list-title">${this.localize('type_title')}</div>`;
      let typeHtml = '';
      if (Object.keys(typesToCharge).length || Object.keys(typesToBuy).length) {
        if (Object.keys(typesToCharge).length) typeHtml += `<div class="buy-box charge-box"><div class="box-title" style="color:var(--apple-red)">${this.localize('need_charge', this.config.charge_threshold)}</div><ul class="type-list">${Object.entries(typesToCharge).map(([t,q])=>`<li><span class="type-badge charge-badge">${t}</span> <b>${q} ${this.localize('pcs')}</b></li>`).join('')}</ul></div>`;
        if (Object.keys(typesToBuy).length) typeHtml += `<div class="buy-box active-buy"><div class="box-title">${this.localize('need_buy', this.config.threshold)}</div><ul class="type-list">${Object.entries(typesToBuy).map(([t,q])=>`<li><span class="type-badge">${t}</span> <b>${q} ${this.localize('pcs')}</b></li>`).join('')}</ul></div>`;
      } else typeHtml += `<div class="buy-box ok">${this.localize('no_buys')}</div>`;
      html += `<div class="inventory-section">${typeHtml}<div class="list-title" style="margin-top:20px">${this.localize('in_use')}</div><ul class="type-list minimal">${Object.entries(allTypesInventory).map(([t,q])=>`<li><span class="type-name">${t}</span> <span class="type-total">${q} ${this.localize('pcs')}</span></li>`).join('')}</ul></div>`;
    } else if (this.activeTab === 'drain') {
      html += `<div class="list-title">${this.localize('drain_title')}</div><div class="battery-list">`;
      const dr = batteries.filter(b => b.drain_rate > 0 && b.isAvailable && !b.isStale).sort((a,b)=>b.drain_rate-a.drain_rate).slice(0, this.config.drain_count);
      dr.length ? dr.forEach(b => html += renderRow(b, true)) : html += `<div class="meta" style="text-align:center">${this.localize('no_drain_data')}</div>`;
      html += `</div>`;
    } else if (this.activeTab === 'maintenance') {
      html += `<div class="list-title">${this.localize('maintenance_title')}</div><div class="battery-list">`;
      batteries.filter(b => b.isAvailable).forEach(b => html += renderRow(b, false, true));
      html += `</div>`;
    }

    this.content.innerHTML = html + `</div>`;
    
    // Tab switching listener
    this.shadowRoot.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => { 
      if (this.activeTab !== t.dataset.tab) {
        this.activeTab = t.dataset.tab; this._lastStateHash = null; this.hass = this._hass; 
      }
    }));

    // More-info listener
    this.shadowRoot.querySelectorAll('.battery-row').forEach(r => r.addEventListener('click', () => { 
      if (!r.classList.contains('problem') && this.activeTab !== 'maintenance') { 
        const ev = new Event('hass-more-info', { bubbles: true, composed: true }); ev.detail = { entityId: r.dataset.entity }; this.dispatchEvent(ev); 
      } 
    }));

    // Reset button listener
    this.shadowRoot.querySelectorAll('.reset-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation(); 
        const entityId = btn.dataset.entity;
        const deviceId = this._hass.entities && this._hass.entities[entityId] ? this._hass.entities[entityId].device_id : null;
        if (deviceId) {
          this._hass.callService('battery_notes', 'set_battery_replaced', { device_id: deviceId });
        } else {
          this._hass.callService('battery_notes', 'set_battery_replaced', { entity_id: entityId });
        }
        btn.querySelector('ha-icon').style.color = 'var(--apple-green)';
        setTimeout(() => { btn.querySelector('ha-icon').style.color = ''; }, 500);
      });
    });

    // Search and Clear input logic
    const sInput = this.shadowRoot.querySelector('#searchInput');
    const sClear = this.shadowRoot.querySelector('#searchClear');
    
    if (sInput) {
      const applySearch = (query) => {
        this.searchQuery = query;
        if (sClear) sClear.style.display = query ? 'block' : 'none';
        const qLower = query.toLowerCase();
        
        this.shadowRoot.querySelectorAll('.battery-row').forEach(row => {
          const entity = row.dataset.entity.toLowerCase();
          const nameText = row.querySelector('.name').textContent.toLowerCase();
          const metaText = row.querySelector('.meta').textContent.toLowerCase();
          
          if (!qLower || nameText.includes(qLower) || entity.includes(qLower) || metaText.includes(qLower)) {
            row.style.display = '';
          } else {
            row.style.display = 'none';
          }
        });
      };

      sInput.addEventListener('input', (e) => applySearch(e.target.value));

      if (sClear) {
        sClear.addEventListener('click', () => {
          sInput.value = '';
          applySearch('');
          sInput.focus();
        });
      }
    }
  }

  addStyles() {
    const s = document.createElement('style');
    s.textContent = `
      :host { --apple-red: #ff3b30; --apple-orange: #ff9500; --apple-green: #34c759; --apple-grey: #8e8e93; }
      ha-card { border-radius: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); overflow: hidden; padding-bottom: 12px; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif; }
      .card-header { font-size: 26px; font-weight: 700; padding: 24px 20px 16px; }
      .tabs-wrapper { display: flex; padding: 0 16px 16px; }
      
      .tabs { display: flex; background: rgba(120, 120, 128, 0.1); border-radius: 9px; padding: 4px; width: 100%; justify-content: space-between; }
      .tab { flex: 1; text-align: center; padding: 8px 0; cursor: pointer; border-radius: 7px; transition: 0.2s; color: var(--secondary-text-color); position: relative; }
      .tab.active { background: var(--card-background-color); box-shadow: 0 3px 8px rgba(0,0,0,0.1); color: var(--primary-text-color); }
      .tab ha-icon { --mdc-icon-size: 22px; }
      .tab-badge { position: absolute; top: 2px; right: calc(50% - 20px); background: var(--apple-red); color: white; font-size: 10px; font-weight: bold; border-radius: 10px; padding: 2px 5px; line-height: 1; }
      .tab-count { font-size: 12px; font-weight: 600; margin-left: 6px; vertical-align: text-bottom; }

      .tab-content { padding: 0 16px; }
      
      .search-bar { display: flex; align-items: center; background: rgba(120, 120, 128, 0.08); border-radius: 8px; padding: 8px 12px; margin-bottom: 16px; }
      .search-bar ha-icon { --mdc-icon-size: 20px; color: var(--secondary-text-color); margin-right: 8px; }
      .search-bar input { flex: 1; background: transparent; border: none; color: var(--primary-text-color); font-family: inherit; font-size: 15px; outline: none; }
      .search-bar input::placeholder { color: var(--secondary-text-color); opacity: 0.7; }
      .search-bar ha-icon#searchClear { margin-right: 0; margin-left: 8px; cursor: pointer; opacity: 0.5; transition: opacity 0.2s; }
      .search-bar ha-icon#searchClear:hover { opacity: 1; color: var(--primary-text-color); }
      
      .battery-list { display: flex; flex-direction: column; gap: 2px; }
      
      .battery-row { display: flex; flex-direction: row; align-items: center; gap: 16px; padding: 12px 16px; border-radius: 12px; margin: 0 -8px; cursor: pointer; }
      .battery-row:hover { background: var(--secondary-background-color, rgba(120, 120, 128, 0.16)); }
      .battery-row:hover .name, .battery-row:hover .meta { color: var(--primary-text-color); }
      
      .icon-wrapper { position: relative; flex: 0 0 auto; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
      .icon-wrapper.good { background: rgba(52, 199, 89, 0.12); color: var(--apple-green); }
      .icon-wrapper.warning { background: rgba(255, 149, 0, 0.12); color: var(--apple-orange); }
      .icon-wrapper.critical { background: rgba(255, 59, 48, 0.12); color: var(--apple-red); }
      .icon-wrapper.problem { background: rgba(142, 142, 147, 0.12); color: var(--apple-grey); }
      
      .icon-wrapper.charging::after {
        content: '+'; position: absolute; color: var(--apple-green); font-weight: bold; font-size: 18px;
        right: -2px; bottom: 0px; animation: floatUp 1.5s infinite ease-in; pointer-events: none; text-shadow: 0 0 4px rgba(255, 255, 255, 0.8);
      }
      @keyframes floatUp { 0% { transform: translateY(5px) scale(0.5); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateY(-15px) scale(1.3); opacity: 0; } }

      .name-col { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; justify-content: center; }
      .name { font-weight: 600; font-size: var(--name-font-size, 17px); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--primary-text-color); }
      .meta { font-size: 13px; color: var(--secondary-text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px; }
      
      .level-col { flex: 0 0 auto; text-align: right; white-space: nowrap; }
      .level { font-weight: 700; font-size: var(--level-font-size, 20px); }
      .level.good { color: var(--apple-green); }
      .level.warning { color: var(--apple-orange); }
      .level.critical { color: var(--apple-red); }
      
      .reset-btn { color: var(--apple-grey); padding: 4px; border-radius: 50%; transition: all 0.2s; cursor: pointer; }
      .reset-btn:hover { background: rgba(142, 142, 147, 0.2); color: var(--primary-text-color); }
      .reset-btn ha-icon { --mdc-icon-size: 24px; transition: color 0.2s; }

      .rec-box { border-radius: 12px; padding: 16px; margin-bottom: 20px; }
      .rec-box.warning { background: rgba(255, 149, 0, 0.08); }
      .rec-box.ok { background: rgba(52, 199, 89, 0.08); color: var(--apple-green); text-align: center; }
      .rec-title { font-weight: 700; font-size: 17px; margin-bottom: 8px; }
      .buy-box { border-radius: 12px; padding: 16px; margin-bottom: 12px; }
      .active-buy { background: rgba(255, 149, 0, 0.1); border: 1px solid rgba(255, 149, 0, 0.2); }
      .charge-box { background: rgba(255, 59, 48, 0.1); border: 1px solid rgba(255, 59, 48, 0.2); }
      .type-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
      .type-list li { display: flex; justify-content: space-between; }
      .type-badge { background: var(--apple-orange); color: #fff; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: 700; }
      .charge-badge { background: var(--apple-red); }
      .list-title { font-weight: 700; font-size: 14px; margin-bottom: 12px; color: var(--secondary-text-color); text-transform: uppercase; letter-spacing: 0.5px;}
    `;
    this.shadowRoot.appendChild(s);
  }
}

class BatteryManagerCardEditor extends HTMLElement {
  setConfig(config) { this._config = config; this.renderForm(); }
  set hass(hass) { this._hass = hass; this.renderForm(); }
  localize(key) {
    const lang = (this._hass && this._hass.language) ? this._hass.language.substring(0, 2) : 'en';
    let translated = translations[lang] ? translations[lang][key] : translations['en'][key];
    if (!translated) translated = translations['en'][key]; return translated;
  }
  renderForm() {
    if (!this._config || !this._hass || this._rendered) return;
    this._rendered = true;
    this.innerHTML = `
      <div class="card-config">
        <div class="option">
          <label for="title">${this.localize('editor_title')}</label>
          <input type="text" id="title" value="${this._config.title !== undefined ? this._config.title : ""}" placeholder="${this.localize('editor_title_ph')}">
        </div>
        <div class="option">
          <label for="default_tab">${this.localize('editor_default_tab')}</label>
          <select id="default_tab">
            <option value="all" ${this._config.default_tab === 'all' || !this._config.default_tab ? 'selected' : ''}>${this.localize('editor_tab_all')}</option>
            <option value="attention" ${this._config.default_tab === 'attention' ? 'selected' : ''}>${this.localize('editor_tab_attention')}</option>
            <option value="type" ${this._config.default_tab === 'type' ? 'selected' : ''}>${this.localize('editor_tab_type')}</option>
            <option value="drain" ${this._config.default_tab === 'drain' ? 'selected' : ''}>${this.localize('editor_tab_drain')}</option>
          </select>
        </div>
        <div class="option checkbox-option">
          <label><input type="checkbox" id="hide_if_all_good" ${this._config.hide_if_all_good ? 'checked' : ''}> ${this.localize('editor_hide_good')}</label>
        </div>
        <div class="option">
          <label for="charge_threshold">${this.localize('editor_charge')}</label>
          <input type="number" id="charge_threshold" value="${this._config.charge_threshold !== undefined ? this._config.charge_threshold : 15}">
        </div>
        <div class="option">
          <label for="threshold">${this.localize('editor_bat')}</label>
          <input type="number" id="threshold" value="${this._config.threshold !== undefined ? this._config.threshold : 20}">
        </div>
        <div class="option">
          <label for="stale_days">${this.localize('editor_stale')}</label>
          <input type="number" id="stale_days" value="${this._config.stale_days !== undefined ? this._config.stale_days : 5}">
        </div>
        <div class="option">
          <label for="drain_count">${this.localize('editor_drain')}</label>
          <input type="number" id="drain_count" value="${this._config.drain_count !== undefined ? this._config.drain_count : 10}">
        </div>
        <div class="option">
          <label for="name_font_size">${this.localize('editor_name_size')}</label>
          <input type="number" id="name_font_size" value="${this._config.name_font_size !== undefined ? this._config.name_font_size : 17}">
        </div>
        <div class="option">
          <label for="level_font_size">${this.localize('editor_level_size')}</label>
          <input type="number" id="level_font_size" value="${this._config.level_font_size !== undefined ? this._config.level_font_size : 20}">
        </div>
      </div>
      <style>
        .card-config { display: flex; flex-direction: column; gap: 16px; margin-bottom: 16px; font-family: var(--paper-font-body1_-_font-family); }
        .option { display: flex; flex-direction: column; gap: 8px; }
        .option label { font-size: 14px; font-weight: 500; color: var(--primary-text-color); }
        .option input, .option select { padding: 10px; font-size: 16px; border: 1px solid var(--divider-color); border-radius: 4px; background: var(--card-background-color); color: var(--primary-text-color); outline: none; }
        .option input:focus, .option select:focus { border-color: var(--primary-color); }
        .checkbox-option label { display: flex; align-items: center; gap: 10px; cursor: pointer; flex-direction: row; }
        .checkbox-option input { width: auto; margin: 0; cursor: pointer; }
      </style>
    `;
    this.querySelectorAll('input, select').forEach(input => {
      input.addEventListener('change', this.valueChanged.bind(this));
      input.addEventListener('input', this.valueChanged.bind(this)); 
    });
  }
  valueChanged(ev) {
    if (!this._config) return;
    const target = ev.target; const newConfig = Object.assign({}, this._config);
    if (target.type === 'checkbox') { newConfig[target.id] = target.checked; } else if (target.id === 'title' || target.id === 'default_tab') { newConfig[target.id] = target.value; } else { newConfig[target.id] = Number(target.value); }
    const event = new CustomEvent("config-changed", { detail: { config: newConfig }, bubbles: true, composed: true, }); this.dispatchEvent(event);
  }
}

customElements.define('battery-manager-card-editor', BatteryManagerCardEditor);
customElements.define('battery-manager-card', BatteryManagerCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "battery-manager-card",
  name: "Battery Manager Card",
  description: "Modern Apple-style battery status card with auto-discovery and drain analytics.",
  preview: true
});

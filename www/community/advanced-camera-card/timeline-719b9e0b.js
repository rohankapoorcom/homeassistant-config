import{_ as e,n as t,t as i,a,x as r,r as o,dd as n}from"./card-fb6e9222.js";import"./timeline-core-2d07e192.js";import"./startOfHour-3c4085c1.js";import"./endOfDay-7d24a950.js";import"./date-picker-ec518cf6.js";let s=class extends a{_getKeys(){const e=[];for(const t of this.cameraManager?.getStore().getCameraIDsWithCapability({anyCapabilities:["clips","snapshots","recordings"]})??[])e.push({type:"camera",cameraID:t});return e}render(){return this.timelineConfig?r`
      <advanced-camera-card-timeline-core
        .hass=${this.hass}
        .viewManagerEpoch=${this.viewManagerEpoch}
        .timelineConfig=${this.timelineConfig}
        .thumbnailConfig=${this.timelineConfig.controls.thumbnails}
        .cameraManager=${this.cameraManager}
        .viewItemManager=${this.viewItemManager}
        .keys=${this._getKeys()}
        .cardWideConfig=${this.cardWideConfig}
        .itemClickAction=${"none"===this.timelineConfig.controls.thumbnails.mode?"play":"select"}
      >
      </advanced-camera-card-timeline-core>
    `:r``}static get styles(){return o(n)}};e([t({attribute:!1})],s.prototype,"hass",void 0),e([t({attribute:!1})],s.prototype,"viewManagerEpoch",void 0),e([t({attribute:!1})],s.prototype,"timelineConfig",void 0),e([t({attribute:!1})],s.prototype,"cameraManager",void 0),e([t({attribute:!1})],s.prototype,"viewItemManager",void 0),e([t({attribute:!1})],s.prototype,"cardWideConfig",void 0),s=e([i("advanced-camera-card-timeline")],s);export{s as AdvancedCameraCardTimeline};

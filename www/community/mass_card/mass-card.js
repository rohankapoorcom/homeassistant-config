function t(t,e,i,s){var n,o=arguments.length,r=o<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(t,e,i,s);else for(var a=t.length-1;a>=0;a--)(n=t[a])&&(r=(o<3?n(r):o>3?n(e,i,r):n(e,i))||r);return o>3&&r&&Object.defineProperty(e,i,r),r}function e(t,e,i,s){return new(i||(i=Promise))(function(n,o){function r(t){try{h(s.next(t))}catch(t){o(t)}}function a(t){try{h(s.throw(t))}catch(t){o(t)}}function h(t){var e;t.done?n(t.value):(e=t.value,e instanceof i?e:new i(function(t){t(e)})).then(r,a)}h((s=s.apply(t,e||[])).next())})}"function"==typeof SuppressedError&&SuppressedError;
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const i=globalThis,s=i.ShadowRoot&&(void 0===i.ShadyCSS||i.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,n=Symbol(),o=new WeakMap;let r=class{constructor(t,e,i){if(this._$cssResult$=!0,i!==n)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(s&&void 0===t){const i=void 0!==e&&1===e.length;i&&(t=o.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&o.set(e,t))}return t}toString(){return this.cssText}};const a=(t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new r(i,t,n)},h=s?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new r("string"==typeof t?t:t+"",void 0,n))(e)})(t):t,{is:c,defineProperty:u,getOwnPropertyDescriptor:l,getOwnPropertyNames:d,getOwnPropertySymbols:p,getPrototypeOf:m}=Object,_=globalThis,f=_.trustedTypes,g=f?f.emptyScript:"",v=_.reactiveElementPolyfillSupport,$=(t,e)=>t,y={toAttribute(t,e){switch(e){case Boolean:t=t?g:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},b=(t,e)=>!c(t,e),w={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:b};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */Symbol.metadata??=Symbol("metadata"),_.litPropertyMetadata??=new WeakMap;let A=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=w){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,e);void 0!==s&&u(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){const{get:s,set:n}=l(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:s,set(e){const o=s?.call(this);n?.call(this,e),this.requestUpdate(t,o,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??w}static _$Ei(){if(this.hasOwnProperty($("elementProperties")))return;const t=m(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty($("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty($("properties"))){const t=this.properties,e=[...d(t),...p(t)];for(const i of e)this.createProperty(i,t[i])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,i]of e)this.elementProperties.set(t,i)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const i=this._$Eu(t,e);void 0!==i&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(h(t))}else void 0!==t&&e.push(h(t));return e}static _$Eu(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((t,e)=>{if(s)t.adoptedStyleSheets=e.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const s of e){const e=document.createElement("style"),n=i.litNonce;void 0!==n&&e.setAttribute("nonce",n),e.textContent=s.cssText,t.appendChild(e)}})(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(void 0!==s&&!0===i.reflect){const n=(void 0!==i.converter?.toAttribute?i.converter:y).toAttribute(e,i.type);this._$Em=t,null==n?this.removeAttribute(s):this.setAttribute(s,n),this._$Em=null}}_$AK(t,e){const i=this.constructor,s=i._$Eh.get(t);if(void 0!==s&&this._$Em!==s){const t=i.getPropertyOptions(s),n="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:y;this._$Em=s;const o=n.fromAttribute(e,t.type);this[s]=o??this._$Ej?.get(s)??o,this._$Em=null}}requestUpdate(t,e,i){if(void 0!==t){const s=this.constructor,n=this[t];if(i??=s.getPropertyOptions(t),!((i.hasChanged??b)(n,e)||i.useDefault&&i.reflect&&n===this._$Ej?.get(t)&&!this.hasAttribute(s._$Eu(t,i))))return;this.C(t,e,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:n},o){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,o??e??this[t]),!0!==n||void 0!==o)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),!0===s&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,i]of t){const{wrapped:t}=i,s=this[e];!0!==t||this._$AL.has(e)||void 0===s||this.C(e,void 0,i,s)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};A.elementStyles=[],A.shadowRootOptions={mode:"open"},A[$("elementProperties")]=new Map,A[$("finalized")]=new Map,v?.({ReactiveElement:A}),(_.reactiveElementVersions??=[]).push("2.1.1");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const S=globalThis,E=S.trustedTypes,x=E?E.createPolicy("lit-html",{createHTML:t=>t}):void 0,I="$lit$",C=`lit$${Math.random().toFixed(9).slice(2)}$`,M="?"+C,U=`<${M}>`,P=document,q=()=>P.createComment(""),N=t=>null===t||"object"!=typeof t&&"function"!=typeof t,O=Array.isArray,T="[ \t\n\f\r]",Q=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,L=/-->/g,k=/>/g,H=RegExp(`>|${T}(?:([^\\s"'>=/]+)(${T}*=${T}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),R=/'/g,D=/"/g,j=/^(?:script|style|textarea|title)$/i,z=(t=>(e,...i)=>({_$litType$:t,strings:e,values:i}))(1),B=Symbol.for("lit-noChange"),V=Symbol.for("lit-nothing"),F=new WeakMap,W=P.createTreeWalker(P,129);function Y(t,e){if(!O(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==x?x.createHTML(e):e}const G=(t,e)=>{const i=t.length-1,s=[];let n,o=2===e?"<svg>":3===e?"<math>":"",r=Q;for(let e=0;e<i;e++){const i=t[e];let a,h,c=-1,u=0;for(;u<i.length&&(r.lastIndex=u,h=r.exec(i),null!==h);)u=r.lastIndex,r===Q?"!--"===h[1]?r=L:void 0!==h[1]?r=k:void 0!==h[2]?(j.test(h[2])&&(n=RegExp("</"+h[2],"g")),r=H):void 0!==h[3]&&(r=H):r===H?">"===h[0]?(r=n??Q,c=-1):void 0===h[1]?c=-2:(c=r.lastIndex-h[2].length,a=h[1],r=void 0===h[3]?H:'"'===h[3]?D:R):r===D||r===R?r=H:r===L||r===k?r=Q:(r=H,n=void 0);const l=r===H&&t[e+1].startsWith("/>")?" ":"";o+=r===Q?i+U:c>=0?(s.push(a),i.slice(0,c)+I+i.slice(c)+C+l):i+C+(-2===c?e:l)}return[Y(t,o+(t[i]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),s]};class K{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let n=0,o=0;const r=t.length-1,a=this.parts,[h,c]=G(t,e);if(this.el=K.createElement(h,i),W.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(s=W.nextNode())&&a.length<r;){if(1===s.nodeType){if(s.hasAttributes())for(const t of s.getAttributeNames())if(t.endsWith(I)){const e=c[o++],i=s.getAttribute(t).split(C),r=/([.?@])?(.*)/.exec(e);a.push({type:1,index:n,name:r[2],strings:i,ctor:"."===r[1]?et:"?"===r[1]?it:"@"===r[1]?st:tt}),s.removeAttribute(t)}else t.startsWith(C)&&(a.push({type:6,index:n}),s.removeAttribute(t));if(j.test(s.tagName)){const t=s.textContent.split(C),e=t.length-1;if(e>0){s.textContent=E?E.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],q()),W.nextNode(),a.push({type:2,index:++n});s.append(t[e],q())}}}else if(8===s.nodeType)if(s.data===M)a.push({type:2,index:n});else{let t=-1;for(;-1!==(t=s.data.indexOf(C,t+1));)a.push({type:7,index:n}),t+=C.length-1}n++}}static createElement(t,e){const i=P.createElement("template");return i.innerHTML=t,i}}function Z(t,e,i=t,s){if(e===B)return e;let n=void 0!==s?i._$Co?.[s]:i._$Cl;const o=N(e)?void 0:e._$litDirective$;return n?.constructor!==o&&(n?._$AO?.(!1),void 0===o?n=void 0:(n=new o(t),n._$AT(t,i,s)),void 0!==s?(i._$Co??=[])[s]=n:i._$Cl=n),void 0!==n&&(e=Z(t,n._$AS(t,e.values),n,s)),e}class J{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??P).importNode(e,!0);W.currentNode=s;let n=W.nextNode(),o=0,r=0,a=i[0];for(;void 0!==a;){if(o===a.index){let e;2===a.type?e=new X(n,n.nextSibling,this,t):1===a.type?e=new a.ctor(n,a.name,a.strings,this,t):6===a.type&&(e=new nt(n,this,t)),this._$AV.push(e),a=i[++r]}o!==a?.index&&(n=W.nextNode(),o++)}return W.currentNode=P,s}p(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class X{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=V,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=Z(this,t,e),N(t)?t===V||null==t||""===t?(this._$AH!==V&&this._$AR(),this._$AH=V):t!==this._$AH&&t!==B&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>O(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==V&&N(this._$AH)?this._$AA.nextSibling.data=t:this.T(P.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:i}=t,s="number"==typeof i?this._$AC(t):(void 0===i.el&&(i.el=K.createElement(Y(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{const t=new J(s,this),i=t.u(this.options);t.p(e),this.T(i),this._$AH=t}}_$AC(t){let e=F.get(t.strings);return void 0===e&&F.set(t.strings,e=new K(t)),e}k(t){O(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const n of t)s===e.length?e.push(i=new X(this.O(q()),this.O(q()),this,this.options)):i=e[s],i._$AI(n),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=t.nextSibling;t.remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class tt{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,n){this.type=1,this._$AH=V,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=n,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=V}_$AI(t,e=this,i,s){const n=this.strings;let o=!1;if(void 0===n)t=Z(this,t,e,0),o=!N(t)||t!==this._$AH&&t!==B,o&&(this._$AH=t);else{const s=t;let r,a;for(t=n[0],r=0;r<n.length-1;r++)a=Z(this,s[i+r],e,r),a===B&&(a=this._$AH[r]),o||=!N(a)||a!==this._$AH[r],a===V?t=V:t!==V&&(t+=(a??"")+n[r+1]),this._$AH[r]=a}o&&!s&&this.j(t)}j(t){t===V?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class et extends tt{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===V?void 0:t}}class it extends tt{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==V)}}class st extends tt{constructor(t,e,i,s,n){super(t,e,i,s,n),this.type=5}_$AI(t,e=this){if((t=Z(this,t,e,0)??V)===B)return;const i=this._$AH,s=t===V&&i!==V||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,n=t!==V&&(i===V||s);s&&this.element.removeEventListener(this.name,this,i),n&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class nt{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){Z(this,t)}}const ot=S.litHtmlPolyfillSupport;ot?.(K,X),(S.litHtmlVersions??=[]).push("3.3.1");const rt=globalThis;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */let at=class extends A{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{const s=i?.renderBefore??e;let n=s._$litPart$;if(void 0===n){const t=i?.renderBefore??null;s._$litPart$=n=new X(e.insertBefore(q(),t),t,void 0,i??{})}return n._$AI(t),n})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return B}};at._$litElement$=!0,at.finalized=!0,rt.litElementHydrateSupport?.({LitElement:at});const ht=rt.litElementPolyfillSupport;ht?.({LitElement:at}),(rt.litElementVersions??=[]).push("4.2.1");let ct=class{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,i){this._$Ct=t,this._$AM=e,this._$Ci=i}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}};
/**
 * @license
 * Copyright 2020 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const ut={},lt=(t=>(...e)=>({_$litDirective$:t,values:e}))(class extends ct{constructor(){super(...arguments),this.key=V}render(t,e){return this.key=t,e}update(t,[e,i]){return e!==this.key&&(((t,e=ut)=>{t._$AH=e;
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */})(t),this.key=e),i}}),dt={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:b},pt=(t=dt,e,i)=>{const{kind:s,metadata:n}=i;let o=globalThis.litPropertyMetadata.get(n);if(void 0===o&&globalThis.litPropertyMetadata.set(n,o=new Map),"setter"===s&&((t=Object.create(t)).wrapped=!0),o.set(i.name,t),"accessor"===s){const{name:s}=i;return{set(i){const n=e.get.call(this);e.set.call(this,i),this.requestUpdate(s,n,t)},init(e){return void 0!==e&&this.C(s,void 0,t,e),e}}}if("setter"===s){const{name:s}=i;return function(i){const n=this[s];e.call(this,i),this.requestUpdate(s,n,t)}}throw Error("Unsupported decorator location: "+s)};function mt(t){return(e,i)=>"object"==typeof i?pt(t,e,i):((t,e,i)=>{const s=e.hasOwnProperty(i);return e.constructor.createProperty(i,t),s?Object.getOwnPropertyDescriptor(e,i):void 0})(t,e,i)}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function _t(t){return mt({...t,state:!0,attribute:!1})}class ft{constructor(t,e){this.hass=t,this.config=e}getQueue(t,i){return e(this,void 0,void 0,function*(){try{const e=yield this.hass.callWS({type:"call_service",domain:"mass_queue",service:"get_queue_items",service_data:{entity:this.config.entity,limit_before:t,limit_after:i},return_response:!0});return e.response[this.config.entity]}catch(t){return console.error("Error getting queue",t),null}})}playQueueItem(t){return e(this,void 0,void 0,function*(){try{yield this.hass.callService("mass_queue","play_queue_item",{entity:this.config.entity,queue_item_id:t})}catch(t){console.error("Error selecting queue item",t)}})}removeQueueItem(t){return e(this,void 0,void 0,function*(){try{yield this.hass.callService("mass_queue","remove_queue_item",{entity:this.config.entity,queue_item_id:t})}catch(t){console.error("Error removing queue item",t)}})}MoveQueueItemNext(t){return e(this,void 0,void 0,function*(){try{yield this.hass.callService("mass_queue","move_queue_item_next",{entity:this.config.entity,queue_item_id:t})}catch(t){console.error("Error moving queue item next",t)}})}MoveQueueItemUp(t){return e(this,void 0,void 0,function*(){try{yield this.hass.callService("mass_queue","move_queue_item_up",{entity:this.config.entity,queue_item_id:t})}catch(t){console.error("Error moving queue item up",t)}})}MoveQueueItemDown(t){return e(this,void 0,void 0,function*(){try{yield this.hass.callService("mass_queue","move_queue_item_down",{entity:this.config.entity,queue_item_id:t})}catch(t){console.error("Error moving queue item down",t)}})}}var gt=a`
  ha-card {
    overflow: hidden;
    width: 100%;
    height: 100%;
    justify-content: center;
    background: unset;
    box-shadow: unset;
  }
  .mass-panel {
    --expansion-panel-content-padding: 0px;
    --md-list-container-color: rgba(0,0,0,0) !important;
    --md-list-item-leading-space: 0px;
    --md-list-item-two-line-container-height: 48px;
  }
    --md-ripple-hover-color: var(--mdc-theme-primary);
    --mdc-ripple-hover-color: var(--mdc-theme-primary);
    --mdc-ripple-color: var(--mdc-theme-primary);
    --md-ripple-color: var(--mdc-theme-primary);
  .main {
    display: flex;
    height: 100%;
    margin: auto;
    padding: 6px 16px 6px 16px;
    width: 100%;
    justify-content: space-around;
    overflow-x: scroll;
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
  }
  .name {
    font-weight: 300;
    font-size: var(--fontSize);
    line-height: var(--fontSize);
    cursor: pointer;
  }
  .header {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .title {
    text-align: center;
    font-size: 1.2rem;
    font-weight: bold;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
  }
  .list {
    height: 400px;
    overflow-y: scroll;
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  *[selected] {
    color: var(--accent-color)
  }
  *[hide] {
  display: none;
  }
`;const vt={expanded:!1,title:"Player Queue",limit_before:5,limit_after:100,show_album_covers:!0,show_artist_names:!0,allow_collapsing:!0};var $t;!function(t){t.CONFIG_MISSING="Invalid configuration.",t.NO_ENTITY="You need to define entity.",t.ENTITY_TYPE="Entity must be a string!",t.MISSING_ENTITY="Entity does not exist!",t.OK="ok"}($t||($t={}));class yt extends at{constructor(){super(...arguments),this.selected=!1,this.showAlbumCovers=!0}callMoveItemUpService(t){t.stopPropagation(),this.moveQueueItemUpService(this.media_item.queue_item_id)}callMoveItemDownService(t){t.stopPropagation(),this.moveQueueItemDownService(this.media_item.queue_item_id)}callMoveItemNextService(t){t.stopPropagation(),this.moveQueueItemNextService(this.media_item.queue_item_id)}callRemoveItemService(t){t.stopPropagation(),this.removeService(this.media_item.queue_item_id)}callOnQueueItemSelectedService(){this.selectedService(this.media_item.queue_item_id,this.media_item.media_content_id)}shouldUpdate(t){if(t.has("selected"))return!0;if(t.has("media_item")){const e=t.get("media_item");return e.media_title!==this.media_item.media_title||e.media_artist!==this.media_item.media_artist||e.media_image!==this.media_item.media_image||e.playing!==this.media_item.playing||e.show_action_buttons!==this.media_item.show_action_buttons||e.show_move_up_next!==this.media_item.show_move_up_next}return!0}renderThumbnail(){const t=!this.media_item.show_action_buttons&&!this.media_item.playing;return this.media_item.media_image&&this.showAlbumCovers?z`
        <img 
          class="thumbnail${t?"-disabled":""}"
          slot="start"
          src="${this.media_item.media_image}"
        >
        </img>
      `:z``}renderTitle(){return z`
      <span 
        slot="headline" 
        class="title"
      >
        ${this.media_item.media_title}
      </span>
    `}renderArtist(){return this.media_item.show_artist_name?z`
        <span 
          slot="supporting-text" 
          class="title"
        >
          ${this.media_item.media_artist}
        </span>
      `:z``}renderActionButtons(){return this.media_item.show_action_buttons?z`
        <span 
          slot="end"
          class="button-group"
        >
          ${this.renderMoveNextButton()}
          ${this.renderMoveUpButton()}
          ${this.renderMoveDownButton()}
          ${this.renderRemoveButton()}
        </span>
      `:z``}renderMoveNextButton(){return this.media_item.show_move_up_next?z`
        <ha-icon-button 
          class="action-button"
          .path=${"M4.08,11.92L12,4L19.92,11.92L18.5,13.33L13,7.83V22H11V7.83L5.5,13.33L4.08,11.92M12,4H22V2H2V4H12Z"}
          @click=${this.callMoveItemNextService}>
        </ha-icon-button>
      `:z``}renderMoveUpButton(){return this.media_item.show_move_up_next?z`
        <ha-icon-button 
          class="action-button"
          .path=${"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}
          @click=${this.callMoveItemUpService}>
        </ha-icon-button>
      `:z``}renderMoveDownButton(){return z`
      <ha-icon-button 
        class="action-button"
        .path=${"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z"}
        @click=${this.callMoveItemDownService}>
      </ha-icon-button>
    `}renderRemoveButton(){return z`
      <ha-icon-button 
        class="action-button"
        .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
        @click=${this.callRemoveItemService}>
      </ha-icon-button>
    `}render(){return z`
      <ha-md-list-item 
        class="button${this.media_item.playing?"-active":""}"
		    @click=${this.callOnQueueItemSelectedService}
        type="button"
      >
        ${this.renderThumbnail()}
        ${this.renderTitle()}
        ${this.renderArtist()}
        ${this.renderActionButtons()}
      </ha-md-list-item>
    `}static get styles(){return[a`
        .button {
          margin: 0.15rem;
          border-radius: 0.7rem;
          background: var(--card-background-color);
          --row-height: 48px;
          --icon-width: 30px;
          height: var(--row-height);
        }
        .button-active {
          margin: 0.15rem;
          border-radius: 0.7rem;
          background-color: rgba(from var(--accent-color) r g b / 0.2);
          --row-height: 48px;
          --icon-width: 30px;
          height: var(--row-height);
          --font-color: var(--mdc-theme-primary);
          padding-inline-start: 0px;
          padding-inline-end: 8px;
          color: var(--accent-color);
        }
        .thumbnail {
          width: var(--row-height);
          height: var(--row-height);
          background-size: contain;
          background-repeat: no-repeat;
          background-position: left;
          border-radius: 0.7rem;
        }
        .thumbnail-disabled {
          width: var(--row-height);
          height: var(--row-height);
          background-size: contain;
          background-repeat: no-repeat;
          background-position: left;
          border-radius: 0.7rem;
          filter: opacity(0.5);
        }
        .button-group {
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: flex-end;
        }
        .action-button {
          width: var(--icon-width);
          transform: scale(1);
          align-content: center;
        }
        .title {
          font-size: 1.1rem;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          min-width: 0;
          color: var(--font-color);
        }
      `]}}t([mt({attribute:!1})],yt.prototype,"media_item",void 0),t([mt({type:Boolean})],yt.prototype,"selected",void 0),customElements.define("mass-media-row",yt);const bt="mass-card",wt="Music Assistant Queue Card";console.info(`%c ${wt} \n%c Version v0.8.1`,"color: teal; font-weight: bold; background: lightgray","color: darkblue; font-weight: bold; background: white"),window.customCards=window.customCards||[],window.customCards.push({type:`${bt}`,name:`${wt}`,preview:!1,description:"Music Assistant Queue Card for Home Assistant",documentationURL:"https://github.com/droans/mass_card"});let At=class extends at{constructor(){super(),this.lastUpdated="",this.queue=[],this.newId="",this._listening=!1,this.queueID="",this.failCt=0,this.maxFailCt=5,this.hasFailed=!1,this.eventListener=t=>{const e=t.data;if("queue_updated"==e.type){e.data.queue_id==this.queueID&&this.getQueue()}},this.onQueueItemSelected=(t,i)=>e(this,void 0,void 0,function*(){this.newId=i,yield this.services.playQueueItem(t),this.getQueue()}),this.onQueueItemRemoved=t=>e(this,void 0,void 0,function*(){yield this.services.removeQueueItem(t),this.queue=this.queue.filter(e=>e.queue_item_id!==t)}),this.onQueueItemMoveNext=t=>e(this,void 0,void 0,function*(){const e=this.getQueueItemIndex(t),i=this.queue.findIndex(t=>t.playing)+1;this.moveQueueItem(e,i),yield this.services.MoveQueueItemNext(t)}),this.onQueueItemMoveUp=t=>e(this,void 0,void 0,function*(){const e=this.getQueueItemIndex(t),i=e-1;this.moveQueueItem(e,i),yield this.services.MoveQueueItemUp(t)}),this.onQueueItemMoveDown=t=>e(this,void 0,void 0,function*(){const e=this.getQueueItemIndex(t),i=e+1;this.moveQueueItem(e,i),yield this.services.MoveQueueItemDown(t)}),this.queue=[]}set hass(t){if(!t)return;const e=t.states[this.config.entity].last_updated;e!==this.lastUpdated&&(this.lastUpdated=e),this._hass=t}get hass(){return this._hass}subscribeUpdates(){this._unsubscribe=this.hass.connection.subscribeEvents(this.eventListener,"mass_queue"),this._listening=!0}static getConfigElement(){return document.createElement(`${bt}-editor`)}static getStubConfig(){return{entity:[],title:"Player Queue",expanded:!1}}testConfig(t){return t?t.entity?"string"!=typeof t.entity?$t.ENTITY_TYPE:this.hass&&!this.hass.states[t.entity]?$t.MISSING_ENTITY:$t.OK:$t.NO_ENTITY:$t.CONFIG_MISSING}setConfig(t){const e=this.testConfig(t);if(e!==$t.OK)throw this.createError(e);this.config=Object.assign(Object.assign({},vt),t)}getQueueItemIndex(t,e=[]){return e.length||(e=this.queue),e.findIndex(e=>e.queue_item_id==t)}moveQueueItem(t,e){this.queue.splice(e,0,this.queue.splice(t,1)[0])}getQueue(){if(this.services&&this.testConfig(this.config)===$t.OK&&!this.hasFailed){if(this.failCt>=this.maxFailCt)throw this.hasFailed=!0,this.createError(`Failed to get queue ${this.failCt.toString()} times! Please check card config and that the services are working properly.`);try{this.services.getQueue(this.config.limit_before,this.config.limit_after).then(t=>{null!=t?this.queue=this.updateActiveTrack(t):this.failCt++}),this.queueID=this.hass.states[this.config.entity].attributes.active_queue}catch(t){this.queue=[]}}}updateActiveTrack(t){let e=this.newId;e.length||(e=this.hass.states[this.config.entity].attributes.media_content_id);const i=t.findIndex(t=>t.media_content_id===e);return t.map((t,e)=>Object.assign(Object.assign({},t),{playing:e===i,show_action_buttons:e>i,show_move_up_next:e>i+1,show_artist_name:this.config.show_artist_names}))}willUpdate(t){(t.has("hass")||t.has("config"))&&(this.hass&&this.config&&(this.services=new ft(this.hass,this.config)),this._listening||this.subscribeUpdates())}updated(t){if(super.updated(t),!this.queue.length&&this.hass&&this.getQueue(),t.has("hass")){const e=t.get("hass");if(e){const t=this.hass,i=e.states[this.config.entity],s=t.states[this.config.entity],n=i.attributes.media_content_id;s.attributes.media_content_id!=n&&this.getQueue()}else this.getQueue()}}shouldUpdate(t){if(t.has("queue"))return!0;if(t.has("hass")){if(!t.get("hass"))return!0}return super.shouldUpdate(t)}renderQueueItems(){const t=this.config.show_album_covers;return this.queue.map(e=>lt(e.queue_item_id,z`
            <mass-media-row
              .media_item=${e}
              .selected=${e.playing}
              .showAlbumCovers=${t}
              .showMoveUpNext=${e.show_move_up_next}
              .showArtistName=${e.show_artist_name}
              .selectedService=${this.onQueueItemSelected}
              .removeService=${this.onQueueItemRemoved}
              .moveQueueItemNextService=${this.onQueueItemMoveNext}
              .moveQueueItemUpService=${this.onQueueItemMoveUp}
              .moveQueueItemDownService=${this.onQueueItemMoveDown}
            >
            </mass-media-row>`))}render(){return z`
      <ha-card>
        <ha-expansion-panel
          class="mass-panel"
          header=${this.config.title}
          .expanded=${this.config.expanded||!this.config.allow_collapsing}
          ${this.config.allow_collapsing?"":"no-collapse"}
        >
          <ha-md-list class="list">
            ${this.renderQueueItems()}
          </ha-md-list>
        </ha-expansion-panel>
      </ha-card>
    `}static get styles(){return gt}getCardSize(){return 3}createError(t){const e=new Error(t),i=document.createElement("hui-error-card");return i.setConfig({type:"error",error:e,origConfig:this.config}),this.error=z`${i}`,e}};t([_t()],At.prototype,"lastUpdated",void 0),t([_t()],At.prototype,"queue",void 0),t([_t()],At.prototype,"config",void 0),t([_t()],At.prototype,"error",void 0),At=t([(t=>(e,i)=>{void 0!==i?i.addInitializer(()=>{customElements.define(t,e)}):customElements.define(t,e)})(`${bt}`)],At);export{At as MusicAssistantCard};

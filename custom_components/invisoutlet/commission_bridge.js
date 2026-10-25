// Frontend hack, isolated. Loaded globally via extra_module_url (see
// commission_bridge.py). Runs in the main frontend app; in the companion app
// hass.auth.external (the external bus) is available, in a browser it is not.
//
// Jobs:
//  1. When "Commission a new outlet" is chosen in the InvisOutlet config-flow
//     menu: in the app, launch the phone's native Matter commissioning by
//     firing the external-bus message directly (no navigation, no panel); in a
//     browser, block the step and explain that the companion app is required.
//     A capturing click listener is used because the menu is inside the flow
//     dialog's shadow DOM; click is composed, so it still reaches document.
//  2. Relay the app's matter/commission/finish message (which only reaches the
//     webview, not the server) to the backend, so the config flow can wait for
//     it and pre-fill the phone-set device name. The app delivers incoming
//     messages by calling window.externalBus(msg); we wrap it.
//
// Reads only public properties of built-in elements. If a frontend release
// changes these, commissioning simply isn't launched from here (the progress
// step's description carries a fallback link) and the name isn't pre-filled.
(() => {
  const DOMAIN = "invisoutlet";
  const COMMISSION_OPTION = "commission";
  const FINISH_COMMAND = "matter/commission/finish";
  const FINISHED_WS = `${DOMAIN}/commission_finished`;

  const APP_STORES = [
    {
      href: "https://apps.apple.com/app/home-assistant/id1099568401?mt=8",
      badge: "/static/images/appstore.svg",
      qr: "/static/images/qr-appstore.svg",
      alt: "Download on the App Store",
    },
    {
      href: "https://play.google.com/store/apps/details?id=io.homeassistant.companion.android",
      badge: "/static/images/playstore.svg",
      qr: "/static/images/qr-playstore.svg",
      alt: "Get it on Google Play",
    },
  ];

  // Explain (in a browser) that commissioning requires the companion app, with
  // store badges + QR codes. Uses HA's own ha-dialog and the bundled store
  // badge/QR SVGs the Matter add-device dialog uses.
  const showCompanionAppDialog = () => {
    const dialog = document.createElement("ha-dialog");
    dialog.setAttribute("header-title", "Add InvisOutlet device");

    const note = document.createElement("p");
    note.textContent =
      "You need to use the Home Assistant Companion app on your mobile phone " +
      "to add InvisOutlet devices.";
    dialog.appendChild(note);

    const install = document.createElement("p");
    install.textContent =
      "Install it from the Google Play Store or the App Store if you don't " +
      "have it. If you're already using the iOS app, make sure your iPhone or " +
      "iPad is running iOS 16 or newer.";
    dialog.appendChild(install);

    const row = document.createElement("div");
    row.style.cssText =
      "display:flex;gap:32px;justify-content:center;flex-wrap:wrap";
    for (const store of APP_STORES) {
      const link = document.createElement("a");
      link.href = store.href;
      link.target = "_blank";
      link.rel = "noreferrer noopener";
      link.style.cssText =
        "display:flex;flex-direction:column;align-items:center;gap:12px";
      const badge = document.createElement("img");
      badge.src = store.badge;
      badge.alt = store.alt;
      badge.style.height = "44px";
      const qr = document.createElement("img");
      qr.src = store.qr;
      qr.alt = store.alt;
      qr.style.width = "180px";
      link.appendChild(badge);
      link.appendChild(qr);
      row.appendChild(link);
    }
    dialog.appendChild(row);

    const ok = document.createElement("ha-button");
    ok.setAttribute("slot", "footer");
    ok.setAttribute("data-dialog", "close");
    ok.textContent = "OK";
    dialog.appendChild(ok);

    dialog.addEventListener("closed", () => dialog.remove());
    document.body.appendChild(dialog);
    dialog.open = true;
  };

  // 1. Launch commissioning (app) or explain (browser) when the option is chosen.
  document.addEventListener(
    "click",
    (ev) => {
      let clickedCommission = false;
      let menu = null;
      for (const node of ev.composedPath()) {
        if (
          node.localName === "ha-list-item" &&
          node.step === COMMISSION_OPTION
        ) {
          clickedCommission = true;
        } else if (node.localName === "step-flow-menu") {
          menu = node;
          break;
        }
      }
      if (!clickedCommission || menu?.step?.handler !== DOMAIN) return;

      const external = menu.hass?.auth?.external;
      if (external) {
        external.fireMessage({ type: "matter/commission" });
      } else {
        // Browser: don't advance to the (never-completing) progress step.
        ev.stopImmediatePropagation();
        showCompanionAppDialog();
      }
    },
    true
  );

  // 2. Relay the finish message (with the phone-set name) to the backend.
  const relayFinish = (raw) => {
    let msg = raw;
    if (typeof raw === "string") {
      try {
        msg = JSON.parse(raw);
      } catch {
        return;
      }
    }
    if (msg?.command !== FINISH_COMMAND) return;
    document.querySelector("home-assistant")?.hass?.callWS({
      type: FINISHED_WS,
      success: !!msg.payload?.success,
      name: msg.payload?.name ?? null,
    });
  };

  const wrap = (fn) => (msg) => {
    relayFinish(msg);
    return fn ? fn(msg) : undefined;
  };
  let wrapped = wrap(window.externalBus);
  try {
    Object.defineProperty(window, "externalBus", {
      configurable: true,
      get: () => wrapped,
      set: (fn) => {
        wrapped = wrap(fn);
      },
    });
  } catch {
    window.externalBus = wrapped;
  }
})();

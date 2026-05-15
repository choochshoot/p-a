(function () {
  const DEFAULT_CONFIG = {
    enabled: false,
    storageKey: "palf_privacy_consent_v1",
    title: "Privacidad",
    message: "Usamos cookies y tecnologias similares para mejorar tu experiencia.",
    acceptText: "Aceptar",
    rejectText: "Rechazar",
    moreInfoText: "Aviso de privacidad",
    moreInfoUrl: "#privacy"
  };

  const CONSENT_GRANTED = {
    analytics_storage: "granted",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    functionality_storage: "granted",
    security_storage: "granted"
  };

  const CONSENT_DENIED = {
    analytics_storage: "denied",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    functionality_storage: "granted",
    security_storage: "granted"
  };

  function pushEvent(name, payload) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: name, ...payload });
  }

  function updateGoogleConsent(status) {
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", status === "accepted" ? CONSENT_GRANTED : CONSENT_DENIED);
    }
  }

  function getStoredChoice(storageKey) {
    try {
      return window.localStorage.getItem(storageKey);
    } catch (error) {
      return null;
    }
  }

  function storeChoice(storageKey, value) {
    try {
      window.localStorage.setItem(storageKey, value);
    } catch (error) {
      // Si localStorage no esta disponible, el banner funciona solo durante la sesion.
    }
  }

  function closeBanner(banner) {
    banner.classList.remove("is-visible");
    window.setTimeout(() => banner.remove(), 240);
  }

  function openPrivacyModal() {
    const privacyLink = document.getElementById("privacyLink");
    if (privacyLink) {
      privacyLink.click();
      return;
    }

    const footer = document.getElementById("footerSection");
    if (footer) footer.scrollIntoView({ behavior: "smooth", block: "end" });
  }

  function buildBanner(config) {
    const banner = document.createElement("aside");
    banner.className = "privacy-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-live", "polite");
    banner.setAttribute("aria-label", config.title);

    const moreInfo = config.moreInfoUrl && config.moreInfoUrl !== "#privacy"
      ? `<a class="privacy-banner__link" href="${config.moreInfoUrl}">${config.moreInfoText}</a>`
      : `<button class="privacy-banner__link" type="button" data-privacy-info>${config.moreInfoText}</button>`;

    banner.innerHTML = `
      <div class="privacy-banner__copy">
        <p class="privacy-banner__title">${config.title}</p>
        <p class="privacy-banner__message">${config.message}</p>
        ${moreInfo}
      </div>
      <div class="privacy-banner__actions">
        <button class="privacy-banner__button privacy-banner__button--ghost" type="button" data-consent="rejected">
          ${config.rejectText}
        </button>
        <button class="privacy-banner__button privacy-banner__button--primary" type="button" data-consent="accepted">
          ${config.acceptText}
        </button>
      </div>
    `;

    banner.querySelectorAll("[data-consent]").forEach((button) => {
      button.addEventListener("click", () => {
        const choice = button.dataset.consent;
        storeChoice(config.storageKey, choice);
        updateGoogleConsent(choice);
        pushEvent("privacy_consent_update", { consent_status: choice });
        closeBanner(banner);
      });
    });

    const infoButton = banner.querySelector("[data-privacy-info]");
    if (infoButton) {
      infoButton.addEventListener("click", openPrivacyModal);
    }

    return banner;
  }

  async function loadConfig() {
    try {
      const response = await fetch("data/site-config.json", { cache: "default" });
      if (!response.ok) return DEFAULT_CONFIG;
      const data = await response.json();
      return { ...DEFAULT_CONFIG, ...(data.privacyBanner || {}) };
    } catch (error) {
      return DEFAULT_CONFIG;
    }
  }

  document.addEventListener("DOMContentLoaded", async () => {
    const config = await loadConfig();
    if (!config.enabled) return;

    const choice = getStoredChoice(config.storageKey);
    if (choice) {
      updateGoogleConsent(choice);
      pushEvent("privacy_consent_existing", { consent_status: choice });
      return;
    }

    const banner = buildBanner(config);
    document.body.appendChild(banner);
    requestAnimationFrame(() => banner.classList.add("is-visible"));
    pushEvent("privacy_banner_view", { consent_status: "pending" });
  });
})();
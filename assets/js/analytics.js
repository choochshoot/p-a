(() => {
  const dataLayer = window.dataLayer = window.dataLayer || [];
  const sessionStart = Date.now();
  const sentScrollDepths = new Set();
  const seenSections = new Set();

  function deviceType() {
    const ua = navigator.userAgent || "";
    if (/iphone|ipad|ipod/i.test(ua)) return "ios";
    if (/android/i.test(ua)) return "android";
    return "desktop";
  }

  function pushEvent(eventName, details = {}) {
    dataLayer.push({
      event: eventName,
      page_path: window.location.pathname,
      page_url: window.location.href,
      page_title: document.title,
      referrer: document.referrer || "",
      device_type: deviceType(),
      viewport_width: window.innerWidth,
      viewport_height: window.innerHeight,
      time_on_page_seconds: Math.round((Date.now() - sessionStart) / 1000),
      ...details
    });
  }

  function sectionLabel(section) {
    if (!section) return "";
    return section.id || section.querySelector("h2")?.textContent?.trim() || "";
  }

  function trackClicks() {
    document.addEventListener("click", event => {
      const link = event.target.closest("a, button");
      if (!link) return;

      const section = link.closest("section");
      const href = link.getAttribute("href") || "";
      const label = link.textContent?.trim() || link.getAttribute("aria-label") || "";
      const isWhatsapp = href.includes("wa.me") || link.classList.contains("whatsapp-float");
      const isMenu = Boolean(link.closest(".section-nav"));
      const isCta = link.classList.contains("btn") || link.closest(".section-cta") || link.closest(".grid-extended-cta");

      if (isWhatsapp) {
        pushEvent("whatsapp_click", { click_text: label || "WhatsApp", click_url: href });
        return;
      }

      if (isMenu) {
        pushEvent("menu_click", { click_text: label, click_url: href });
        return;
      }

      if (isCta) {
        pushEvent("cta_click", {
          click_text: label,
          click_url: href,
          section_id: sectionLabel(section)
        });
        return;
      }

      if (link.closest(".card-premium, .card-special, .grid-card, .grid-extended-card, .service-feature-item")) {
        pushEvent("content_card_click", {
          click_text: label,
          section_id: sectionLabel(section)
        });
      }
    });
  }

  function trackScrollDepth() {
    window.addEventListener("scroll", () => {
      const doc = document.documentElement;
      const scrollable = doc.scrollHeight - window.innerHeight;
      if (scrollable <= 0) return;

      const depth = Math.round((window.scrollY / scrollable) * 100);
      [50, 90].forEach(target => {
        if (depth >= target && !sentScrollDepths.has(target)) {
          sentScrollDepths.add(target);
          pushEvent("scroll_depth", { scroll_depth: target });
        }
      });
    }, { passive: true });
  }

  function trackSections() {
    const sections = [...document.querySelectorAll("section[id]")];
    if (!sections.length || !("IntersectionObserver" in window)) return;

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;

        const id = sectionLabel(entry.target);
        if (!id || seenSections.has(id)) return;

        seenSections.add(id);
        pushEvent("section_view", {
          section_id: id,
          section_title: entry.target.querySelector("h2")?.textContent?.trim() || ""
        });
      });
    }, { threshold: 0.45 });

    sections.forEach(section => observer.observe(section));
  }

  function trackReadTime() {
    [15, 30, 60, 120].forEach(seconds => {
      window.setTimeout(() => {
        pushEvent("read_time", { read_time_seconds: seconds });
      }, seconds * 1000);
    });
  }

  function initWhenContentExists(retries = 20) {
    if (document.querySelector("section[id]")) {
      trackSections();
      return;
    }

    if (retries > 0) {
      window.setTimeout(() => initWhenContentExists(retries - 1), 250);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    pushEvent("page_ready");
    trackClicks();
    trackScrollDepth();
    trackReadTime();
    initWhenContentExists();
  });
})();

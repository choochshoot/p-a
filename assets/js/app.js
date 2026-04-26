/* ===================================
   UTILITIES
=================================== */

function safe(value, fallback = "") {
  return value ?? fallback;
}

/* ===================================
   HERO
=================================== */

function renderHero(hero) {
  if (!hero?.enabled) return;

  const heroSection = document.getElementById("heroSection");
  if (!heroSection) return;

  heroSection.style.backgroundImage = `url('${hero.background}')`;

  heroSection.innerHTML = `
    <div class="hero-content">
      ${hero.logo ? `<img src="${hero.logo}" alt="Logo" class="hero-logo">` : ""}
      <h1>${safe(hero.title)}</h1>
      <p>${safe(hero.subtitle)}</p>
      ${hero.cta?.enabled ? `
        <a href="${hero.cta.url}" class="btn btn-premium">
          ${hero.cta.text}
        </a>
      ` : ""}
    </div>
  `;
}

/* ===================================
   RENDER REGISTRY (NEW CORE)
=================================== */

function renderGridExtended(section) {


  if (!section.items) {
    console.warn("⚠️ grid-extended sin items:", section);
  }
  
  return `
    <section id="${section.id}" class="grid-extended-section">
      <div class="container">

        <div class="grid-extended-header reveal">
          <h2>${safe(section.title)}</h2>
          ${section.subtitle ? `<p class="grid-extended-subtitle">${section.subtitle}</p>` : ""}
          ${section.cta ? `
            <div class="grid-extended-cta">
              <a href="${section.cta.url}" class="btn btn-premium">
                ${section.cta.text}
              </a>
            </div>
          ` : ""}
        </div>

        <div class="grid-extended-container">
          ${(section.items || []).map(item => `
            <article class="grid-extended-card reveal">

              <span class="grid-extended-number">
                ${item.number}
              </span>

              <div class="grid-extended-icon lottie-icon"
                   data-path="${item.icon}"
                   data-loop="false">
              </div>

              <h3>${safe(item.title)}</h3>
              <p>${safe(item.description)}</p>

              ${item.link ? `
                <a href="${item.link}" class="grid-extended-link">
                  Conocer más →
                </a>
              ` : ""}
            </article>
          `).join("")}
        </div>

      </div>
    </section>
  `;
}



function renderGrid(section) {

  // 🧠 DEBUG opcional
  if (!section.items) {
    console.warn("⚠️ GRID sin items:", section);
  }

  return `
    <section id="${section.id}" class="grid-section">
      <div class="container">
        <h2 class="reveal">${safe(section.title)}</h2>
        <p class="reveal">${safe(section.text)}</p>

        <div class="grid-container">
          ${(section.items || []).map(item => `
            <div class="grid-card reveal">
              <div class="lottie-icon" 
                  data-path="${item.lottie}"
                  data-autoplay="true"
                  data-loop="false">
              </div>
              <h3>${safe(item.title)}</h3>
              <p>${safe(item.text)}</p>
            </div>
          `).join("")}
        </div>
      </div>
    </section>
  `;
}


function renderCardsPremium(section) {

  if (!section.items) {
    console.warn("⚠️ cards-premium sin items:", section);
  }

  return `
    <section id="${section.id}" class="cards-premium-section">
      <div class="container">

        <div class="section-header reveal">
          <h2>${safe(section.title)}</h2>
          ${section.text ? `<p>${safe(section.text)}</p>` : ""}
        </div>

        <div class="cards-premium-grid">
          ${(section.items || []).map(item => `
            <article class="card-premium reveal">
              <h3>${safe(item.title)}</h3>
              <p>${safe(item.text)}</p>
            </article>
          `).join("")}
        </div>

      </div>
    </section>
  `;
}

function renderDefault(section, contact) {

  const MAX_ITEMS = 3;

  let listItems = section.text
    ? section.text
        .split("\n")
        .filter(item => item.trim() !== "")
    : [];

  let isCollapsible = listItems.length > MAX_ITEMS;

  let visibleItems = isCollapsible
    ? listItems.slice(0, MAX_ITEMS)
    : listItems;

  let hiddenItems = isCollapsible
    ? listItems.slice(MAX_ITEMS)
    : [];

  const listHTML = listItems.length
    ? `
      <ul class="premium-list">

        ${visibleItems.map((item, index) => {

          if (index === visibleItems.length - 1 && isCollapsible) {
            return `
              <li>
                ${item.trim()}
                <span class="read-more-inline">
                  ...
                  <button class="read-more-btn-inline">Leer más</button>
                </span>
              </li>
            `;
          }

          return `<li>${item.trim()}</li>`;
        }).join("")}

        ${isCollapsible ? `
          <div class="collapsible-extra">
            ${hiddenItems.map(item => `<li>${item.trim()}</li>`).join("")}
          </div>
        ` : ""}

      </ul>
    `
    : "";

  const galleryHTML = section.gallery?.length
    ? `
      <div class="section-gallery">
        ${section.gallery.map(img => `
          <img src="${img}" loading="lazy" />
        `).join("")}
      </div>
    `
    : "";

  const imageHTML = section.image
    ? `
      <div class="section-media reveal reveal-left">
        <img 
          src="${section.image}" 
          loading="lazy"
          decoding="async"
          alt="${safe(section.title)}"
        >

        ${galleryHTML}
      </div>
    `
    : "";  

  const quoteHTML = section.quote?.text
    ? `
      <blockquote class="section-quote">
        <p>"${section.quote.text}"</p>
        ${section.quote.author ? `<span>- ${section.quote.author}</span>` : ""}
      </blockquote>
    `
    : "";

  const mapHTML = (section.map && contact?.mapEmbed)
    ? `
      <div class="map-container reveal">
        <iframe
          src="${contact.mapEmbed}"
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade">
        </iframe>
      </div>
    `
    : "";

  const ctaHTML = section.cta
    ? `
      <div class="section-cta reveal">
        <a href="${section.cta.url}" class="btn">
          ${section.cta.text}
        </a>
      </div>
    `
    : "";

  return `
    <section id="${section.id}">
      <div class="container card card-reveal">
        <h2>${safe(section.title)}</h2>

        <div class="section-layout">
          ${imageHTML}
          <div class="section-content reveal reveal-right">
            ${listHTML}
            ${quoteHTML}
          </div>
        </div>

        ${mapHTML}
        ${ctaHTML}
      </div>
    </section>
  `;
}

const sectionRenderers = {
  "grid-extended": renderGridExtended,
  "grid": renderGrid,
  "default": renderDefault,
  "cards-premium": renderCardsPremium
};

      /* ===================================
        SECTIONS
      =================================== */

      function renderSections(sections, contact) {
        const container = document.getElementById("dynamicContent");
        if (!container) return;

        container.innerHTML = "";

        sections
          .filter(section => section.enabled)
          .forEach(section => {

            // 🧠 NEW CORE (registry)
            const renderer = sectionRenderers[section.type];

            if (renderer) {
              container.innerHTML += renderer(section, contact);
              return;
            }

            // ⚠️ fallback controlado (solo log)
            console.warn(`⚠️ No renderer for type: ${section.type}`);

          });

        // IMPORTANTE:
        initLotties();
      }

          

/* ===================================
   FOOTER
=================================== */

function renderFooter(contact) {
  const footer = document.getElementById("footerSection");
  if (!footer || !contact?.enabled) return;

  footer.innerHTML = `
    <div class="footer-container">
      <p>
        © ${new Date().getFullYear()} Pulido Asesores.
        Todos los derechos reservados.
      </p>
      <p>
        <a href="#" id="privacyLink">Aviso de Privacidad</a>
      </p>
    </div>

    <!-- Modal Aviso de Privacidad -->
    <div id="privacyModal" class="privacy-modal">
      <div class="privacy-content">
        <button id="closePrivacy" class="close-privacy">&times;</button>

        <h3>Aviso de Privacidad</h3>

        <p>
          En Pulido Asesores respetamos y protegemos sus datos personales
          conforme a la Ley Federal de Protección de Datos Personales en
          Posesión de los Particulares.
        </p>

        <p>
          La información proporcionada será utilizada exclusivamente para fines
          de contacto profesional, prestación de servicios de auditoría,
          cumplimiento fiscal y comunicación institucional.
        </p>

        <p>
          Usted puede ejercer sus derechos ARCO (Acceso, Rectificación,
          Cancelación y Oposición) enviando una solicitud al correo:
          contacto@pulidoasesores.com
        </p>

        <p>
          Pulido Asesores implementa medidas de seguridad técnicas,
          administrativas y físicas para proteger su información.
        </p>

      </div>
    </div>
  `;
}

function activatePrivacyModal() {
  const link = document.getElementById("privacyLink");
  const modal = document.getElementById("privacyModal");
  const closeBtn = document.getElementById("closePrivacy");

  if (!link || !modal || !closeBtn) return;

  link.addEventListener("click", (e) => {
    e.preventDefault();
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  });

  closeBtn.addEventListener("click", () => {
    modal.classList.remove("active");
    document.body.style.overflow = "auto";
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove("active");
      document.body.style.overflow = "auto";
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      modal.classList.remove("active");
      document.body.style.overflow = "auto";
    }
  });
}


/* ===================================
   SCROLL REVEAL
=================================== */

function activateReveal() {
  const reveals = document.querySelectorAll(".reveal, .card-reveal");

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, { threshold: 0.15 });

  reveals.forEach(el => observer.observe(el));
}

/* ===================================
   DYNAMIC SECTION MENU
=================================== */

function renderMenu(sections) {

  const nav = document.getElementById("dynamicMenu");
  if (!nav) return;

  const enabledSections = sections.filter(
    section => section.enabled && section.id && section.title
  );

  nav.innerHTML = `
    <div class="menu-container">
      <button class="menu-toggle" id="menuToggle" aria-label="Abrir menú">
        ☰
      </button>

      <ul class="menu-list">
        ${enabledSections.map(section => `
          <li>
            <a href="#${section.id}">
              ${section.menuLabel || section.title}
            </a>
          </li>
        `).join("")}
      </ul>
    </div>
  `;

  // 👇 Inicializamos aquí porque el menú acaba de generarse
  initMenuBehavior();
}

function initMenuBehavior() {

  const toggle = document.getElementById("menuToggle");
  const list = document.querySelector(".menu-list");

  if (!toggle || !list) return;

  toggle.addEventListener("click", () => {

    list.classList.toggle("active");

    if (list.classList.contains("active")) {
      toggle.innerHTML = "✕";
      toggle.style.color = "#1f3e63";
    } else {
      toggle.innerHTML = "☰";
      toggle.style.color = "#ffffff";
    }

  });

  // 👉 Cerrar al hacer click en un link
  const links = list.querySelectorAll("a");

  links.forEach(link => {
    link.addEventListener("click", () => {
      list.classList.remove("active");
      toggle.innerHTML = "☰";
      toggle.style.color = "#ffffff";
    });
  });

  // 👉 NUEVO: Cerrar al tocar fuera
  document.addEventListener("click", function (e) {

    const isMenuOpen = list.classList.contains("active");
    if (!isMenuOpen) return;

    const clickedInsideMenu = e.target.closest(".menu-list");
    const clickedToggle = e.target.closest("#menuToggle");

    if (!clickedInsideMenu && !clickedToggle) {
      list.classList.remove("active");
      toggle.innerHTML = "☰";
      toggle.style.color = "#ffffff";
    }

  });
}


/* ===================================
   READ MORE (COLLAPSIBLE UX)
=================================== */

function initReadMore() {
  document.querySelectorAll(".read-more-btn-inline").forEach(btn => {

    btn.addEventListener("click", () => {

      const list = btn.closest(".premium-list");
      const extra = list?.querySelector(".collapsible-extra");
      

      if (!list || !extra) return;

      // 🔥 NUEVO (aquí está la clave)
      const section = btn.closest("section");
      const media = section.querySelector(".section-media");
      const gallery = media ? media.querySelector(".section-gallery") : null;

      if (extra.classList.contains("open")) {

        // 🔽 CONTRAER
        extra.style.maxHeight = null;
        extra.classList.remove("open");
        btn.textContent = "Leer más";

        // 🔽 OCULTAR GALERÍA
        if (gallery) {
          gallery.style.maxHeight = null;
          gallery.style.opacity = 0;
        }

      } else {

        // 🔼 EXPANDIR TEXTO
        extra.classList.add("open");
        extra.style.maxHeight = extra.scrollHeight + "px";
        btn.textContent = "Ver menos";

        // 🔼 MOSTRAR GALERÍA
        if (gallery) {
          gallery.style.maxHeight = gallery.scrollHeight + "px";
          gallery.style.opacity = 1;
        }

        // 🔥 opcional (UX pro)
        section.scrollIntoView({ behavior: "smooth", block: "center" });
      }

    });

  });
}

/* ===================================
   SCROLL SPY (DESKTOP ONLY)
=================================== */

function initScrollSpy() {

  // 👇 solo desktop
  if (window.innerWidth < 1024) return;

  const sections = document.querySelectorAll("section[id]");
  const menuLinks = document.querySelectorAll(".menu-list a");

  if (!sections.length || !menuLinks.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {

        if (entry.isIntersecting) {

          // quitar active
          menuLinks.forEach(link => link.classList.remove("active"));

          const id = entry.target.getAttribute("id");

          const activeLink = document.querySelector(`.menu-list a[href="#${id}"]`);

          if (activeLink) {
            activeLink.classList.add("active");
          }

        }

      });
    },
    {
     rootMargin: "-120px 0px -50% 0px"
    }
  );

  sections.forEach(section => observer.observe(section));
}

/* ===================================
   INITIALIZE UI (Modular Boot)
=================================== */

function initializeUI(data) {
  renderHero(data.hero);
  renderMenu(data.sections); // 👈 IMPORTANTE
  renderSections(data.sections, data.contact);
  renderFooter(data.contact);

  // ❌ NO repetir initLotties aquí

  activateReveal();
  activatePrivacyModal();
  initReadMore(); // 👈 UX collapsible

  initScrollSpy(); // 🔥 AQUÍ EXACTO
}

/* ===================================
   INIT
=================================== */

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch(`data/content.json?v=${Date.now()}`);
    const data = await response.json();

    /* ===================================
      SEO META FROM JSON
    =================================== */

    if (data.meta?.enabled) {

      document.getElementById("metaTitle").textContent = data.meta.title || "";
      document.getElementById("metaDescription").setAttribute("content", data.meta.description || "");
      document.getElementById("metaKeywords").setAttribute("content", data.meta.keywords || "");

      const canonical = document.getElementById("canonicalUrl");
      if (canonical) canonical.setAttribute("href", data.meta.url || "");

      document.getElementById("ogTitle").setAttribute("content", data.meta.title || "");
      document.getElementById("ogDescription").setAttribute("content", data.meta.description || "");
      document.getElementById("ogUrl").setAttribute("content", data.meta.url || "");
    }

    initializeUI(data); // 👈 TODO centralizado

  } catch (error) {
    console.error("Error loading content:", error);
  }
});

/* ===================================
   HERO PARALLAX
=================================== */

window.addEventListener("scroll", () => {
  const hero = document.querySelector(".hero");
  if (!hero) return;

  hero.style.backgroundPosition = `center ${window.scrollY * 0.15}px`;
});

// ===================================
// MENU STICKY (DESKTOP UX)
// ===================================

window.addEventListener("scroll", () => {

  // 🔒 solo desktop
  if (window.innerWidth < 1024) return;

  const menu = document.querySelector(".section-nav");
  if (!menu) return;

  if (window.scrollY > 80) {
    menu.classList.add("menu-sticky");
  } else {
    menu.classList.remove("menu-sticky");
  }

});

// ================================
// STICKY MENU (SCROLL BEHAVIOR)
// ================================

function initStickyMenu() {

  const menu = document.querySelector(".section-nav");

  if (!menu) return;

  window.addEventListener("scroll", () => {

    // SOLO DESKTOP
    if (window.innerWidth < 1024) return;

    if (window.scrollY > 120) {
      menu.classList.add("menu-sticky");
    } else {
      menu.classList.remove("menu-sticky");
    }

  });
}

// inicializar
initStickyMenu();

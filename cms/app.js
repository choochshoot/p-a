const sectionTypes = [
  "default",
  "grid",
  "grid-extended",
  "cards-premium",
  "cards-special",
  "services-feature"
];

let content = null;
let selectedSectionIndex = null;
let dirty = false;

const $ = (selector) => document.querySelector(selector);

function setStatus(message, type = "info") {
  const status = $("#status");
  status.textContent = message;
  status.dataset.type = type;
}

function markDirty() {
  dirty = true;
  setStatus("Hay cambios sin guardar.");
}

function get(obj, path, fallback = "") {
  return path.split(".").reduce((acc, key) => acc?.[key], obj) ?? fallback;
}

function set(obj, path, value) {
  const parts = path.split(".");
  const last = parts.pop();
  const target = parts.reduce((acc, key) => {
    if (!acc[key] || typeof acc[key] !== "object") acc[key] = {};
    return acc[key];
  }, obj);
  target[last] = value;
}

function slugify(value) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "") || "nueva-seccion";
}

function uniqueId(base) {
  const ids = new Set(content.sections.map((section) => section.id));
  let id = slugify(base);
  let index = 2;
  while (ids.has(id)) {
    id = `${slugify(base)}-${index}`;
    index += 1;
  }
  return id;
}

function bindField(selector, path, options = {}) {
  const input = $(selector);
  if (!input) return;

  const value = get(content, path, options.defaultValue ?? "");
  if (input.type === "checkbox") {
    input.checked = Boolean(value);
  } else {
    input.value = value ?? "";
  }

  input.oninput = () => {
    const nextValue = input.type === "checkbox" ? input.checked : input.value;
    set(content, path, nextValue);
    markDirty();
  };
}

function bindMeta() {
  bindField("#metaTitle", "meta.title");
  bindField("#metaDescription", "meta.description");
  bindField("#metaUrl", "meta.url");
  bindField("#metaKeywords", "meta.keywords");
  bindField("#contactWhatsapp", "contact.whatsapp");
  bindField("#contactEmail", "contact.email");
  bindField("#contactAddress", "contact.address");
}

function bindHero() {
  if (!content.hero) content.hero = {};
  if (!content.hero.cta) content.hero.cta = { enabled: true, text: "", url: "" };

  bindField("#heroEnabled", "hero.enabled", { defaultValue: true });
  bindField("#heroTitle", "hero.title");
  bindField("#heroSubtitle", "hero.subtitle");
  bindField("#heroBackground", "hero.background");
  bindField("#heroLogo", "hero.logo");
  bindField("#heroCtaText", "hero.cta.text");
  bindField("#heroCtaUrl", "hero.cta.url");
}

function renderSectionList() {
  const list = $("#sectionList");
  list.innerHTML = "";

  content.sections.forEach((section, index) => {
    const item = document.createElement("li");
    item.className = `section-item${index === selectedSectionIndex ? " active" : ""}`;
    item.innerHTML = `
      <button type="button" data-select="${index}">
        <span class="section-title">${section.title || "(Sin titulo)"}</span>
        <span class="section-meta">${section.id} · ${section.type}${section.enabled ? "" : " · oculta"}</span>
      </button>
      <span class="move-buttons">
        <button type="button" data-move="${index}" data-dir="-1" aria-label="Subir">↑</button>
        <button type="button" data-move="${index}" data-dir="1" aria-label="Bajar">↓</button>
      </span>
    `;
    list.appendChild(item);
  });

  list.querySelectorAll("[data-select]").forEach((button) => {
    button.addEventListener("click", () => {
      selectedSectionIndex = Number(button.dataset.select);
      renderSectionList();
      renderSectionForm();
    });
  });

  list.querySelectorAll("[data-move]").forEach((button) => {
    button.addEventListener("click", () => {
      const from = Number(button.dataset.move);
      const to = from + Number(button.dataset.dir);
      if (to < 0 || to >= content.sections.length) return;
      const [section] = content.sections.splice(from, 1);
      content.sections.splice(to, 0, section);
      selectedSectionIndex = to;
      markDirty();
      renderSectionList();
      renderSectionForm();
    });
  });
}

function sectionTemplate(type) {
  const base = {
    enabled: true,
    id: uniqueId(type),
    type,
    title: "Nueva sección",
    text: "",
    menuLabel: "",
    showInMenu: true
  };

  if (type === "default") {
    return { ...base, map: false, cta: null, image: null, gallery: [], quote: null };
  }

  if (type === "grid") {
    return { ...base, items: [{ title: "Nuevo item", text: "", lottie: "" }] };
  }

  if (type === "grid-extended") {
    return {
      ...base,
      subtitle: "",
      cta: null,
      items: [{ number: "01", title: "Nuevo item", description: "", icon: "", link: null }]
    };
  }

  if (type === "services-feature") {
    return {
      ...base,
      subtitle: "",
      lottie: "assets/lotties/Isometricdatanalysis.json",
      footerText: "",
      items: [{ icon: "analysis", title: "Nuevo item", text: "" }]
    };
  }

  return { ...base, items: [{ title: "Nuevo item", text: "" }] };
}

function updateSelectedSection(path, value) {
  const section = content.sections[selectedSectionIndex];
  set(section, path, value);
  markDirty();
  renderSectionList();
}

function field(label, key, value = "", tag = "input", attrs = "") {
  const safeValue = String(value ?? "").replaceAll("&", "&amp;").replaceAll('"', "&quot;");
  const control = tag === "textarea"
    ? `<textarea data-section-field="${key}" rows="5" ${attrs}>${String(value ?? "")}</textarea>`
    : `<input data-section-field="${key}" value="${safeValue}" ${attrs}>`;
  return `<label>${label}${control}</label>`;
}

function renderSectionForm() {
  const form = $("#sectionForm");
  const section = content.sections[selectedSectionIndex];

  if (!section) {
    form.innerHTML = '<div class="empty-state">Selecciona una sección para editarla.</div>';
    return;
  }

  const itemsJson = JSON.stringify(section.items ?? [], null, 2);
  const galleryJson = JSON.stringify(section.gallery ?? [], null, 2);
  const quoteJson = JSON.stringify(section.quote ?? null, null, 2);
  const ctaJson = JSON.stringify(section.cta ?? null, null, 2);

  form.innerHTML = `
    <div class="form-grid">
      <label>Activa
        <select data-section-field="enabled">
          <option value="true"${section.enabled ? " selected" : ""}>Si</option>
          <option value="false"${!section.enabled ? " selected" : ""}>No</option>
        </select>
      </label>
      ${field("ID", "id", section.id)}
      <label>Tipo
        <select data-section-field="type">
          ${sectionTypes.map((type) => `<option value="${type}"${type === section.type ? " selected" : ""}>${type}</option>`).join("")}
        </select>
      </label>
      ${field("Titulo", "title", section.title)}
      ${field("Etiqueta menu", "menuLabel", section.menuLabel ?? "")}
      <label>Mostrar en menu
        <select data-section-field="showInMenu">
          <option value="true"${section.showInMenu !== false ? " selected" : ""}>Si</option>
          <option value="false"${section.showInMenu === false ? " selected" : ""}>No</option>
        </select>
      </label>
      ${field("Texto", "text", section.text ?? "", "textarea")}
      ${field("Subtitulo", "subtitle", section.subtitle ?? "")}
      ${field("Imagen principal", "image", section.image ?? "")}
      ${field("Lottie", "lottie", section.lottie ?? "")}
      ${field("Footer text", "footerText", section.footerText ?? "", "textarea")}
      <label class="json-field">Items JSON
        <textarea data-json-field="items" rows="10">${itemsJson}</textarea>
        <span class="help">Edita cards, grid items o timeline respetando el formato JSON.</span>
      </label>
      <label class="json-field">Galeria JSON
        <textarea data-json-field="gallery" rows="4">${galleryJson}</textarea>
      </label>
      <label class="json-field">Quote JSON
        <textarea data-json-field="quote" rows="4">${quoteJson}</textarea>
      </label>
      <label class="json-field">CTA JSON
        <textarea data-json-field="cta" rows="4">${ctaJson}</textarea>
      </label>
    </div>
    <div class="asset-row">
      <label>Subir imagen de sección <input id="sectionUpload" type="file" accept="image/*"></label>
      <button class="secondary" data-upload="sectionUpload" data-target-section-field="image" data-folder="secciones" type="button">Usar como imagen</button>
    </div>
    <div class="actions-row">
      <button id="duplicateSectionButton" class="secondary" type="button">Duplicar sección</button>
      <button id="deleteSectionButton" class="danger" type="button">Eliminar sección</button>
    </div>
  `;

  form.querySelectorAll("[data-section-field]").forEach((input) => {
    input.addEventListener("input", () => {
      let value = input.value;
      if (input.dataset.sectionField === "enabled" || input.dataset.sectionField === "showInMenu") {
        value = input.value === "true";
      }
      updateSelectedSection(input.dataset.sectionField, value);
    });
  });

  form.querySelectorAll("[data-json-field]").forEach((input) => {
    input.addEventListener("change", () => {
      try {
        content.sections[selectedSectionIndex][input.dataset.jsonField] = JSON.parse(input.value || "null");
        markDirty();
      } catch (error) {
        setStatus(`JSON invalido en ${input.dataset.jsonField}: ${error.message}`, "error");
      }
    });
  });

  $("#duplicateSectionButton").addEventListener("click", () => {
    const copy = structuredClone(section);
    copy.id = uniqueId(`${section.id}-copia`);
    copy.title = `${section.title} copia`;
    content.sections.splice(selectedSectionIndex + 1, 0, copy);
    selectedSectionIndex += 1;
    markDirty();
    renderSectionList();
    renderSectionForm();
  });

  $("#deleteSectionButton").addEventListener("click", () => {
    const title = section.title || section.id;
    if (!confirm(`Eliminar "${title}"?`)) return;
    content.sections.splice(selectedSectionIndex, 1);
    selectedSectionIndex = null;
    markDirty();
    renderSectionList();
    renderSectionForm();
  });

  bindUploadButtons();
}

function validateBeforeSave() {
  const errors = [];
  const ids = new Set();

  content.sections.forEach((section) => {
    if (!section.id) errors.push("Hay una sección sin ID.");
    if (ids.has(section.id)) errors.push(`ID duplicado: ${section.id}`);
    ids.add(section.id);
    if (!sectionTypes.includes(section.type)) errors.push(`Tipo no soportado: ${section.type}`);
    if (!section.title) errors.push(`La sección ${section.id} no tiene titulo.`);
  });

  return errors;
}

async function loadContent() {
  const response = await fetch("/api/content");
  if (!response.ok) {
    throw new Error("Abre el CMS con python cms/server.py para poder leer y guardar.");
  }

  const payload = await response.json();
  content = payload.content;
  selectedSectionIndex = null;
  dirty = false;
  bindHero();
  bindMeta();
  renderSectionList();
  renderSectionForm();
  setStatus("Contenido cargado.");
}

async function saveContent() {
  const errors = validateBeforeSave();
  if (errors.length) {
    setStatus(errors.join(" "), "error");
    return;
  }

  const response = await fetch("/api/content", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content })
  });

  const payload = await response.json();
  if (!response.ok) {
    setStatus((payload.errors || [payload.error || "No se pudo guardar."]).join(" "), "error");
    return;
  }

  dirty = false;
  setStatus("Guardado. Se creó respaldo en data/backups.");
}

async function uploadImage(fileInputId, target) {
  const fileInput = $(`#${fileInputId}`);
  if (!fileInput?.files?.length) {
    setStatus("Selecciona una imagen primero.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("folder", target.folder || "cms");

  const response = await fetch("/api/upload", {
    method: "POST",
    body: formData
  });
  const payload = await response.json();

  if (!response.ok) {
    setStatus(payload.error || "No se pudo subir la imagen.", "error");
    return;
  }

  if (target.contentPath) {
    set(content, target.contentPath, payload.path);
    bindHero();
  }

  if (target.sectionField) {
    content.sections[selectedSectionIndex][target.sectionField] = payload.path;
    renderSectionForm();
    renderSectionList();
  }

  markDirty();
  setStatus(`Imagen lista: ${payload.path}`);
}

function bindUploadButtons() {
  document.querySelectorAll("[data-upload]").forEach((button) => {
    button.onclick = () => {
      const inputId = button.dataset.upload;
      const targetSectionField = button.dataset.targetSectionField;
      uploadImage(inputId, {
        contentPath: button.dataset.contentPath || null,
        sectionField: targetSectionField || null,
        folder: button.dataset.folder
      });
    };
  });
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab, .panel").forEach((el) => el.classList.remove("active"));
    tab.classList.add("active");
    $(`#${tab.dataset.panel}`).classList.add("active");
  });
});

$("#addSectionButton").addEventListener("click", () => {
  const type = prompt(`Tipo de sección:\n${sectionTypes.join(", ")}`, "default");
  if (!type || !sectionTypes.includes(type)) return;
  content.sections.push(sectionTemplate(type));
  selectedSectionIndex = content.sections.length - 1;
  markDirty();
  renderSectionList();
  renderSectionForm();
});

$("#saveButton").addEventListener("click", saveContent);
$("#reloadButton").addEventListener("click", loadContent);
window.addEventListener("beforeunload", (event) => {
  if (!dirty) return;
  event.preventDefault();
  event.returnValue = "";
});

bindUploadButtons();
loadContent().catch((error) => setStatus(error.message, "error"));

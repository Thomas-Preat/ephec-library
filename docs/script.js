function isRelativeUrl(url) {
  return url && !/^(?:[a-z]+:|\/\/|#|\/)/i.test(url);
}

function resolveRelativeUrl(url, sourcePath) {
  if (!isRelativeUrl(url) || !sourcePath) {
    return url;
  }

  const basePath = sourcePath.slice(0, sourcePath.lastIndexOf("/") + 1);
  return new URL(url, `${window.location.href.replace(/[^/]*$/, "")}${basePath}`).toString();
}

function renderMarkdown(markdown, sourcePath) {
  if (window.marked) {
    marked.setOptions({
      gfm: true,
      breaks: true,
    });

    const rendered = marked.parse(markdown);
    const safeHtml = window.DOMPurify ? DOMPurify.sanitize(rendered) : rendered;
    const container = document.createElement("div");
    container.innerHTML = safeHtml;

    container.querySelectorAll("img[src], a[href]").forEach(node => {
      if (node.tagName === "IMG") {
        node.src = resolveRelativeUrl(node.getAttribute("src"), sourcePath);
        return;
      }

      node.href = resolveRelativeUrl(node.getAttribute("href"), sourcePath);
    });

    return container.innerHTML;
  }

  const escaped = markdown
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
  return `<pre><code>${escaped}</code></pre>`;
}

function normalizeText(value) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

async function copyTextToClipboard(text) {
  if (!text) {
    return false;
  }

  if (navigator.clipboard && navigator.clipboard.writeText) {
    await navigator.clipboard.writeText(text);
    return true;
  }

  const area = document.createElement("textarea");
  area.value = text;
  document.body.appendChild(area);
  area.select();
  const ok = document.execCommand("copy");
  document.body.removeChild(area);
  return ok;
}

function wireCopyButton(button, getText) {
  if (!button) {
    return;
  }

  button.onclick = async () => {
    const original = button.textContent;

    try {
      const copied = await copyTextToClipboard(getText());
      button.textContent = copied ? "Copie" : "Echec";
    } catch {
      button.textContent = "Echec";
    }

    setTimeout(() => {
      button.textContent = original;
    }, 1000);
  };
}

async function loadCategories() {
  const res = await fetch("files.json");
  const data = await res.json();

  const categoriesDiv = document.getElementById("categories");
  const searchInputEl = document.getElementById("module-search");
  const homeLinkEl = document.getElementById("home-link");
  const codeEl = document.getElementById("code");
  const libraryMetaEl = document.getElementById("library-meta");
  const descriptionEl = document.getElementById("description");
  const homeSectionEl = document.getElementById("home-section");
  const homeCodeEl = document.getElementById("home-code");
  const exampleSectionEl = document.getElementById("example-section");
  const exampleCodeEl = document.getElementById("example-code");
  const exampleMetaEl = document.getElementById("example-meta");
  const codePanelEl = document.getElementById("code-panel");
  const pageTitleEl = document.querySelector("#main h1");
  const copyHomeBtnEl = document.getElementById("copy-home-code");
  const copyExampleBtnEl = document.getElementById("copy-example-code");
  const copyLibraryBtnEl = document.getElementById("copy-library-code");
  const homeDescriptionHtml = descriptionEl.innerHTML;
  const categoryRecords = [];
  let activeFileEl = null;

  wireCopyButton(copyHomeBtnEl, () => homeCodeEl.textContent);
  wireCopyButton(copyExampleBtnEl, () => exampleCodeEl.textContent);
  wireCopyButton(copyLibraryBtnEl, () => codeEl.textContent);

  const showHome = () => {
    if (activeFileEl) {
      activeFileEl.classList.remove("active");
      activeFileEl = null;
    }

    homeLinkEl.classList.add("active");
    pageTitleEl.textContent = "Bienvenue sur la bibliotheque EPHEC";
    libraryMetaEl.textContent = "Page d'accueil";
    descriptionEl.innerHTML = homeDescriptionHtml;
    descriptionEl.hidden = false;
    homeSectionEl.hidden = false;
    exampleSectionEl.hidden = true;
    exampleCodeEl.textContent = "";
    exampleMetaEl.textContent = "";
    codeEl.textContent = "";
    codePanelEl.hidden = true;
    codePanelEl.open = false;
  };

  homeLinkEl.onclick = showHome;

  for (const category in data) {
    const categoryDiv = document.createElement("div");
    categoryDiv.className = "category closed";

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "category-toggle";
    toggle.setAttribute("aria-expanded", "false");

    const titleText = document.createElement("span");
    titleText.textContent = category.toUpperCase();

    const caret = document.createElement("span");
    caret.className = "caret";
    caret.textContent = "▾";

    toggle.appendChild(titleText);
    toggle.appendChild(caret);

    const filesContainer = document.createElement("div");
    filesContainer.className = "files";
    const fileRecords = [];

    toggle.onclick = () => {
      const isClosed = categoryDiv.classList.toggle("closed");
      toggle.setAttribute("aria-expanded", String(!isClosed));
    };

    data[category].forEach(file => {
      const fileEl = document.createElement("div");
      fileEl.className = "file";
      fileEl.textContent = file.name.toUpperCase();
      fileRecords.push({
        el: fileEl,
        searchText: normalizeText(`${category} ${file.name} ${file.path}`),
      });

      fileEl.onclick = async () => {
        const requests = [fetch(file.path)];

        if (file.descriptionPath) {
          requests.push(fetch(file.descriptionPath));
        } else {
          requests.push(null);
        }

        if (file.examplePath) {
          requests.push(fetch(file.examplePath));
        }

        const responses = await Promise.all(requests.filter(Boolean));
        const code = await responses[0].text();
        let description = "# Documentation indisponible\n\nAucune documentation Markdown n'a encore ete ajoutee pour ce module.";
        let exampleCode = "";
        let responseIndex = 1;

        if (file.descriptionPath) {
          if (responses[responseIndex] && responses[responseIndex].ok) {
            description = await responses[responseIndex].text();
          }
          responseIndex += 1;
        }

        if (file.examplePath && responses[responseIndex] && responses[responseIndex].ok) {
          exampleCode = await responses[responseIndex].text();
        }

        if (activeFileEl) {
          activeFileEl.classList.remove("active");
        }

        homeLinkEl.classList.remove("active");
        fileEl.classList.add("active");
        activeFileEl = fileEl;

        codeEl.textContent = code;
        codePanelEl.hidden = false;
        libraryMetaEl.textContent = `Module: ${file.name}`;
        descriptionEl.hidden = false;
        homeSectionEl.hidden = true;
        descriptionEl.innerHTML = renderMarkdown(description, file.descriptionPath);
        if (exampleCode) {
          exampleCodeEl.textContent = exampleCode;
          exampleMetaEl.textContent = `Exemple pour ${file.name}`;
          exampleSectionEl.hidden = false;
        } else {
          exampleCodeEl.textContent = "";
          exampleMetaEl.textContent = "";
          exampleSectionEl.hidden = true;
        }
        codePanelEl.open = false;
        pageTitleEl.textContent = file.name.toUpperCase();
      };

      filesContainer.appendChild(fileEl);
    });

    categoryDiv.appendChild(toggle);
    categoryDiv.appendChild(filesContainer);
    categoriesDiv.appendChild(categoryDiv);
    categoryRecords.push({
      categoryDiv,
      toggle,
      fileRecords,
    });
  }

  const applySearch = () => {
    const term = normalizeText(searchInputEl.value.trim());

    for (const record of categoryRecords) {
      let visibleCount = 0;

      for (const fileRecord of record.fileRecords) {
        const visible = !term || fileRecord.searchText.includes(term);
        fileRecord.el.style.display = visible ? "" : "none";
        if (visible) {
          visibleCount += 1;
        }
      }

      record.categoryDiv.style.display = visibleCount > 0 ? "" : "none";

      if (!term) {
        record.categoryDiv.classList.add("closed");
        record.toggle.setAttribute("aria-expanded", "false");
      } else if (visibleCount > 0) {
        record.categoryDiv.classList.remove("closed");
        record.toggle.setAttribute("aria-expanded", "true");
      }
    }
  };

  searchInputEl.addEventListener("input", applySearch);

  showHome();
}

loadCategories();

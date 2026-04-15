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

function fetchNoCache(url) {
  return fetch(url, { cache: "no-store" });
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
  const res = await fetchNoCache("files.json");
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
  const codeVariantsEl = document.getElementById("code-variants");
  const pageTitleEl = document.querySelector("#main h1");
  const copyHomeBtnEl = document.getElementById("copy-home-code");
  const copyExampleBtnEl = document.getElementById("copy-example-code");
  const copyLibraryBtnEl = document.getElementById("copy-library-code");
  const homeDescriptionHtml = descriptionEl.innerHTML;
  const categoryRecords = [];
  let activeFileEl = null;
  let activeVariantButtonEl = null;

  wireCopyButton(copyHomeBtnEl, () => homeCodeEl.textContent);
  wireCopyButton(copyExampleBtnEl, () => exampleCodeEl.textContent);
  wireCopyButton(copyLibraryBtnEl, () => codeEl.textContent);

  const hideVariants = () => {
    codeVariantsEl.hidden = true;
    codeVariantsEl.innerHTML = "";
    activeVariantButtonEl = null;
  };

  const setActiveSidebarItem = itemEl => {
    if (activeFileEl) {
      activeFileEl.classList.remove("active");
    }
    itemEl.classList.add("active");
    activeFileEl = itemEl;
    homeLinkEl.classList.remove("active");
  };

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
    hideVariants();
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
    const groupRecords = [];
    const groupRecordByName = new Map();

    toggle.onclick = () => {
      const isClosed = categoryDiv.classList.toggle("closed");
      toggle.setAttribute("aria-expanded", String(!isClosed));
    };

    data[category].forEach(file => {
      if (Array.isArray(file.variants) && file.variants.length > 0) {
        const fileEl = document.createElement("div");
        fileEl.className = "file";
        fileEl.textContent = file.name.toUpperCase();

        const variantNames = file.variants.map(variant => variant.name).join(" ");
        fileRecords.push({
          el: fileEl,
          parentGroupRecord: null,
          searchText: normalizeText(`${category} ${file.name} ${variantNames}`),
        });

        fileEl.onclick = async () => {
          let description = "# Documentation indisponible\n\nAucune documentation Markdown n'a encore ete ajoutee pour ce module.";

          if (file.descriptionPath) {
            const descriptionResponse = await fetchNoCache(file.descriptionPath);
            if (descriptionResponse.ok) {
              description = await descriptionResponse.text();
            }
          }

          setActiveSidebarItem(fileEl);

          descriptionEl.hidden = false;
          homeSectionEl.hidden = true;
          descriptionEl.innerHTML = renderMarkdown(description, file.descriptionPath);
          pageTitleEl.textContent = file.name.toUpperCase();

          codePanelEl.hidden = false;
          codePanelEl.open = false;
          codeVariantsEl.hidden = false;
          codeVariantsEl.innerHTML = "";

          const loadVariant = async variant => {
            const requests = [fetchNoCache(variant.path)];
            if (variant.examplePath) {
              requests.push(fetchNoCache(variant.examplePath));
            }

            const responses = await Promise.all(requests);
            const code = await responses[0].text();
            let exampleCode = "";

            if (variant.examplePath && responses[1] && responses[1].ok) {
              exampleCode = await responses[1].text();
            }

            codeEl.textContent = code;
            libraryMetaEl.textContent = `Module: ${file.name} | Variante: ${variant.name}`;

            if (exampleCode) {
              exampleCodeEl.textContent = exampleCode;
              exampleMetaEl.textContent = `Exemple pour ${variant.name}`;
              exampleSectionEl.hidden = false;
            } else {
              exampleCodeEl.textContent = "";
              exampleMetaEl.textContent = "";
              exampleSectionEl.hidden = true;
            }
          };

          file.variants.forEach((variant, index) => {
            const variantButton = document.createElement("button");
            variantButton.type = "button";
            variantButton.className = "variant-tab";
            variantButton.textContent = variant.name.toUpperCase();

            variantButton.onclick = async () => {
              if (activeVariantButtonEl) {
                activeVariantButtonEl.classList.remove("active");
              }
              variantButton.classList.add("active");
              activeVariantButtonEl = variantButton;
              await loadVariant(variant);
            };

            codeVariantsEl.appendChild(variantButton);

            if (index === 0) {
              variantButton.classList.add("active");
              activeVariantButtonEl = variantButton;
            }
          });

          await loadVariant(file.variants[0]);
        };

        filesContainer.appendChild(fileEl);
        return;
      }

      let targetContainer = filesContainer;
      let parentGroupRecord = null;

      if (file.group) {
        if (!groupRecordByName.has(file.group)) {
          const groupDiv = document.createElement("div");
          groupDiv.className = "module-group closed";

          const groupToggle = document.createElement("button");
          groupToggle.type = "button";
          groupToggle.className = "module-group-toggle";
          groupToggle.setAttribute("aria-expanded", "false");

          const groupTitleText = document.createElement("span");
          groupTitleText.textContent = file.group.toUpperCase();

          const groupCaret = document.createElement("span");
          groupCaret.className = "caret";
          groupCaret.textContent = "▾";

          groupToggle.appendChild(groupTitleText);
          groupToggle.appendChild(groupCaret);

          const groupFilesContainer = document.createElement("div");
          groupFilesContainer.className = "module-group-files";

          groupToggle.onclick = () => {
            const isClosed = groupDiv.classList.toggle("closed");
            groupToggle.setAttribute("aria-expanded", String(!isClosed));
          };

          groupDiv.appendChild(groupToggle);
          groupDiv.appendChild(groupFilesContainer);
          filesContainer.appendChild(groupDiv);

          const newGroupRecord = {
            name: file.group,
            groupDiv,
            groupToggle,
            filesContainer: groupFilesContainer,
            visibleCount: 0,
          };

          groupRecords.push(newGroupRecord);
          groupRecordByName.set(file.group, newGroupRecord);
        }

        parentGroupRecord = groupRecordByName.get(file.group);
        targetContainer = parentGroupRecord.filesContainer;
      }

      const fileEl = document.createElement("div");
      fileEl.className = "file";
      fileEl.textContent = file.name.toUpperCase();
      fileRecords.push({
        el: fileEl,
        parentGroupRecord,
        searchText: normalizeText(`${category} ${file.group || ""} ${file.name} ${file.path}`),
      });

      fileEl.onclick = async () => {
        const requests = [fetchNoCache(file.path)];

        if (file.descriptionPath) {
          requests.push(fetchNoCache(file.descriptionPath));
        } else {
          requests.push(null);
        }

        if (file.examplePath) {
          requests.push(fetchNoCache(file.examplePath));
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

        setActiveSidebarItem(fileEl);

        codeEl.textContent = code;
        hideVariants();
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

      targetContainer.appendChild(fileEl);
    });

    categoryDiv.appendChild(toggle);
    categoryDiv.appendChild(filesContainer);
    categoriesDiv.appendChild(categoryDiv);
    categoryRecords.push({
      categoryDiv,
      toggle,
      fileRecords,
      groupRecords,
    });
  }

  const applySearch = () => {
    const term = normalizeText(searchInputEl.value.trim());

    for (const record of categoryRecords) {
      let visibleCount = 0;

      for (const groupRecord of record.groupRecords) {
        groupRecord.visibleCount = 0;
      }

      for (const fileRecord of record.fileRecords) {
        const visible = !term || fileRecord.searchText.includes(term);
        fileRecord.el.style.display = visible ? "" : "none";
        if (visible) {
          visibleCount += 1;
          if (fileRecord.parentGroupRecord) {
            fileRecord.parentGroupRecord.visibleCount += 1;
          }
        }
      }

      for (const groupRecord of record.groupRecords) {
        groupRecord.groupDiv.style.display = groupRecord.visibleCount > 0 ? "" : "none";

        if (!term) {
          groupRecord.groupDiv.classList.add("closed");
          groupRecord.groupToggle.setAttribute("aria-expanded", "false");
        } else if (groupRecord.visibleCount > 0) {
          groupRecord.groupDiv.classList.remove("closed");
          groupRecord.groupToggle.setAttribute("aria-expanded", "true");
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

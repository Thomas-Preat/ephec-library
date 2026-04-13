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

async function loadCategories() {
  const res = await fetch("files.json");
  const data = await res.json();

  const categoriesDiv = document.getElementById("categories");
  const codeEl = document.getElementById("code");
  const libraryMetaEl = document.getElementById("library-meta");
  const descriptionEl = document.getElementById("description");
  const exampleSectionEl = document.getElementById("example-section");
  const exampleCodeEl = document.getElementById("example-code");
  const exampleMetaEl = document.getElementById("example-meta");
  const codePanelEl = document.getElementById("code-panel");
  const pageTitleEl = document.querySelector("#main h1");
  let activeFileEl = null;

  for (const category in data) {
    const categoryDiv = document.createElement("div");
    categoryDiv.className = "category";

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "category-toggle";
    toggle.setAttribute("aria-expanded", "true");

    const titleText = document.createElement("span");
    titleText.textContent = category;

    const caret = document.createElement("span");
    caret.className = "caret";
    caret.textContent = "▾";

    toggle.appendChild(titleText);
    toggle.appendChild(caret);

    const filesContainer = document.createElement("div");
    filesContainer.className = "files";

    toggle.onclick = () => {
      const isClosed = categoryDiv.classList.toggle("closed");
      toggle.setAttribute("aria-expanded", String(!isClosed));
    };

    data[category].forEach(file => {
      const fileEl = document.createElement("div");
      fileEl.className = "file";
      fileEl.textContent = file.name;

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
        let description = "# Summary unavailable\n\nNo markdown documentation was found for this module yet.";
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

        fileEl.classList.add("active");
        activeFileEl = fileEl;

        codeEl.textContent = code;
        libraryMetaEl.textContent = file.path;
        descriptionEl.innerHTML = renderMarkdown(description, file.descriptionPath);
        if (exampleCode) {
          exampleCodeEl.textContent = exampleCode;
          exampleMetaEl.textContent = file.examplePath;
          exampleSectionEl.hidden = false;
        } else {
          exampleCodeEl.textContent = "";
          exampleMetaEl.textContent = "";
          exampleSectionEl.hidden = true;
        }
        codePanelEl.open = false;
        pageTitleEl.textContent = file.name;
      };

      filesContainer.appendChild(fileEl);
    });

    categoryDiv.appendChild(toggle);
    categoryDiv.appendChild(filesContainer);
    categoriesDiv.appendChild(categoryDiv);
  }
}

loadCategories();

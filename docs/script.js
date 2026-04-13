function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderInlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const html = [];
  let inList = false;
  let inCodeBlock = false;
  let codeBuffer = [];
  let paragraphBuffer = [];

  function flushParagraph() {
    if (!paragraphBuffer.length) {
      return;
    }

    html.push(`<p>${renderInlineMarkdown(paragraphBuffer.join(" "))}</p>`);
    paragraphBuffer = [];
  }

  function closeList() {
    if (!inList) {
      return;
    }

    html.push("</ul>");
    inList = false;
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();

    if (line.startsWith("```") || line.startsWith("~~~")) {
      flushParagraph();
      closeList();

      if (inCodeBlock) {
        html.push(`<pre><code>${escapeHtml(codeBuffer.join("\n"))}</code></pre>`);
        codeBuffer = [];
        inCodeBlock = false;
      } else {
        inCodeBlock = true;
      }

      continue;
    }

    if (inCodeBlock) {
      codeBuffer.push(rawLine);
      continue;
    }

    if (!line) {
      flushParagraph();
      closeList();
      continue;
    }

    const headingMatch = line.match(/^(#{1,3})\s+(.+)$/);
    if (headingMatch) {
      flushParagraph();
      closeList();
      const level = headingMatch[1].length;
      html.push(`<h${level}>${renderInlineMarkdown(headingMatch[2])}</h${level}>`);
      continue;
    }

    const listMatch = line.match(/^[-*]\s+(.+)$/);
    if (listMatch) {
      flushParagraph();
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      html.push(`<li>${renderInlineMarkdown(listMatch[1])}</li>`);
      continue;
    }

    paragraphBuffer.push(line);
  }

  flushParagraph();
  closeList();

  if (inCodeBlock) {
    html.push(`<pre><code>${escapeHtml(codeBuffer.join("\n"))}</code></pre>`);
  }

  return html.join("");
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
        descriptionEl.innerHTML = renderMarkdown(description);
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

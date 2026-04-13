async function loadCategories() {
  const res = await fetch("files.json");
  const data = await res.json();

  const categoriesDiv = document.getElementById("categories");
  const codeEl = document.getElementById("code");
  const codeMetaEl = document.getElementById("code-meta");
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
        const fileRes = await fetch(file.path);
        const code = await fileRes.text();

        if (activeFileEl) {
          activeFileEl.classList.remove("active");
        }

        fileEl.classList.add("active");
        activeFileEl = fileEl;

        codeEl.textContent = code;
        codeMetaEl.textContent = file.path;
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

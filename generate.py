import os
import json
import shutil

BASE_DIR = "code"
DOCS_CODE_DIR = "docs/code"
OUTPUT_FILE = "docs/files.json"

data = {}

os.makedirs(DOCS_CODE_DIR, exist_ok=True)

for category in os.listdir(BASE_DIR):
    category_path = os.path.join(BASE_DIR, category)

    if not os.path.isdir(category_path):
        continue

    data[category] = []

    dest_category = os.path.join(DOCS_CODE_DIR, category)
    os.makedirs(dest_category, exist_ok=True)

    for file in os.listdir(category_path):
        if file.endswith(".py"):
            src = os.path.join(category_path, file)
            dst = os.path.join(dest_category, file)

            shutil.copyfile(src, dst)

            data[category].append({
                "name": file,
                "path": f"code/{category}/{file}"
            })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("files.json generated!")
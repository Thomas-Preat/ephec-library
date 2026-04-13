import os
import json

BASE_DIR = "docs/code"
DESCRIPTION_DIR = "docs/descriptions"
OUTPUT_FILE = "docs/files.json"

data = {}

for category in sorted(os.listdir(BASE_DIR)):
    category_path = os.path.join(BASE_DIR, category)

    if not os.path.isdir(category_path):
        continue

    data[category] = []

    for file in sorted(os.listdir(category_path)):
        if file.endswith(".py"):
            file_stem = os.path.splitext(file)[0]
            description_file = os.path.join(DESCRIPTION_DIR, category, f"{file_stem}.md")

            data[category].append({
                "name": file,
                "path": f"code/{category}/{file}",
                "descriptionPath": (
                    f"descriptions/{category}/{file_stem}.md"
                    if os.path.exists(description_file)
                    else None
                )
            })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("files.json generated!")
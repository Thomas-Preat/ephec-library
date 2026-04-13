import os
import json

BASE_DIR = "docs/code"
OUTPUT_FILE = "docs/files.json"

data = {}

for category in os.listdir(BASE_DIR):
    category_path = os.path.join(BASE_DIR, category)

    if not os.path.isdir(category_path):
        continue

    data[category] = []

    for file in os.listdir(category_path):
        if file.endswith(".py"):
            data[category].append({
                "name": file,
                "path": f"code/{category}/{file}"
            })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("files.json generated!")
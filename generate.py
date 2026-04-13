import os
import json

BASE_DIR = "code"
OUTPUT_FILE = "docs/files.json"

data = {}

for category in os.listdir(BASE_DIR):
    category_path = os.path.join(BASE_DIR, category)

    if not os.path.isdir(category_path):
        continue

    data[category] = []

    for file in os.listdir(category_path):
        if file.endswith(".py"):
            file_path = os.path.join(category_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            data[category].append({
                "name": file,
                "content": content
            })

os.makedirs("docs", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("files.json generated!")
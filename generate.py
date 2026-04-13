import os
import json

BASE_DIR = "docs/elements"
OUTPUT_FILE = "docs/files.json"

data = {}


def rel_from_docs(path):
    return os.path.relpath(path, "docs").replace("\\", "/")


def display_name(element):
    return element.replace("_", " ").replace("-", " ")

for category in sorted(os.listdir(BASE_DIR)):
    category_path = os.path.join(BASE_DIR, category)

    if not os.path.isdir(category_path):
        continue

    data[category] = []

    for element in sorted(os.listdir(category_path)):
        element_path = os.path.join(category_path, element)
        if not os.path.isdir(element_path):
            continue

        preferred_library = os.path.join(element_path, f"{element}.py")
        if os.path.exists(preferred_library):
            library_file = preferred_library
        else:
            library_candidates = sorted(
                name
                for name in os.listdir(element_path)
                if name.endswith(".py") and not name.endswith("_example.py")
            )
            if not library_candidates:
                continue
            library_file = os.path.join(element_path, library_candidates[0])

        preferred_description = os.path.join(element_path, f"{element}.md")
        if os.path.exists(preferred_description):
            description_file = preferred_description
        else:
            description_candidates = sorted(
                name for name in os.listdir(element_path) if name.endswith(".md")
            )
            description_file = (
                os.path.join(element_path, description_candidates[0])
                if description_candidates
                else None
            )

        preferred_example = os.path.join(element_path, f"{element}_example.py")
        if os.path.exists(preferred_example):
            example_file = preferred_example
        else:
            example_candidates = sorted(
                name for name in os.listdir(element_path) if name.endswith("_example.py")
            )
            example_file = (
                os.path.join(element_path, example_candidates[0])
                if example_candidates
                else None
            )

        data[category].append(
            {
                "name": display_name(element),
                "path": rel_from_docs(library_file),
                "descriptionPath": rel_from_docs(description_file) if description_file else None,
                "examplePath": rel_from_docs(example_file) if example_file else None,
            }
        )

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("files.json generated!")
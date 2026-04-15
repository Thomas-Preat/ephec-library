import os
import json

BASE_DIR = "docs/elements"
OUTPUT_FILE = "docs/files.json"

data = {}


def rel_from_docs(path):
    return os.path.relpath(path, "docs").replace("\\", "/")


def display_name(element):
    return element.replace("_", " ").replace("-", " ")


def pick_group_description(group_path, group_name):
    candidates = [
        os.path.join(group_path, f"{group_name}.md"),
        os.path.join(group_path, "index.md"),
        os.path.join(group_path, "README.md"),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None


def pick_module_files(element_path, preferred_name):
    preferred_library = os.path.join(element_path, f"{preferred_name}.py")
    if os.path.exists(preferred_library):
        library_file = preferred_library
    else:
        library_candidates = sorted(
            name
            for name in os.listdir(element_path)
            if name.endswith(".py") and not name.endswith("_example.py")
        )
        if not library_candidates:
            return None, None, None
        library_file = os.path.join(element_path, library_candidates[0])

    preferred_description = os.path.join(element_path, f"{preferred_name}.md")
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

    preferred_example = os.path.join(element_path, f"{preferred_name}_example.py")
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

    return library_file, description_file, example_file


def build_module_entry(element_path, element_name, group=None):
    library_file, description_file, example_file = pick_module_files(element_path, element_name)
    if not library_file:
        return None

    entry = {
        "name": display_name(element_name),
        "path": rel_from_docs(library_file),
        "descriptionPath": rel_from_docs(description_file) if description_file else None,
        "examplePath": rel_from_docs(example_file) if example_file else None,
    }

    if group:
        entry["group"] = display_name(group)

    return entry


def build_bundle_entry(group_path, group_name):
    description_file = pick_group_description(group_path, group_name)
    if not description_file:
        return None

    variants = []
    for nested_element in sorted(os.listdir(group_path)):
        nested_path = os.path.join(group_path, nested_element)
        if not os.path.isdir(nested_path):
            continue

        nested_entry = build_module_entry(nested_path, nested_element)
        if nested_entry:
            variants.append(nested_entry)

    if not variants:
        return None

    return {
        "name": display_name(group_name),
        "descriptionPath": rel_from_docs(description_file),
        "variants": variants,
    }

for category in sorted(os.listdir(BASE_DIR)):
    category_path = os.path.join(BASE_DIR, category)

    if not os.path.isdir(category_path):
        continue

    data[category] = []

    for element in sorted(os.listdir(category_path)):
        element_path = os.path.join(category_path, element)
        if not os.path.isdir(element_path):
            continue

        direct_entry = build_module_entry(element_path, element)
        if direct_entry:
            data[category].append(direct_entry)
            continue

        # Support grouped modules with one extra nesting level:
        # docs/elements/<category>/<group>/<module>/...
        bundle_entry = build_bundle_entry(element_path, element)
        if bundle_entry:
            data[category].append(bundle_entry)
            continue

        for nested_element in sorted(os.listdir(element_path)):
            nested_path = os.path.join(element_path, nested_element)
            if not os.path.isdir(nested_path):
                continue

            nested_entry = build_module_entry(nested_path, nested_element, group=element)
            if nested_entry:
                data[category].append(nested_entry)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("files.json generated!")
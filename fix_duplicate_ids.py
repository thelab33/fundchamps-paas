import os
import re
from collections import defaultdict

TEMPLATE_DIR = "app/templates"
ID_REGEX = re.compile(r'id="([^"]+)"')

def find_duplicate_ids():
    id_map = defaultdict(list)
    for root, _, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for match in ID_REGEX.finditer(content):
                        id_map[match.group(1)].append(path)
    duplicates = {k:v for k,v in id_map.items() if len(v) > 1}
    return duplicates

def fix_duplicate_ids():
    occurrences = defaultdict(int)
    for root, _, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                new_content = content
                matches = list(ID_REGEX.finditer(content))
                # Process backwards to not mess up indices
                for match in reversed(matches):
                    id_val = match.group(1)
                    occurrences[id_val] += 1
                    if occurrences[id_val] > 1:
                        suffix = f"-{occurrences[id_val]}"
                        start, end = match.span(1)
                        new_content = new_content[:start] + id_val + suffix + new_content[end:]
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed duplicates in: {path}")

if __name__ == "__main__":
    print("Checking duplicate IDs...")
    duplicates = find_duplicate_ids()
    if not duplicates:
        print("No duplicate IDs found.")
    else:
        print(f"Found duplicate IDs: {list(duplicates.keys())}")
        fix_duplicate_ids()
        print("Duplicate IDs fixed by appending suffixes.")

import os
import re

MACRO_DIRS = [
    "./templates/macros",
    "./app/templates/macros"
]

MACRO_PATTERN = re.compile(
    r"({%\s*macro\s+[\w_]+\([^\)]*)\*\*kwargs([^\)]*\)\s*-?%})"
)
KWARG_USAGE_PATTERN = re.compile(r"\{%\s*for\s+k,\s*v\s+in\s+kwargs\.items\(\)\s*.*?%}")
MACRO_CALL_PATTERN = re.compile(r"(\{\{\s*[\w_]+\([^\}]*)\b([a-zA-Z0-9_]+)=['\"]?[^\),\}]+['\"]?")

def patch_macro_signature(code):
    # Replace **kwargs with attrs=None
    return MACRO_PATTERN.sub(r"\1attrs=None\2", code)

def patch_macro_body(code):
    # Replace kwargs.items() usage with attrs.items()
    return KWARG_USAGE_PATTERN.sub("{% if attrs %}\n  {% for k, v in attrs.items() if v is not none %}\n    {{ k.replace('_','-') }}=\"{{ v }}\"\n  {% endfor %}\n{% endif %}", code)

def patch_macro_calls(code):
    # Optionally: This does NOT automatically bundle stray unknown kwargs into attrs
    # Just a placeholder for future logic if you want to automate usage updates too.
    return code  # Out of scope for now (safer to patch usage manually)

def patch_file(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    original = content
    content = patch_macro_signature(content)
    content = patch_macro_body(content)
    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Patched: {path}")
    else:
        print(f"— No changes: {path}")

def scan_and_patch():
    for macro_dir in MACRO_DIRS:
        if not os.path.isdir(macro_dir):
            continue
        for root, _, files in os.walk(macro_dir):
            for file in files:
                if file.endswith(".html"):
                    patch_file(os.path.join(root, file))

if __name__ == "__main__":
    print("🔍 FundChamps Macro Patcher: Upgrading all macros for attrs compatibility...")
    scan_and_patch()
    print("\n🌟 All done! Review your macros and test in dev. SaaS-grade extensibility unlocked.")



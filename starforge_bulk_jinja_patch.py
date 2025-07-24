import re
import os
import shutil

ROOT = "app/templates/partials"

# Pattern for bad Jinja: {{ {% ... %} }}
BAD_PATTERN = re.compile(r"{{\s*{%\s*if.*?%}.*?{%\s*endif\s*%}\s*}}", re.DOTALL)

def backup_file(filepath):
    shutil.copy2(filepath, filepath + ".starforgebak")

def scan_and_patch(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    matches = list(BAD_PATTERN.finditer(content))
    if not matches:
        return False

    print(f"\n🔎 Found {len(matches)} issues in {filepath}")

    # Simple auto-patch logic for src and style only!
    patched = content
    for match in matches:
        jinja_snip = match.group(0)
        # Determine if it's an image or style context for the patch
        if "src=" in content[match.start()-10:match.end()+10]:
            # Replace with {{ patched_var }}
            patched_var = "autopatched_img_src"
            # Insert logic up top (brute force for now)
            if '{% set ' + patched_var not in patched:
                logic = (
                    f"{{% set {patched_var} = 'images/fallback.jpg' %}}\n"
                    f"{{% if team and team.img %}}\n"
                    f"  {{% set {patched_var} = team.img %}}\n"
                    f"{{% endif %}}\n"
                    f"{{% if {patched_var} and '://' not in {patched_var} %}}\n"
                    f"  {{% set {patched_var} = url_for('static', filename={patched_var}) %}}\n"
                    f"{{% endif %}}\n"
                )
                patched = logic + patched
            patched = patched.replace(jinja_snip, f"{{{{ {patched_var} }}}}")
        else:
            print(f"⚠️  Not auto-patching (manual): {jinja_snip}")

    # Backup original
    backup_file(filepath)

    # Write patched version
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(patched)

    print(f"✅ {filepath} auto-patched & backed up.")
    return True

def main():
    print("🔦 Starforge Bulk Jinja Patch Scanner")
    for root, dirs, files in os.walk(ROOT):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                try:
                    scan_and_patch(path)
                except Exception as e:
                    print(f"❌ Error patching {path}: {e}")

    print("\n✨ All partials scanned! Manual review recommended for flagged lines.")
    print("Backups saved with .starforgebak extension.")

if __name__ == "__main__":
    main()

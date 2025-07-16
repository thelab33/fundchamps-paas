import os
import re

# Define the templates folder path
TEMPLATES_PATH = "app/templates/"

# Define a list of files that need to be patched
files_to_patch = [
    "index.html",
    "base.html",
    "partials/hero_and_fundraiser.html",
    "partials/fundraiser_meter.html",
    "partials/testimonials.html",
]


# Function to replace HTML entities with corresponding characters
def replace_html_entities(content):
    content = content.replace("&lt;", "<")
    content = content.replace("&gt;", ">")
    content = content.replace("&amp;", "&")
    content = content.replace("&quot;", '"')
    content = content.replace("&apos;", "'")
    return content


# Function to fix invalid Jinja2 tag syntax
def fix_jinja_syntax(content):
    # Fix issues like `if=""`, `loop.index=""` by removing invalid parts
    content = re.sub(r'if=""', "", content)
    content = re.sub(r'loop.index=""', "", content)
    content = re.sub(r'{%\s*="\s*%}', "", content)
    return content


# Function to patch a single file
def patch_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # Replace HTML entities
    content = replace_html_entities(content)

    # Fix Jinja2 tag issues
    content = fix_jinja_syntax(content)

    # Write the patched content back to the file
    with open(file_path, "w") as f:
        f.write(content)

    print(f"Patched: {file_path}")


# Function to patch all files
def patch_templates():
    for template_file in files_to_patch:
        file_path = os.path.join(TEMPLATES_PATH, template_file)
        if os.path.exists(file_path):
            patch_file(file_path)
        else:
            print(f"Warning: File not found: {file_path}")


# Run the patching process
if __name__ == "__main__":
    patch_templates()

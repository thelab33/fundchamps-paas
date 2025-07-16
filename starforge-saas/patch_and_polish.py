import os
import re


def fix_html_tags(template_dir):
    """Fix unclosed HTML tags and update static paths in template files."""
    patterns = {
        "href": r'(<a\s+[^>]*href=")([^"]+)(")',  # Match <a> href links
        "src": r'(<img\s+[^>]*src=")([^"]+)(")',  # Match <img> src links
    }

    # Iterate over all templates in the template_dir
    for root, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".html"):
                template_file = os.path.join(root, file)

                try:
                    with open(template_file, "r") as f:
                        content = f.read()

                    # Iterate over the patterns for href and src
                    for pattern_type, pattern in patterns.items():
                        matches = re.findall(pattern, content)

                        for match in matches:
                            static_path = match[1]
                            # Update static path with url_for
                            new_tag = f'{match[0]}{{ url_for("static", filename="{static_path[7:]}") }}{match[2]}'
                            content = content.replace(
                                match[0] + match[1] + match[2], new_tag
                            )

                    # Write updated content back to the template file
                    with open(template_file, "w") as f:
                        f.write(content)

                    print(f"Added url_for to static references in {template_file}")

                except Exception as e:
                    print(f"Error processing {template_file}: {e}")


if __name__ == "__main__":
    fix_html_tags(
        "path/to/your/templates"
    )  # Make sure to pass the correct template directory

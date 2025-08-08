from bs4 import BeautifulSoup
import re

def audit_html_spacing(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    issues = []

    # Check for sections with 'pb-16' or large padding-bottom
    sections = soup.find_all("section")
    for section in sections:
        if "pb-16" in section.get("class", []):
            issues.append(
                f"Section with ID {section.get('id', 'unknown')} has excessive padding-bottom (pb-16). Consider reducing this."
            )

    # Check for empty containers (div, section, etc. with no content)
    empty_containers = soup.find_all(["div", "section"])
    for container in empty_containers:
        if (
            not container.contents
            and "pb" in container.get("class", [])
        ):
            issues.append(
                f"Empty container <{container.name}> with padding found. It may be causing unnecessary space."
            )

    # Check for footer spacing (padding or margin)
    footer = soup.find("footer")
    if footer:
        if "pb" in footer.get("class", []) or "pt" in footer.get("class", []):
            issues.append(
                "Footer has padding or margin that may be contributing to extra space."
            )

    # Check for hero section with large height (min-h-screen or py-*)
    hero = soup.find(id="hero")
    if hero:
        if "min-h-screen" in hero.get("class", []):
            issues.append(
                "Hero section has large min-height (min-h-screen) which could push content down."
            )
        if any(
            re.search(r"py-\d+", class_name) for class_name in hero.get("class", [])
        ):
            issues.append(
                "Hero section has padding (py-*) that may be causing excessive space."
            )

    return issues

def main():
    # Load the HTML file
    with open("app/templates/index.html", "r") as file:  # Use the correct file path
        html_content = file.read()

    issues = audit_html_spacing(html_content)

    if issues:
        print("Found spacing issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No spacing issues found.")

if __name__ == "__main__":
    main()


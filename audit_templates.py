import os
import re
import argparse

# Regex patterns to check for common issues
FORBIDDEN_DOCTYPE_TAG = "<!DOCTYPE html>"
JINJA2_EXTENDS_PATTERN = re.compile(r'{%\s*extends\s*"base\.html"\s*%}')
ARIA_TAG_PATTERN = re.compile(r'aria-([a-z-]+)="([^"]+)"')

# Function to search for 'DOCTYPE html' tag in partials
def find_doctype_in_files(file_content, file_path):
    if FORBIDDEN_DOCTYPE_TAG in file_content:
        print(f"Error: DOCTYPE html found in partial: {file_path}")

# Function to check Jinja2 template syntax (extends, block, include)
def check_jinja2_syntax(file_content, file_path):
    if not JINJA2_EXTENDS_PATTERN.search(file_content):
        print(f"Warning: Missing '{{% extends 'base.html' %}}' in {file_path}")

# Function to check for correct use of aria attributes for accessibility
def check_aria_attributes(file_content, file_path):
    matches = ARIA_TAG_PATTERN.findall(file_content)
    for match in matches:
        if match[0] not in ['labelledby', 'label', 'modal']:
            print(f"Warning: Invalid ARIA attribute '{match[0]}' found in {file_path}")

# Function to look for unused variables in template (not a foolproof check but basic)
def check_for_unused_variables(file_content, file_path):
    variables = re.findall(r'{{\s*([a-zA-Z0-9_]+)\s*}}', file_content)
    unused_variables = set(variables) - set(re.findall(r'{{\s*(\w+)\s*}}', file_content))
    if unused_variables:
        print(f"Warning: Unused variables {unused_variables} in {file_path}")

# Function to audit a single file
def audit_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            # Run the various checks
            find_doctype_in_files(file_content, file_path)
            check_jinja2_syntax(file_content, file_path)
            check_aria_attributes(file_content, file_path)
            check_for_unused_variables(file_content, file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Function to audit all templates in the provided directory
def audit_templates(template_dir):
    print(f"Auditing templates in directory: {template_dir}")
    for subdir, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(subdir, file)
                print(f"Checking: {file_path}")  # Adding a print to verify the files being processed
                audit_file(file_path)

# Main function to parse arguments and run the audit
def main():
    parser = argparse.ArgumentParser(description="Audit templates for common issues.")
    parser.add_argument("template_dir", help="The directory containing the HTML templates")
    args = parser.parse_args()

    audit_templates(args.template_dir)

if __name__ == "__main__":
    main()


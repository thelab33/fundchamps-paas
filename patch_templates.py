import os

# Directory to search for files
TEMPLATE_DIR = 'app/templates'

# List of files that need patching
FILES_TO_PATCH = [
    'index.html',
    'macros.html',
    'partials/hero_and_fundraiser.html',
    'partials/tiers.html',
    'partials/newsletter.html',
    'partials/sponsor_form.html',
    'partials/story_video_modal.html',
    'partials/footer.html',
    'partials/digital_hub.html',
    'partials/sponsor_spotlight.html',
    'partials/header_and_announcement.html',
    'partials/stats.html',
    'partials/testimonials.html',
    'partials/program_stats_and_calendar.html',
    'partials/about_and_mission.html',
    'partials/testimonial_popover.html',
    'partials/hero_overlay_quote.html',
    'admin/sponsors.html',
    'admin/base.html',
    'admin/dashboard.html',
    'macros/confetti.html',
    'macros/ui.html',
    'macros/progress.html',
    'macros/starforge.html'
]

# Function to add '{% extends 'base.html' %}' to the beginning of the file
def patch_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Debugging: Check the first line content
    print(f"Checking first line of {file_path}: {content[0].strip()}")

    # Check if the first line doesn't contain the extends statement
    if not content[0].startswith("{% extends 'base.html' %}"):
        # Insert extends at the top of the file
        content.insert(0, "{% extends 'base.html' %}\n")

        # Rewrite the file with the patch
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(content)
        
        print("Patched: Added '{}' to {}".format("{% extends 'base.html' %}", file_path))
    else:
        print(f"No patch needed for {file_path}")

# Iterate through all the templates and patch the ones missing '{% extends 'base.html' %}'
def patch_templates(template_dir):
    for subdir, _, files in os.walk(template_dir):
        for file in files:
            if file in FILES_TO_PATCH and file.endswith('.html'):
                file_path = os.path.join(subdir, file)
                patch_file(file_path)

# Run the patching process
patch_templates(TEMPLATE_DIR)


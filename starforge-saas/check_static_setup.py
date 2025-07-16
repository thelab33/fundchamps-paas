import os

# Define the paths for the necessary static directories and files
static_dir = "app/static"
css_dir = os.path.join(static_dir, "css")
js_dir = os.path.join(static_dir, "js")
images_dir = os.path.join(static_dir, "images")

# List of files that should be present in the static folder
required_files = {
    "css": ["tailwind.min.css", "globals.css", "components.css"],
    "js": ["main.js", "htmx.min.js", "alpine.min.js", "aos.js"],
    "images": [
        "logo.webp",
        "connect-atx-team.jpg",
        "sponsor_a_logo.png",
        "sponsor_b_logo.png",
        "sponsor_c_logo.png",
        "board/coach-angel.jpg",
        "board/coach-bj.jpg",
        "board/mimi.jpg",
        "board/chris.jpg",
        "pay/paypal.svg",
        "pay/venmo.svg",
        "pay/applepay.svg",
        "connect-atx-story.mp4",
    ],
}


def check_directory_exists(path):
    """Check if a directory exists."""
    if not os.path.isdir(path):
        print(f"[ERROR] Directory not found: {path}")
        return False
    return True


def check_files_in_directory(directory, files):
    """Check if specific files exist within a directory."""
    for file in files:
        file_path = os.path.join(directory, file)
        if not os.path.isfile(file_path):
            print(f"[ERROR] Missing file: {file_path}")
        else:
            print(f"[SUCCESS] Found file: {file_path}")


def check_flask_static_config():
    """Check if Flask is configured correctly for static files."""
    print("[INFO] Verifying Flask static file serving configuration...")
    if not os.path.isdir("app/static"):
        print("[ERROR] The 'static' folder is missing in your Flask app.")
    else:
        print("[SUCCESS] 'static' folder found in Flask app.")


def main():
    # Check if the required directories exist
    print("[INFO] Checking if required static directories exist...")
    check_directory_exists(css_dir)
    check_directory_exists(js_dir)
    check_directory_exists(images_dir)

    # Check if the required files exist in the static directories
    print("\n[INFO] Checking if all required CSS files are present...")
    check_files_in_directory(css_dir, required_files["css"])

    print("\n[INFO] Checking if all required JS files are present...")
    check_files_in_directory(js_dir, required_files["js"])

    print("\n[INFO] Checking if all required image files are present...")
    check_files_in_directory(images_dir, required_files["images"])

    # Check Flask static file config
    check_flask_static_config()


if __name__ == "__main__":
    main()

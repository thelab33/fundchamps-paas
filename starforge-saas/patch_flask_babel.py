import os
import sys
import subprocess


# Step 1: Install Flask-Babel if not already installed
def install_flask_babel():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask-Babel"])
        print("Flask-Babel installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install Flask-Babel. Please check your environment.")
        sys.exit(1)


# Step 2: Patch the Flask application to include Flask-Babel
def patch_flask_app():
    app_file = "app/__init__.py"  # Adjust the file path if needed
    babel_setup_code = """
from flask_babel import Babel

# Initialize Babel
babel = Babel(app)

# Configure the default language (optional, change as needed)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
"""

    # Check if the app file exists
    if not os.path.exists(app_file):
        print(f"Error: The file {app_file} does not exist.")
        sys.exit(1)

    # Read the current contents of the file
    with open(app_file, "r") as f:
        content = f.read()

    # Check if Babel is already configured in the file
    if "from flask_babel import Babel" in content:
        print("Flask-Babel is already set up.")
    else:
        print("Patching Flask app to include Flask-Babel...")
        # Insert the necessary imports and setup code
        with open(app_file, "a") as f:
            f.write(babel_setup_code)
        print(f"Flask app patched successfully in {app_file}. Please restart your app.")


# Step 3: Patch the templates to ensure `_` (underscore) function is available
def patch_templates():
    template_file = "app/templates/index.html"  # Adjust the file path as needed
    try:
        with open(template_file, "r") as f:
            content = f.read()

        # Check if the line with translation function is present
        if "_(" in content:
            print("Translation function `_()` already used in the template.")
        else:
            print(f"Adding translation function `_()` to {template_file}.")
            # Add a fallback translation function usage example
            content = content.replace(
                "{{ team.team_name if team else _('Your Organization') }}",
                "{{ _('Home') }} · {{ team.team_name if team else _('Your Organization') }}",
            )
            with open(template_file, "w") as f:
                f.write(content)
            print(f"Template patched successfully in {template_file}.")

    except Exception as e:
        print(f"Error while patching template: {e}")
        sys.exit(1)


# Step 4: Execute the patch script
def main():
    print("Starting patch script...")

    # Install Flask-Babel if necessary
    install_flask_babel()

    # Patch the Flask app
    patch_flask_app()

    # Patch the templates (add _() usage)
    patch_templates()

    print("Patch completed successfully!")


if __name__ == "__main__":
    main()

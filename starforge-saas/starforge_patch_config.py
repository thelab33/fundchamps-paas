import os


def patch_config():
    config_dir = "app/config"
    init_path = os.path.join(config_dir, "__init__.py")

    # Check if __init__.py exists, and if so, backup it
    if os.path.exists(init_path):
        backup_path = init_path + ".bak"
        print(f"Backing up {init_path} to {backup_path}")
        os.rename(init_path, backup_path)

    # Write the corrected import to __init__.py
    with open(init_path, "w") as file:
        file.write("from .flask_config import DevelopmentConfig, ProductionConfig\n")

    print(f"Patched {init_path} with correct imports.")


if __name__ == "__main__":
    patch_config()

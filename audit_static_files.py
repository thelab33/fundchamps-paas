import os

# Path to your static folder
STATIC_PATH = 'app/static'
# File extensions to check (you can add more if needed)
EXTENSIONS = ['.css', '.js', '.jpg', '.jpeg', '.png', '.webp', '.mp4', '.svg']

def check_static_files():
    missing_files = []
    
    # Walk through the static folder and list files
    for root, dirs, files in os.walk(STATIC_PATH):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                # Check if the file exists by the path
                file_path = os.path.join(root, file)
                if not os.path.exists(file_path):
                    missing_files.append(file_path)
    
    # Output the missing files if any
    if missing_files:
        print(f"Missing static files:\n{chr(10).join(missing_files)}")
    else:
        print("All static files are accounted for!")

if __name__ == "__main__":
    check_static_files()

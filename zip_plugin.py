import os
import zipfile

def add_to_zip(zip_file, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
            zip_file.write(file_path, arcname)

def create_zip_with_contents():
    zip_filename = "blender_to_unity_fbx_exporter.zip"
    
    # Get the absolute path of the current script directory
    base_dir = os.path.abspath(os.path.dirname(__file__))

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add __init__.py
        init_path = os.path.join(base_dir, "__init__.py")
        if os.path.exists(init_path):
            zipf.write(init_path, "__init__.py")
        else:
            print(f"Warning: {init_path} not found. Skipping.")

        # Add blender_manifest.toml
        manifest_path = os.path.join(base_dir, "blender_manifest.toml")
        if os.path.exists(manifest_path):
            zipf.write(manifest_path, "blender_manifest.toml")
        else:
            print(f"Warning: {manifest_path} not found. Skipping.")

        # Add the folder and its contents
        folder_path = os.path.join(base_dir, "blender_to_unity_fbx_exporter")
        add_to_zip(zipf, folder_path)

    print(f"Created {zip_filename} with __init__.py, blender_manifest.toml, and {folder_path} contents.")

if __name__ == "__main__":
    create_zip_with_contents()

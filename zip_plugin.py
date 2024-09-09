
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
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add __init__.py
        zipf.writestr("__init__.py", "")
        
        # Add the folder and its contents
        folder_path = "blender_to_unity_fbx_exporter"
        add_to_zip(zipf, folder_path)

    print(f"Created {zip_filename} with __init__.py and {folder_path} contents.")

if __name__ == "__main__":
    create_zip_with_contents()

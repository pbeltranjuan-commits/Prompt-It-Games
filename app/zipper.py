import zipfile
import os
import glob

def create_zip(folder_path: str, zip_name: str) -> str:
    """Comprimeix tota la carpeta output/ en un ZIP llest per enviar."""
    zip_path = os.path.join(folder_path, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in glob.glob(f"{folder_path}/**/*", recursive=True):
            if os.path.isfile(file) and not file.endswith('.zip'):
                arcname = os.path.relpath(file, folder_path)
                zf.write(file, arcname)
    return zip_path

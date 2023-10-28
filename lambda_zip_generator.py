import os

def install_dependencies(folder):
    os.system(f"xcopy {folder} {folder}_copy\ /E /H /q")
    os.system(f"pip install -r requirements.txt -t {folder}_copy")
    os.system(f"powershell Compress-Archive -Path {folder}_copy/* -CompressionLevel Optimal -DestinationPath {folder}.zip")
    os.system(f"rmdir /s /q {folder}_copy -y")


install_dependencies("money")
import os

def install_dependencies(folder):
    print(f"Copy files for {folder}")
    os.system(f"cp -r {folder} {folder}_copy")
    os.system(f"cp utils.py {folder}_copy")
    os.system(f"rm -rf {folder}_copy/__pycache__")
    print(f"Install requirements for {folder}")
    os.system(f"pip install -r requirements.txt -t {folder}_copy")
    print(f"Generate zip file for {folder}")
    os.system(f"cd {folder}_copy && zip -r ../{folder}.zip .")
    os.system(f"rm -rf {folder}_copy")

for item in [
    "account", "asset", "broker",
    "deposit", "money", "position"
]:
    install_dependencies(item)

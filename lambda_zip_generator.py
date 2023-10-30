import os

def install_dependencies(folder):
    print(f"Copy files for {folder}")
    os.system(f"cp -r {folder} {folder}_copy")
    os.system(f"cp resources.utils.py {folder}_copy")
    os.system(f"cp resources.comparison.py {folder}_copy")
    os.system(f"cp resources.filters.py {folder}_copy")
    os.system(f"rm -rf {folder}_copy/__pycache__")
    print(f"Install requirements for {folder}")
    os.system(f"pip install -r requirements.txt -t {folder}_copy")
    print(f"Generate zip file for {folder}")
    os.system(f"cd {folder}_copy && zip -r ../positions_backend_micro/data/{folder}.zip .")
    os.system(f"rm -rf {folder}_copy")

for item in [
    "account", "asset", "broker",
    "deposit", "money", "position"
]:
    install_dependencies(item)

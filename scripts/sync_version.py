import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def sync_version():
    meson_file = ROOT / "meson.build"
    if not meson_file.exists():
        print("meson.build not found!")
        sys.exit(1)

    content = meson_file.read_text(encoding="utf-8")
    match = re.search(r"version:\s*'([0-9a-zA-Z\.\-]+)'", content)
    if not match:
        print("Could not find version string in meson.build")
        sys.exit(1)
    
    version = match.group(1)
    print(f"Parsed version '{version}' from meson.build")

    # 1. Update pyproject.toml
    pyproject_file = ROOT / "pyproject.toml"
    if pyproject_file.exists():
        py_content = pyproject_file.read_text(encoding="utf-8")
        py_content = re.sub(
            r'^version\s*=\s*".*"', 
            f'version = "{version}"', 
            py_content, 
            flags=re.MULTILINE
        )
        pyproject_file.write_text(py_content, encoding="utf-8")
        print("Updated pyproject.toml")

    # 2. Update __init__.py
    init_file = ROOT / "src" / "udm" / "__init__.py"
    if init_file.exists():
        init_content = init_file.read_text(encoding="utf-8")
        init_content = re.sub(
            r'^__version__\s*=\s*".*"', 
            f'__version__ = "{version}"', 
            init_content, 
            flags=re.MULTILINE
        )
        init_file.write_text(init_content, encoding="utf-8")
        print("Updated src/udm/__init__.py")

    # 3. Update constants.py
    constants_file = ROOT / "src" / "udm" / "constants.py"
    if constants_file.exists():
        const_content = constants_file.read_text(encoding="utf-8")
        const_content = re.sub(
            r'^APP_VERSION\s*=\s*".*"', 
            f'APP_VERSION = "{version}"', 
            const_content, 
            flags=re.MULTILINE
        )
        constants_file.write_text(const_content, encoding="utf-8")
        print("Updated src/udm/constants.py")

if __name__ == "__main__":
    sync_version()

# Universal Dev Manager

A professional, cross-platform desktop application that lets developers **search, select, and install** programming languages, compilers, SDKs, and developer tools from a comprehensive catalog — all from a single, beautiful Qt-based GUI.

---

## ✨ Features

| Feature | Details |
|---|---|
| **50+ Tools** | Languages, compilers, SDKs, frameworks, AI/ML, mobile & web dev |
| **Instant Search** | Type to filter the tool list in real time |
| **Category Filter** | Dropdown to filter by Languages, Compilers, SDKs, Frameworks, etc. |
| **Smart Install** | Install button stays disabled until ≥1 item is selected |
| **Cross-Platform** | Windows (winget), Linux (apt), macOS (Homebrew) |
| **Auto Detection** | Skips tools that are already installed |
| **PATH Management** | Automatically configures environment variables |
| **Live Progress** | Progress bar, status label, and colour-coded log console |
| **Thread-Safe** | Installations run in background threads — GUI never freezes |
| **Configurable** | All tools loaded dynamically from `tools.json` |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** — Fast Python package manager
- **Windows**: `winget` (ships with Windows 10 / 11)
- **Linux**: `apt` (Debian / Ubuntu)
- **macOS**: `brew` (Homebrew) — auto-installed if missing

### Install & Run

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the application
uv run python -m udm
```

For admin / elevated mode (recommended on Windows):

```bash
uv run python -m udm --elevate
```

---

## 📦 Building Distributables

### Using Meson

```bash
meson setup builddir
meson compile -C builddir build-exe       # Windows .exe
meson compile -C builddir build-appimage  # Linux AppImage
meson compile -C builddir build-dmg       # macOS .dmg
```

### Direct Scripts

```bash
uv run python scripts/build_exe.py       # Windows
bash scripts/build_appimage.sh            # Linux
bash scripts/build_dmg.sh                 # macOS
```

Output appears in the `dist/` folder.

---

## ⚙️ Configuration

Edit `tools.json` to add, remove, or modify tools. Each entry:

```json
{
  "key": "python",
  "name": "Python",
  "description": "General-purpose programming language",
  "category": "Languages",
  "detect_cmd": "python --version",
  "detect_cmd_alt": "python3 --version",
  "install_command_windows": "winget install --id Python.Python.3.12 ...",
  "install_command_linux": "sudo apt-get install -y python3",
  "install_command_mac": "brew install python",
  "path_dirs_windows": ["%LOCALAPPDATA%\\Programs\\Python\\Python312"],
  "path_required": true
}
```

---

## 🔒 Security

- Tools are **never reinstalled** if already detected
- All downloads use official package managers (winget, apt, brew)
- No third-party download servers
- PATH changes use the Windows Registry API (not truncation-prone `setx`)

---

## 📄 License

Provided as-is for educational and professional use. Free to modify and distribute.

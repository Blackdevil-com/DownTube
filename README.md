# Downloader


# 🎬 DownTube

> A lightweight YouTube downloader for Windows — built with Python, PySide6, and yt-dlp. Packaged as a standalone `.exe` with a one-click installer.

DownTube provides a clean desktop GUI for downloading YouTube videos and audio. No browser extensions, no command-line knowledge required — just paste a URL and download.

---

## ✨ Features

- **YouTube Video & Audio Download** — Powered by `yt-dlp`, one of the most actively maintained download libraries
- **Desktop GUI** — Built with PySide6 for a native-feeling Windows interface
- **Standalone Executable** — Distributed as a single `.exe` via PyInstaller; no Python installation needed for end users
- **Windows Installer** — Packaged with Inno Setup for a proper install/uninstall experience with desktop shortcut
- **Automated Build Pipeline** — `build.py` handles version bumping, `yt-dlp` updates, PyInstaller compilation, and installer generation in one command
- **Auto yt-dlp Updater** — Build script always fetches the latest `yt-dlp` before packaging, keeping downloads working even as YouTube changes

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| GUI Framework | PySide6 (Qt for Python) |
| Download Engine | yt-dlp |
| Executable Builder | PyInstaller |
| Installer Packager | Inno Setup 6 |
| Build Automation | Python (`build.py`) + Batch script |

---

## 📋 Requirements

**To run from source:**
- Python 3.9+
- Dependencies listed below

**To build the installer:**
- [Inno Setup 6](https://jrsoftware.org/isdl.php) installed at `E:\Softwares\Inno Setup 6\` (or update the path in `build.py`)

---

## 🚀 Getting Started

### Run from Source

```bash
# 1. Clone the repository
git clone https://github.com/Blackdevil-com/DownTube.git
cd DownTube

# 2. Install dependencies
pip install PySide6 yt-dlp

# 3. Run the app
python src/main.py
```

### Build a Distributable `.exe`

```bash
# Builds EXE via PyInstaller using run_script.bat
python -m PyInstaller --onefile --windowed ^
  --name DownTube ^
  --icon=src\icon.ico ^
  --hidden-import=yt_dlp ^
  --add-data "src\icon.ico;." ^
  src\main.py
```

### Full Release Build (EXE + Installer)

```bash
# Runs the full pipeline:
# 1. Bumps patch version in version.txt
# 2. Updates yt-dlp to latest
# 3. Cleans old build artifacts
# 4. Compiles EXE with PyInstaller
# 5. Updates version in DownTube.iss
# 6. Builds Windows installer with Inno Setup

python build.py
```

The installer will be output to the `installer/` directory as `DownTubeSetup.exe`.

---

## 📁 Project Structure

```
DownTube/
├── src/
│   ├── main.py          # Application entry point (PySide6 GUI)
│   └── icon.ico         # App icon
├── build.py             # Automated release build script
├── run_script.bat       # PyInstaller build command
├── DownTube.iss         # Inno Setup installer configuration
└── version.txt          # Current version (auto-incremented by build.py)
```

---

## ⚙️ Build Pipeline

```
python build.py
       │
       ├── 1. Read version.txt → bump patch → write back
       ├── 2. pip install -U yt-dlp
       ├── 3. Clean /build and /dist directories
       ├── 4. run_script.bat → PyInstaller → dist/DownTube.exe
       ├── 5. Patch AppVersion in DownTube.iss
       └── 6. ISCC.exe DownTube.iss → installer/DownTubeSetup.exe
```

---

## 📸 Screenshots

> *(Add screenshots of the app UI here)*

---

## ⚠️ Disclaimer

This tool is intended for downloading content you have the right to download (e.g., your own videos, Creative Commons licensed content, or content where the platform permits downloading). Please respect YouTube's Terms of Service and copyright laws in your region.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Bharath Kumar L**
- GitHub: [@Blackdevil-com](https://github.com/Blackdevil-com)
- LinkedIn: [bharath-kumar-l-0a320b319](https://linkedin.com/in/bharath-kumar-l-0a320b319)

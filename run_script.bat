python -m PyInstaller --onefile --windowed ^
--name DownTube ^
--icon=src\icon.ico ^
--hidden-import=yt_dlp ^
--add-data "src\icon.ico;." ^
--exclude-module PySide6.QtQml ^
--exclude-module PySide6.QtQuick ^
--exclude-module PySide6.QtMultimedia ^
--exclude-module PySide6.QtWebEngine ^
src\main.py

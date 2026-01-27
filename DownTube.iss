[Setup]
AppName=DownTube
AppVersion=1.0
DefaultDirName={pf}\DownTube
DefaultGroupName=DownTube
OutputDir=installer
OutputBaseFilename=DownTubeSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; DestName: "DownTube.exe"; Flags: ignoreversion

[Icons]
Name: "{group}\DownTube"; Filename: "{app}\DownTube.exe"
Name: "{commondesktop}\DownTube"; Filename: "{app}\DownTube.exe"

[Run]
Filename: "{app}\DownTube.exe"; Description: "Launch DownTube"; Flags: nowait postinstall skipifsilent

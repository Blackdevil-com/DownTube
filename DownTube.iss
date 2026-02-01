[Setup]
AppName=DownTube
AppVersion=1.0.2
DefaultDirName={pf}\DownTube
DefaultGroupName=DownTube
OutputDir=installer
OutputBaseFilename=DownTubeSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=src\icon.ico

[Files]
Source: "dist\DownTube.exe"; DestDir: "{app}"; DestName: "DownTube.exe"; Flags: ignoreversion

[Icons]
Name: "{group}\DownTube"; Filename: "{app}\DownTube.exe"
Name: "{commondesktop}\DownTube"; Filename: "{app}\DownTube.exe"

[Run]
Filename: "{app}\DownTube.exe"; Description: "Launch DownTube"; Flags: nowait postinstall skipifsilent

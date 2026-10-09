#define AppName "TRACE Edge"
#define AppVersion "1.4.0"
[Setup]
AppId={{E3A7A901-0E16-4DA5-B2AA-1B9B0E764A20}
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={autopf}\TRACE Edge
DefaultGroupName=TRACE Edge
OutputDir=output
OutputBaseFilename=TRACE-Edge-Setup-v1.4.0
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
[Files]
Source: "..\desktop\dist\TRACE-Edge-Manager.exe"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\TRACE Edge"; Filename: "{app}\TRACE-Edge-Manager.exe"
Name: "{autodesktop}\TRACE Edge"; Filename: "{app}\TRACE-Edge-Manager.exe"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"
[Run]
Filename: "{app}\TRACE-Edge-Manager.exe"; Description: "Open TRACE Edge"; Flags: postinstall nowait skipifsilent

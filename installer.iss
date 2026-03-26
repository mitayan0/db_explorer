#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppName=DB Explorer
AppVersion={#AppVersion}
AppPublisher=Datafluent BD
AppCopyright=Copyright (C) 2026 Datafluent BD
DefaultDirName={autopf}\DB Explorer
DefaultGroupName=DB Explorer
OutputDir=installer_output
OutputBaseFilename=DB-Explorer-v{#AppVersion}-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LicenseFile=LICENSE.txt
; Require 64-bit Windows
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Include all files from the one-folder PyInstaller build
Source: "dist\DB_Explorer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\DB Explorer"; Filename: "{app}\DB_Explorer.exe"
Name: "{group}\{cm:UninstallProgram,DB Explorer}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\DB Explorer"; Filename: "{app}\DB_Explorer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\DB_Explorer.exe"; Description: "{cm:LaunchProgram,DB Explorer}"; Flags: nowait postinstall skipifsilent

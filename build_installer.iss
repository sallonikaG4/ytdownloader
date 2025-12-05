; Inno Setup Script for YouTube to MP3 Downloader
; This creates a Windows installer that includes Python, FFmpeg, and the application

#define MyAppName "YouTube to MP3 Downloader"
#define MyAppVersion "2.1.0"
#define MyAppPublisher "WaLLe"
#define MyAppURL "https://github.com"
#define MyAppExeName "YouTubeToMP3.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
OutputDir=dist
OutputBaseFilename=YouTubeToMP3_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\YouTubeToMP3.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "download_ffmpeg.ps1"; DestDir: "{tmp}"; Flags: deleteafterinstall
; Note: Python runtime is included in the PyInstaller bundle
; FFmpeg will be installed automatically during setup

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

[Run]
; Install FFmpeg automatically (if not already installed)
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File ""{tmp}\download_ffmpeg.ps1"" -InstallPath ""{app}\ffmpeg"""; StatusMsg: "Installing FFmpeg (this may take a few minutes)..."; Flags: runhidden waituntilterminated; Check: not IsFFmpegInstalled
; Launch application after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
var
  FFmpegInstalled: Boolean;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  FFmpegInstalled := False;
  
  // Check if FFmpeg is already installed
  if Exec('ffmpeg', '-version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    FFmpegInstalled := True;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if CurPageID = wpReady then
  begin
    // Inform user about FFmpeg installation if needed
    if not FFmpegInstalled then
    begin
      if MsgBox('FFmpeg is required for audio conversion.' + #13#10 + #13#10 +
                'The installer will attempt to download and install FFmpeg automatically.' + #13#10 +
                'This may take a few minutes and requires an internet connection.' + #13#10 + #13#10 +
                'Do you want to continue?',
                mbConfirmation, MB_YESNO) = IDNO then
      begin
        Result := False;
      end;
    end;
  end;
end;

function IsFFmpegInstalled(): Boolean;
begin
  Result := FFmpegInstalled;
end;

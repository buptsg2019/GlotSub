; GlotSub 安装程序脚本 (Inno Setup)
; 需要先安装 Inno Setup: https://jrsoftware.org/isdl.php

#define MyAppName "GlotSub"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "GlotSub Team"
#define MyAppURL "https://github.com/your-repo/GlotSub"
#define MyAppExeName "GlotSub.exe"

[Setup]
; 注意: AppId 的值用于标识此应用程序
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer
OutputBaseFilename=GlotSub_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "dist\GlotSub.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "INSTALL.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
var
  TesseractPage: TOutputProgressWizardPage;
  DownloadPage: TDownloadWizardPage;
  TesseractInstalled: Boolean;

// 检查 Tesseract OCR 是否已安装
function IsTesseractInstalled: Boolean;
var
  TesseractPath: String;
begin
  Result := False;
  // 检查注册表
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Tesseract-OCR', 'Path', TesseractPath) then
  begin
    Result := FileExists(TesseractPath + 'tesseract.exe');
  end;
  // 检查常见安装路径
  if not Result then
  begin
    if FileExists('C:\Program Files\Tesseract-OCR\tesseract.exe') then
      Result := True
    else if FileExists('C:\Program Files (x86)\Tesseract-OCR\tesseract.exe') then
      Result := True;
  end;
end;

// 使用 Chocolatey 安装 Tesseract
function InstallTesseractWithChoco: Boolean;
var
  ResultCode: Integer;
begin
  Result := False;
  if Exec('choco', 'install tesseract -y --params="/Language:chi_sim /Language:eng"', '', 
          SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    Result := (ResultCode = 0);
  end;
end;

// 下载并安装 Tesseract
function DownloadAndInstallTesseract: Boolean;
var
  DownloadUrl: String;
  SetupFile: String;
  ResultCode: Integer;
begin
  Result := False;
  DownloadUrl := 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.0.20241111.exe';
  SetupFile := ExpandConstant('{tmp}\tesseract-setup.exe');
  
  // 下载 Tesseract 安装程序
  if DownloadPage.Clear then
  begin
    DownloadPage.Add(DownloadUrl, SetupFile, '');
    try
      DownloadPage.Show;
      try
        if DownloadPage.Download then
        begin
          // 静默安装 Tesseract（需要管理员权限）
          if Exec(SetupFile, '/S /D="C:\Program Files\Tesseract-OCR"', '', 
                  SW_HIDE, ewWaitUntilTerminated, ResultCode) then
          begin
            Result := (ResultCode = 0);
          end;
        end;
      finally
        DownloadPage.Hide;
      end;
    except
      // 下载失败，返回 False
      Result := False;
    end;
  end;
end;

procedure InitializeWizard;
begin
  TesseractInstalled := IsTesseractInstalled;
  
  if not TesseractInstalled then
  begin
    // 创建下载页面
    DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), 
                                       SetupMessage(msgPreparingDesc), nil);
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  // 在准备安装页面检查 Tesseract
  if CurPageID = wpReady then
  begin
    if not TesseractInstalled then
    begin
      if MsgBox('检测到系统未安装 Tesseract OCR。' + #13#10 + #13#10 +
                'GlotSub 需要 Tesseract OCR 才能运行。' + #13#10 + #13#10 +
                '是否现在自动安装 Tesseract OCR？' + #13#10 +
                '（需要管理员权限和网络连接）',
                mbConfirmation, MB_YESNO) = IDYES then
      begin
        // 先尝试使用 Chocolatey
        if Exec('choco', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
        begin
          if InstallTesseractWithChoco then
          begin
            TesseractInstalled := True;
            MsgBox('Tesseract OCR 安装成功！', mbInformation, MB_OK);
          end;
        end;
        
        // 如果 Chocolatey 失败，尝试下载安装
        if not TesseractInstalled then
        begin
          if DownloadAndInstallTesseract then
          begin
            TesseractInstalled := True;
            MsgBox('Tesseract OCR 安装成功！', mbInformation, MB_OK);
          end
          else
          begin
            MsgBox('自动安装 Tesseract OCR 失败。' + #13#10 + #13#10 +
                   '请手动安装 Tesseract OCR：' + #13#10 +
                   'https://github.com/UB-Mannheim/tesseract/wiki' + #13#10 + #13#10 +
                   '安装时请确保勾选中文语言包（Chinese Simplified）。',
                   mbError, MB_OK);
          end;
        end;
      end
      else
      begin
        MsgBox('警告：未安装 Tesseract OCR，程序可能无法正常运行。' + #13#10 +
               '安装完成后，请手动安装 Tesseract OCR。',
               mbWarning, MB_OK);
      end;
    end;
  end;
end;


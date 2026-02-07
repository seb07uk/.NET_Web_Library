![Logo](https://github.com/seb07uk/.NET_Web_Library/blob/main/screenshot.png)


# .NET Web Library 2.0

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-polsoft.ITS-green.svg)

A powerful tool for managing .NET Runtime installations across multiple versions with a modern GUI interface.

## 🌟 Features

- ✅ Install and update multiple .NET Runtime versions (6.0, 7.0, 8.0, 9.0)
- 🌐 Bilingual interface (Polish/English)
- 🎨 Modern dark-themed GUI
- 💾 Remembers window size preferences
- 📦 Supports both Desktop Runtime and Runtime packages
- 🔄 Automatic update detection

## 📋 Requirements

### System Requirements
- **OS:** Windows 10 or newer (64-bit)
- **RAM:** 2 GB minimum (4 GB recommended)
- **Disk Space:** 500 MB free space
- **Internet:** Required for downloading packages

### ⚠️ CRITICAL: Required Files

The application **MUST** have `winget.exe` in the same directory to function!

```
📂 Application Directory/
├── 📄 DotNet_Installer.exe
├── 📄 winget.exe              ⬅️ REQUIRED!
├── 📄 icon.ico
├── 📄 Help.html
└── 📄 window_config.txt       (created automatically)
```

## 📥 Installation

### Step 1: Download winget.exe

**winget.exe** is Microsoft's Windows Package Manager and is essential for this application.

🔗 **Download from:** [https://github.com/microsoft/winget-cli/releases](https://github.com/microsoft/winget-cli/releases)

**Instructions:**
1. Visit the link above
2. Download the latest release
3. If you download `.msixbundle`, install it first, then find `winget.exe` in:
   ```
   C:\Program Files\WindowsApps\Microsoft.DesktopAppInstaller_*\
   ```
4. Copy `winget.exe` to your application folder

### Step 2: Organize Files

Place all files in the same directory:
- `DotNet_Installer.exe` (main application)
- `winget.exe` (Windows Package Manager)
- `icon.ico` (application icon)
- `Help.html` (help documentation)

### Step 3: Verify Installation

Run the verification script:
```batch
check_requirements.bat        # Polish
check_requirements_EN.bat     # English
```

This will verify all required files are present.

### Step 4: Run the Application

Double-click `DotNet_Installer.exe` and start managing your .NET installations!

## 🚀 Usage

1. **Select a .NET version** from the available packages
2. **Click "Install/Update"** button
3. **Wait** for the installation to complete
4. **Success notification** will appear when done

### Available .NET Versions

- .NET Desktop Runtime 6.0.x
- .NET Desktop Runtime 7.0.x
- .NET Desktop Runtime 8.0.x
- .NET Desktop Runtime 9.0.x
- .NET Runtime 6.0.x
- .NET Runtime 7.0.x
- .NET Runtime 8.0.x
- .NET Runtime 9.0.x

## 🎯 Additional Features

| Feature | Description |
|---------|-------------|
| 🌐 **Microsoft .NET** | Opens official Microsoft .NET website |
| 📜 **PowerShell Script** | Runs PowerShell installation script |
| 🐧 **Bash Script** | Runs Bash installation script (Linux/macOS) |
| 📖 **Help** | Opens bilingual help documentation |
| ℹ️ **About** | Shows application and author information |
| 🌐 **Language** | Switch between Polish and English |

## 🛠️ Building from Source

### Prerequisites
- Python 3.8 or newer
- pip package manager

### Build Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the executable:**
   
   **Windows:**
   ```batch
   build_exe.bat
   ```
   
   **Manual:**
   ```bash
   pyinstaller --onefile --windowed --icon=icon.ico dotnet_installer.py
   ```

3. **Copy winget.exe to dist/ directory**

## 🐛 Troubleshooting

### Problem: "Cannot find winget.exe"
**Solution:** Ensure `winget.exe` is in the same folder as `DotNet_Installer.exe`

### Problem: "Installation failed"
**Solutions:**
- Check internet connection
- Run as Administrator
- Verify sufficient disk space

### Problem: "Application won't start"
**Solutions:**
- Run as Administrator
- Check Windows Event Viewer for errors
- Verify all Windows components are installed

## 📚 Documentation

- `README.txt` - Complete documentation (Polish)
- `Help.html` - Interactive help (Polish & English)
- `INSTALLATION_GUIDE.txt` - Quick installation guide (English)

## 👨‍💻 Author

**Sebastian Januchowski**
- Organization: polsoft.ITS London
- Email: polsoft.its@fastservice.com
- GitHub: [@seb07uk](https://github.com/seb07uk)

## 📄 License

© 2025 polsoft.ITS™ - All rights reserved

This software is provided "AS IS" without any warranties.
The author is not liable for any damages arising from the use of this software.

## 🔄 Changelog

### Version 2.0 (2025)
- ✨ Added support for local winget.exe file
- 🎨 Enhanced user interface
- 🌐 Added bilingual help (PL/EN)
- 🔧 Improved installation stability
- 💾 Added window size persistence
- 📖 Comprehensive documentation

### Version 1.0
- 🎉 Initial release
- ⚙️ Basic .NET installation functionality

---

<div align="center">

**Made with ❤️ by polsoft.ITS**

[Report Bug](https://github.com/seb07uk/dotnet-installer/issues) · [Request Feature](https://github.com/seb07uk/dotnet-installer/issues)

</div>

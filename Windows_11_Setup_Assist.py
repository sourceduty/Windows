# =======================================================================
#                       Windows 11 Setup Assist
# =======================================================================
#
# Copyright (C) 2024, Sourceduty - All Rights Reserved.
#
# This Python program automates several setup tasks for a fresh Windows 11
# installation, including:
# 
# 1. Removing default installed apps such as Xbox, Microsoft Edge, etc.
# 2. Changing the mouse speed to maximum (full speed).
# 3. Hiding all desktop icons.
# 4. Enabling dark mode for Windows 11.
# 5. Installing essential software: VLC, Notepad++, and Google Chrome.
# 
# The program requires administrative privileges to modify system settings
# and install software. It also requires an active internet connection to
# download the installers for VLC, Notepad++, and Google Chrome.
# 
# Usage:
# - Save the script as `windows_setup.py`.
# - Run the script in an elevated (administrator) command prompt.
# 
# Note:
# - Changes made by this script (e.g., removing default apps, changing mouse
#   speed, etc.) will take effect immediately, but a system restart may be
#   necessary for all changes to fully apply.
# =======================================================================

import os
import subprocess
import sys
import time

# Function to run PowerShell commands
def run_powershell(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Success: {command}")
        else:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Exception: {e}")

# Function to remove default installed apps
def remove_default_apps():
    print("Removing default apps...")
    apps_to_remove = [
        "XboxApp", "Microsoft.3DViewer", "Microsoft.MicrosoftEdge", 
        "Microsoft.Movies & TV", "Microsoft.OneNote", "Microsoft.BingWeather", 
        "Microsoft.GetHelp", "Microsoft.SkypeApp", "Microsoft.MicrosoftStickyNotes"
    ]
    
    for app in apps_to_remove:
        run_powershell(f"Get-AppxPackage -Name {app} | Remove-AppxPackage")

# Function to change mouse speed to maximum
def change_mouse_speed():
    print("Changing mouse speed to full...")
    registry_key = r"HKCU\Control Panel\Cursors"
    os.system(f'reg add "{registry_key}" /v MouseSpeed /t REG_SZ /d 2 /f')
    os.system(f'reg add "{registry_key}" /v MouseThreshold1 /t REG_SZ /d 0 /f')
    os.system(f'reg add "{registry_key}" /v MouseThreshold2 /t REG_SZ /d 0 /f')

# Function to remove desktop icons
def remove_desktop_icons():
    print("Removing desktop icons...")
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v HideIcons /t REG_DWORD /d 1 /f')

# Function to enable dark mode
def enable_dark_mode():
    print("Enabling dark mode...")
    registry_key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    os.system(f'reg add "{registry_key}" /v AppsUseLightTheme /t REG_DWORD /d 0 /f')
    os.system(f'reg add "{registry_key}" /v SystemUseLightTheme /t REG_DWORD /d 0 /f')

# Function to install software (VLC, Notepad++, Google Chrome)
def install_software():
    print("Installing VLC, Notepad++, and Google Chrome...")
    
    # Install VLC
    vlc_installer = "https://get.videolan.org/vlc/last/win64/vlc-3.0.18-win64.exe"
    subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {vlc_installer} -OutFile 'C:\\Temp\\vlc_installer.exe'"])
    subprocess.run([r"C:\Temp\vlc_installer.exe", "/S"])

    # Install Notepad++
    npp_installer = "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.7/npp.8.5.7.Installer.x64.exe"
    subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {npp_installer} -OutFile 'C:\\Temp\\npp_installer.exe'"])
    subprocess.run([r"C:\Temp\npp_installer.exe", "/S"])

    # Install Google Chrome
    chrome_installer = "https://dl.google.com/chrome/install/latest/chrome_installer.exe"
    subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {chrome_installer} -OutFile 'C:\\Temp\\chrome_installer.exe'"])
    subprocess.run([r"C:\Temp\chrome_installer.exe", "/silent", "/install"])

    # Wait for installation to finish
    time.sleep(5)
    print("Software installation completed.")

# Main function
def main():
    # Check if running with admin privileges
    if not os.environ.get('USERPROFILE'):
        print("Please run the script with administrator privileges.")
        sys.exit(1)

    # Perform tasks
    remove_default_apps()
    change_mouse_speed()
    remove_desktop_icons()
    enable_dark_mode()
    install_software()

    print("All tasks completed successfully.")

if __name__ == "__main__":
    main()

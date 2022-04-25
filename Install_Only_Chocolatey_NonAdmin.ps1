Set-ExecutionPolicy Bypass -Scope Process -Force;
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
# Set directory for installation - Chocolatey does not lock
# down the directory if not the default
$InstallDir='C:\ProgramData\chocoportable'
$env:ChocolateyInstall="$InstallDir"

# If your PowerShell Execution policy is restrictive, you may
# not be able to get around that. Try setting your session to
# Bypass.
Set-ExecutionPolicy Bypass -Scope Process -Force;

# All install options - offline, proxy, etc at
# https://chocolatey.org/install
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# ahora se debe reiniciar

# despues de reiniciar

# Source file location
$source = 'https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi'
# Destination to save the file
$destination = 'wsl_update.msi'
#Download the file
Invoke-WebRequest -Uri $source -OutFile $destination

# ejecutar el .msi
.\wsl_update.msi /quiet

# setear a version 2 por defecto
wsl --set-default-version 2


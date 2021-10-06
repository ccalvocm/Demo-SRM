Set-ExecutionPolicy Bypass -Scope Process -Force;
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

#instalar git
choco install git.commandline -yfd
$sh = New-Object -ComObject "Wscript.Shell"
$intButton = $sh.Popup("git instalado correctamente",0,"Instalador SRM",0+64)

#intalar miniconda
choco install miniconda3 --params="'/AddToPath:1 /InstallationType:JustMe'" -y
$intButton = $sh.Popup("miniconda instalado correctamente",0,"Instalador SRM",0+64)
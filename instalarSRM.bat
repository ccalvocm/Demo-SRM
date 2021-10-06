Powershell.exe -Command "Set-ExecutionPolicy Bypass -Scope Process -Force;"
start powershell -NoProfile -ExecutionPolicy Bypass -Command "& './ChocolateyInstallNonAdmin.ps1'"
start powershell -NoProfile -ExecutionPolicy Bypass -Command "& './gitCondaInstall.ps1'"

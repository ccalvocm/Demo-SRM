Powershell.exe -Command "Set-ExecutionPolicy Bypass -Scope Process -Force;"
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& './ChocolateyInstallNonAdmin.ps1'"
start cmd /c PowerShell -NoProfile -ExecutionPolicy Bypass -file ./gitCondaInstall.ps1

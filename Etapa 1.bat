Powershell.exe -Command "Set-ExecutionPolicy Bypass -Scope Process -Force;"
Powershell.exe -NoProfile -ExecutionPolicy unrestricted -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& './ChocolateyInstallNonAdmin.ps1'"
mshta "about:<script>alert('Git instalado existosamente, ejecutar Etapa2.bat');close()</script>"
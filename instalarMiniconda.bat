Powershell.exe -Command "Set-ExecutionPolicy Bypass -Scope Process -Force;"
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& './ChocolateyInstallNonAdmin.ps1'" & if exist Demo-SRM\ (CD Demo-SRM\
call git pull
CD ..
) else (
call git clone https://github.com/ccalvocm/Demo-SRM.git
)
Powershell.exe -Command "conda create -n pySRM python=3.8 -y" &
Powershell.exe -Command "call conda install mamba -n base -c conda-forge -y" &
Powershell.exe -Command "call mamba env update -n pySRM --file .\Demo-SRM\pySRM_win.yaml"
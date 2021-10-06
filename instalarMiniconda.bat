Powershell.exe -Command "Set-ExecutionPolicy Bypass -Scope Process -Force;"
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& './ChocolateyInstallNonAdmin.ps1'" & if exist Demo-SRM\ (CD Demo-SRM\
call git pull
CD ..
) else (
call git clone https://github.com/ccalvocm/Demo-SRM.git
)
call conda create -n pySRM python=3.8 -y &
call conda install mamba -n base -c conda-forge -y &
call mamba env update -n pySRM --file .\Demo-SRM\pySRM_win.yaml
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
choco install git.commandline -y
$sh = New-Object -ComObject "Wscript.Shell"
$intButton = $sh.Popup("git instalado correctamente",0,"Instalador SRM",0+64)

#intalar miniconda
choco install miniconda3 --params="'/AddToPath:1 /InstallationType:JustMe'" -y
$intButton = $sh.Popup("miniconda instalado correctamente",0,"Instalador SRM",0+64)

#recargar entorno
refreshenv

#chequear carpeta del modelo SRM
if (Test-Path -Path Demo-SRM\) {
    cd Demo-SRM\
    git pull
    cd ..
    $intButton = $sh.Popup("SRM actualizado correctamente",0,"Instalador SRM",0+64)
} else {
    git clone https://github.com/ccalvocm/Demo-SRM.git
    $intButton = $sh.Popup("SRM descargado correctamente",0,"Instalador SRM",0+64)
}

#crear entorno virtual
conda create -n pySRM python=3.8 -y

#instalar mamba
conda install mamba -n base -c conda-forge -y

#actualizar entorno virtual
mamba env update -n pySRM --file .\Demo-SRM\pySRM_win.yaml
$intButton = $sh.Popup("SRM configurado correctamente",0,"Instalador SRM",0+64)
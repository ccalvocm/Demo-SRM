Set-ExecutionPolicy Bypass -Scope Process -Force;
$sh = New-Object -ComObject "Wscript.Shell"

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
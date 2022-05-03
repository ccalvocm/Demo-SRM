# Demo SRM
## Transferencia de modelos
 
### Requisitos:
 Puerto 443 abierto  
 OS Windows  
 macOS Big Sur  
 
 
### Instalación (Windows 7):
 1. Instalar Powershell 3 desde el siguiente enlace: [Powershell 3](https://download.microsoft.com/download/E/7/6/E76850B8-DA6E-4FF5-8CCE-A24FC513FD16/Windows6.1-KB2506143-x64.msu) 
 2. Instalar .NET Framework 4+ desde el siguiente enlace: [Net Framework](https://go.microsoft.com/fwlink/?linkid=2088632)
 3. Descargar el instalador ["instalarSRM.zip"](https://github.com/ccalvocm/Demo-SRM/raw/main/instalarSRM.zip)
 4. Descomprimir el archivo ["instalarSRM.zip"](https://github.com/ccalvocm/Demo-SRM/raw/main/instalarSRM.zip)
 5. Presionar el ejecutable "Etapa 1.bat"
 6. Presionar el ejecutable "Etapa 2.bat"
 
### Instalación sin permisos de administrador (Windows 10):
1. Abrir una ventana de Windows PowerShell (CTRL+X y persionar Windows Powershell) <img src="https://raw.githubusercontent.com/ccalvocm/Hackathon_Fach/main/Imagenes/logoPS.png" height="5%" width="5%" >
2. Copiar y pegar el siguiente código en la ventana de Windows Powershell:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Set-ExecutionPolicy Bypass -Scope Process -Force; $InstallDir='C:\ProgramData\chocoportable'; $env:ChocolateyInstall="$InstallDir"; $ErrorActionPreference = 'SilentlyContinue'; Remove-Item $InstallDir -Recurse -Force; Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')); $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User"); choco install git.commandline -yfd; $sh = New-Object -ComObject "Wscript.Shell"; choco install miniconda3 --params="'/AddToPath:1 /RegisterPython=1 /InstallationType:JustMe'" -y -f; $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User"); Remove-Item .\Demo-SRM\ -Recurse -Force; git clone --depth=1 https://github.com/ccalvocm/Demo-SRM.git; conda create -n pySRM python=3.8 -y; conda env update -n pySRM --file .\Demo-SRM\pySRM_win.yaml; conda install -n pySRM -c conda-forge geemap=0.13.1 -y; $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User"); $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath("Desktop")+"\CNR-SRM.lnk"); $Shortcut.TargetPath = "$HOME\Demo-SRM\CNR-SRM.exe"; $Shortcut.WorkingDirectory = "$HOME\Demo-SRM"; $Shortcut.Save(); $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath("Desktop")+"\Actualizar_SRM.lnk"); $Shortcut.TargetPath = "$HOME\Demo-SRM\Actualizar_SRM.exe"; $Shortcut.WorkingDirectory = "$HOME\Demo-SRM"; $Shortcut.Save(); $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath("Desktop")+"\interfaz_clima_GEE.lnk"); $Shortcut.TargetPath = "$HOME\Demo-SRM\interfaz_clima_GEE.exe"; $Shortcut.WorkingDirectory = "$HOME\Demo-SRM"; $Shortcut.Save(); start .\Demo-SRM; mshta "about:<script>alert('SRM instalado exitosamente, acceso directo creado en escritorio.');close()</script>"
```
3. Abrir el explorador de windows (tecla Windows + E), ubicar su carpeta de usuario (usualmente C:\Usuarios\SuNombredeUsuario), abrir la carpeta "Demo-SRM" y hacer doble click en el archivo CNR-SRM.exe



### Instalación con permisos de administrador (Windows 10):
 1. Descargar el instalador ["instalarSRM.zip"](https://github.com/ccalvocm/Demo-SRM/raw/main/instalarSRM.zip)
 2. Descomprimir el archivo ["instalarSRM.zip"](https://github.com/ccalvocm/Demo-SRM/raw/main/instalarSRM.zip)
 3. Presionar el ejecutable "Etapa 1.bat"
 4. Presionar el ejecutable "Etapa 2.bat"

### Ejecución Interfaz del modelo SRM:
 1. Navegar a la carpeta Demo-SRM
 2. Presionar "CNR-SRM.exe"

### Ejecución de la herramienta de descarga de clima
 1. Navegar a la carpeta Demo-SRM
 2. Presionar "interfaz_clima_GEE.exe"

### Actualización:
 1. Navegar a la carpeta Demo-SRM
 2. Presionar "Actualizar_SRM.exe"

### Desinstalación:
 1. Entrar a la carpeta Demo-SRM
 2. Presionar "Desinstalar_SRM.exe"

### Video tutorial de instalación:
[![Watch the video](https://raw.githubusercontent.com/ccalvocm/Demo-SRM/main/thumbnails/Portada_video_instalacion.png)](https://cirencl-my.sharepoint.com/:v:/g/personal/ccalvo_ciren_cl/EV97xbfFNuFMgSetIpBZmRsBxy8K3y6UArHAYxkQ4N5ILA?e=lbw9hM)

### Video tutorial de ejecución:
[![Watch the video](https://raw.githubusercontent.com/ccalvocm/Demo-SRM/main/thumbnails/Portada_video_ejecucion.png)](https://cirencl-my.sharepoint.com/:v:/g/personal/ccalvo_ciren_cl/EUV5X2QLNGtKiktQkVIsj6oBTHhpwm4IjcuSXhgLfWxWlA?e=PkQgvG)

### Guía y manual de usuario:
https://github.com/ccalvocm/Demo-SRM/blob/main/Manual_SRM/SRM_Manual_Usuario.pdf

### Contacto:
 - Felipe Arróspide: farrospide@ciren.cl
 - Carlos Calvo: ccalvo@ciren.cl


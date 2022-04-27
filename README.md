# Demo SRM
## Transferencia de modelos
 
### Requisitos:
 OS Windows  
 macOS Big Sur
### Instalación (Windows 7):
 1. Instalar Powershell 3 desde el siguiente enlace: [Powershell 3](https://download.microsoft.com/download/E/7/6/E76850B8-DA6E-4FF5-8CCE-A24FC513FD16/Windows6.1-KB2506143-x64.msu) 
 2. Instalar .NET Framework 4+ desde el siguiente enlace: [Net Framework](https://go.microsoft.com/fwlink/?linkid=2088632)
 3. Descargar el instalador ["instalarSRM.zip"](https://github.com/ccalvocm/Demo-SRM/raw/main/instalarSRM.zip)
 4. Descomprimir el archivo ["instalarSRM.zip"](https://github.com/ccalvocm/Demo-SRM/raw/main/instalarSRM.zip)
 5. Presionar el ejecutable "Etapa 1.bat"
 6. Presionar el ejecutable "Etapa 2.bat"
 
### Instalación con permisos de administrador (Windows 10):
 1. Descargar el instalador ["instalarSRM.zip"](https://github.com/ccalvocm/Demo-SRM/raw/main/instalarSRM.zip)
 2. Descomprimir el archivo ["instalarSRM.zip"](https://github.com/ccalvocm/Demo-SRM/raw/main/instalarSRM.zip)
 3. Presionar el ejecutable "Etapa 1.bat"
 4. Presionar el ejecutable "Etapa 2.bat"

### Instalación sin permisos de administrador (Windows 10):
1. Abrir una ventana de Windows PowerShell <img src="https://raw.githubusercontent.com/ccalvocm/Hackathon_Fach/main/Imagenes/logoPS.png" height="6%" width="6%" >
2. Copiar y pegar el siguiente código en la ventana de Windows Powershell 

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Set-ExecutionPolicy Bypass -Scope Process -Force; $InstallDir='C:\ProgramData\chocoportable'; $env:ChocolateyInstall="$InstallDir"; Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')); mshta "about:<script>alert('Choco instalado correctamente, abrir una nueva ventana de Windows Powershell');close()</script>"
```
3. Abrir otra nueva ventana de Windows PowerShell <img src="https://raw.githubusercontent.com/ccalvocm/Hackathon_Fach/main/Imagenes/logoPS.png" height="6%" width="6%" >
4. Copiar y pegar el siguiente código en la ventana de Windows Powershell
```
choco install git.commandline -yfd; $sh = New-Object -ComObject "Wscript.Shell"; choco install miniconda3 --params="'/AddToPath:1 /InstallationType:JustMe'" -y; git clone --depth=1 https://github.com/ccalvocm/Demo-SRM.git; conda create -n pySRM python=3.8 -y; conda env update -n pySRM --file .\Demo-SRM\pySRM_win.yaml; mshta "about:<script>alert('SRM instalado existosamente');close()</script>"
```

### Ejecución:
 1. Esperar a que termine el ejecutable "Etapa 2.bat"
 2. Navegar a la carpeta Demo-SRM
 3. Presionar "interfaz_SRM.bat"

### Actualización:
 1. Para actualizar los archivos de SRM a la última versión entrar a la carpeta Demo-SRM
 2. Presionar "Actualizar SRM.bat"

### Desinstalación:
 1. Entrar a la carpeta Demo-SRM
 2. Presionar "Desinstalar_SRM.bat"

### Contacto:
 - Felipe Arróspide: farrospide@ciren.cl
 - Carlos Calvo: ccalvo@ciren.cl

### Video tutorial de instalación:
[![Watch the video](https://raw.githubusercontent.com/ccalvocm/Demo-SRM/main/thumbnails/Portada_video_instalacion.png)](https://cirencl-my.sharepoint.com/:v:/g/personal/ccalvo_ciren_cl/EV97xbfFNuFMgSetIpBZmRsBxy8K3y6UArHAYxkQ4N5ILA?e=lbw9hM)

### Video tutorial de ejecución:
[![Watch the video](https://raw.githubusercontent.com/ccalvocm/Demo-SRM/main/thumbnails/Portada_video_ejecucion.png)](https://cirencl-my.sharepoint.com/:v:/g/personal/ccalvo_ciren_cl/EUV5X2QLNGtKiktQkVIsj6oBTHhpwm4IjcuSXhgLfWxWlA?e=PkQgvG)

### Guía y manual de usuario:
https://github.com/ccalvocm/Demo-SRM/blob/main/Manual_SRM/SRM_Manual_Usuario.pdf


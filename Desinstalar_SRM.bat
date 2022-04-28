call choco uninstall miniconda3
CD ..
call rmdir /s /q %~dp0..\Demo-SRM
call del "%USERPROFILE%\Desktop\CNR-SRM.lnk"
mshta "about:<script>alert('Git instalado existosamente, ejecutar Etapa2.bat');close()</script>"

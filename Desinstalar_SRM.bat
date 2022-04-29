call choco uninstall miniconda3
CD ..
call del "%USERPROFILE%\Desktop\CNR-SRM.lnk"
call del "%USERPROFILE%\Desktop\Actualizar_SRM.lnk"
call del "%USERPROFILE%\Desktop\interfaz_clima_GEE.lnk"
call rmdir /s /q %~dp0..\Demo-SRM
mshta "about:<script>alert('SRM desinstalado');close()</script>"

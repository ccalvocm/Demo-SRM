for /l %%A in (1,1,8) do cd %~dp0LU_%%A & start cmd /k RunSlave.bat

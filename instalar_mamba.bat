powershell.exe -command "& Invoke-Webrequest -URI https://micromamba.snakepit.net/api/micromamba/win-64/latest -OutFile micromamba.tar.bz2"
C:\PROGRA~1\7-Zip\7z.exe x micromamba.tar.bz2 -aoa
C:\PROGRA~1\7-Zip\7z.exe x micromamba.tar -ttar -aoa -r .\Library\bin\micromamba.exe
$Env:MAMBA_ROOT_PREFIX=(Join-Path -Path $HOME -ChildPath micromamba)
$Env:MAMBA_EXE=(Join-Path -Path (Get-Location) -ChildPath micromamba.exe)
.\Library\bin\micromamba.exe create -f ./test/env_win.yaml -y

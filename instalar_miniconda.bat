powershell.exe -command "& Invoke-Webrequest -URI https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile Miniconda3-latest-Windows-x86_64.exe"
start /wait "" Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3
%UserProfile%\Miniconda3\_conda.exe env create -f .\pySRM_win.yaml

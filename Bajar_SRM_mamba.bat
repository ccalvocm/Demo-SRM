git clone https://github.com/ccalvocm/Demo-SRM.git &
call conda env create -n pySRM python=3.8 -y &
call conda install mamba -n base -c conda-forge -y & 
call mamba env update -n pySRM --file .\Demo-SRM\pySRM_win.yaml
git clone https://github.com/ccalvocm/Demo-SRM.git
conda env create -n pySRM python=3.8
conda install mamba -n base -c conda-forge
mamba env update -n pySRM --file .\Demo-SRM\pySRM_win.yaml
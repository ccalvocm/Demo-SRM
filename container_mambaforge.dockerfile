FROM condaforge/mambaforge:latest

COPY envA.yml envA.yml
COPY envA_requirements.txt envA_requirements.txt
# hasta aca, al correro Docker, se inicializa con (base) creado
# conda y mamba habilitados
RUN apt-get update -y

RUN echo "Etc/UTC" > /etc/timezone
# libglib preegunta por zona horaria, ver este tema
# RUN apt-get install \
    #libglib2.0-0 \
    #libgl1-mesa-glx \
    #libxcomposite-dev \
    #libxdamage1 \
    #libxrender1 \
    #libxrandr2 \
    #libxcursor1 \
    #libxi6 \
    #libxtst6 \
    #libxkbcommon-x11-0 \
    #libdbus-1-3 \
    #libasound2 \
#    vim -y \
#    gcc \
#    qt5-default

# probar el qt-5 default, sin resultados

RUN /bin/bash -c "mamba env create -f envA.yml"
RUN /bin/bash -c "conda init bash"
RUN /bin/bash -c "conda activate envA"

# hasta aca todo bien, 
# RUN git clone https://github.com/ccalvocm/Demo-SRM.git
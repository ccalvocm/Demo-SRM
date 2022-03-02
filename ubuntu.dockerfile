# seleccionar imagen base
FROM ubuntu:latest

COPY envA.yml envA.yml
COPY envA_requirements.txt envA_requirements.txt

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
# correr comandos para actualizar e instalar librerias
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    tzdata \
    git \
    wget \
    g++ \
    gcc \
    vim \
    ca-certificates \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libxcomposite-dev \
    libxdamage1 \
    libxrender1 \
    libxrandr2 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libxkbcommon-x11-0 \
    libxss1 \
    libdbus-1-3 \
    libasound2 \
    qt5-default \
    libpci-dev \
    libxcb-util-dev \
    libnss3 \
    libgconf-2-4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libnss3-dev \
    libxss-dev \
    python3-opencv \
    xterm \
    && rm -rf /var/lib/apt/lists/*
    

# display
ENV DISPLAY=host.docker.internal:0.0

# proceso de instalar miniconda
ENV PATH="/root/miniconda3/bin:$PATH"
ARG PATH="/root/miniconda3/bin:$PATH"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && echo "Running $(conda --version)" && \
    conda init bash && \
    . /root/.bashrc && \
    conda update conda && \
    conda env create --file envA.yml && \
    conda activate envA && \
    pip install -r envA_requirements.txt

RUN echo 'conda activate envA' >> /root/.bashrc

# RUN git clone https://www.github.com/ccalvocm/Demo-SRM.git

ENTRYPOINT [ "/bin/bash", "-l" ]

# CMD [ "cd Demo-SRM && python interfaz.py" ]
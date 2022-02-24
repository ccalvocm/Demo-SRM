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
    firefox \
    && rm -rf /var/lib/apt/lists/*
    

# display

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

ENTRYPOINT [ "/bin/bash", "-l" ]

CMD [ "firefox" ]
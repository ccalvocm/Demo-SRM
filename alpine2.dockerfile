# FROM alpine:latest
FROM ubuntu:latest
# RUN apk update && apk add -f pcmanfm featherpad lxtask xterm firefox
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
ENV DISPLAY=host.docker.internal:0.0
ARG USERNAME=srm
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# archivos necesarios para entorno conda
COPY ciren2_light.yml ciren2_light.yml

# variables de entorno para instalar anaconda
ENV PATH="/root/miniconda3/bin:$PATH"
ARG PATH="/root/miniconda3/bin:$PATH"

RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends \
    pcmanfm \
    featherpad \
    lxtask \
    xterm \
    wget \
    libasound2\
    git \
    sudo \
    tzdata \
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
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && chgrp -R $USER_GID /root/ \
    && chmod 770 -R /root \
    && echo "Running $(conda --version)" \
    && conda init bash \
    && . /root/.bashrc \
    && conda update conda \
    && conda env create --file ciren2_light.yml \
    && conda activate ciren2 

RUN git clone --depth=1 https://www.github.com/ccalvocm/Demo-SRM.git \
    && chgrp -R $USER_GID /Demo-SRM/ \
    && chmod 770 -R /Demo-SRM

RUN echo "source /root/miniconda3/bin/activate" >> /home/srm/.bashrc

ENTRYPOINT [ "/bin/bash", "-l" ]
USER srm
SHELL ["/bin/bash", "-c"]
RUN source /root/miniconda3/bin/activate && conda activate ciren2



# # Create the user
# RUN groupadd --gid $USER_GID $USERNAME \
#     && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
#     #
#     # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
#     && apt-get update \
#     && apt-get install -y sudo \
#     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
#     && chmod 0440 /etc/sudoers.d/$USERNAME


# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# RUN apt-get update && apt-get -y upgrade && \
#     apt-get install -y --no-install-recommends \
#     sudo \
#     tzdata \
#     git \
#     g++ \
#     gcc \
#     vim \
#     ca-certificates \
#     libglib2.0-0 \
#     libgl1-mesa-glx \
#     libxcomposite-dev \
#     libxdamage1 \
#     libxrender1 \
#     libxrandr2 \
#     libxcursor1 \
#     libxi6 \
#     libxtst6 \
#     libxkbcommon-x11-0 \
#     libxss1 \
#     libdbus-1-3 \
#     libasound2 \
#     qt5-default \
#     libpci-dev \
#     libxcb-util-dev \
#     libnss3 \
#     libgconf-2-4 \
#     libatk1.0-0 \
#     libatk-bridge2.0-0 \
#     libgdk-pixbuf2.0-0 \
#     libgtk-3-0 \
#     libgbm-dev \
#     libnss3-dev \
#     libxss-dev \
#     python3-opencv \
#     && rm -rf /var/lib/apt/lists/*

# proceso de instalar miniconda
# RUN groupadd --gid $USER_GID $USERNAME \
#     && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash\
#     #
#     # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
#     && apt-get update \
#     && apt-get install -y sudo \
#     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
#     && chmod 0440 /etc/sudoers.d/$USERNAME \
#     && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
#     && mkdir /root/.conda \
#     && bash Miniconda3-latest-Linux-x86_64.sh -b \
#     && rm -f Miniconda3-latest-Linux-x86_64.sh \
#     && chgrp -R $USER_GID /root/ \
#     && chmod 770 -R /root \
#     && echo "Running $(conda --version)" \
#     && conda init bash \
#     && . /root/.bashrc \
#     && conda update conda \
#     && conda env create --file ciren2_light.yml \
#     && conda activate ciren2 
    #pip install -r envA_requirements.txt


# RUN echo 'conda activate ciren2' >> /root/.bashrc

# COPY basic_app.py basic_app.py

# RUN git clone --depth=1 https://www.github.com/ccalvocm/Demo-SRM.git \
#     && chgrp -R $USER_GID /Demo-SRM/ \
#     && chmod 770 -R /Demo-SRM

# ENTRYPOINT [ "/bin/bash", "-l" ]
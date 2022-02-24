FROM ubuntu:latest

ENV PATH="/root/miniconda3/bin:$PATH"
ARG PATH="/root/miniconda3/bin:$PATH"
ADD ciren2_env.yml /tmp/env.yml

USER root
RUN apt-get update -y
RUN apt-get install -y wget
# RUN apt-get install libgl1-mesa-glx -y
# RUN apt-get install libxtst6 -y
# RUN apt-get install libxss1 -y
# RUN apt install libpci-dev -y
# RUN apt-get install libxcb-util-dev -y

# COPY Miniconda3-py38_4.11.0-Linux-x86_64.sh /Miniconda3-py38_4.11.0-Linux-x86_64.sh
# RUN bash Miniconda3-py38_4.11.0-Linux-x86_64.sh -b -p $HOME/miniconda

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

#RUN bash ~/miniconda.sh -b -p $HOME/miniconda

#SHELL ["/bin/bash", "-c"]
#RUN echo "source $HOME/miniconda/bin/activate" > ~/.bashrc
#RUN conda install mamba -n base -c conda-forge --yes

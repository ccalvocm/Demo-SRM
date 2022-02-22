FROM continuumio/anaconda3:latest

ADD ciren2_env.yml /tmp/ciren2.yml
# COPY . /

USER root
RUN apt-get update -y
RUN apt-get install libgl1-mesa-glx -y
RUN apt-get install libxtst6 -y
RUN apt-get install libxss1 -y
RUN apt install libpci-dev -y
RUN apt-get install libxcb-util-dev -y

RUN conda env create -f /tmp/ciren2.yml
RUN git clone https://github.com/ccalvocm/Demo-SRM.git
RUN echo "source activate $(head -1 /tmp/ciren2.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/ciren2.yml | cut -d' ' -f2)/bin:$PATH
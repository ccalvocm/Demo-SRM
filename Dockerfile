FROM mambaorg/micromamba:0.15.2
COPY --chown=micromamba:micromamba pySRM_UNIX.yaml /tmp/pySRM_UNIX.yaml
COPY . /
USER root
RUN apt-get update -y
RUN apt-get install libgl1-mesa-glx -y
USER 1000
RUN micromamba install -y -n base -f /tmp/pySRM_UNIX.yaml
WORKDIR /
CMD ['cd /']
CMD ["python", "interfaz.py"]
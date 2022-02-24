FROM mambaorg/micromamba:0.21.2
COPY envA_requirements.txt pip_requirements.txt
RUN micromamba install --yes --name base --channel conda-forge \
      python=3.9  \
      rasterio \
      ca-certificates \
      openssl \
      gdal \
      certifi \
      pip && \
    micromamba clean --all --yes
    # && \
    #pip install -r pip_requirements.txt
FROM jupyter/minimal-notebook:2c80cf3537ca

ADD . /srv
WORKDIR /srv

# Create Python2 environment
RUN conda create --yes -p $CONDA_DIR/envs/python2 python=2.7
RUN /bin/bash -c "source activate python2"
RUN conda install -y --name python2 gdal
RUN pip install awscli --upgrade --user

COPY requirements.txt /tmp/
RUN conda install --yes --file /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Add pip2.7 shortcut and install Python2 packages
RUN ln -s $CONDA_DIR/envs/python2/bin/pip $CONDA_DIR/bin/pip2.7 && \
    pip2.7 install --upgrade pip && \
    pip2.7 install \
        geojsonio \
        geopandas \
        ipykernel \
        ipyleaflet \
        ipywidgets \
        matplotlib \
        numpy \
        opencv-python==3.3.0.10 \
        pyproj \
        rasterio==1.0a12 \
        setuptools \
        scikit-image \
        shapely \ 
        boto3\
        setuptools==39.2.0

USER root
# Install dependencies for pycurl, a dependency of label-maker
RUN apt-get update && apt-get install -y libcurl4-openssl-dev

# Activate Python2 kernel globally and upon kernel launch.
USER root
RUN pip install kernda --no-cache && \
    $CONDA_DIR/envs/python2/bin/python -m ipykernel install && \
    kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json && \
    pip uninstall kernda -y

# Enable Jupyter extentions
USER $NB_USER
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter nbextension enable --py --sys-prefix ipyleaflet

# Clean up
USER root
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

# fix certs for rasterio
# https://stackoverflow.com/a/30154802/2344416
RUN mkdir -p /etc/pki/tls/certs
RUN cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt

RUN export hawaii_debris_access_key=AKIAIVIXRTCOLJ5XKPUQ
RUN export hawaii_debris_secret_key=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

RUN chmod 777 .
USER $NB_USER

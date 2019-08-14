FROM osgeo/gdal:ubuntu-small-latest

RUN apt update\
    && apt install -y\
        git\
        python3-pip

COPY . /home/recipes/

WORKDIR /home/recipes/

RUN pip3 install -e .
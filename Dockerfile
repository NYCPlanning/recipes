FROM osgeo/gdal:ubuntu-small-latest

RUN apt install -y\
        git\
        python3-pip

COPY . /home/recipes/

WORKDIR /home/recipes/

RUN pip3 install -e .

RUN pip3 install -r requirements.txt
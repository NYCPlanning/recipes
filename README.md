# recipes

## Instructions to load a dataset into recipes:

0. Add the dataset's information as a new row in the recipes.csv
eg. `dcp_mappluto`

| dstSRS | srcSRS | schema_name | version_name | geometryType |  layerCreationOptions | metaInfo | path | srcOpenOptions | newFieldNames |
| ----------- | ------------- | ------------- | ------------- | ----------- | ------------- | ------------- | ------------- | ----------- | ------------- |
| EPSG:4326 | EPSG:2263 | dcp_mappluto | 18v2_1 | POLYGON | ['OVERWRITE=YES', 'PRECISION=NO'] | bytes | https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_mappluto_18v2_1_shp.zip/MapPLUTO.shp  | [] | [] |

1. Intialize a docker container
```
docker run -itd\
    --name=recipes-$USER\
    -v `pwd`:/home/recipes\
    -w /home/recipes\
    --env-file .env\
    sptkl/cook:latest bash -c 'pip3 install -r requirements.txt; pip3 install -e .; bash'
```

2. Load a dataset into recipe postgres database
```
docker exec recipes-$USER cook run <schema_name>
```

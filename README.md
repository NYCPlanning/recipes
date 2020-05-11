# recipes

## Instructions to load a dataset into recipes:

0. Add the dataset's information as a new row in the recipes.csv
eg. `dcp_mappluto`

| dstSRS | srcSRS | schema_name | version_name | geometryType |  layerCreationOptions | metaInfo | path | srcOpenOptions | newFieldNames |
| ----------- | ------------- | ------------- | ------------- | ----------- | ------------- | ------------- | ------------- | ----------- | ------------- |
| EPSG:4326 | EPSG:2263 | dcp_mappluto | 18v2_1 | POLYGON | ['OVERWRITE=YES', 'PRECISION=NO'] | bytes | https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_mappluto_18v2_1_shp.zip/MapPLUTO.shp  | [] | [] |

+ ### The git push Method: 
    1. after you finish editing the recipes.csv, add an array of recipes you want to run to your commit message e.g.
    ```
    git commit -m "'recipe1' 'recipe2'"
    ```
    2. then do a git push to the master branch or some other branch so that github actions would be trigger to run the recipes. 
    3. Note that if you do not wish to trigger any of the github actions jobs, include `[skip ci]` in your commit message
+ ### The Docker Method:
    1. Intialize a docker container
    ```
    docker run -itd\
        --name=recipes\
        -v `pwd`:/home/recipes\
        -w /home/recipes\
        --env-file .env\
        nycplanning/cook:latest bash -c 'pip3 install -r requirements.txt; pip3 install -e .; bash'
    ```

    2. Load a dataset into recipe postgres database
    ```
    docker exec recipes cook run <schema_name>
    ```
## Update Log
### 2020/03/31 
updating GIS zoning shapefiles and get ready for zoningtaxlots
### 2020/04/17 
pulling the latest `dpr_capitalprojects`
### 2020/04/30 
updating GIS zoning shapefiles and get ready for zoningtaxlots
### 2020/05/11
Reloading GIS zoning shapefiles and get ready for zoningtaxlots



# recipes

## Instructions to load a dataset into recipes:

**For new datasets:** Add the dataset's information as a new row in the recipes.csv
eg. `dcp_mappluto`

| dstSRS | srcSRS | schema_name | version_name | geometryType |  layerCreationOptions | metaInfo | path | srcOpenOptions | newFieldNames |
| ----------- | ------------- | ------------- | ------------- | ----------- | ------------- | ------------- | ------------- | ----------- | ------------- |
| EPSG:4326 | EPSG:2263 | dcp_mappluto | 18v2_1 | POLYGON | ['OVERWRITE=YES', 'PRECISION=NO'] | bytes | https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_mappluto_18v2_1_shp.zip/MapPLUTO.shp  | [] | [] |

+ ### Github dispatch for non-ZTL recipes: 

    ```
    curl --location --request POST 'https://api.github.com/repos/NYCPlanning/recipes/dispatches?Accept=application/vnd.github.v3+json&Content-Type=application/json'       \
    --header 'Authorization: Bearer {token goes here} \
    --header 'Content-Type: text/plain' \
    --data-raw '{"event_type" : "run", "client_payload": {"recipes": "recipe1 recipe2 recipe3"}}'
    ```
+ ### ZTL bulk build:
    1. Document in the log below
    2. Commit to master using [ztl] 

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
### 2020/11/04
updating GIS zoning shapefiles and get ready for zoningtaxlots [ztl]
The e-designation file has not been updated yet -- pending schema change

### 2020/10/08
updating GIS zoning shapefiles and get ready for zoningtaxlots [ztl]

### 2020/09/14
updating GIS zoning shapefiles and get ready for zoningtaxlots (DTM was not ready for update on 09/08) [ztl]

### 2020/09/08
updating GIS zoning shapefiles and get ready for zoningtaxlots [ztl]

### 2020/08/07
updating GIS zoning shapefiles and get ready for zoningtaxlots

### 2020/07/02
reloading May address points data because of incorrect spatial transform

### 2020/06/29
updating GIS zoning shapefiles and get ready for zoningtaxlots

### 2020/06/10
updating GIS zoning shapefiles and get ready for zoningtaxlots

### 2020/03/31 
updating GIS zoning shapefiles and get ready for zoningtaxlots

### 2020/04/17 
pulling the latest `dpr_capitalprojects`

### 2020/04/30 
updating GIS zoning shapefiles and get ready for zoningtaxlots

### 2020/05/11
Reloading GIS zoning shapefiles and get ready for zoningtaxlots



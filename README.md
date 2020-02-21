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
    git commit -m "('dcp_mih' 'dcp_limitedheight')"
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
        sptkl/cook:latest bash -c 'pip3 install -r requirements.txt; pip3 install -e .; bash'
    ```

    2. Load a dataset into recipe postgres database
    ```
    docker exec recipes cook run <schema_name>
    ```

    3. **Special case:** Some datasets can be from different sources, which feed into different data products.
    For example, `doe_lcgms` can be either from DOE via email to build [CEQR school data product](https://github.com/NYCPlanning/ceqr-app-data)
    or from Open data to build [Facilities database](https://github.com/NYCPlanning/db-facilities-tmp)
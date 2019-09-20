# recipes

## Instructions to load a dataset into recipes:

0. Add the dataset's information as a new row in the recipes.csv

1. Intialize a docker container
```
docker run -itd\
    --name=recipes\
    -v `pwd`:/home/recipes\
    -w /home/recipes\
    --env-file .env\
    sptkl/cook:latest bash -c 'pip3 install -r requirements.txt; pip3 install -e .; bash'
```

2. Convert all recipes into json files
```
docker exec recipes cook convert
```

3. Load a dataset into recipe postgres database
```
docker exec recipes cook run <schema_name>
```

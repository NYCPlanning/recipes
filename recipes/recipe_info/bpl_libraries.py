import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import os
import requests

if __name__ == "__main__":
    table_name = "bpl_libraries"
    url = "https://www.bklynlibrary.org/locations/json"
    response = requests.get(url)
    content = json.loads(response.content)
    data = []
    for i in content["locations"]:
        data.append(i["data"])
    df = pd.DataFrame.from_dict(data, orient="columns")

    output_path = f"recipes/facdb/{table_name}.csv"
    df.to_csv(output_path)

    recipe_config = {
        "dstSRS": "EPSG:4326",
        "srcSRS": "EPSG:4326",
        "schema_name": table_name,
        "version_name": "",
        "geometryType": "NONE",
        "layerCreationOptions": ["OVERWRITE=YES", "PRECISION=NO"],
        "metaInfo": "https://www.bklynlibrary.org",
        "path": output_path,
        "srcOpenOptions": [
            "AUTODETECT_TYPE=NO",
            "EMPTY_STRING_AS_NULL=YES",
            "GEOM_POSSIBLE_NAMES=the_geom",
            "X_POSSIBLE_NAMES=longitude,Longitude,Lon,lon,x",
            "Y_POSSIBLE_NAMES=latitude,Latitude,Lat,lat,y",
        ],
        "newFieldNames": [],
    }

    archiver = Archiver(
        engine=os.environ["RECIPE_ENGINE"], ftp_prefix=os.environ["FTP_PREFIX"]
    )
    archiver.archive_table(recipe_config)

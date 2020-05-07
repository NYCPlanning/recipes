import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import os
import requests

if __name__ == "__main__":
    table_name = "nypl_libraries"
    url = "https://refinery.nypl.org/api/nypl/locations/v1.0/locations"
    content = requests.get(url).content
    records = json.loads(content)["locations"]
    data = []
    for i in records:
        parsed = dict(
            lon=str(i["geolocation"]["coordinates"][0]),
            lat=str(i["geolocation"]["coordinates"][1]),
            name=i["name"],
            zipcode=i["postal_code"],
            address=i["street_address"],
            locality=i["locality"],
            region=i["region"],
        )
        data.append(parsed)
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
        "metaInfo": "https://www.nypl.org/locations/list",
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

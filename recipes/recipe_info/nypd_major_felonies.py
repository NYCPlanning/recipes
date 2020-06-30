import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import tempfile
import os

if __name__ == "__main__":
    table_name = "nypd_major_felonies"
    url = "https://data.cityofnewyork.us/resource/qgea-i56i.csv?$query=SELECT%20*%20WHERE%20ky_cd%20IN%20(101,104,105,106,107,109,110)%20LIMIT%20500000"
    df = pd.read_csv(url, encoding="unicode_escape", dtype="str")

    temp_file = tempfile.NamedTemporaryFile(
        mode="w+", suffix=".csv", delete=True, newline=""
    )
    df.to_csv(temp_file, index=False)

    recipe_config = {
        "dstSRS": "EPSG:4326",
        "srcSRS": "EPSG:4326",
        "schema_name": table_name,
        "version_name": "",
        "geometryType": "NONE",
        "layerCreationOptions": ["OVERWRITE=YES", "PRECISION=NO"],
        "metaInfo": "NYC Open Data",
        "path": temp_file.name,
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
    temp_file.close()

import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import requests
import tempfile
import os

if __name__ == "__main__":
    url = "https://www.nycgovparks.org/bigapps/DPR_CapitalProjectTracker_001.json"
    data = json.loads(requests.get(url).content)
    df = pd.DataFrame(data)
    df = df[["TrackerID", "FMSID", "Title", "TotalFunding", "Locations"]]
    df["Locations"] = df["Locations"].apply(lambda x: x.get("Location"))
    df2 = df.drop(columns=["Locations"]).join(df["Locations"].explode().to_frame())
    horiz_exploded = pd.json_normalize(df2["Locations"])
    horiz_exploded.index = df2.index
    df3 = pd.concat([df2, horiz_exploded], axis=1).drop(columns=["Locations"])
    df3 = df3.rename(
            columns={
                "TrackerID": "proj_id",
                "FMSID": "fmsid",
                "Title": "desc",
                "TotalFunding": "total_funding",
                "ParkID": "park_id",
                "Latitude": "lat",
                "Longitude": "lon"
            }
        )
    df3 = df3[["proj_id", "fmsid", "desc", "total_funding", "park_id", "lat", "lon"]]

    temp_file = tempfile.NamedTemporaryFile(
        mode="w+", suffix=".csv", delete=True, newline=""
    )
    df3.to_csv(temp_file, index=False)

    recipe_config = {
        "dstSRS": "EPSG:4326",
        "srcSRS": "EPSG:4326",
        "schema_name": "dpr_capitalprojects",
        "version_name": "",
        "geometryType": "POINT",
        "layerCreationOptions": ["OVERWRITE=YES", "PRECISION=NO"],
        "metaInfo": "PARKS website",
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

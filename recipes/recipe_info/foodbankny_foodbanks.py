import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import os
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl

if __name__ == "__main__":
    table_name = "foodbankny_foodbanks"
    url = "https://www.foodbanknyc.org/wp-admin/admin-ajax.php?action=asl_load_stores&nonce=83cc04ac0d&load_all=0&layout=1&lat=40.7983474111969&lng=-73.9395518&nw%5B%5D=41.15908281222903&nw%5B%5D=-74.4614023859375&se%5B%5D=40.43761201016478&se%5B%5D=-73.4177012140625"
    hdr = {"User-Agent": "Mozilla/5.0"}
    req = Request(url, headers=hdr)
    gcontext = ssl.SSLContext()
    page = urlopen(req, context=gcontext)
    soup = BeautifulSoup(page, features="lxml")
    p = soup.find("p").get_text()
    data = json.loads(p)
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
        "metaInfo": "http://www.foodbanknyc.org/get-help/",
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

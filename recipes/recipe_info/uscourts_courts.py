import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import os
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl


def get_location(boro):
    response = requests.get(sites.get(boro)).content
    locations = json.loads(response).get("results").get("locations")
    return locations


# deduplicate, --> in reality there's no duplicated items
def removeduplicate(it):
    seen = []
    for x in it:
        t = tuple(x.items())
        if t not in seen:
            yield x
            seen.append(t)


if __name__ == "__main__":
    table_name = "uscourts_courts"
    sites = {
        "NY": "https://www.uscourts.gov/fedcf-query?query={%22by%22:%22location%22,%22page%22:0,%22description%22:%22New%20York,%20NY,%20USA%22,%22county%22:%22New%20York%22,%22state%22:%22NY%22,%22zip%22:%2210007%22,%22country%22:%22US%22,%22locationType%22:%22other%22,%22lat%22:40.7127503,%22lng%22:-74.00597649999997,%22filters%22:%22default%22}",
        "BK": "https://www.uscourts.gov/fedcf-query?query={%22by%22:%22location%22,%22page%22:0,%22description%22:%22Brooklyn,%20NY,%20USA%22,%22county%22:%22Kings%22,%22state%22:%22NY%22,%22zip%22:%2211216%22,%22country%22:%22US%22,%22locationType%22:%22other%22,%22lat%22:40.6781281,%22lng%22:-73.94416899999999,%22filters%22:%22default%22}",
    }

    data = get_location("NY") + get_location("BK")
    data = list(removeduplicate(data))
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
        "metaInfo": "https://www.uscourts.gov/federal-court-finder/search",
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

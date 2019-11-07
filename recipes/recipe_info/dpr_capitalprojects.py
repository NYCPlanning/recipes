import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import requests
import tempfile
import os

if __name__ == "__main__":
    url = 'https://www.nycgovparks.org/bigapps/DPR_CapitalProjectTracker_001.json'
    data = json.loads(requests.get(url).content)
    df = pd.DataFrame(data)

    df = df[['TrackerID', 'FMSID', 'Title', 'TotalFunding', 'Locations']]
    df['park_id'] = df['Locations'].apply(lambda x: x['Location'][0]['ParkID'])
    df['lat'] = df['Locations'].apply(lambda x: x['Location'][0]['Latitude'])
    df['lon'] = df['Locations'].apply(lambda x: x['Location'][0]['Longitude'])
    df = df.rename(columns = {'TrackerID': 'proj_id', 'FMSID':'fmsid', 'Title':'desc', 'TotalFunding': 'total_funding'})
    df = df[['proj_id','fmsid','desc','total_funding','park_id','lat', 'lon']]

    temp_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.csv', delete=True, newline='')
    df.to_csv(temp_file, index=False)

    recipe_config = {"dstSRS": "EPSG:4326",
                        "srcSRS": "EPSG:4326",
                        "schema_name": "dpr_capitalprojects",
                        "version_name": "",
                        "geometryType": "POINT",
                        "layerCreationOptions": [
                            "OVERWRITE=YES",
                            "PRECISION=NO"
                        ],
                        "metaInfo": "PARKS website",
                        "path": temp_file.name,
                        "srcOpenOptions": [
                            "AUTODETECT_TYPE=NO",
                            "EMPTY_STRING_AS_NULL=YES",
                            "GEOM_POSSIBLE_NAMES=the_geom",
                            "X_POSSIBLE_NAMES=longitude,Longitude,Lon,lon,x",
                            "Y_POSSIBLE_NAMES=latitude,Latitude,Lat,lat,y"
                        ],
                        "newFieldNames": []
                    }

    archiver = Archiver(engine=os.environ['RECIPE_ENGINE'], ftp_prefix=os.environ['FTP_PREFIX'])
    archiver.archive_table(recipe_config)
    temp_file.close()
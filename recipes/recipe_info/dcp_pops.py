import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import tempfile
import os

ftp_prefix = os.environ.get('FTP_PREFIX')

if __name__ == "__main__":
    table_name = 'dcp_pops'
    url='recipes/data/dcp/POPS_Export_Public_Official_Records(2019-11-14_10.6).csv'
    df = pd.read_csv(url)

    temp_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.csv', delete=True, newline='')
    df.to_csv(temp_file, index=False)

    output_path = f'recipes/output/facdb/{table_name}.csv'
    df.to_csv(output_path)

    recipe_config = {"dstSRS": "EPSG:4326",
                        "srcSRS": "EPSG:4326",
                        "schema_name": table_name,
                        "version_name": "",
                        "geometryType": "NONE",
                        "layerCreationOptions": [
                            "OVERWRITE=YES",
                            "PRECISION=NO"
                        ],
                        "metaInfo": "https://www.bklynlibrary.org",
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
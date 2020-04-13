import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import tempfile
import os

if __name__ == "__main__":
    table_name = 'dcas_ipis'
    
    '''
    url = ''
    df = pd.read_excel(url)
    '''

    file_path = 'recipes/data/20200319_example use data output and DCAS notes.xlsx'
    df = pd.read_excel(file_path, sheet_name='Sample data')
    df = df.rename(columns={'Owned/Leased':'owned_leased'})
    print(list(df))
    #temp_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.csv', delete=True, newline='')
    df.to_csv('temp.csv', index=False)

    recipe_config = {"dstSRS": "EPSG:4326",
                        "srcSRS": "EPSG:4326",
                        "schema_name": table_name,
                        "version_name": "",
                        "geometryType": "NONE",
                        "layerCreationOptions": [
                            "OVERWRITE=YES",
                            "PRECISION=NO"
                        ],
                        "metaInfo": "local",
                        "path": 'temp.csv',
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
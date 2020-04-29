import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import tempfile
import os

if __name__ == "__main__":
    table_names = {'sca_capacity_projects_tcu':'recipes/data/feb_2020_capacity_projects_tcu_removal.xlsx'}
    
    for k,v in table_names.items():
    
        table_name = k
        path = v
        df = pd.read_excel(path)

        #temp_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.csv', delete=False, newline='')
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
        #temp_file.close()
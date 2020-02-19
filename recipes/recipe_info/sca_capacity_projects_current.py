import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import tempfile
import os

if __name__ == "__main__":
    table_names = {'sca_capacity_projects_current':'https://dnnhh5cc1.blob.core.windows.net/portals/0/Capital_Plan/Local%20Law%20167%20Reports/List%20of%20Projects%20in%20Process.xlsx?sr=b&si=DNNFileManagerPolicy&sig=8ohDbLPbG0fBi4KD7lj53kM4XHp9tyAjYVEKp9G1IlI%3D'}
    
    for k,v in table_names.items():
    
        table_name = k
        url = v
        df = pd.read_excel(url)

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
                            "metaInfo": "SCA Local Law 167",
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
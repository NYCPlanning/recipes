import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import tempfile
import os

ftp_prefix = os.environ.get('FTP_PREFIX')

if __name__ == "__main__":
    table_name = 'dcp_sfpsd'
    url='https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/facilities_csv_201901.zip'
    df = pd.read_csv(url)
    df = df[df.pgtable.str.contains('amtrak_facilities_sfpsd|bbpc_facilities_sfpsd|hrpt_facilities_sfpsd|'\
                                    'mta_facilities_sfpsd|nysdot_facilities_sfpsd|panynj_facilities_sfpsd|'\
                                    'tgi_facilities_sfpsd|rioc_facilities_sfpsd')]

    temp_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.csv', delete=True, newline='')
    df.to_csv(temp_file, index=False)

    output_path = f'recipes/facdb/{table_name}.csv'
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
                        "metaInfo": "bytes",
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
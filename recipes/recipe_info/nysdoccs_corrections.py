import pandas as pd
from sqlalchemy import create_engine
import json
from cook import Archiver
import os
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import usaddress
import re

def get_hnum(address): 
        result = [k for (k,v) in usaddress.parse(address) \
                if re.search("Address", v)]
        return ' '.join(result)

def get_sname(address): 
        result = [k for (k,v) in usaddress.parse(address) \
                if re.search("Street", v)]
        return ' '.join(result)

def get_zipcode(address): 
        result = [k for (k,v) in usaddress.parse(address) \
                if re.search("ZipCode", v)]
        return ' '.join(result)

if __name__ == "__main__":
    table_name = 'nysdoccs_corrections'
    url= 'http://www.doccs.ny.gov/faclist.html'
    soup = BeautifulSoup(requests.get(url).content, features='html.parser')
    data = []
    for i in soup.find_all('tr')[1:]:
        info = [item.strip() for item in i.get_text().split('\n') if item not in ['', 'Map', 'Driving Directions']]
        address_long = ', '.join(info[1:-2]).split(', (')[0]
        county = (', '.join(info[1:-2]).split(', (')[1]).split('(')[1].split(' Co')[0]
        result = dict(
            facility_name = info[0],
            address = address_long,
            house_number = get_hnum(address_long),
            street_name = get_sname(address_long).replace(',',''), 
            county = county,
            zipcode = get_zipcode(address_long),
            security_level = info[-2],
            male_or_female = info[-1]
        )
        data.append(result)
    df = pd.DataFrame.from_dict(data, orient='columns')

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
                        "metaInfo": "https://www1.nyc.gov/site/doc/about/facilities-locations.page",
                        "path": output_path,
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
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
    table_name = 'nycdoc_corrections'
    url = 'https://www1.nyc.gov/site/doc/about/facilities-locations.page'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    gcontext = ssl.SSLContext()
    page = urlopen(req, context=gcontext)
    soup = BeautifulSoup(page, features='html.parser')
    data = []
    targets = ['Anna M. Kross Center (AMKC)',
            'Bellevue Hospital Prison Ward (BHPW)', 
            'Brooklyn Detention Complex (BKDC)', 
            'Elmhurst Hospital Prison Ward (EHPW)', 
            'Manhattan Detention Complex (MDC)', 
            'Queens Detention Complex (QDC)', 
            'Vernon C. Bain Center (VCBC)']
    for i in soup.find_all('p'):
        info = i.get_text('|').split('|')
        if info[0] in targets:
            result = dict(
                name = info[0], 
                address1 = info[1], 
                address2 = info[2],
                house_number = get_hnum(info[1]), 
                street_name = get_sname(info[1]),
                zipcode = get_zipcode(info[2])
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
#!/usr/bin/env python
# coding: utf-8
from cook import Archiver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

table_name = 'hra_centers'

lookup = {
    'Casa Office': '1hpyh201fVvv_p6oZKa6IOP8zzeebRy5p',
    'Snap Center':'1GBr0_gE1VBUtJZRLJosLSl1B9Xo',
    'Jobs and Service Center':'1uC3LcicVmGp_CZcyQZkGuf8rLGY', 
    'Medicaid Office':'1Ypu_qfcW7jBGDA_2uK1xP3TwUTw',
    'OCSS Center': '1MYy3WOFBNgJ4D4-rqMYoXs2R3dk'
}

results = []
for factype,mid in lookup.items():
    url=f'https://www.google.com/maps/d/kml?mid={mid}&forcekml=1'
    html_content = requests.get(url).content
    soup = BeautifulSoup(html_content, 'html.parser')
    descriptions = soup.find_all('description')
    facility = soup.find_all('name')
    data = []
    for d in range(1,len(descriptions)):
        item = descriptions[d].text.replace('\xa0',' ')
        item = item.split('<br>')
        result = {}
        fclty = facility[d+1].text
        result['factype'] = factype
        for i in range(len(item)):
            result['facname'] = fclty.replace('\xa0',' ')
            parse = item[i].split(': ')
            if len(parse) == 1:
                pass
            else:
                key = parse[0]
                value = parse[1]
                if key in ['Location Address', 'Address']: key = 'address'
                if key in ['Zip Code', 'Zipcode']: key = 'zipcode'
                if 'hour' in key.lower(): key = 'hour'
                result[key] = value
                data.append(result)
    results += data

df=pd.DataFrame(results).drop_duplicates().reset_index()
df = df.drop(columns=['index'])
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
                "metaInfo": "https://www1.nyc.gov/site/hra/locations/locations.page",
                "path": output_path,
                "srcOpenOptions": [
                    "AUTODETECT_TYPE=NO",
                    "EMPTY_STRING_AS_NULL=YES"
                ],
                "newFieldNames": []
                    }

archiver = Archiver(engine=os.environ['RECIPE_ENGINE'], 
                    ftp_prefix=os.environ['FTP_PREFIX'])
archiver.archive_table(recipe_config)
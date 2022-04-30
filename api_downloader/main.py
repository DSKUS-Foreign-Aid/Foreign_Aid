import os 
import requests
import json
import glob 

import pandas as pd 
from api_downloader import API_DOWNLOADER

# TODO 
# 1. Include other countries -> each indicators can have different numbers of countries
# 2. Way to append additional indicators to original dataset 

FILE_DIR = './test'
COUNTRIES = ''

# default values of countries is '' which means get all of countries in that indicator. 
# if you want to get specific countries, you can make this input like below 
# COUNTRIES = 'BOL;CRI;DMA;SLV;GUY;PAN;URY;SUR;ARG;BRA;CHL;MEX;PRY;BLZ;COL;ECU;GTM;HND;NIC;PER;KOR'


# Get set of indicators in a topic 
# If you have the indicator that you need and already know that code, this can be passed 
# indicator -> str
indi_url = 'http://api.worldbank.org/v2/topic/11/indicator?format=json&per_page=150'

res = requests.get(indi_url)
indicators = json.loads(res.content.decode('utf-8'))

print('start')
for i in indicators[1]:
    try:
        downloader = API_DOWNLOADER(indicator=i['id'], file_dir=FILE_DIR, countries = COUNTRIES)
        downloader.operate()
        print(i['id'])
    except:
        pass 
print('download done')

def merge_csv(dir):
    
    # merging the files
    files_joined = os.path.join(dir, "*.csv")
    
    list_files = glob.glob(files_joined)
    
    df = pd.concat(map(pd.read_csv, list_files), ignore_index=True)
    cols = df.columns.tolist()

    for i in cols:
        if 'Unnamed' in i:
            del df[i]
            cols.remove(i)

    years = sorted(cols[4:])
    head_cols = cols[:4]
    head_cols.extend(years)
    
    df.columns = head_cols

    df.to_csv(f'{dir}/merged.csv', mode='w')


merge_csv(FILE_DIR)
print('merge done')

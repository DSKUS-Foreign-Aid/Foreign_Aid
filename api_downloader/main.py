import os 
import requests
import json
import glob 

import pandas as pd 
from api_downloader import API_DOWNLOADER


file_dir = './test'
indi_url = 'http://api.worldbank.org/v2/topic/2/indicator?format=json&per_page=77'

res = requests.get(indi_url)
indicators = json.loads(res.content.decode('utf-8'))

for i in indicators[1]:
    try:
        downloader = API_DOWNLOADER(INDICATOR=i['id'], FILE_DIR=file_dir)
        downloader.operate()
        print(i['id'])
    except:
        pass 


def merge_csv(dir):
    
    # merging the files
    files_joined = os.path.join(dir, "*.csv")
    
    list_files = glob.glob(files_joined)
    
    df = pd.concat(map(pd.read_csv, list_files), ignore_index=True)
    del df['Unnamed: 0']
    
    df.to_csv(f'{dir}/merged.csv', mode='w')


merge_csv(file_dir)
import os
import zipfile
import sys
import pandas as pd

from urllib import request

# Get data from 'World Development Indicators' dataset
class API_DOWNLOADER():

    def __init__(self, INDICATOR, FILE_DIR):
        
        self.ctr = 'BOL;CRI;DMA;SLV;GUY;PAN;URY;SUR;ARG;BRA;CHL;MEX;PRY;BLZ;COL;ECU;GTM;HND;NIC;PER;KOR'
        self.idct = INDICATOR
        self.folder =  f'{FILE_DIR}/downloads'
        self.dir = f'{self.folder}/{self.idct}'
        
        self.api_download()
        self.change_csv_file_name()
        self.change_colunm_name()
        
        
    def api_download(self):        
        try:
            os.makedirs(f'{self.folder}')      
        except:
            pass
        
        url = f'http://api.worldbank.org/v2/country/{self.ctr}/indicator/{self.idct}/?source=2&downloadformat=csv&dataformat=table'
        zip_file = f'{self.dir}.zip'
        request.urlretrieve(url, zip_file)
        print('Download Done')
        
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(f'{self.dir}')
                
    
    def change_csv_file_name(self):     
        names = os.listdir(f'{self.dir}')
        os.rename(f'{self.dir}/{names[0]}', f'{self.dir}/{self.idct}.csv')
        
        print('File has been renamed')


    def change_colunm_name(self):
        df = pd.read_csv(f'{self.dir}/{self.idct}.csv', header=2)
        del df['Unnamed: 65']

        new_names = {
                    'Country Name' : 'Country_Name',
                    'Country Code' : 'Country_Code',
                    'Indicator Name' : 'Series_Name',
                    'Indicator Code' : 'Series_Code',
                }

        df.rename(columns=new_names, inplace=True)
        df.to_csv(f'{self.dir}/{self.idct}.csv', mode='w')        

        print('Columns has been renamed & updated csv file')


if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print(len(sys.argv))
        print(sys.argv)
        print('INDICATOR, FILE_DIR are required')

    else :

        indicator = (sys.argv[1])
        file_dir = (sys.argv[2])

        downloader = API_DOWNLOADER(indicator, file_dir)
        
    # e.g. python api_downloader.py AG.AGR.TRAC.NO ./test
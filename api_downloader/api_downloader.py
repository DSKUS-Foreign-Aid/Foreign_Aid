import os
import glob
import shutil
import zipfile
import sys
import pandas as pd

from urllib import request

# Get data from 'World Development Indicators' dataset
class API_DOWNLOADER():

    def __init__(self, INDICATOR, FILE_DIR, existing_csv = None):
        
        self.ctr = 'BOL;CRI;DMA;SLV;GUY;PAN;URY;SUR;ARG;BRA;CHL;MEX;PRY;BLZ;COL;ECU;GTM;HND;NIC;PER;KOR'
        self.idct = INDICATOR
        self.dir = FILE_DIR
        self.folder =  f'{FILE_DIR}/{self.idct}'
        self.csv_file = f'{FILE_DIR}/{self.idct}.csv'
        self.existing_csv_file = existing_csv
        self.flag = False
        
    def api_download(self):        
        
        try:
            os.makedirs(f'{self.folder}')      
        except:
            pass
        
        url = f'http://api.worldbank.org/v2/country/{self.ctr}/indicator/{self.idct}/?downloadformat=csv&dataformat=table'
        zip_file = f'{self.folder}/{self.idct}.zip'
        request.urlretrieve(url, zip_file)
        
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(self.folder)
    
    def delete_item(self):
        
        metadata_files = os.path.join(self.folder, "Metadata*.csv")
        [os.remove(f) for f in glob.glob(metadata_files)]
        [os.remove(f) for f in glob.glob(f'{self.folder}/*.zip')]
    
    def change_csv_file_name(self):     
               
        names = os.listdir(self.folder)

        try:
            os.rename(f'{self.folder}/{names[0]}', self.csv_file)
        except:
            self.flag = True
            pass
        
        shutil.rmtree(f'{self.folder}')
        
    def change_colunm_name(self):
        
        if self.flag:
            pass 
        else:
            df = pd.read_csv(self.csv_file, header=2)
            del df['Unnamed: 65']

            new_names = {
                        'Country Name' : 'Country_Name',
                        'Country Code' : 'Country_Code',
                        'Indicator Name' : 'Series_Name',
                        'Indicator Code' : 'Series_Code',
                    }

            df.rename(columns=new_names, inplace=True)
            df.to_csv(self.csv_file, mode='w')        

    def merge_csv(self):
        
        # merging the files
        files_joined = os.path.join( f'{self.dir}', "*.csv")
        
        list_files = glob.glob(files_joined)
        
        df = pd.concat(map(pd.read_csv, list_files), ignore_index=True)
        del df['Unnamed: 0']
        
        df.to_csv(f'{self.dir}/merged.csv', mode='w')

    def operate(self):

        if self.existing_csv_file:
            self.api_download()
            self.delete_item()
            self.change_csv_file_name()
            self.change_colunm_name()
            
        else:
            self.api_download()
            self.delete_item()
            self.change_csv_file_name()
            self.change_colunm_name()
            # self.merge_csv()


# if __name__ == "__main__":
#     if len(sys.argv) != 3: 
#         print(len(sys.argv))
#         print(sys.argv)
#         print('INDICATOR, FILE_DIR are required')

#     else:
#         indicator = (sys.argv[1])
#         file_dir = (sys.argv[2])

#         downloader = API_DOWNLOADER(indicator, file_dir)

        
    # e.g. python api_downloader.py AG.AGR.TRAC.NO ./test
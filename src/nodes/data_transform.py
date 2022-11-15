import logging
import re
import pandas as pd
import os
logger = logging.getLogger('nodes.data_transform')


def update(url,params):
    '''Recebe uma url com um arquivo csv, faz a leitura em um dataframe faz modificações no arquivo e salva o arquivo em csv'''
    try:
        date = re.findall('\d{2}-\d{2}-\d{4}', url)[0].replace('-','_')
        filename = 'corona_' + date + '.csv'
        
        df = pd.read_csv(url)
        colnames = df.rename({'Province_State':'province', 
                          'Country_Region':'country',
                          'Admin2':'Admin'}, 
                         axis=1).columns
    
        df.columns = [col.lower() for col in colnames]
        df['last_update'] = pd.to_datetime(df['last_update'])
        df.country = df.country.str.replace('*','',regex=False)
        df['anomesdia'] = df['last_update'].apply(lambda x : f'{str(x.year)}-{str(x.month).zfill(2)}-{str(x.day).zfill(2)}')
        df.to_csv(params.processed_data+'/'+ filename,index=False)
        logger.info(f'O arquivo {filename} foi tratado com sucesso')
    except:
        logger.warning(f'O arquivo {filename} não foi tratado')
	
def not_done(params):
    if params.force_execution:
        pass
    else:
        csv_files = []
        for filename in params.csv_files:
            f = 'corona_'+filename.split('/')[-1].replace('-','_') 
            if f not in os.listdir(params.processed_data+'/'):
                csv_files.append(filename)
        params.csv_files = csv_files
    if len(params.csv_files)>0:
        return True
    else:
        return False
import logging
import pandas as pd
import os
import sqlalchemy
logger = logging.getLogger('nodes.data_storage')


def update(filename,client,params):
    '''Faz a leitura de um arquivo csv e salva o dataframe no banco de dados sql'''
    table_name = filename.split('.')[0]

    df = pd.read_csv(params.processed_data+'/'+filename)
    
    df.to_sql(table_name, con=client.engine, if_exists='replace', index=False)
    logger.info(f'{table_name} criada com sucesso no banco de dados')

def done(client, params):
    if params.force_execution:
        pass
    else:
        csv_files = []
        for filename in params.lista_csv:
            f = filename.split('.')[0]
            if f not in sqlalchemy.inspect(client.engine).get_table_names():
                csv_files.append(filename)
        params.lista_csv = csv_files
    if len(params.lista_csv)>0:
        return True
    else:
        return False
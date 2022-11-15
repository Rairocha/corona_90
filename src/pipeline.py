import logging

from client import Client
from nodes import data_gathering
from nodes import data_preparation
from nodes import data_storage
from nodes import data_transform
from nodes import data_viz
from params import Params 
import os 
import re

def process(client, params):  
    """
    The ETL pipeline.
    
    It contains the main nodes of the extract-transform-load 
    pipeline from the process. 
    
    Parameters
    ----------
    
    client: Client
    parmas: Params
    
    Notes 
    -----
    The main idea is to consider each task as a conceptual **node**. 
    This function, `process` is the **pipeline** that integrates all 
    tasks together. Each node is a .py file imported from the `nodes`
    directory. 
    
    The main idea is that each node can be in one of the following state:
        - up-to-date: the task to be done given the input parameters is 
        already completed. Hence, no rework is needed.

        - out-of-date: the task to be done is not completed and should be 
        run.

    """
    params.csv_files = data_preparation.run(params)

    if not data_gathering.done(client, params):
        data_gathering.update(client, params)

    if data_transform.not_done(params):
        list(map(lambda file : data_transform.update(file,params),
                    params.csv_files[:5]))
                    
    params.lista_csv=[file for file in os.listdir(params.processed_data+'/') if re.search('corona_\d{2}_\d{2}_\d{4}.csv',file)]
    if not data_storage.done(client, params):
         [data_storage.update(file,client,params) for file in params.lista_csv]

    if not data_viz.done(client, params):
        data_viz.update(client, params)


if __name__ == '__main__': 

    params = Params()

    logging.basicConfig(filename=params.log_name,
                    level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    client = Client(params)
    process(client, params)
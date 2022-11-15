import logging
import requests
from bs4 import BeautifulSoup
logger = logging.getLogger('nodes.data_preparation')


def run(params):
    """Recebe uma url com um repositorio do github, encontra os arquivos csv e retorna uma lista com a url raw dos arquivos"""
    response = requests.get(params.url)
    html = response.content
    soup = BeautifulSoup(html,'lxml')
    csv_files = ['https://raw.githubusercontent.com' + tag['href'].replace('/blob','') for tag in soup.find_all('a') if tag['href'].endswith('.csv')]
    logger.info(f'Encontramos {len(csv_files)} arquivos para coletar')
    return csv_files
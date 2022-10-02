from logger import ErrLog
import pandas as pd
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests
import json
from tqdm import tqdm

logger = ErrLog('log')

def get_indices(state):

    state = state.lower()
    url = f'https://poweroutage.us/api/web/counties?key=23786238976131&countryid=us&statename={state}'
    response = requests.get(url, allow_redirects=True)
    content_str = response.content.decode('utf-8')
    content_json = json.loads(content_str)
    indices = []
    for obj in content_json['WebCountyRecord']:
        indices.append(str(obj['CountyId']))

    return indices

def parse_county(idx):
    info = []
    url = f'https://poweroutage.us/area/county/{idx}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    county_name = soup.select('h1#CountyName')[0].text
    info.append(county_name)
    info_items = soup.select('div.container > div.row > div.col-xs-12')
    for info_item in info_items:
        try:
            info_val = info_item.select('div.col-xs-4')[0].text
        except:
            info_val = info_item.select('item.datetime')[0].text
        info.append(info_val)
    providers_info = {}
    providers = soup.select('td.row')
    for provider in providers:
        provider_name = provider.select('div.col-xs-12 a')[0].text
        customers_info = [cus.text for cus in provider.select('div.text-right')]
        providers_info[provider_name] = customers_info
    info.append(providers_info)
    return info
    

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--state', default='florida')
    opt = parser.parse_args()
    
    state_info = []
    info_columns = ['county_name', 'customers_tracked', 'customers_out', 'outage%', 'last_updated', 'electric_providers (provider_name: customer_tracked, customer_out, last_updated)']
    try:
        county_indices = get_indices(opt.state)
        for idx in tqdm(county_indices, total=len(county_indices), desc='Parsing counties'):
            county_info = parse_county(idx)
            state_info.append(county_info)
        state_summary = pd.DataFrame(columns=info_columns, data=state_info)
        state_summary.to_csv(f'power_outage_at_{opt.state}.csv', index=False)
    except:
        logger.exception()
    
    print('Job done')



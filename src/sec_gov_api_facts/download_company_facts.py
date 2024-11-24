
import os
import requests
import pickle
import pandas as pd
# ------------------------------------------------------------
def download_company_facts(cik: str):

    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'

    headers = { 'User-Agent': os.environ.get('SEC_GOV_USER_AGENT') }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response
# ------------------------------------------------------------
# symbol = 'hood'
# cik = '0001783879'

def download_and_save_company_facts(symbol: str, cik: str):

    response = download_company_facts(cik)

    file = os.path.join('data', symbol, 'company_facts_response.pkl')

    os.makedirs(os.path.dirname(file), exist_ok=True)

    with open(file, 'wb') as f:
        pickle.dump(response.json(), f)

    df_all = pd.DataFrame()

    taxonomies = response.json()['facts']

    for taxonomy in taxonomies:
        
        facts = list(response.json()['facts'][taxonomy].keys())

        facts.sort()

        for fact in facts:

            units = response.json()['facts'][taxonomy][fact]['units'].keys()

            for unit in units:
                print(f'{taxonomy:<10}: {fact:<50}: {unit:<10}')

                tmp = pd.DataFrame(response.json()['facts'][taxonomy][fact]['units'][unit])

                tmp['taxonomy'] = taxonomy

                tmp['fact'] = fact

                tmp['unit'] = unit

                df_all = pd.concat([df_all, tmp])

    df_all = df_all[['filed', 'fy', 'fp', 'start', 'end', 'frame', 'form', 'taxonomy', 'fact', 'unit', 'accn', 'val']]
            
    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    os.makedirs(os.path.dirname(file), exist_ok=True)

    df_all.to_pickle(file)

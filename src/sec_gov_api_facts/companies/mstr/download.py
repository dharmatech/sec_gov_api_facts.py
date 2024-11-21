
import os
import pickle
import pandas as pd

from sec_gov_api_facts.download_company_facts import download_company_facts
# ------------------------------------------------------------
symbol = 'mstr'
cik = '0001050446'

response = download_company_facts(cik)

file = os.path.join('data', symbol, 'company_facts_response.pkl')

os.makedirs(os.path.dirname(file), exist_ok=True)

with open(file, 'wb') as f:
    pickle.dump(response.json(), f)
# ------------------------------------------------------------

facts = list(response.json()['facts']['us-gaap'].keys())

facts.sort()

df_all = pd.DataFrame()

for fact in facts:

    print(fact)

    if 'USD' in response.json()['facts']['us-gaap'][fact]['units']:

        tmp = pd.DataFrame(response.json()['facts']['us-gaap'][fact]['units']['USD'])

        # tmp = tmp[['end', 'val']]

        tmp['fact'] = fact

        df_all = pd.concat([df_all, tmp])

    else:
            print(f'No USD in {fact}. Has these units: {list(response.json()['facts']['us-gaap'][fact]['units'].keys())}')
        
file = os.path.join('data', symbol, 'df_all_facts.pkl')

os.makedirs(os.path.dirname(file), exist_ok=True)

df_all.to_pickle(file)

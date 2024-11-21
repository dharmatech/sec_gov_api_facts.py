
import os
import requests

def download_company_facts(cik: str):

    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'

    headers = { 'User-Agent': os.environ.get('SEC_GOV_USER_AGENT') }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response

# response = download_company_facts('0001318605')

# with open('tsla-company-facts-response.pkl', 'wb') as f:
#     pickle.dump(response.json(), f)
# # ------------------------------------------------------------
# import pickle

# with open('tsla-company-facts.pkl', 'rb') as f:
#     result = pickle.load(f)

# result['facts']['us-gaap']

# response = result
# # ------------------------------------------------------------
# facts = list(result['facts']['us-gaap'].keys())

# facts.sort()

# for elt in facts:
#     print(elt)
# # ------------------------------------------------------------
# df_all = pd.DataFrame()

# for fact in facts:

#     print(fact)

#     if 'USD' in response.json()['facts']['us-gaap'][fact]['units']:

#         tmp = pd.DataFrame(response.json()['facts']['us-gaap'][fact]['units']['USD'])

#         # tmp = tmp[['end', 'val']]

#         tmp['fact'] = fact

#         df_all = pd.concat([df_all, tmp])

#     else:
#             print(f'No USD in {fact}. Has these units: {list(response.json()['facts']['us-gaap'][fact]['units'].keys())}')
        
# # write dataframe to pickle file

# df_all.to_pickle('tsla-df-all-facts.pkl')

# # ------------------------------------------------------------

# df_all[df_all['fact'] == 'Revenues']

# # ------------------------------------------------------------
# tmp = df_all[df_all['fact'] == 'RevenueFromContractWithCustomerExcludingAssessedTax']

# tmp[tmp['frame'].isna() == False]
# # ------------------------------------------------------------

# tmp = df_all[df_all['fact'] == 'Revenues']

# tmp[tmp['frame'].isna() == False].tail(40)




# # ------------------------------------------------------------
# result['facts']['us-gaap']





# # Now `result` contains the deserialized dictionary


# url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0001318605.json'

# headers = { 'User-Agent': os.environ.get('SEC_GOV_USER_AGENT') }

# response = requests.get(url, headers=headers)

# response.raise_for_status()

# from pprint import pprint

# pprint(response.json()['facts'], depth=1)
# pprint(response.json()['facts']['us-gaap'].keys(), depth=1)
# pprint(response.json()['facts']['dei'], depth=1)


# ls = list(response.json()['facts']['us-gaap'].keys())

# ls.sort()

# for elt in ls:
#     print(elt)

# for elt in response.json()['facts']['us-gaap'].keys():
#     print(elt)


# response.json()['facts']['us-gaap']['AccountsAndNotesReceivableNet']

# pprint(response.json()['facts']['us-gaap']['AccountsAndNotesReceivableNet']['units']['USD'], depth=1)




# # df = pd.json_normalize(list(json_result['facts'].values()))

# df = pd.json_normalize(response.json()['facts']['us-gaap'])




# response.json()

# df = pd.DataFrame(response.json()['filings']['recent'])





# # ------------------------------------------------------------
# df_all = pd.DataFrame()

# tmp = pd.DataFrame(response.json()['facts']['us-gaap']['AccountsAndNotesReceivableNet']['units']['USD'])

# tmp = tmp[['end', 'val']]

# tmp['fact'] = 'AccountsAndNotesReceivableNet'

# df_all = pd.concat([df_all, tmp])

# tmp = pd.DataFrame(response.json()['facts']['us-gaap']['AccountsPayableCurrent']['units']['USD'])

# tmp = tmp[['end', 'val']]

# tmp['fact'] = 'AccountsPayableCurrent'

# df_all = pd.concat([df_all, tmp])

# df_all
# # ------------------------------------------------------------

# # ------------------------------------------------------------
# df_all = pd.DataFrame()

# for fact in facts:

#     print(fact)

#     if 'USD' in response.json()['facts']['us-gaap'][fact]['units']:

#         tmp = pd.DataFrame(response.json()['facts']['us-gaap'][fact]['units']['USD'])

#         tmp = tmp[['end', 'val']]

#         tmp['fact'] = fact

#         df_all = pd.concat([df_all, tmp])

#     else:
#             print(f'No USD in {fact}. Has these units: {list(response.json()['facts']['us-gaap'][fact]['units'].keys())}')
            



# 'shares' in response.json()['facts']['us-gaap']['AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount']['units']
# 'USD' in response.json()['facts']['us-gaap']['AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount']['units']
# # ------------------------------------------------------------

# df_all
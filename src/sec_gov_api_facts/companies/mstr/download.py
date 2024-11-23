
# python -m sec_gov_api_facts.companies.mstr.download

from sec_gov_api_facts.download_company_facts import download_and_save_company_facts

symbol = 'mstr'
cik = '0001050446'

download_and_save_company_facts(symbol, cik)


# python -m sec_gov_api_facts.companies.nvda.download

from sec_gov_api_facts.download_company_facts import download_and_save_company_facts

symbol = 'tsla'
cik = '0001318605'

download_and_save_company_facts(symbol, cik)

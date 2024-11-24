import os
import pandas as pd

from sec_gov_api_facts.calc_months      import calc_months
from sec_gov_api_facts.calc_4th_quarter import calc_4th_quarter

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

symbol = 'hood'

# ----------------------------------------------------------------------

# fact = 'CashAndCashEquivalentsAtCarryingValue'

# fact = 'CashAndSecuritiesSegregatedUnderFederalAndOtherRegulations'

def get_fact(df: pd.DataFrame, fact: str):

    df = pd.DataFrame(df)

    df = df[df['fact'] == fact]

    df.sort_values(by=['end'])
    
    df = df.dropna(subset=['frame'])

    # df = calc_months(df)
   
    # df = df.query('months == 3 or months == 12')

    # df = df[df['end'].dt.year == df['fy']]

    # df = df[((df['months'] == 3) & (df['fp'] == 'FY')) == False]

    # df = df.query("form != '10-K/A'")

    # df = calc_4th_quarter(df)

    return df
# ----------------------------------------------------------------------

items_assets = {

    'CashAndCashEquivalentsAtCarryingValue': 'Cash and cash equivalents',
    'CashAndSecuritiesSegregatedUnderFederalAndOtherRegulations': 'Cash and cash equivalents segregated under federal and other regulations',
    'ReceivablesFromBrokersDealersAndClearingOrganizations': 'Receivables from brokers, dealers, and clearing organizations',
    'ContractWithCustomerReceivableAfterAllowanceForCreditLossCurrent': 'Receivables from users, net',
    'SecuritiesBorrowed': 'Securities borrowed',
    'DepositsWithClearingOrganizationsAndOthersSecurities': 'Deposits with clearing organizations',
    'SafeguardingAssetPlatformOperatorCryptoAsset': 'Asset related to user cryptocurrencies safeguarding obligation',
    # hood:UserHeldFractionalSharesAmount
    'DebtSecuritiesHeldToMaturityExcludingAccruedInterestAfterAllowanceForCreditLossCurrent': 'Held-to-maturity investments',
    'PrepaidExpenseCurrent': 'Prepaid expenses',
    'DeferredCostsCurrent': 'Deferred customer match incentives',
    'OtherAssetsCurrent': 'Other current assets',
    'PropertyPlantAndEquipmentNet': 'Property, software, and equipment, net',
    'Goodwill': 'Goodwill',
    'IntangibleAssetsNetExcludingGoodwill': 'Intangible assets, net',
    'DebtSecuritiesHeldToMaturityExcludingAccruedInterestAfterAllowanceForCreditLossNoncurrent': 'Non-current held-to-maturity investments',
    'DeferredCosts': 'Non-current deferred customer match incentives',
    'OtherAssetsNoncurrent': 'Other non-current assets, including non-current prepaid expenses of $4 as of December 31, 2023 and $22 as of September 30, 2024',


    # 'InterestIncomeExpenseNet': 'Net interest revenues',
    # 'FloorBrokerageExchangeAndClearanceFees': 'Brokerage and transaction',
    # # hood:TechnologyAndDevelopmentExpense
    # 'OtherCostAndExpenseOperating': 'Operations',
    # 'MarketingExpense': 'Marketing',
    # 'GeneralAndAdministrativeExpense': 'General and administrative',
}

items_assets_totals = {
    'AssetsCurrent': 'Total current assets',
    'Assets': 'Total assets',
}

items_liabilities = {
    'AccountsPayableAndAccruedLiabilitiesCurrent': 'Accounts payable and accrued expenses',
    'ContractWithCustomerLiabilityCurrent': 'Payables to users',
    'SecuritiesLoaned': 'Securities loaned',
    'SafeguardingLiabilityPlatformOperatorCryptoAsset': 'User cryptocurrencies safeguarding obligation',
    # hood:FractionalSharesRepurchaseObligationAmount
    'OtherLiabilitiesCurrent': 'Other current liabilities',
    'OtherLiabilitiesNoncurrent': 'Other non-current liabilities',


}






items_capital = {
    'AdditionalPaidInCapital': 'Additional paid-in capital',
    'AccumulatedOtherComprehensiveIncomeLossNetOfTax': 'Accumulated other comprehensive income (loss)',
    'RetainedEarningsAccumulatedDeficit': 'Accumulated deficit',
}


items_liabilities_totals = {
    'LiabilitiesCurrent': 'Total current liabilities',
    'Liabilities': 'Total liabilities',
}

# 'StockholdersEquity'
# 'LiabilitiesAndStockholdersEquity'


@st.cache_data
def setup_dataframe():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)
    
    # df[df['fact'] == 'CashAndCashEquivalentsAtCarryingValue']


    df_all = pd.DataFrame()

    for item in items_assets.keys():
        df_ = get_fact(df, item)
        df_all = pd.concat([df_all, df_])
       
    return df_all

df_all = setup_dataframe()

@st.cache_data
def setup_dataframe_liabilities():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)
    
    df_all = pd.DataFrame()

    for item in items_liabilities.keys():
        df_ = get_fact(df, item)
        df_all = pd.concat([df_all, df_])    

    for item in items_capital.keys():
        df_ = get_fact(df, item)
        df_all = pd.concat([df_all, df_])
       
    return df_all

df_all_liabilities = setup_dataframe_liabilities()

file = os.path.join('data', symbol, 'df_all_facts.pkl')

df = pd.read_pickle(file)




# df_revenues               = get_fact(df, 'Revenues')
# df_operating_expenses     = get_fact(df, 'OperatingExpenses')
# df_income_loss_before_income_taxes = get_fact(df, 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest')
# df_net_income_loss = get_fact(df, 'NetIncomeLoss')

# fig = px.area(df_all, x='end', y='val_', color='fact', title=f'{symbol.upper()} : Consolidated Statement of Operations', width=1000, height=600)

# fig = px.area(df_all, x='end', y='val', color='fact', title=f'{symbol.upper()} : Consolidated Statement of Operations', width=1000, height=600)

fig = px.bar(df_all, x='end', y='val', color='fact', title=f'{symbol.upper()} : Consolidated Statement of Operations', barmode='relative', width=1200, height=600)

for item in items_assets_totals.keys():
    df_ = get_fact(df, item)
    fig.add_trace(go.Scatter(x=df_['end'], y=df_['val'], mode='lines', name=items_assets_totals[item]))

# fig.add_trace(go.Scatter(x=df_revenues['end'], y=df_revenues['val_'], mode='lines', name='Revenues'))
# fig.add_trace(go.Scatter(x=df_operating_expenses['end'], y=df_operating_expenses['val_'], mode='lines', name='Operating Expenses'))
# fig.add_trace(go.Scatter(x=df_income_loss_before_income_taxes['end'], y=df_income_loss_before_income_taxes['val_'], mode='lines', name='Income (loss) before income taxes'))
# fig.add_trace(go.Scatter(x=df_net_income_loss['end'], y=df_net_income_loss['val_'], mode='lines', name='Net income (loss)'))

st.plotly_chart(fig)
# ----------------------------------------------------------------------
fig = px.bar(df_all_liabilities, x='end', y='val', color='fact', title=f'{symbol.upper()} : Consolidated Statement of Operations', barmode='relative', width=1200, height=600)

for item in items_liabilities_totals.keys():
    df_ = get_fact(df, item)
    fig.add_trace(go.Scatter(x=df_['end'], y=df_['val'], mode='lines', name=items_liabilities_totals[item]))

st.plotly_chart(fig)
# ----------------------------------------------------------------------

def clear_cache():
    setup_dataframe.clear()
    setup_dataframe_liabilities.clear()

# st.button('Clear cache', on_click=setup_dataframe.clear)
st.button('Clear cache', on_click=clear_cache)
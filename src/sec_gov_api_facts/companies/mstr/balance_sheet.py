import os
import pandas as pd

# from calc_months      import calc_months
# from calc_4th_quarter import calc_4th_quarter

from sec_gov_api_facts.calc_months      import calc_months
from sec_gov_api_facts.calc_4th_quarter import calc_4th_quarter

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

symbol = 'mstr'

# ----------------------------------------------------------------------

def balance_sheet_item(df: pd.DataFrame, fact: str):

    df = pd.DataFrame(df)

    df = df[df['fact'] == fact]

    df['end'] = pd.to_datetime(df['end'])

    df = df[df['end'].dt.year == df['fy']]

    return df
# ----------------------------------------------------------------------

@st.cache_data
def setup_dataframe():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)

    df_all = pd.DataFrame()
    
    items = [
        'CashAndCashEquivalentsAtCarryingValue',
        'RestrictedCashAndCashEquivalentsAtCarryingValue',
        'AccountsReceivableNetCurrent',
        'PrepaidExpenseAndOtherAssetsCurrent',
        'IndefiniteLivedIntangibleAssetsExcludingGoodwill',
        'PropertyPlantAndEquipmentNet',
        'OperatingLeaseRightOfUseAsset',
        'DeferredIncomeTaxAssetsNet',
    ]

    for item in items:
        df_ = balance_sheet_item(df, item)
        df_all = pd.concat([df_all, df_])

    return df_all

@st.cache_data
def setup_dataframe_liabilities():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)

    df_all = pd.DataFrame()
    
    liabilities = [
        'EmployeeRelatedLiabilitiesCurrent',
        'InterestPayableCurrent',
        'LongTermDebtCurrent',
        'ContractWithCustomerLiabilityCurrent',
        'LongTermDebtNoncurrent',
        'ContractWithCustomerLiabilityNoncurrent',
        'OperatingLeaseLiabilityNoncurrent',
        'OtherLiabilitiesNoncurrent',
        'DeferredIncomeTaxLiabilitiesNet'
    ]

    for item in liabilities:
        df_ = balance_sheet_item(df, item)
        # df_['val'] = df_['val'] * -1
        df_all = pd.concat([df_all, df_])

    equity = [
        'AdditionalPaidInCapitalCommonStock',               # Additional paid-in capital
        'TreasuryStockValue',                               # Treasury stock
        'AccumulatedOtherComprehensiveIncomeLossNetOfTax',  # Accumulated other comprehensive loss
        'RetainedEarningsAccumulatedDeficit',               # Accumulated deficit
    ]

    for item in equity:
        df_ = balance_sheet_item(df, item)

        # if item not in ['TreasuryStockValue']:
        #     df_['val'] = df_['val'] * -1

        df_all = pd.concat([df_all, df_])    

    return df_all

df_all_assets = setup_dataframe()

df_all_liabilities = setup_dataframe_liabilities()

df_all_liabilities.loc[df_all_liabilities['fact'] == 'TreasuryStockValue', 'val'] = df_all_liabilities.loc[df_all_liabilities['fact'] == 'TreasuryStockValue', 'val'] * -1

file = os.path.join('data', symbol, 'df_all_facts.pkl')

df = pd.read_pickle(file)

df_assets = balance_sheet_item(df, 'Assets')

df_liabilities = balance_sheet_item(df, 'Liabilities')

df_liabilities_and_equity = balance_sheet_item(df, 'LiabilitiesAndStockholdersEquity')

# ----------------------------------------------------------------------
fig = go.Figure()

fig = px.bar(data_frame=df_all_assets, x='end', y='val', color='fact', title=f'{symbol.upper()} : Balance sheet assets', width=1000, height=600, barmode='relative')

fig.add_trace(go.Scatter(x=df_assets['end'], y=df_assets['val'], mode='lines', name='Assets'))

st.plotly_chart(fig)
# ----------------------------------------------------------------------
fig = go.Figure()

fig = px.bar(data_frame=df_all_liabilities, x='end', y='val', color='fact', title=f'{symbol.upper()} : Balance sheet liabilities and equity', width=1000, height=600, barmode='relative')

fig.add_trace(go.Scatter(x=df_liabilities['end'], y=df_liabilities['val'], mode='lines', name='Liabilities'))

fig.add_trace(go.Scatter(x=df_liabilities_and_equity['end'], y=df_liabilities_and_equity['val'], mode='lines', name='Liabilities and Equity'))

st.plotly_chart(fig)
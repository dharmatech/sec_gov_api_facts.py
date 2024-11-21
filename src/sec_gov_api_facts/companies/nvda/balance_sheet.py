import os
import pandas as pd

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

symbol = 'nvda'
# ----------------------------------------------------------------------
def balance_sheet_item(df: pd.DataFrame, fact: str):

    df = pd.DataFrame(df)

    df = df[df['fact'] == fact]

    df = df.dropna(subset=['frame'])

    return df
# ----------------------------------------------------------------------
@st.cache_data
def setup_dataframe():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)

    df_all = pd.DataFrame()
    
    items = [
        'CashAndCashEquivalentsAtCarryingValue',    # Cash and cash equivalents
        'MarketableSecuritiesCurrent',              # Marketable securities
        'AccountsReceivableNetCurrent',             # Accounts receivable, net
        'InventoryNet',                             # Inventories
        'PrepaidExpenseAndOtherAssetsCurrent',      # Prepaid expenses and other current assets

        'PropertyPlantAndEquipmentNet',             # Property and equipment, net
        'OperatingLeaseRightOfUseAsset',            # Operating lease assets
        'Goodwill',                                 # Goodwill
        'IntangibleAssetsNetExcludingGoodwill',     # Intangible assets, net
        'DeferredIncomeTaxAssetsNet',               # Deferred income tax assets
        'OtherAssetsNoncurrent',                    # Other assets
    ]

    for item in items:
        df_ = balance_sheet_item(df, item)
        df_all = pd.concat([df_all, df_])

    for item in items:        
        df_all.loc[df_all['fact'] == item, 'fact'] = f'A: {item}'        
    
    return df_all

@st.cache_data
def setup_dataframe_liabilities():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)

    df_all = pd.DataFrame()
    
    liabilities = [
        'AccountsPayableCurrent',            # Accounts payable
        'AccruedLiabilitiesCurrent',         # Accrued and other current liabilities
        'DebtCurrent',                       # Short-term debt
        'LongTermDebtNoncurrent',            # Long-term debt
        'OperatingLeaseLiabilityNoncurrent', # Long-term operating lease liabilities
        'OtherLiabilitiesNoncurrent',        # Other long-term liabilities
    ]
    
    for item in liabilities:
        df_ = balance_sheet_item(df, item)
        df_['val'] = df_['val'] * -1
        df_all = pd.concat([df_all, df_])

    for item in liabilities:        
        df_all.loc[df_all['fact'] == item, 'fact'] = f'L: {item}'

    equity = [
        'PreferredStockValueOutstanding',                  # Preferred stock
        'CommonStockValue',                                # Common stock
        'AdditionalPaidInCapital',                         # Additional paid-in capital
        'AccumulatedOtherComprehensiveIncomeLossNetOfTax', # Accumulated other comprehensive income
        'RetainedEarningsAccumulatedDeficit',              # Retained earnings
    ]

    for item in equity:
        df_ = balance_sheet_item(df, item)
        
        df_['val'] = df_['val'] * -1

        df_all = pd.concat([df_all, df_])    

    for item in equity:        
        df_all.loc[df_all['fact'] == item, 'fact'] = f'E: {item}'

    return df_all

df_all_assets = setup_dataframe()

df_all_liabilities = setup_dataframe_liabilities()

# ----------------------------------------------------------------------

file = os.path.join('data', symbol, 'df_all_facts.pkl')

df = pd.read_pickle(file)

df_assets = balance_sheet_item(df, 'Assets')

df_assets_current = balance_sheet_item(df, 'AssetsCurrent')

df_liabilities = balance_sheet_item(df, 'Liabilities')

df_liabilities_and_equity = balance_sheet_item(df, 'LiabilitiesAndStockholdersEquity')

df_liabilities['val'] = df_liabilities['val'] * -1

df_liabilities_and_equity['val'] = df_liabilities_and_equity['val'] * -1

# ----------------------------------------------------------------------

fig = go.Figure()

df_all = pd.concat([df_all_assets, df_all_liabilities])

fig = px.bar(data_frame=df_all, x='end', y='val', color='fact', title=f'{symbol.upper()} : Balance sheet', width=1000, height=600, barmode='relative')

fig.add_trace(go.Scatter(x=df_assets['end'], y=df_assets['val'], mode='lines', name='Assets'))

fig.add_trace(go.Scatter(x=df_assets_current['end'], y=df_assets_current['val'], mode='lines', name='AssetsCurrent'))
 
fig.add_trace(go.Scatter(x=df_liabilities['end'], y=df_liabilities['val'], mode='lines', name='Liabilities'))

fig.add_trace(go.Scatter(x=df_liabilities_and_equity['end'], y=df_liabilities_and_equity['val'], mode='lines', name='Liabilities and Equity'))

st.plotly_chart(fig)
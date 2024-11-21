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


# df_all_liabilities[df_all_liabilities['fact'] == 'TreasuryStockValue']['val'] = df_all_liabilities[df_all_liabilities['fact'] == 'TreasuryStockValue']['val'] * -1

df_all_liabilities.loc[df_all_liabilities['fact'] == 'TreasuryStockValue', 'val'] = df_all_liabilities.loc[df_all_liabilities['fact'] == 'TreasuryStockValue', 'val'] * -1

# TreasuryStockValue

# df_all.query('fact == "NetIncomeLoss"').tail(40)

# df_all_liabilities[df_all_liabilities['fact'] == 'AdditionalPaidInCapitalCommonStock']

# df_all_liabilities[df_all_liabilities['fact'] == 'TreasuryStockValue']

# df_all_liabilities[df_all_liabilities['fact'] == 'AccumulatedOtherComprehensiveIncomeLossNetOfTax']

# df_all_liabilities[df_all_liabilities['fact'] == 'RetainedEarningsAccumulatedDeficit']




# df = pd.read_pickle('tsla-df-all-facts.pkl')

file = os.path.join('data', symbol, 'df_all_facts.pkl')

df = pd.read_pickle(file)

df_assets = balance_sheet_item(df, 'Assets')

df_liabilities = balance_sheet_item(df, 'Liabilities')

df_liabilities_and_equity = balance_sheet_item(df, 'LiabilitiesAndStockholdersEquity')

# df_liabilities['val'] = df_liabilities['val'] * -1

# df_liabilities_and_equity['val'] = df_liabilities_and_equity['val'] * -1

# df_revenues               = statement_of_operations_item(df, 'Revenues')
# df_gross_profit           = statement_of_operations_item(df, 'GrossProfit')
# df_income_from_operations = statement_of_operations_item(df, 'OperatingIncomeLoss')
# df_income_before_taxes    = statement_of_operations_item(df, 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest')

# tmp = pd.concat([df_revenues, df_gross_profit, df_income_from_operations, df_income_before_taxes])

# tmp.drop(columns=['accn'])

# tmp[['end', 'fact', 'val_']]

# for elt in df['fact'].unique():
#     print(elt)


# fig = px.line(df_all, x='end', y='val', color='fact', title='Facts Over Time', width=1000, height=600)

# fig = px.area(df_all, x='end', y='val_', color='fact', title=f'{symbol.upper()} : Consolidated Statement of Operations', width=1000, height=600)

# ----------------------------------------------------------------------
# fig = px.area(df_all_assets, x='end', y='val', color='fact', title=f'{symbol.upper()} : Balance sheet', width=1000, height=600)

# fig.add_trace(go.Scatter(x=df_assets['end'], y=df_assets['val'], mode='lines', name='Assets'))

# st.plotly_chart(fig)
# # ----------------------------------------------------------------------
# fig = px.area(df_all_liabilities, x='end', y='val', color='fact', title=f'{symbol.upper()} : Balance sheet', width=1000, height=600)

# fig.add_trace(go.Scatter(x=df_liabilities['end'], y=df_liabilities['val'], mode='lines', name='Liabilities'))

# fig.add_trace(go.Scatter(x=df_liabilities_and_equity['end'], y=df_liabilities_and_equity['val'], mode='lines', name='Liabilities and Equity'))

# st.plotly_chart(fig)
# ----------------------------------------------------------------------





# import pandas as pd
# import plotly.graph_objects as go

# # Create a list to hold all traces
# traces = []

# # Create traces for each unique fact in df_all
# for fact in df_all['fact'].unique():
#     df_fact = df_all[df_all['fact'] == fact]
#     trace = go.Scatter(
#         x=df_fact['end'],
#         y=df_fact['val'],
#         mode='lines',
#         fill='tozeroy',
#         name=fact,
#         line=dict(width=0.5)
#     )
#     traces.append(trace)

# # Create traces for each unique fact in df_all_liabilities
# for fact in df_all_liabilities['fact'].unique():
#     df_fact = df_all_liabilities[df_all_liabilities['fact'] == fact]
#     trace = go.Scatter(
#         x=df_fact['end'],
#         y=df_fact['val'],
#         mode='lines',
#         fill='tonexty',
#         name=fact,
#         line=dict(width=0.5)
#     )
#     traces.append(trace)

# # Create the figure and add all traces
# fig = go.Figure()
# for trace in traces:
#     fig.add_trace(trace)

# # Update the layout
# fig.update_layout(
#     title='Combined Balance Sheet and Liabilities',
#     xaxis_title='Date',
#     yaxis_title='Value',
#     width=1000,
#     height=600
# )

# # Display the plot
# st.plotly_chart(fig)





# import pandas as pd
# import plotly.graph_objects as go

# # Create a list to hold all traces
# traces = []

# # Create traces for each unique fact in df_all
# for fact in df_all['fact'].unique():
#     df_fact = df_all[df_all['fact'] == fact]
#     trace = go.Scatter(
#         x=df_fact['end'],
#         y=df_fact['val'],
#         mode='lines',
#         # fill='tozeroy',
#         fill='tonexty',
#         name=fact,
#         line=dict(width=0.5)
#     )
#     traces.append(trace)

# # Create traces for each unique fact in df_all_liabilities
# for fact in df_all_liabilities['fact'].unique():
#     df_fact = df_all_liabilities[df_all_liabilities['fact'] == fact]
#     trace = go.Scatter(
#         x=df_fact['end'],
#         y=df_fact['val'],
#         mode='lines',
#         fill='tonexty',
#         name=fact,
#         line=dict(width=0.5)
#     )
#     traces.append(trace)

# # Create the figure and add all traces
# fig = go.Figure()
# for trace in traces:
#     fig.add_trace(trace)

# # Update the layout
# fig.update_layout(
#     title='Combined Balance Sheet and Liabilities',
#     xaxis_title='Date',
#     yaxis_title='Value',
#     width=1000,
#     height=600
# )

# # Display the plot
# st.plotly_chart(fig)


# fig = go.Figure()

# df_all = pd.concat([df_all_assets, df_all_liabilities])

# fig = px.bar(data_frame=df_all, x='end', y='val', color='fact', title=f'{symbol.upper()} : Balance sheet', width=1000, height=600, barmode='relative')

# fig.add_trace(go.Scatter(x=df_assets['end'], y=df_assets['val'], mode='lines', name='Assets'))

# fig.add_trace(go.Scatter(x=df_liabilities['end'], y=df_liabilities['val'], mode='lines', name='Liabilities'))

# fig.add_trace(go.Scatter(x=df_liabilities_and_equity['end'], y=df_liabilities_and_equity['val'], mode='lines', name='Liabilities and Equity'))

# st.plotly_chart(fig)


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
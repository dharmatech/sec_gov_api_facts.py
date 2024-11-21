import os
import pandas as pd

# from calc_months      import calc_months
# from calc_4th_quarter import calc_4th_quarter

from sec_gov_api_facts.calc_months      import calc_months
from sec_gov_api_facts.calc_4th_quarter import calc_4th_quarter

import streamlit as st
import plotly.express as px

symbol = 'mstr'

# ----------------------------------------------------------------------
def statement_of_operations_item(df: pd.DataFrame, fact: str):

    df = pd.DataFrame(df)

    df = df[df['fact'] == fact]

    df = calc_months(df)

    df = df.query('months == 3 or months == 12')

    df = df[df['end'].dt.year == df['fy']]

    df = df[((df['months'] == 3) & (df['fp'] == 'FY')) == False]

    df = df.query("form != '10-K/A'")

    df = calc_4th_quarter(df)

    return df
# ----------------------------------------------------------------------

@st.cache_data
def setup_dataframe():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)

    df_all = pd.DataFrame()

    df_ = statement_of_operations_item(df, 'NetIncomeLoss')
    df_all = pd.concat([df_all, df_])

    df_ = statement_of_operations_item(df, 'NetIncomeLossAttributableToNoncontrollingInterest')
    df_all = pd.concat([df_all, df_])

    df_ = statement_of_operations_item(df, 'IncomeTaxExpenseBenefit')
    df_all = pd.concat([df_all, df_])

    df_ = statement_of_operations_item(df, 'OtherNonoperatingIncomeExpense')
    df_['val'] = df_['val'] * -1
    df_all = pd.concat([df_all, df_])

    df_ = statement_of_operations_item(df, 'InterestExpenseNonoperating')
    df_['val'] = df_['val'] * -1
    df_all = pd.concat([df_all, df_])

    df_ = statement_of_operations_item(df, 'InvestmentIncomeInterest')
    df_['val'] = df_['val'] * -1
    df_all = pd.concat([df_all, df_])    

    df_ = statement_of_operations_item(df, 'OperatingExpenses')
    df_all = pd.concat([df_all, df_])

    df_ = statement_of_operations_item(df, 'CostOfRevenue')
    df_all = pd.concat([df_all, df_])
   
    return df_all

df_all = setup_dataframe()

# df_all.query('fact == "NetIncomeLoss"').tail(40)

# df = pd.read_pickle('tsla-df-all-facts.pkl')

file = os.path.join('data', symbol, 'df_all_facts.pkl')

df = pd.read_pickle(file)

df_revenues               = statement_of_operations_item(df, 'Revenues')
df_gross_profit           = statement_of_operations_item(df, 'GrossProfit')
df_income_from_operations = statement_of_operations_item(df, 'OperatingIncomeLoss')
df_income_before_taxes    = statement_of_operations_item(df, 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest')

# tmp = pd.concat([df_revenues, df_gross_profit, df_income_from_operations, df_income_before_taxes])

# tmp.drop(columns=['accn'])

# tmp[['end', 'fact', 'val_']]

# for elt in df['fact'].unique():
#     print(elt)


# fig = px.line(df_all, x='end', y='val', color='fact', title='Facts Over Time', width=1000, height=600)

fig = px.area(df_all, x='end', y='val_', color='fact', title=f'{symbol.upper()} : Consolidated Statement of Operations', width=1000, height=600)

import plotly.graph_objects as go

fig.add_trace(go.Scatter(x=df_revenues['end'], y=df_revenues['val_'], mode='lines', name='Revenues'))
fig.add_trace(go.Scatter(x=df_gross_profit['end'], y=df_gross_profit['val_'], mode='lines', name='Gross Profit'))
fig.add_trace(go.Scatter(x=df_income_from_operations['end'], y=df_income_from_operations['val_'], mode='lines', name='Income From Operations'))
fig.add_trace(go.Scatter(x=df_income_before_taxes['end'], y=df_income_before_taxes['val_'], mode='lines', name='Income Before Taxes'))

st.plotly_chart(fig)



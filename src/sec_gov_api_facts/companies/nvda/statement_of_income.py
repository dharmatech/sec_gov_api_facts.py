import os
import pandas as pd

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

symbol = 'nvda'
# ----------------------------------------------------------------------
def calc_4th_quarter(df: pd.DataFrame) -> pd.DataFrame:

    df = pd.DataFrame(df)
    
    df['val_1'] = df['val'].shift(1)
    df['val_2'] = df['val'].shift(2)
    df['val_3'] = df['val'].shift(3)

    df['val_123'] = df['val_1'] + df['val_2'] + df['val_3']

    df = df.drop(columns=['val_1', 'val_2', 'val_3'])

    df.loc[df['frame'].str.len() == 6, 'val_'] = df[df['frame'].str.len() == 6]['val'] - df[df['frame'].str.len() == 6]['val_123']

    df.loc[df['frame'].str.len() == 8, 'val_'] = df[df['frame'].str.len() == 8]['val']

    return df
# ----------------------------------------------------------------------

def get_fact(df: pd.DataFrame, fact: str):

    df = pd.DataFrame(df)

    df = df[df['fact'] == fact]

    df = df.dropna(subset=['frame'])
        
    df = df[~df['frame'].str.endswith('Q4')]
    
    df = df.sort_values(by=['end'])

    df = calc_4th_quarter(df)

    return df
# ----------------------------------------------------------------------
@st.cache_data
def setup_dataframe():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)

    df_all = pd.DataFrame()
    
    items = [
        
        'NetIncomeLoss',              # Net income
        'IncomeTaxExpenseBenefit',    # Income tax expense        

        'InvestmentIncomeInterest',   # Interest income
        'InterestExpenseNonoperating' # Interest expense
        'OtherNonoperatingIncomeExpense', # Other, net

        'ResearchAndDevelopmentExpense', # Research and development
        'SellingGeneralAndAdministrativeExpense', # Sales, general and administrative
        'CostOfRevenue', # Cost of revenue
    ]

    for item in items:
        df_ = get_fact(df, item)

        if item in ['InvestmentIncomeInterest', 'InterestExpenseNonoperating', 'OtherNonoperatingIncomeExpense']:
            df_['val'] = df_['val'] * -1

        df_all = pd.concat([df_all, df_])
    
    return df_all

df_all = setup_dataframe()

# ----------------------------------------------------------------------

file = os.path.join('data', symbol, 'df_all_facts.pkl')

df = pd.read_pickle(file)

df_revenues = get_fact(df, 'Revenues')

df_gross_profit = get_fact(df, 'GrossProfit')

df_operating_income_loss = get_fact(df, 'OperatingIncomeLoss')

df_income_before_income_tax = get_fact(df, 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest')
# ----------------------------------------------------------------------

fig = go.Figure()

fig = px.area(data_frame=df_all, x='end', y='val_', color='fact', title=f'{symbol.upper()} : Statement of income', width=1000, height=600)

fig.add_trace(go.Scatter(x=df_revenues['end'], y=df_revenues['val_'], mode='lines', name='Revenues'))

fig.add_trace(go.Scatter(x=df_gross_profit['end'], y=df_gross_profit['val_'], mode='lines', name='GrossProfit'))

fig.add_trace(go.Scatter(x=df_operating_income_loss['end'], y=df_operating_income_loss['val_'], mode='lines', name='OperatingIncomeLoss'))

fig.add_trace(go.Scatter(x=df_income_before_income_tax['end'], y=df_income_before_income_tax['val_'], mode='lines', name='Income before income tax'))

st.plotly_chart(fig)

# ----------------------------------------------------------------------

# tmp = df_all[['end', 'fact', 'val_']]

# pivot_df = tmp.pivot(index='end', columns='fact', values='val_')

# pivot_df.reset_index(inplace=True)

# pivot_df['ratio'] = pivot_df['CostOfRevenue'] / pivot_df['NetIncomeLoss']

# fig = px.line(pivot_df, x='end', y='ratio', title='Cost of Revenue / Net Income Loss', width=1000, height=600)

# st.plotly_chart(fig)
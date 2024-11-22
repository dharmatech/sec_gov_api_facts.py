import os
import pandas as pd

from sec_gov_api_facts.calc_months      import calc_months
from sec_gov_api_facts.calc_4th_quarter import calc_4th_quarter

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

symbol = 'hood'

# ----------------------------------------------------------------------

def statement_of_operations_item(df: pd.DataFrame, fact: str):

    df = pd.DataFrame(df)

    df = df[df['fact'] == fact]
    
    df = df.dropna(subset=['frame'])

    df = calc_months(df)
   
    # df = df.query('months == 3 or months == 12')

    # df = df[df['end'].dt.year == df['fy']]

    # df = df[((df['months'] == 3) & (df['fp'] == 'FY')) == False]

    # df = df.query("form != '10-K/A'")

    df = calc_4th_quarter(df)

    return df
# ----------------------------------------------------------------------


statement_of_operations_items = {
    'InterestIncomeExpenseNet': 'Net interest revenues',
    'FloorBrokerageExchangeAndClearanceFees': 'Brokerage and transaction',
    # hood:TechnologyAndDevelopmentExpense
    'OtherCostAndExpenseOperating': 'Operations',
    'MarketingExpense': 'Marketing',
    'GeneralAndAdministrativeExpense': 'General and administrative',
}

@st.cache_data
def setup_dataframe():

    file = os.path.join('data', symbol, 'df_all_facts.pkl')

    df = pd.read_pickle(file)

    df_all = pd.DataFrame()

    # Transaction-based revenues
    # RevenueFromContractWithCustomerExcludingAssessedTax
    # hood:TransactionBasedRevenuesMember

    for item in statement_of_operations_items.keys():
        df_ = statement_of_operations_item(df, item)
        df_all = pd.concat([df_all, df_])

    # Other revenues
    # RevenueFromContractWithCustomerExcludingAssessedTax
    # us-gaap:FinancialServiceOtherMember
       
    return df_all

df_all = setup_dataframe()

file = os.path.join('data', symbol, 'df_all_facts.pkl')

df = pd.read_pickle(file)

df_revenues               = statement_of_operations_item(df, 'Revenues')
df_operating_expenses     = statement_of_operations_item(df, 'OperatingExpenses')
df_income_loss_before_income_taxes = statement_of_operations_item(df, 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest')
df_net_income_loss = statement_of_operations_item(df, 'NetIncomeLoss')

fig = px.area(df_all, x='end', y='val_', color='fact', title=f'{symbol.upper()} : Consolidated Statement of Operations', width=1000, height=600)

fig.add_trace(go.Scatter(x=df_revenues['end'], y=df_revenues['val_'], mode='lines', name='Revenues'))
fig.add_trace(go.Scatter(x=df_operating_expenses['end'], y=df_operating_expenses['val_'], mode='lines', name='Operating Expenses'))
fig.add_trace(go.Scatter(x=df_income_loss_before_income_taxes['end'], y=df_income_loss_before_income_taxes['val_'], mode='lines', name='Income (loss) before income taxes'))
fig.add_trace(go.Scatter(x=df_net_income_loss['end'], y=df_net_income_loss['val_'], mode='lines', name='Net income (loss)'))

st.plotly_chart(fig)

st.button('Clear cache', on_click=setup_dataframe.clear)
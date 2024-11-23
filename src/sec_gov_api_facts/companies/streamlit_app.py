
import streamlit as st

items = [
    'hood/statement_of_operations.py',

    'mstr/balance_sheet.py',
    'mstr/statement_of_operations.py',

    'nvda/balance_sheet.py',
    'nvda/statement_of_income.py',

    'tsla/statement_of_operations.py',
]

pages = []

for item in items:
    pages.append(st.Page(page=item, title=item.replace('.py', ''), url_path=item.replace('/', '_')))

nav = st.navigation(pages)

nav.run()
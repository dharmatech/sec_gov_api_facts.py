
import pandas as pd

def calc_months(tmp : pd.DataFrame) -> pd.DataFrame:

    tmp['start'] = pd.to_datetime(tmp['start'])
    tmp['end']   = pd.to_datetime(tmp['end'])

    tmp['months'] = ((tmp['end'].dt.year - tmp['start'].dt.year) * 12 + (tmp['end'].dt.month - tmp['start'].dt.month))

    tmp['months'] = tmp['months'] + 1

    return tmp
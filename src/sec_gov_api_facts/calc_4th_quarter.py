
import pandas as pd

def calc_4th_quarter(df: pd.DataFrame) -> pd.DataFrame:

    df = pd.DataFrame(df)
    
    df['val_1'] = df['val'].shift(1)
    df['val_2'] = df['val'].shift(2)
    df['val_3'] = df['val'].shift(3)

    df['val_123'] = df['val_1'] + df['val_2'] + df['val_3']

    df = df.drop(columns=['val_1', 'val_2', 'val_3'])

    df.loc[df['months'] == 12, 'val_'] = df.loc[df['months'] == 12, 'val'] - df.loc[df['months'] == 12, 'val_123']

    df.loc[df['months'] == 3, 'val_'] = df.loc[df['months'] == 3, 'val']

    return df
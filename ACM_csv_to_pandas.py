import pandas as pd
import numpy as np

def make_dataframe(file_name):
    file = file_name
    widths = [8, 9, 10, 12, 10, 12, 12, 12, 12, 13, 13, 13]
    df = pd.read_fwf(file, encoding='unicode_escape', header=None, widths=widths, usecols=[1, 2, 3, 4, 5, 6, 7, 8])
    df.set_index(pd.to_datetime(df[1] + ' ' + df[2], yearfirst=True), inplace=True)
    df.drop([1, 2], axis=1, inplace=True)
    columns = ['Temperature (°C)', 'Relative Humidity (%)', 'Current CH1 (nA)', 'Current CH2 (nA)', 'Current CH3 (nA)',
               'Current CH4 (nA)']
    currents = ['Current CH1 (nA)', 'Current CH2 (nA)', 'Current CH3 (nA)', 'Current CH4 (nA)']
    environmental = ['Temperature (°C)', 'Relative Humidity (%)']
    df.columns = columns

    i = 1
    for column in df[currents]:
        df[column] = df[column].str.replace('I1:', '')
        df[column] = df[column].str.replace('I2:', '')
        df[column] = df[column].str.replace('I3:', '')
        df[column] = df[column].str.replace('I4:', '')
        df['n_or_u'] = np.where(df[column].str.contains('uA'), True, False)
        df[column] = df[column].str.extract('(\d+.\d+)')
        df[column] = df[column].astype('float')
        df[column] = np.where(df['n_or_u'] == True, df[column] * 1000, df[column])
        column_name = 'Electrical Quantity CH' + str(i) + ' (C)'
        df[column_name] = df[column].cumsum()
        df[column_name] = df[column_name] * 0.00000006
        i = i + 1

    i = 1
    for column in df[environmental]:
        df[column] = df[column].str.extract('(\d+.\d+)')
        df[column] = df[column].astype('float')

    df.drop('n_or_u', inplace=True, axis=1)

    return df

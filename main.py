import ACM_csv_to_pandas
import pandas as pd
# import libraries
import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os
import xlsxwriter
from io import BytesIO
from streamlit_pandas_profiling import st_profile_report
import pandas_profiling
import plotly.graph_objects as go

# Set up tkinter
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)

# Folder picker button
with st.sidebar.header('1. Select the ACM data'):
    st.sidebar.title('Folder Picker')
    st.sidebar.write('Please select a folder:')
    clicked = st.sidebar.button('Folder Picker')
    if clicked:
        dir_name = filedialog.askdirectory(master=root)
        st.session_state['dir_name'] = dir_name
        folders = os.listdir(dir_name)
        st.session_state['folders'] = folders
    if 'dir_name' in st.session_state:
        selected_folders = st.sidebar.multiselect('Select what folders should be added', st.session_state.folders)
        st.text_input('Selected folder:', st.session_state.dir_name)

create_df = st.button('Generate the ACM dataset based on the selected folders')
firstfile = True
if create_df:
    for subdir, dirs, files in os.walk(st.session_state.dir_name):
        if any(x in subdir for x in selected_folders):
            for file in files:
                if file.startswith('Data'):
                    file_name = os.path.join(subdir, file)
                    if firstfile:
                        df = ACM_csv_to_pandas.make_dataframe(file_name)
                        firstfile = False
                        continue
                    df_acm = ACM_csv_to_pandas.make_dataframe(file_name)
                    df = pd.concat([df, df_acm])

    df = ACM_csv_to_pandas.electrical_quantity(df)
    try:
        st.session_state['df'] = df
        st.write(df)
    except:
        st.info('No folders were selected')

# @st.cache
# def convert_df(df):
#  # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')

@st.cache
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

if 'df' in st.session_state:
    df = st.session_state.df
    generate_EDA = st.button("Generate pandas profiling report!")
    if generate_EDA:
        pr = df.profile_report()
        st_profile_report(pr)
    # csv = convert_df(df)
    excel = to_excel(df)
    st.download_button('📥 Download the ACM data in xlsx format', excel, file_name='df_test.xlsx')

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Current CH3 (nA)'], name='Current channel 3', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Current CH4 (nA)'], name='Current channel 4', mode='lines+markers'))
    fig.update_layout(
        title='Current ACM channel 3 and 4',
        title_x=0.5,
        yaxis_title='Current (nA)'
    )
    st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Temperature (°C)'], name='Temperature', mode='lines+markers'))
    fig.update_layout(
        title='Temperature',
        title_x=0.5,
        yaxis_title='Temperature (°C)'
    )
    st.plotly_chart(fig)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Relative Humidity (%)'], name='RH', mode='lines+markers'))
    fig.update_layout(
        title='Relative humidity',
        title_x=0.5,
        yaxis_title='Relative Humidity (%)'
    )
    st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Electrical Quantity CH3 (C)'], name='Electrical quantity channel 3', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Electrical Quantity CH4 (C)'], name='Electrical quantity channel 4', mode='lines+markers'))
    fig.update_layout(
        title='Current ACM channel 3 and 4',
        title_x=0.5,
        yaxis_title='Electrical Quantity (C)'
    )
    st.plotly_chart(fig)


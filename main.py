import ACM_csv_to_pandas
import pandas as pd
# import libraries
import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os
from streamlit_pandas_profiling import st_profile_report
import pandas_profiling

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

create_df = st.button('Generate the ACm dataset based on the selected folders')
firstfile = True
if create_df:
    for subdir, dirs, files in os.walk(st.session_state.dir_name):
        if any(x in subdir for x in selected_folders):
            print(subdir)
            for file in files:
                if file.startswith('Data'):
                    file_name = os.path.join(subdir, file)
                    if firstfile:
                        df = ACM_csv_to_pandas.make_dataframe(file_name)
                        firstfile = False
                        continue
                    df_acm = ACM_csv_to_pandas.make_dataframe(file_name)
                    df = pd.concat([df, df_acm])

    try:
        st.session_state['df'] = df
        st.write(df)
    except:
        st.info('No folders were selected')

if 'df' in st.session_state:
    df = st.session_state.df
    generate_EDA = st.button("Generate pandas profiling report!")
    if generate_EDA:
        pr = df.profile_report()
        st_profile_report(pr)
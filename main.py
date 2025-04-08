import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
import streamlit as st

## LOAD DATA DIRECTLY FROM SS WEBSITE
# @st.cache_data
# def load_name_data():
#     names_file = 'https://www.ssa.gov/oact/babynames/names.zip'
#     response = requests.get(names_file)
#     with zipfile.ZipFile(BytesIO(response.content)) as z:
#         dfs = []
#         files = [file for file in z.namelist() if file.endswith('.txt')]
#         for file in files:
#             with z.open(file) as f:
#                 df = pd.read_csv(f, header=None)
#                 df.columns = ['name','sex','count']
#                 df['year'] = int(file[3:7])
#                 dfs.append(df)
#         data = pd.concat(dfs, ignore_index=True)
#     data['pct'] = data['count'] / data.groupby(['year', 'sex'])['count'].transform('sum')
#     return data

## LOAD DATA FROM A SAVED FILE
#df = pd.read_csv('all_names.csv')


# LOAD DATA FROM A SMALLER NAME DATASET ON GITHUB
url = 'https://raw.githubusercontent.com/esnt/Data/refs/heads/main/Names/popular_names.csv'
df = pd.read_csv(url)

df['total_births'] = df.groupby(['year', 'sex'])['n'].transform('sum')
df['prop'] = df['n'] / df['total_births']


st.title('My Name App')

tab1, tab2, tab3 = st.tabs(['Overall', 'By Name', 'By Year'])

with tab1:
    st.write('Here is stuff about all the data')
    
with tab2:
    st.write('Name')
    
    noi = 'Emily'
    noi = st.text_input('Enter a name')
    plot_female = st.checkbox('Plot female line', key='female_name')
    plot_male = st.checkbox('Plot male line', key='male_name')
    name_df = df[df['name']==noi]

    fig = plt.figure(figsize=(15, 8))

    if plot_female:
        sns.lineplot(data=name_df[name_df['sex'] == 'F'], x='year', y='prop', label='Female')

    if plot_male:
        sns.lineplot(data=name_df[name_df['sex'] == 'M'], x='year', y='prop', label='Male')

    plt.title(f'Popularity of {noi} over time')
    plt.xlim(1880, 2025)
    plt.xlabel('Year')
    plt.ylabel('Proportion')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()

    st.pyplot(fig)

with tab3:
    st.write('Year')

    year_of_interest = 1999
    year_of_interest = st.text_input('Enter a year')
    plot_female = st.checkbox('Plot female line', key='female_year')
    plot_male = st.checkbox('Plot male line', key='male_year')

    top_names = df[df['year'] == int(year_of_interest)]

    fig = plt.figure(figsize=(15, 8))

    if plot_male:
        top_male = top_names[top_names['sex'] == 'M'].nlargest(10, 'n')
        sns.barplot(data=top_male, x='n', y='name')
    
    if plot_female:
        top_female = top_names[top_names['sex'] == 'F'].nlargest(10, 'n')
        sns.barplot(data=top_female, x='n', y='name')

    
    plt.title(f"Top 10 Female Names in {year_of_interest}")
    plt.xlabel('Count')
    plt.ylabel('Name')
    plt.tight_layout()
    
    st.pyplot(fig)





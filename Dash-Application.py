# 3 Pillares of Dash
# 1. Dash Components
#   - The "blocks" that make up the Plotly Dashboards
# 2. Plotly Graphs
#   - Very self-explanatory
# 3. The Callback
#   - Connects dash components and plotly graphs to enable interactivity

import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

### DATA SECTION ###

df = pd.read_csv("covid_dataset\\time_series_covid_19_confirmed_US.csv")

df_time_confirmed_US_NaN = df[df.isna().any(axis=1)]
# This df is providing too much info that we won't need in general, so let's delete UID, iso2, iso3, code3, and FIPS. We will keep Admin 2 because it would probably give us good data in terms of precision

df.drop('UID', axis=1, inplace=True) # inplace is used to not have to redefine df_time_confirmed_US
df.drop('iso2', axis=1, inplace=True) # axis = 1 is for columns, axis = 0 is for rows
df.drop('iso3', axis=1, inplace=True) 
df.drop('code3', axis=1, inplace=True) 

df['Province_State'] = df['Province_State'].fillna('N/A')
"""df['Admin2'].dropna(inplace = True)
df['FIPS'].dropna(inplace = True)"""
df = df.dropna()
df_time_confirmed_US_NaN = df[df.isna().any(axis=1)]

df.rename(columns={'Long_': 'Long', 
                    'State_Country': 'Combined_Key', 
                    'Province_State' : 'State', 
                    'Country_Region' : 'Country/Region', 
                    'Admin2' : 'City'}, 
                    inplace = True)

df = df.reset_index()
df = pd.concat([df.reset_index().iloc[:, 4], df.iloc[:, 8:]], axis = 1)
df = pd.melt(df, var_name = "Date", id_vars = "State", value_name = "Total Cases")

df['Date'] = df['Date'].astype('datetime64[ns]')

#dff = dff.groupby(["Date"].month)["Total Cases"].sum()

#print(dff.dtypes)

df['Month'] = df["Date"].dt.month
df['Year'] = df["Date"].dt.year
df = df.groupby(["State", "Year", "Month"], as_index=False)["Total Cases"].sum()

##########################################*****APP LAYOUT HERE*****##########################################

"""app.layout = html.Div([

    dcc.Dropdown(id = "slct_month",
                 options = [className={"label":""}]),

])"""
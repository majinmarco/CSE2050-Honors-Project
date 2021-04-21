# 3 Pillares of Dash
# 1. Dash Components
#   - The "blocks" that make up the Plotly Dashboards
# 2. Plotly Graphs
#   - Very self-explanatory
# 3. The Callback
#   - Connects dash components and plotly graphs to enable interactivity

from numpy.lib.function_base import copy
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
#df["Month/Year"] = str("{}/{}".format(df["Month"], df["Year"]))

df = df.groupby(["State", "Year", "Month"], as_index = False)["Total Cases"].sum()

l = []
for i in range(df['Month'].count()):
    l.append("{}/{}".format(df.iloc[i, 2], df.iloc[i, 1]))

df["Month/Year"] = pd.Series(l)

#df.groupby(["State", "Year", "Month"], as_index = False)["Total Cases"].sum()

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

l = df['State'].tolist()

for i in range(len(l)):
    l[i] = us_state_abbrev[l[i]]

df["State"] = pd.Series(l)

######################### OTHER TABLE FOR GRAPH COMPONENT #########################################

df_graph = pd.read_csv("covid_dataset\\time_series_covid_19_confirmed_US.csv")

df_graph.drop('UID', axis=1, inplace=True) # inplace is used to not have to redefine df_time_confirmed_US
df_graph.drop('iso2', axis=1, inplace=True) # axis = 1 is for columns, axis = 0 is for rows
df_graph.drop('iso3', axis=1, inplace=True) 
df_graph.drop('code3', axis=1, inplace=True) 

df_graph = df_graph.dropna()

df_graph.rename(columns={'Long_': 'Long', 
                    'State_Country': 'Combined_Key', 
                    'Province_State' : 'State', 
                    'Country_Region' : 'Country/Region', 
                    'Admin2' : 'City'}, 
                    inplace = True)

df_graph = df_graph.reset_index()
df_graph = pd.concat([df_graph.reset_index().iloc[:, 4], df_graph.iloc[:, 8:]], axis = 1)
df_graph = pd.melt(df_graph, var_name = "Date", id_vars = "State", value_name = "Total Cases")

df_graph['Date'] = df_graph['Date'].astype('datetime64[ns]')

l = df_graph['State'].tolist()

for i in range(len(l)):
    l[i] = us_state_abbrev[l[i]]

df_graph["State"] = pd.Series(l)

df_graph['Month'] = df_graph["Date"].dt.month
df_graph['Year'] = df_graph["Date"].dt.year

df_graph = df_graph.groupby(['Date', 'Month', 'Year'], as_index=False)['Total Cases'].sum()

l = []
for i in range(df_graph['Month'].count()):
    l.append("{}/{}".format(df_graph.iloc[i, 1], df_graph.iloc[i, 2]))

df_graph["Month/Year"] = pd.Series(l)

# Daily Cases

l = []
for i in range(df_graph['Total Cases'].count()-1, -1, -1):
    if i >= 1:
        l.append(df_graph.iloc[i, 3] - df_graph.iloc[i-1, 3])
    else:
        l.append(df_graph.iloc[i, 3])
l.reverse()

df_graph["Daily Cases"] = pd.Series(l)

##########################################*****APP LAYOUT HERE*****##########################################

app.layout = html.Div([
    html.H1("Total Cases per State in the USA", style={'text-align':'center'}),
    
    dcc.Dropdown(id = "slct_month",
                 options = [{"label":"Jan 2020", "value":"1/2020"},
                            {"label":"Feb 2020", "value":"2/2020"},
                            {"label":"Mar 2020", "value":"3/2020"},
                            {"label":"Apr 2020", "value":"4/2020"},
                            {"label":"May 2020", "value":"5/2020"},
                            {"label":"Jun 2020", "value":"6/2020"},
                            {"label":"Jul 2020", "value":"7/2020"},
                            {"label":"Aug 2020", "value":"8/2020"},
                            {"label":"Sep 2020", "value":"9/2020"},
                            {"label":"Oct 2020", "value":"10/2020"},
                            {"label":"Nov 2020", "value":"11/2020"},
                            {"label":"Dec 2020", "value":"12/2020"},
                            {"label":"Jan 2021", "value":"1/2021"}],
                multi = False,
                value = "1/2020",
                ),
    html.Div(id = "output_container", children = []),
    html.Br(),

    html.Div(children = [dcc.Graph(id = 'us_covid_map', figure = {}, style={'display': 'inline-block'}),
    dcc.Graph(id = 'monthly_graph', figure={}, style={'display': 'inline-block'})])
])

##########################################*****APP CALLBACK HERE*****##########################################

@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='us_covid_map', component_property='figure'),
    Output(component_id='monthly_graph', component_property='figure')],
    Input(component_id='slct_month', component_property='value')
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The date range chosen by the user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Month/Year"] == option_slctd]
    
    df_g = df_graph.copy()
    df_g = df_g[df_g['Month/Year'] == option_slctd]

    mp = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='State',
        scope='usa',
        color='Total Cases',
        hover_data=['State', 'Total Cases'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Total Cases':'Total Cases'},
        template='plotly_dark'
    )

    # Daily cases 
        
    fig = px.line(
        df_g,
        x = "Date",
        y = "Daily Cases",
        title="{} Daily Cases".format(df_g.iloc[0,4]),
    )
    fig.update_layout()

    return container, mp, fig

if __name__ == '__main__':
    app.run_server(debug = True)
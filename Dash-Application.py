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
import plotly.io as pio

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

df['Month'] = df["Date"].dt.month
df['Year'] = df["Date"].dt.year

df = df.groupby(["State", "Year", "Month"], as_index = False)["Total Cases"].sum()

l = []
for i in range(df['Month'].count()):
    l.append("{}/{}".format(df.loc[i, 'Month'], df.loc[i, 'Year']))

df["Month/Year"] = pd.Series(l)

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

df_graph = df_graph.groupby(['State', 'Date', 'Month', 'Year'], as_index=False)['Total Cases'].sum()

l = []
for i in range(df_graph['Month'].count()):
    l.append("{}/{}".format(df_graph.loc[i, 'Month'], df_graph.loc[i, 'Year']))

df_graph["Month/Year"] = pd.Series(l)

# Daily Cases

l = []
for i in range(df_graph['Total Cases'].count()-1, -1, -1):
    if i >= 1:
        l.append(df_graph.loc[i, 'Total Cases'] - df_graph.loc[i-1, 'Total Cases'])
    else:
        l.append(df_graph.loc[i, 'Total Cases'])
l.reverse()

df_graph["Daily Cases"] = pd.Series(l)

df_graph_all = df_graph.groupby(['Date', 'Month/Year'], as_index = False)['Daily Cases'].sum()

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

    dcc.Dropdown(id = "slct_state",
                options = [{"label" : i, "value" : j} for i, j in us_state_abbrev.items()],
                multi = False,
                value = 'CA',
                ),

    html.Div(id = "output_container", children = []),
    html.Div(id = "other_output_container", children = []),
    html.Br(),

    html.Div(children = [dcc.Graph(id = 'us_covid_map', figure = {}, style={'display': 'inline-block'}),
    dcc.Graph(id = 'monthly_graph', figure={}, style={'display': 'inline-block'}),
    dcc.Graph(id = 'full_graph', figure = {})])
])

##########################################*****APP CALLBACK HERE*****##########################################

@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='other_output_container', component_property='children'),
    Output(component_id='us_covid_map', component_property='figure'),
    Output(component_id='monthly_graph', component_property='figure'),
    Output(component_id='full_graph', component_property='figure')],
    [Input(component_id='slct_month', component_property='value'),
    Input(component_id='slct_state', component_property='value')]
)

def update_graph(month_slctd, state_slctd):
    print(month_slctd, state_slctd)
    print(type(month_slctd), type(state_slctd))

    container = "The date range chosen by the user was: {}".format(month_slctd)
    container_2 = "State chosen by the user was: {}".format(state_slctd)

    dff = df.copy()
    dff = dff[dff["Month/Year"] == month_slctd]
    
    if state_slctd != None:
        df_g = df_graph.copy()
        df_g = df_g[df_g['State'] == state_slctd]
        df_g.reset_index(drop = True, inplace = True)
        df_g.dropna(inplace = True)
        df_g.loc[0, 'Daily Cases'] = 0
    else:
        df_g = df_graph_all.copy()
        df_g.loc[0, 'Daily Cases'] = 0

    df_all = df_graph.copy()
    df_all = df_graph.groupby('Date', as_index = False)['Daily Cases'].sum()
    df_all.dropna(inplace = True)
    df_all.loc[0, 'Daily Cases'] = 0

    pio.templates.default = 'ggplot2'

    mp = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='State',
        scope='usa',
        color='Total Cases',
        hover_data=['State', 'Total Cases'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Total Cases':'Total Cases'},
    )

    # Daily cases 
        
    fig = px.line(
        df_g,
        x = "Date",
        y = "Daily Cases",
        title="Daily Cases for {}".format(state_slctd),
    )
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ]),
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
    )

    initial_range = [
    df_g[df_g['Month/Year'] == month_slctd].reset_index(drop = True).loc[0, 'Date'], df_g[df_g['Month/Year'] == month_slctd].reset_index(drop = True).loc[df_g[df_g['Month/Year'] == month_slctd].reset_index(drop = True).shape[0]-1, 'Date']]

    fig['layout']['xaxis'].update(range=initial_range)

    fig_all = px.line(
        df_all,
        x = 'Date',
        y = 'Daily Cases',
        title = 'All Daily Cases',
    )

    return container, container_2, mp, fig, fig_all

if __name__ == '__main__':
    app.run_server(debug = True)
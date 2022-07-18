import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import os

assets_path = os.getcwd() +'/assets'

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(url)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], assets_folder=assets_path)
load_figure_template('DARKLY')

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#343434",
}

sidebar = html.Div(
    [
        html.H2("Parameters", className="display-6"),
        html.Hr(),
        html.P(
            "Here you can choose:", className="lead"
        ),
        dbc.Nav(
            [
                html.Br(),
                html.P("Launch Site:"),
                dcc.Dropdown(id='site-dropdown',
                
                             options=[
                                      {'label': 'All', 'value': 'ALL'},
                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
                                     ],
                             value='ALL',
                             placeholder="Select Launch Site",
                             searchable=True,
                             style = {"background-color":"black", "color": "white"}
                            ),
                html.Br(),
                html.Br(),
                html.P("Payload range (Kg):"),
                html.Br(),
                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500:'2500',5000:'5000',
                                                7500:'7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
)

app.layout = html.Div(children=[html.Br(),
                                html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#F0F8FF',
                                               'font-size': 40}),
                                dbc.Row([dbc.Col(sidebar),
                                         dbc.Col(dcc.Graph(id = 'success-pie-chart'), width = 9, style = {'margin-left':'7px', 'margin-top':'7px', 'margin-right':'46px'}),
                                         dbc.Col(dcc.Graph(id = 'success-payload-scatter-chart'), width = 9, style = {'margin-left':'320px', 'margin-top':'14px', 'margin-right':'15px'}),

                                        ]),

                                html.Br(),
                                
                                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(df, names='class', title=f'Total Success Launches for {entered_site}')
        return fig
        
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site, payload_mass):
    if entered_site == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_mass[0]) & (spacex_df['Payload Mass (kg)'] <= payload_mass[1])]
        fig = px.scatter(filtered_data, x="Payload Mass (kg)", y="class", color="Booster Version Category", size='Flight Number')
        return fig
    else:
        data = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        filtered_data = data[(spacex_df['Payload Mass (kg)'] >= payload_mass[0]) & (spacex_df['Payload Mass (kg)'] <= payload_mass[1])]
        fig = px.scatter(filtered_data, color="Booster Version Category", x="Payload Mass (kg)", y="class", size='Flight Number')
        return fig

if __name__ == '__main__':
    app.run_server()

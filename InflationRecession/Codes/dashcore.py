#%%writefile dash_app.py

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import world_bank_data as wb

parent_dir = 'https://raw.githubusercontent.com/debanjansaha-git/Deb-NEU-DataAnalytics-Fall22/main/InflationRecession/'
df = pd.read_csv(parent_dir + 'Data/Cleaned_Data_more_countries.csv', index_col=0)
ind_file = pd.read_csv(parent_dir + 'World%20Bank%20Selected%20Indicators%20-%20Sheet1.csv')
indicators = list(ind_file['Indicator Code'].dropna())
indicator = [{'label': ind, 'value': ind} for ind in indicators]
countries = wb.get_countries()
df2 = df.merge(countries, 
               left_on='level_0', 
               right_on='id',
               how='left')
df_hvg = pd.read_csv(parent_dir + '/Data/hvg_data.csv')
df_nvg = pd.read_csv(parent_dir + '/Data/nvg_data.csv')



scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

# Colors
colors = {
    'background': '#2f9fb3',
    'graph_bg'  : '#aef6f7',
    'title'     : '#f9f8f3',
    'text'      : '#7a4d4a',
    }

app = Dash(__name__)

app.layout = html.Div([    
    # Header
        html.Div([], className = 'col-0'), 

        html.Div([
            html.H1(children='Factors Influencing Inflation on Various Economies',
                    style = {'textAlign' : 'center', 
                            'color' : colors['title'],
                            'font-family': 'Helvetica'}
            )],
            className='col-1',
            style = {'padding-top' : '1%'}
        ),

        html.Div([
            html.H2(children='Select Indicator',
            style = {'text-align' : 'left', 'color' : colors['text']}),
            # Dropdown
            html.Div([
            dcc.Dropdown(
                id='overlay_choice',
                options=indicator,
                value='NY.GDP.MKTP.KD.ZG',
                style = {'font-family': 'Helvetica',
                        'font-size': '13px', 
                        'color' : colors['text'], 
                        'white-space': 'nowrap', 
                        'text-overflow': 'ellipsis'}
                ),
            ],style =  {'width' : '30%', 
                        'margin-top' : '5px', 
                        'margin-bottom' : '5px', 
                        'text-align' : 'left', 
                        'paddingLeft': 5,
                        'color' : colors['graph_bg']}),
        ], style = {'margin-top' : '5px', 
                    'margin-bottom' : '5px', 
                    'text-align' : 'left', 
                    'paddingLeft': 25}
        ),

        html.Div([
        # World Map Graph
        dcc.Graph(
            id='graph1',
            figure={
                'layout': {
                    'plot_bgcolor': colors['graph_bg'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']}
                    }
            }),
        ], style = {'margin-top' : '15px', 
                    'margin-bottom' : '15px', 
                    'text-align' : 'left', 
                    'paddingLeft': 50,
                    'paddingRight': 50,
                    'background-color' : colors['background']}
        ),
        html.Div([
        # Slider
        dcc.Slider(
            df2['level_1'].min(),
            df2['level_1'].max(),
            id='year_slider',
            step=None,
            value=df2['level_1'].min(),
            marks={str(level_1): str(level_1) for level_1 in df2['level_1'].unique()}
            
        ),
        ], style = {'margin-top' : '15px', 
                    'margin-bottom' : '15px', 
                    'text-align' : 'left', 
                    'paddingLeft': 50,
                    'paddingRight': 50,
                    'background-color' : colors['background']}
        ),

        html.Div([
            html.Div([
                html.H2(children='Visibility Graph Network',
                style = {'text-align' : 'left', 'paddingLeft': 25, 'color' : colors['text']}),
            ], className = 'col-2'), 
            # HVG & NVG Scatter Plots
            html.Div([dcc.Graph(id='graph_hvg')], 
                        style = {'margin-top' : '5px', 
                            'margin-bottom' : '5px', 
                            'text-align' : 'left', 
                            'paddingLeft': 50,
                            'paddingRight': 50,
                            'background-color' : colors['background']}),
            html.Div([dcc.Graph(id='graph_nvg')], 
                        style = {'margin-top' : '5px', 
                            'margin-bottom' : '5px', 
                            'text-align' : 'left', 
                            'paddingLeft': 50,
                            'paddingRight': 50,
                            'background-color' : colors['background']}),
            
            
            ], style = {'margin-top' : '5px', 
                        'margin-bottom' : '5px', 
                        'text-align' : 'left', 
                        'background-color' : colors['background']}
        ),
        
    ],
    className = 'col-2',
    style = {'paddingLeft': 10,
            'paddingRight': 10,
            'background-color' : colors['background']}
    )

### Callback
@app.callback(
    [Output('graph1', 'figure'),
     Output('graph_hvg', 'figure'),
     Output('graph_nvg', 'figure'),
     ],
    [Input('overlay_choice', 'value'),
     Input('year_slider', 'value'),
     ])
def update_figure(overlay_choice, year_slider):
    filtered_df = df2.loc[df2['level_1'] == year_slider, ['level_0','level_1','iso2Code','name','region','longitude','latitude',overlay_choice]]
    df_hvg_indicator = df_hvg[df_hvg['indicator code'] == overlay_choice]
    df_nvg_indicator = df_nvg[df_nvg['indicator code'] == overlay_choice]

    # plot map
    fig1 = px.choropleth(filtered_df, 
                        locations='level_0',
                        locationmode = 'ISO-3',
                        scope='world',
                        color=overlay_choice,
                        hover_name='name',
                        color_continuous_scale=px.colors.sequential.Viridis,
                        animation_frame='level_1',
                        title='Indicator Distribution in World Map'
                        )
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    # scatter plot HVG
    fig2 = px.scatter(df_hvg_indicator, x="Average degree", y="Average path length", color='country',
                    size='Network diameter', hover_data=['Network diameter'],
                    title='Horizontal Visibility Graph by Countries')

    # scatter plot NVG
    fig3 = px.scatter(df_nvg_indicator, x="Average degree", y="Average path length", color='country',
                 size='Network diameter', hover_data=['Network diameter'],
                 title='Natural Visibility Graph by Countries')

    # return the 3 graph objects
    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)

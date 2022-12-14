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


scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

# fig = px.choropleth(filtered_df, locations="level_0",
#                    color=overlay_choice,
#                    hover_name='name',
#                    color_continuous_scale=px.colors.sequential.Viridis,
#                    animation_frame='level_1',
#                    )

# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app = Dash(__name__)

app.layout = html.Div([
    # Header
    html.H1(children='Factors Influencing Inflation - Recession'),
    html.H2(children='Select Indicator'),
    # Dropdown
    dcc.Dropdown(
        id='overlay_choice',
        options=indicator,
        value='NY.GDP.MKTP.KD.ZG'
    ),

   
    dcc.Graph(id='graph', figure=fig),

# fig = px.scatter_geo(df, locations="level_0",
#                      color="continent", # which column to use to set the color of markers
#                      hover_name="country", # column added to hover information
#                      size="pop", # size of markers
#                      projection="natural earth")
# # fig = dict( data=data, layout=layout )    

    


    # Slider
    # dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['level_1'].min(),
        df['level_1'].max(),
        id='year_slider',
        step=None,
        value=df['level_1'].min(),
        marks={str(level_1): str(level_1) for level_1 in df['level_1'].unique()}
        
    )
])


### Callback
@app.callback(
    Output('graph', 'figure'),
    [Input('overlay_choice', 'value'),
     Input('year_slider', 'value'),
     ])
def update_figure(overlay_choice, year_slider):
    filtered_df = df.loc[df['level_1'] == year_slider, overlay_choice]

    fig = px.choropleth(filtered_df, locations="level_0",
                        color=overlay_choice,
                        hover_name='name',
                        color_continuous_scale=px.colors.sequential.Viridis,
                        animation_frame='level_1',
                        )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)



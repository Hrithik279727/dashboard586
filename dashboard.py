app = dash.Dash(__name__)
server = app.server
# specify the layout of the dashboard
app.layout = html.Div([
    html.H1(children=["MTCF Single Vehicle Pedestrian Crash Dashboard"],
            style={#'backgroundColor':'#619ac3', 
                   'text-align':'center'}),
    
    html.H2(children=dcc.Markdown("Data Source: [Michigan Traffic Crash Facts](https://www.michigantrafficcrashfacts.org/)"),
            style={'text-align':'left'}),
    
    html.H2(children=["IMSE 586 Course Project - Team 15"],
            style={'text-align':'left'}),
    
    html.H2(children=["Section 1. Pedestrian-Single Vehicle Crash Variable Distribution"],            
            style={'backgroundColor':'#EAE8C1', 
                   'text-align':'center',
                   'margin': '1px'}),    
    
    html.H3(children=["Step 1 - Select Date Range"], style={'margin': '10px'}),
    
    dcc.DatePickerRange(id='date_range', 
                        start_date='2019-01-01',
                        end_date='2022-12-31',
                        style={'display': 'flex', 'justify-content': 'left', 
                               'align-items': 'center',}
                       ),   
    
    html.H3(children=["Step 2 - Select Variable to Visualize"],style={'margin': '5px'}),
    
    dcc.Dropdown(["Rural/Urban Area (2016+)","Road Conditions","Lighting Conditions",\
                  "Worst Injury in Crash","Day of Week","Weather Conditions (2016+)",\
                  "Person Gender","Person Degree of Injury","Crash Month",\
                  "Crash: Hit-and-Run","Crash: Drinking","Crash: Intersection",\
                  "Crash: Young Driver","Day of Week","Crash: Driver Distracted (2016+)"],
                  "Road Conditions", id='variable_d'),
    
    html.H3(children=["Step 3 - Visualize by Injury Severity"],style={'margin': '5px'}),
    
    dcc.RadioItems(id='injury', 
                   options={"No":"Do Not Group by Injury Level",
                            "KABCO":"Group by KABCO Injury Level",
                            "Binary":"Group by Binary Injury Level",
                          },
                   value='No', #default option value
                   inline=False, #display options on same line
                 ),    
    
    
    dcc.Graph(id='count_graph'),
    
    html.H2(children=["Section 2. Pedestrian-Single vehicle Crashes Geographical Distribution"],            
            style={'backgroundColor':'#EAE8C1', 
                   'text-align':'center',
                   'margin': '1px'}),
    
    html.H3(children=["Step 1 - Select Date Range"], style={'margin': '10px'}),
    
    dcc.DatePickerRange(id='date_range_geo', 
                        start_date='2019-01-01',
                        end_date='2022-12-31',
                        style={'display': 'flex', 'justify-content': 'left', 'align-items': 'center'}
                       ), 
    
    html.H3(children=["Step 2 - Visualize by Injury Severity"],style={'margin': '10px'}),
    
    dcc.RadioItems(id='injury_geo', 
                   options={"All":"All injury levels",
                            "O":"No Injury (O)",
                            "B":"Suspected Minor Injury (B)",
                            "C":"Possible Injury (C)",
                            "A":"Suspected Serious Injury (A)",
                            "K":"Fatal Injury (K)",
                            
                          },
                   value='All', #default option value
                   inline=False, #display options on same line
                 ),      
    
    dcc.Graph(id='loaction_graph', style = {'margin': '2px'}),
    
])

# specify the callback function (control the behavior of the dashboard behind the scne)

@app.callback(
    Output(component_id='count_graph', component_property='figure'), # output, the function returns to the component 'trend-graph'
    Input(component_id='date_range', component_property='start_date'),
    Input(component_id='date_range', component_property='end_date'),
    Input(component_id='variable_d', component_property='value'),
    Input(component_id='injury', component_property='value'),
)

def update_figure(start_date, end_date, variable_d_value, injury_value):
    
    df_updated = (
        df.loc[df.index.dropna()]
          .sort_index()
          .loc[start_date:end_date]
    )
    
    df_new = df_updated.query("`Person Degree of Injury` != 'Uncoded & Errors'").copy()
    df_new['Binary_injury'] = (df_new['Person Degree of Injury']
                                        .apply(lambda x: 'Serious/Fatal Injury' 
                                               if x in ['Suspected Serious Injury (A)', 'Fatal Injury (K)'] 
                                               else 'No/Possible/Minor Injury'))
    
    if injury_value == 'No':
    
        fig = px.bar(df_updated[[variable_d_value,'Person Degree of Injury']].value_counts().reset_index(),
                     x=variable_d_value, y='count')
        
        fig.update_layout(title_font_size=16,)
        fig.update_xaxes(title=variable_d_value,type='category')
        fig.update_yaxes(title='Count')
        
        fig.update_layout(
            #plot_bgcolor='#49494b',
            paper_bgcolor='#FFFEFE',
            #font_color='#b0d5df',
            )
    
        return fig
    
    elif injury_value == 'KABCO':
    
        fig = px.bar(df_updated[[variable_d_value,'Person Degree of Injury']].value_counts().reset_index(),
                     x=variable_d_value, y='count',
                     color='Person Degree of Injury',
                     barmode="group")
        
        fig.update_layout(
            #plot_bgcolor='#49494b',
            paper_bgcolor='#FFFEFE',
            #font_color='#b0d5df',
            )
    
        return fig

    elif injury_value == 'Binary':
        
        
        
        fig = px.bar(df_new[[variable_d_value,'Binary_injury']].value_counts().reset_index(),
                     x=variable_d_value, y='count',
                     color='Binary_injury',
                     barmode="group")
        
        fig.update_layout(
            #plot_bgcolor='#49494b',
            paper_bgcolor='#FFFEFE',
            #font_color='#b0d5df',
            )    

        return fig       
 

@app.callback(
    Output(component_id='loaction_graph', component_property='figure'), # output, the function returns to the component 'trend-graph'
    Input(component_id='date_range_geo', component_property='start_date'),
    Input(component_id='date_range_geo', component_property='end_date'),
    Input(component_id='injury_geo', component_property='value'),
)


def update_figure(start_date, end_date, injury_geo_value):
    
    df_geo = (
        df.loc[df.index.dropna()]
          .sort_index()
          .loc[start_date:end_date]
    )
    
    if injury_geo_value == 'B':
        df_geo_ = df_geo.query("`Person Degree of Injury`=='Suspected Minor Injury (B)'")
    elif injury_geo_value == 'C':
        df_geo_ = df_geo.query("`Person Degree of Injury`=='Possible Injury (C)'")
    elif injury_geo_value == 'A':
        df_geo_ = df_geo.query("`Person Degree of Injury`=='Suspected Serious Injury (A)'")
    elif injury_geo_value == 'O':
        df_geo_ = df_geo.query("`Person Degree of Injury`=='No Injury (O)'")
    elif injury_geo_value == 'K':
        df_geo_ = df_geo.query("`Person Degree of Injury`=='Fatal Injury (K)'")
    else:
        df_geo_ = df_geo
      
    
    fig = px.scatter_mapbox(df_geo_, lat='Crash Latitude', lon='Crash Longitude', 
                        hover_name='Crash Instance',
                        color='Person Degree of Injury',
                        hover_data=['Person Age','Person Gender','Person Degree of Injury'])


    fig.update_layout(
        mapbox_style="open-street-map",  # you can choose other map styles like "carto-positron", "stamen-terrain", etc.
        mapbox_zoom=9,
        mapbox_center={"lat": 42.32, "lon": -83.17},
        width=1400,  
        height=800,
    )
    
    fig.update_layout(
        #plot_bgcolor='#49494b',
        paper_bgcolor='#FFFEFE',
        #font_color='#b0d5df',
    )

    return fig
    
    

if __name__ == '__main__':
    
    app.run() #app.run() show below /external link
    #app.run_server(host='0.0.0.0', debug=True)
    #app.run()
    
#    app.run_server(
#        port=8050,
#        host='0.0.0.0',
#        debug=True
#    )

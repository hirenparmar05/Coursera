# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
launch_sites = spacex_df['Launch Site'].unique()

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',  # Default value to show all sites
        placeholder="Select a Launch Site here",
        searchable=True  # Enable search functionality
    ),
    html.Br(),
    
    # TASK 2: Pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # TASK 3: Add a slider to select payload range
    html.P("Payload range (Kg):"),
    
    # Add a placeholder for the slider (to be completed later)
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, 
        max=max_payload, 
        step=1000,
        marks={int(min_payload): str(int(min_payload)), int(max_payload): str(int(max_payload))},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        # Pie chart for all sites, showing the total success (class=1) and failure (class=0)
        fig = px.pie(
            filtered_df, 
            names='class', 
            title='Total Success Launches for All Sites',
            hole=0.3
        )
        return fig
    else:
        # Filter the dataframe for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Pie chart for the specific site, showing success (class=1) vs failure (class=0)
        fig = px.pie(
            site_df, 
            names='class', 
            title=f'Total Success Launches for {entered_site}',
            hole=0.3
        )
        return fig

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class',
            color="Booster Version Category",
            title="Correlation between Payload and Success for All Sites"
        )
        return fig
    else:
        # Filter the data based on the selected launch site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_df, x='Payload Mass (kg)', y='class',
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for {entered_site}"
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

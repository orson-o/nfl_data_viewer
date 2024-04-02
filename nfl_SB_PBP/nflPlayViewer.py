import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objs as go
from PIL import Image
import base64
from io import BytesIO
import os
from dash_bootstrap_templates import load_figure_template
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

# Get the current working directory
cwd = os.getcwd()
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css2?family=Roboto&display=swap"
]

# Build the path to the image
image_path = os.path.join(cwd, 'my_dash_app', 'images', '4840654.jpg')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# Function to convert PIL image to Data URI
def pil_to_data_uri(img):
    data = BytesIO()
    img.save(data, "JPEG")
    data_uri = "data:image/jpeg;base64," + base64.b64encode(data.getvalue()).decode('utf-8')
    return data_uri

# Load the PIL image and convert it to a Data URI
pil_image_path = 'images/4840654.jpg'
pil_image = Image.open(pil_image_path)
image_data_uri = pil_to_data_uri(pil_image)
# Load the data
df = pd.read_csv('data/sb_2000_2023.csv', low_memory=False)
team_directions = df.groupby('game_id')['posteam'].unique().apply(lambda teams: {team: idx for idx, team in enumerate(teams)}).to_dict()
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the sidebar layout for selecting game_id
# Define the sidebar layout for selecting game_id
sidebar = dbc.Col(
    html.Div([
        html.H2("Select Game", className="display-4"),
        html.Hr(),
        dcc.Dropdown(
            id='game-id-dropdown',
            options=[{'label': game_id, 'value': game_id} for game_id in df['game_id'].unique()],
            value=df['game_id'].iloc[0],
            className='dropdown',
            clearable=False
        ),
    ], className='sidebar'),
    width=2
)

# Define the main content layout with the football field image and description window
# Adjusted content layout to include the line graph
content = dbc.Col(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='field-graph',
                        figure={},
                        config={'staticPlot': True}  # Disable zoom and pan
                    ),
                    width=9,
                ),
                dbc.Col(
                    [
                        html.Div(
                            id='desc-window',
                            className='desc-window',
                            style={'overflow-y': 'scroll', 'height': '150px'},
                        ),
                        dcc.Graph(
                            id='bar-graph',
                            className='small-bar-graph-container'
                        ),
                        html.Div(
                            id='score-dis',
                            className='score-dis',
                            style={'overflow-y': 'scroll', 'height': '200px'},
                        ),
                    ],
                    width=3,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Slider(
                        id='time-slider',
                        min=df['game_seconds_remaining'].min(),
                        max=df['game_seconds_remaining'].max(),
                        value=df['game_seconds_remaining'].min(),
                        marks={str(time): str(time) for time in df['game_seconds_remaining'].unique()},
                        updatemode='drag'
                    ),
                    width=12,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='line-graph',  # This is the correct placement for the line graph
                ),
                width=12,
            )
        ),
    ],
    width=10,
)


# Construct the app layout
app.layout = dbc.Container(
    dbc.Row([sidebar, content]),
    fluid=True
)

# Callback to update the football field and description window based on the selected game_id and time
@app.callback(
    [Output('field-graph', 'figure'), 
     Output('bar-graph', 'figure'), 
     Output('desc-window', 'children'), 
     Output('score-dis', 'children'),
     Output('line-graph', 'figure')],  # Target output for the line graph
    [Input('game-id-dropdown', 'value'), Input('time-slider', 'value')]
)


def update_output(selected_game_id, game_seconds_remaining):
    filtered_df = df[(df['game_id'] == selected_game_id) & (df['game_seconds_remaining'] <= game_seconds_remaining)]

    # Create figure
    fig = go.Figure()

    # Add the football field image
    # Add the football field image
# In your update_output callback
    field_image = {
        "source": image_data_uri,  # Use the Data URI for the image
        "xref": "x",
        "yref": "y",
        "x": -14.95,
        "y": 100,
        "sizex": 130,
        "sizey": 100,  # Adjusted for field aspect ratio based on dimensions
        "sizing": "stretch",
        "opacity": 1.0,
        "layer": "below"
    }
    fig.add_layout_image(field_image)

    # Set axes properties
    fig.update_xaxes(showgrid=False, range=[-14.95, 120])
    fig.update_yaxes(showgrid=False, range=[0, 100])

    # Add play markers
    if not filtered_df.empty:
        play = filtered_df.iloc[-1]
        if play['posteam_type'] == 'home':
            end_yardline =100-play['yardline_100'] + play['yards_gained']
            start_yardline = 100-play['yardline_100']
        else:
            end_yardline = play['yardline_100'] - play['yards_gained']
            start_yardline = play['yardline_100']

        fig.add_shape(
            type="line",
            x0=start_yardline,
            y0=0,
            x1=start_yardline,
            y1=100,
            line=dict(color="blue", width=5)
        )
        fig.add_shape(
            type="line",
            x0=end_yardline,
            y0=0,
            x1=end_yardline,
            y1=100,
            line=dict(color="red", width=5)
    )
            # Check if touchdown is 1
    if play['touchdown'] == 1:
        # Add a specific graphic to your figure
        endzone_yardline = 111 if play['posteam_type'] == 'home' else -1
        fig.add_shape(
            type="rect",
            x0=endzone_yardline - 10,  # assuming the endzone is 10 yards
            y0=0,
            x1=endzone_yardline,
            y1=100,
            line=dict(color="red", width=3),
            fillcolor="red"
        )
    

    # Add the football field image

    

    # Hide axis line, grid, ticklabels and title
    fig.update_xaxes(showline=False, zeroline=False, tickvals=[], title_text='')
    fig.update_yaxes(showline=False, zeroline=False, tickvals=[], title_text='')

    # Set figure size
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),  # Set all margins to 0
        paper_bgcolor='#161d33',  # Set the background color of the entire figure
        plot_bgcolor='#161d33',  # Set the background color to transparent
        # Remove width and height for true autosizing
    )
    score_string = f"Down: {play['down']:.0f}"
   

    # Create a new Figure object
    fig2 = go.Figure()

    # Add a bar graph for the home and away teams
    fig2.add_trace(
        go.Bar(
            x=[play['home_team'], play['away_team']],
            y=[play['total_home_score'], play['total_away_score']],
            marker_color=['blue', 'red'],  # Change the color of the bars
            marker_line=dict(width=1),  # Change the width of the border

            name='Scores'
        )
    ) 
    fig2.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=10, b=10),  # Adjust the size of the margins
        paper_bgcolor='#161d33',  # Set the background color of the entire figure
        plot_bgcolor='#161d33',  # Set the background color to transparent
    )
    fig3 = go.Figure()
    # Assuming 'vegas_home_wpa' and 'game_time_remaining' are columns in filtered_df
    # Ensure filtered_df is sorted by 'game_time_remaining' if it's not already
    fig3.add_trace(
        go.Scatter(
            x=filtered_df['game_seconds_remaining'],
            y=filtered_df['home_wp_post'],
            mode='lines+markers',
            name='Vegas Home WPA'
        )
    )
    fig3.update_layout(
        title='Win Probability Added (WPA) for Home Team Over Time',
        xaxis_title='Game Time Played (Seconds)',
        yaxis_title='Vegas Home WPA',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='#161d33',
        plot_bgcolor='#161d33',
        font=dict(color='white')
    )

    
    return fig,fig2, play['desc'], score_string,fig3
# Display the figure in a new window
       

@app.callback(
    Output('time-slider', 'marks'),
    [Input('game-id-dropdown', 'value')]
)
def update_slider_marks(selected_game_id):
    unique_times = df[df['game_id'] == selected_game_id]['game_seconds_remaining'].unique()
    return {time: str(time) for time in unique_times}


if __name__ == '__main__':
    app.run_server(debug=True)

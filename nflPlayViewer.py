import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import os
import plotly.graph_objects as go
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Get the current working directory
cwd = os.getcwd()
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


# Build the path to the image
image_path = os.path.join(cwd, 'my_dash_app', 'images', '4840654.jpg')
server = app.server
# Function to convert PIL image to Data URI
def pil_to_data_uri(img):
    data = BytesIO()
    img.save(data, "JPEG")
    data_uri = "data:image/jpeg;base64," + base64.b64encode(data.getvalue()).decode('utf-8')
    return data_uri
def pil_to_data_uri_logo(img):
    data = BytesIO()
    img.save(data, "PNG")
    data_uri = "data:image/png;base64," + base64.b64encode(data.getvalue()).decode('utf-8')
    return data_uri
# run some code for applying logo image
logo_path = 'images/logo.png'
pil_logo = Image.open(logo_path)
logo_data_uri = pil_to_data_uri_logo(pil_logo)
# same as ^ but for the field image
pil_image_path = 'images/4840654.jpg'
pil_image = Image.open(pil_image_path)
image_data_uri = pil_to_data_uri(pil_image)
# load the play button image
play_img_path = 'images/play_pause.png'
play_img = Image.open(play_img_path)
play_img_src = pil_to_data_uri_logo(play_img)
# Load the data

# Initialize the Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
df = pd.read_csv('data/sb_2000_2023.csv', low_memory=False)
team_directions = df.groupby('game_id')['posteam'].unique().apply(lambda teams: {team: idx for idx, team in enumerate(teams)}).to_dict()
# Define the sidebar layout for selecting game_id
# Define the sidebar layout for selecting game_id


# Construct the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Img(src=logo_data_uri, style={'height': '0%', 'width': '0%'}),
                html.Hr(),
                dcc.Dropdown(
                    id='game-id-dropdown',
                    options=[{'label': game_id, 'value': game_id} for game_id in df['game_id'].unique()],
                    value=df['game_id'].iloc[0],
                    className='dropdown',
                    clearable=False,
                    style={'background-color': '#fffff', 'color': 'red'}
                ),
            ], className='sidebar'),
            width=2,
            style={'maxWidth': '200px'}  # Set the maximum width of the sidebar
        ),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='field-graph',
                        figure={},
                        config={'staticPlot': True}  # Disable zoom and pan
                    ),    html.Img(id='play-pause-button', src=play_img_src, className = 'btnImg', n_clicks=0, style={'cursor': 'pointer', 'height': '50px', 'background-color': '#fffff'}),

dcc.Interval(
    id='auto-stepper',
    interval=1*1000,  # in milliseconds (e.g., 1000ms = 1 second per step)
    n_intervals=0,
    disabled=True,  # Initially disabled
),
                    dcc.Slider(
                        id='time-slider',
                        className='time-slider',
                        value=df['...1'].min(),
                        marks={str(time): str(time) for time in df['...1'].unique()},
                        updatemode='drag',

                    ),
                ], width=9),
                dbc.Col([
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
                ], width=3),
            ]),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(
                        id='line-graph',
                        className='centered-container',
                        style={'margin-top': '-100px'},  # Adjust the value as needed to move the graph up
                    ),
                    width=12,
                )
            ),
        ], width=10),
    ]),
], fluid=True)

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
    filtered_df = df[(df['game_id'] == selected_game_id) & (df['...1'] <= game_seconds_remaining)]

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
            dwn_distance = 100 -play['yardline_100']+play['ydstogo']
        else:
            end_yardline = play['yardline_100'] - play['yards_gained']
            start_yardline = play['yardline_100']
            dwn_distance = play['yardline_100']-play['ydstogo']
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

        # Add an arrow
        fig.add_annotation(
            x=end_yardline,
            y=50,
            ax=start_yardline,
            ay=50,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="white"
        )
        fig.add_shape(
            type="line",
            x0=dwn_distance,
            y0=0,
            x1=dwn_distance,
            y1=100,
            line=dict(color="yellow", width=4)
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
    score_string = f"Down: {play['down']:.0f} | Possession: {play['posteam']} | Time: {play['time']} | Quarter: {play['qtr']} "


    # Create a new Figure object
    fig2 = go.Figure()
    if play["home_team"]=="CAR":
        home_image = "nfl_SB_PBP/images/team_logos/arizona-cardinals.svg"
    # Add a bar graph for the home and away teams
    fig2.add_trace(
        go.Bar(
            x=[play['home_team'], play['away_team']],
            y=[play['total_home_score'], play['total_away_score']],
            marker_color=[play['home_color'], play['away_color']],  # Change the color of the bars
            marker_line=dict(width=5),  # Change the width of the border
            name='Scores'
        )
    )



    fig2.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=10, b=10),  # Adjust the size of the margins
        paper_bgcolor='#1b2444',  # Set the background color of the entire figure
        plot_bgcolor='#1b2444',  # Set the background color to transparent
        font=dict(color='white')  # Set the text color to green

    )
    fig3 = go.Figure()
    # Assuming 'vegas_home_wpa' and 'game_time_remaining' are columns in filtered_df
    # Ensure filtered_df is sorted by 'game_time_remaining' if it's not already
    fig3.add_trace(
        go.Scatter(
            x=filtered_df['...1'],
            y=filtered_df['home_wp_post'],
            mode='lines+markers',
            name='Vegas Home WPA'
        )
    )
    fig3.update_xaxes(
        tickvals=filtered_df['...1']*10,

        ticktext=[i for i in range(len(filtered_df['...1']),10)]
    )

    fig3.update_layout(
        title='Win Probability Added (WPA) for Home Team Over Time',
        xaxis_title='Play Number',
        yaxis_title='Vegas Home WPA',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='#161d33',
        plot_bgcolor='#161d33',
        font=dict(color='white'),
    )


    return fig,fig2, play['desc'], score_string,fig3
# Display the figure in a new window


@app.callback(
    [Output('time-slider', 'min'), Output('time-slider', 'max')],
    [Input('game-id-dropdown', 'value')]
)
def update_slider_range(selected_game_id):
    filtered_df = df[df['game_id'] == selected_game_id]
    min_time = filtered_df['...1'].min()
    max_time = filtered_df['...1'].max()
    return min_time, max_time
@app.callback(
    Output('time-slider', 'step'),
    Input('game-id-dropdown', 'value')  # Assuming this is the ID of your dropdown
)
def update_step(selected_game_id):
    # Filter the DataFrame based on the selected game ID
    filtered_df = df[df['game_id'] == selected_game_id]

    # Calculate the new step value
    step = (filtered_df['...1'].max() - filtered_df['...1'].min()) / len(filtered_df['...1'].unique())

    return step
@app.callback(
    Output('time-slider', 'marks'),
    [Input('game-id-dropdown', 'value')]
)
def update_slider_marks(selected_game_id):
    # Filter the DataFrame based on the selected game ID
    filtered_df = df[df['game_id'] == selected_game_id]

    # Get the unique values in the '...1' column
    unique_values = filtered_df['...1'].unique()

    # Create a dictionary where the keys and values are the unique values
    marks = {str(value) : str(value) for value in unique_values}

    return marks
@app.callback(
    Output('auto-stepper', 'disabled'),
    [Input('play-pause-button', 'n_clicks')],
    [State('auto-stepper', 'disabled')],
)
def toggle_interval(n_clicks, is_disabled):
    if n_clicks:
        return not is_disabled
    return is_disabled
@app.callback(
    Output('time-slider', 'value'),
    [Input('auto-stepper', 'n_intervals')],
    [State('time-slider', 'value'),
     State('time-slider', 'max')]
)
def update_slider(n_intervals, current_value, max_value):
    if current_value is None:
        return 0
    new_value = (current_value + 1)
    return new_value
from dash import callback_context

# @app.callback(
#     Output('play-pause-button', 'style'),
#     [Input('play-pause-button', 'n_clicks')],
#     [State('play-pause-button', 'style')]
# )
# def toggle_play_pause_style(n_clicks, current_style):
#     if n_clicks is None:
#         raise PreventUpdate

#     triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]
#     if triggered_id == 'play-pause-button':
#         if current_style and 'boxShadow' in current_style:
#             # Assuming play was active, so remove the shadow to indicate pause
#             return {**current_style, 'boxShadow': '', 'transform': ''}
#         else:
#             # Play was not active, so add the shadow to indicate play
#             return {**current_style, 'boxShadow': '0 0 10px red', 'transform': 'scale(1.0)'}
#     else:
#         return current_style

if __name__ == '__main__':
    app.run_server(debug=True)

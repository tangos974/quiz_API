import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import requests
from main import possible_subjects
from main import possible_uses

# Initialize the Dash app
app_dash = dash.Dash(__name__)

# Define the layout of the Dash app
app_dash.layout = html.Div(children=[
    html.H1(children='FastAPI-Dash Integration'),

    html.Div(children='''
        Welcome to the integration of FastAPI and Dash.
    '''),

    # Button to get a random question
    html.Button('Get Random Question', id='get-random-question-btn', n_clicks=0),

    # Display area for the random question
    html.Div(id='random-question-output'),

    # Button to get a random filtered question
    html.Button('Get Random Filtered Question', id='get-random-filtered-question-btn', n_clicks=0),

    # Dropdown for selecting the 'use' parameter for filtered questions
    dcc.Dropdown(
        id='use-dropdown',
        options=[{'label': use, 'value': use} for use in possible_uses],
        value=None,
        placeholder='Select a use'
    ),

    # Display area for the random filtered question
    html.Div(id='random-filtered-question-output'),

    # Button to get multiple responses
    html.Button('Get Multiple Responses', id='get-multiple-responses-btn', n_clicks=0),

    # Input for the number of responses
    dcc.Input(id='num-responses-input', type='number', value=1, min=1, max=20),

    # Display area for multiple responses
    html.Div(id='multiple-responses-output'),

    # Add a new button to stop the Dash app
    html.Button('Stop Dash App', id='stop-dash-app-btn', n_clicks=0)
])

# Define callback functions to interact with FastAPI API
@app_dash.callback(
    Output('random-question-output', 'children'),
    [Input('get-random-question-btn', 'n_clicks')]
)
def get_random_question(n_clicks):
    if n_clicks > 0:
        response = requests.get('http://localhost:8000/random_question')
        data = response.json()
        return f"Random Question: {data['question']}"

@app_dash.callback(
    Output('random-filtered-question-output', 'children'),
    [Input('get-random-filtered-question-btn', 'n_clicks')],
    [dash.dependencies.State('use-dropdown', 'value')]
)
def get_random_filtered_question(n_clicks, use):
    if n_clicks > 0:
        response = requests.get(f'http://localhost:8000/random_filtered_question?use={use}')
        data = response.json()
        return f"Random Filtered Question: {data['question']}"

@app_dash.callback(
    Output('multiple-responses-output', 'children'),
    [Input('get-multiple-responses-btn', 'n_clicks')],
    [dash.dependencies.State('use-dropdown', 'value'),
     dash.dependencies.State('num-responses-input', 'value')]
)
def get_multiple_responses(n_clicks, use, num_responses):
    if n_clicks > 0:
        response = requests.get(f'http://localhost:8000/multiple_responses?use={use}&num_responses={num_responses}')
        data = response.json()
        questions = [q['question'] for q in data['questions']]
        return f"Multiple Responses: {', '.join(questions)}"

@app_dash.callback(
    Output('random-question-output', 'children'),
    [Input('stop-dash-app-btn', 'n_clicks')]
)
def stop_dash_app(n_clicks):
    if n_clicks > 0:
        response = requests.get('http://localhost:8000/stop_dash_app')
        data = response.json()
        return f"Message from FastAPI: {data['message']}"

# Run the Dash app
if __name__ == '__main__':
    app_dash.run_server(debug=False)
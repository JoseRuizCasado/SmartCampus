import plotly.graph_objects as go
import pandas as pd
import json
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from query_smartcampus import get_data


df_noise = pd.read_csv('data-noise.csv')
fig_noise = go.Figure([go.Scatter(x=df_noise['Date'], y=df_noise['Data'])])

df_temp = pd.read_csv('data-temp.csv')
try:
    del df_temp['Unnamed: 0']
except:
    pass

fig_temp = go.Figure([go.Scatter(x=df_temp['Date'], y=df_temp['Temperature']), go.Scatter(x=df_temp['Date'], y=df_temp['Humidity'])])

content = html.Div(
    [
        html.H1('Personal Stock Price Dashboard', 
                style={'textAlign': 'center'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph", figure=fig_noise),
                        width={"size": 8, "offset": 2}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph-temp", figure=fig_temp),
                        width={"size": 8, "offset": 2}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(width={"size": 0.01, "offset": 2}),
                dbc.Col(dbc.FormGroup([
                            dbc.Button(
                                id='dowload-button',
                                n_clicks=0,
                                children='Download',
                                color="primary",
                                block=True
                            ),
                        ]),
                        width={"size": 4, "offset": 2}),
                html.Div(id='intermediate-value', style={'display': 'none'})
            ],
            
        ),
        dcc.Interval(id='interval', interval=300000)
    ]
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([content])

@app.callback(
    Output('intermediate-value', 'children'),
    [Input('dowload-button', 'n_clicks')])
def show_input(n_clicks):
    """Save DataFrame data to csv file.

    Args:
      n_clicks: Number of clicks maked since app is running.

    Returns:
      Nothing, this event doesn't update fronted.

    """
    df_noise.to_csv('data-noise.csv', index=False)
    df_temp.to_csv('data-temp.csv', index=False)
    return ''


@app.callback(
    Output('graph', 'figure'),
    [Input('interval', 'n_intervals')]
)
def streamFig(value):
    """Update grapah periodically. Make request to UMA SmartCampus and append data
    to global DataFrame
    Args:
      value: Number of intervals executed since app is running.

    Returns:
      The new figure object to update in front end.

    """
    global df_noise
    (noise, timestamp), (temp, hum, ts) = get_data()
    new_data = {'Noise': noise, 'Date': timestamp}
    if timestamp not in df_noise['Date'].tolist():
        # Update dataframe if timestamp of the requested
        # is not in the dataframe
        df_noise = df_noise.append(new_data, ignore_index=True)

    fig = go.Figure([go.Scatter(x=df_noise['Date'], y=df_noise['Data'])])
    return(fig)


@app.callback(
    Output('graph-temp', 'figure'),
    [Input('interval', 'n_intervals')]
)
def streamFigTemp(value):
    """Update grapah periodically. Make request to UMA SmartCampus and append data
    to global DataFrame
    Args:
      value: Number of intervals executed since app is running.

    Returns:
      The new figure object to update in front end.

    """
    global df_temp
    (noise, timestamp), (temp, hum, ts) = get_data()
    new_data = {'Temperature': temp, 'Humidity': hum, 'Date': ts}
    if timestamp not in df_temp['Date'].tolist():
        # Update dataframe if timestamp of the requested
        # is not in the dataframe
        df_temp = df_temp.append(new_data, ignore_index=True)

    fig = go.Figure([go.Scatter(x=df_temp['Date'], y=df_temp['Temperature']), go.Scatter(x=df_temp['Date'], y=df_temp['Humidity'])])
    return(fig)


if __name__ == '__main__':
    app.run_server(port='8083', debug=True)

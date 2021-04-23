# UMA Smart Campus Dashboard
This is a simple dashboard to visualize UMA noise sensor.

## Data recollection
The sensor measure the noise and transmit it using Fiware. To take
this data in the dashboard HTTP request is made.

It is needed to take a token to log in in Fiware service. Without this
token the request can't be done.

## Dashboard
The dashboard is make with Dash. A plotly graph is show to see data as time serie.
This graph is updated automatically every 5 minutes bia Interval object.


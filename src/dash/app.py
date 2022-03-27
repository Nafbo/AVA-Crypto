from dash import Dash, dcc, html, Input, Output
import pandas as pd
from ..essais.test import wallet_balance
import json

app = Dash(__name__)

df = wallet_balance("0xFEC4f9D5B322Aa834056E85946A32c35A3f5aDD8")

app.layout = html.Div([
    dcc.Input(
        placeholder='Enter a value...',
        type='text',
        value=''
    ),
    html.Hr(),
    html.Details([
        html.Summary('Contents of wallet'),
        dcc.Markdown(
            id='clientside-figure-json'
        )
    ])
])


@app.callback(
    Output('clientside-figure-json', 'children'),
    Input('clientside-figure-store', 'data')
)
def generated_figure_json(data):
    return '```\n'+json.dumps(data, indent=2)+'\n```'


if __name__ == '__main__':
    app.run_server(debug=True)

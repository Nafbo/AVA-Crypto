from dash import Dash, dcc, html, Input, Output
import pandas as pd
from src.essais.compute_wallet import fetch_wallet_balance
import json

app = Dash(__name__)

app.layout = html.Div([
    dcc.Input(
        id='my-input', 
        placeholder='Enter a value...', 
        type='text',
        value='0xFEC4f9D5B322Aa834056E85946A32c35A3f5aDD8'
    ),
    html.Hr(),
    html.Details([
        html.Summary('Contents of wallet'),
        dcc.Markdown(
            id='pretty-json'
        )
    ])
])

@app.callback(
    Output('pretty-json', 'children'),
    Input('my-input', 'value')
)
def compute_wallet(wallet_adress):
    json_file = fetch_wallet_balance(wallet_adress)
    return '```\n'+json.dumps(json_file, indent=2)+'\n```'

def launch_app():
    return app.run_server(debug=True)

if __name__ == '__main__':
    launch_app()

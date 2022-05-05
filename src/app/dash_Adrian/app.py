import dash
from dash import Dash, dcc, html
import pandas as pd
import sys
sys.path.insert(0, '../feature')
import unittest
from main_feature import *
data=df


app = dash.Dash(__name__)



app.layout = html.Div(
    children=[
        html.H1(children="Crypto Dashboard", style={"text-align":"center","fontSize": "48px", "color": "blue"}),
        html.P(
            children="Metamask Account",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Name"],
                        "y": data["Balance"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Balance Metamask Wallet"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Name"],
                        "y": data["Profit/Loss"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Profit/Loss Metamask Wallet"},
            },
        ),

         dcc.Graph(
            figure={
                "dataa": [
                    {
                        "x": data["contract_name"],
                        "y": data["contract_decimals"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Balance plus"},
            },
        ),

        dcc.Graph(
            figure={
                'data': [
                    {'x': data["Name"], 'y': data["Profit/Loss"], 'type': 'bar', 'name': data["Name"]},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )

    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
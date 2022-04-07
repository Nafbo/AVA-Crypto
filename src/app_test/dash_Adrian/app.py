import dash
from dash import Dash, dcc, html
import pandas as pd
from main import df,dff

data = df
dataa=dff
'''data.sort_values("Balance", inplace=True)'''

app = dash.Dash(__name__)
'''
external_stylesheets = [
    {
        "href": "/Users/adri22/Desktop/AVA-Crypto/img/icons8-bitcoin-accepted-64.png"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Crypto Dashboard : Understand Your Account Easily!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children=" /Users/adri22/Desktop/AVA-Crypto/img/icons8-bitcoin-accepted-64.png"),
                html.H1(
                    children="Crypto Dashboard : Understand Your Account Easily! ", className="header-title"
                ),
                html.P(
                    children="Get all your wallet and cryptocurrencies prices",
                    className="header-description",
                ),
            ],
            className="header",
        ),

'''
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
                        "x": dataa["contract_name"],
                        "y": dataa["contract_decimals"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Balance plus"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

#------------ import librairies -----------------------------------------------------------------------------------------------------------

from numpy import number
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output



#------------ démarre l'app et import dataframe ---------------------------------------------------------------------------------------------

app=Dash(__name__)


#pd.set_option('display.float_format', lambda x: '%.5f' % x) => ecriture non scientifique
#pd.reset_option('display.float_format') => remettre l'orignal format

wallet=pd.read_csv("ressources/csv.csv")

number_crypto=wallet.loc[:,["Name","Balance"]]

number_crypto.reset_index(inplace=True)

#print(number_crypto)
# fig = go.Figure(data=[go.pie(labels=number_crypto['Name'], values=number_crypto["Balance"], hole=.3)])  
# serveur=app.server
#------------------------------------------------------------------------------------------------------------------------------------------
#App layout

app.layout = html.Div([

    html.H1("Bienvenue sur votre dashboard", style={"text-align":"center"}),

    dcc.Dropdown(id='slct_wallet',
                    options=[
                        {"label":"Choisir votre wallet", "value":0},
                        {"label":"Wallet 1", "value":1},
                        {"label":"Wallet 2", "value":2},
                        {"label":"Wallet 3", "value":3},],
                     multi=False,
                     value = 0,
                     style={'display': 'inline-block', 'vertical-align': 'middle',
                   "min-width": "150px",
                   'height': "30px",
                   "textAlign":"center",            
                   "borderColor":"black",
                   "bordeRadius":"50px"}
                    ),
              
    #dcc.Graph(id='graph_crypto_wallet', figure=fig),

    #html.Hr(),

   



    # html.Button("button1", id='btn-nclicks-1',n_clicks=0,
    #                style={'display': 'inline-block', 'vertical-align': 'middle',
    #                "min-width": "150px",
    #                'height': "25px",
    #                "margin-top": "0px",
    #                "margin-left": "15px",
    #                "border-color":"rgb(163, 221, 203)",
    #                "border-radius":"55px"}),
    # html.Button(number_crypto['Name'][1], id='btn-nclicks-2', n_clicks=0, style={'display': 'inline-block', 'vertical-align': 'middle',
    #                "min-width": "150px",
    #                'height': "25px",
    #                "margin-top": "0px",
    #                "margin-left": "15px",
    #                "border-color":"rgb(163, 221, 203)",
    #                "border-radius":"55px"}),
    # html.Button('Button 3', id='btn-nclicks-3', n_clicks=0,style ={'display': 'inline-block', 'vertical-align': 'middle',
    #                "min-width": "150px",
    #                'height': "25px",
    #                "margin-top": "0px",
    #                "margin-left": "15px",
    #                "border-color":"rgb(163, 221, 203)",
    #                "border-radius":"55px"}),
    
    dcc.Graph(
        figure={
            'number_crypto': [
                {'x': number_crypto['Name'], 
                'y':number_crypto['Balance'], 
                'type': 'lines',},
        
            ],
            "layout": {
                'title': 'Dash Data Visualization'
            } 
        }
    ),

    html.Div(id='output_container', children=[]),

   
])

#------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='graph', component_property='figure')],
    [Input(component_id='slct_wallet',  component_property='value')],
)

def update_graph(option_slct):
   print(option_slct)
   print(type(option_slct))

   wallet_chose="The wallet chose by the user was {}".format(option_slct)



   return wallet_chose, fig
    
#------------------------------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True)




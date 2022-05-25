# -----IMPORT -----------------------------------------------------
from ctypes import alignment
from tracemalloc import stop
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from matplotlib import image
import plotly.express as px
import pandas as pd
import base64
import plotly.graph_objs as go
from dash import Dash, dash_table


from src.app.feature_wallet.wallet import wallet
from src.app.feature_history.wallet_history import wallet_history
from src.app.feature_price.price import price
from src.app.feature_transaction.transaction import transaction
# ------- INITIALISATION DATA --------------------------------------------------------
# wallet=pd.read_csv("src/app/dash_Alice/ressources/wallet_ex.csv")    
# wallet["Name"].fillna("Unknown", inplace=True)
#print (wallet("0x102e0206113e2b662ea784eb5db4e8de1d18c8ae", 1))

adress_curent = "0xdB24106BfAA506bEfb1806462332317d638B2d82"
blockchain = 1
default_transaction=transaction(adress_curent, blockchain)
# print(default_transaction)
# "0x102e0206113e2b662ea784eb5db4e8de1d18c8ae", 1

wallet,total=wallet(adress_curent, blockchain)
default_name=wallet['Name'].head(1)

wallet_history = wallet_history(adress_curent, blockchain)
history = px.line(wallet_history, x='Date', y='Holdings (en USD)')

image_ava_filename = 'src/app/dash/ressources/AVA_logo.png'
encoded_image_ava = base64.b64encode(open(image_ava_filename, 'rb').read()) 

image_plus_filename = 'src/app/dash/ressources/plus.png'
encoded_image_plus = base64.b64encode(open(image_plus_filename, 'rb').read()) 

image_moins_filename = 'src/app/dash/ressources/minus.png'
encoded_image_moins = base64.b64encode(open(image_moins_filename, 'rb').read()) 

ethereum_logo = 'src/app/dash/ressources/ethereum_logo.png'
encoded_image_ethereum = base64.b64encode(open(ethereum_logo, 'rb').read())

bitcoin_logo = 'src/app/dash/ressources/bitcoin_logo.png'
encoded_image_bitcoin = base64.b64encode(open(bitcoin_logo, 'rb').read())

cardano_logo = 'src/app/dash/ressources/cardano_logo.png'
encoded_image_cardano = base64.b64encode(open(cardano_logo, 'rb').read())

button_filename = 'src/app/dash/ressources/AVA_button.png'
encoded_image_button = base64.b64encode(open(button_filename, 'rb').read())

# ------- APP -----------------------------------------------------------

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ],  #dbc.themes.ZEPHIR
            meta_tags=[{'name': 'viewport',       # permet à l'app d'être responsive pour téléphone  
                     'content': 'width=device-width, initial-scale=1.0'}]
                     
            )

# navbar = dbc.Nav([
#     dbc.NavLink("Global View", href="/" ,active="exact"),
#     dbc.NavLink("Transactions", href="/transactions", active ="exact")
# ]),

# content = html.Div(id="page-content", className="card border-secondary mb-3"),
# ------- LAYOUT --------------------------------------------------------

app.layout= dbc.Container([    #dbc.Container mieux que html.div pour bootstrap

 #-------------- HEADER --------------#

    dbc.Row([   #divise la page en 3 ligne : le titres / dropdown / derniers bar chart
        dbc.Col([  #divise les lignes en colonnes ici que le titre
            html.Div([

                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image_ava.decode()),
                    height = "60px"
                ),
            ]), 
        ], width=1),
 
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.H4(adress_curent, className='modal-title ')
                ],className="py-1 "),  
            ]), #parametre du text w/ bootstrap   df. bootstrap cheatsheet  
        ], className="card border-success ", width={'size':9, 'offset':1}),
        
        dbc.Col([
            html.Button([
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image_button.decode()),
                    height = "50px"
                ),
            ], className='btn btn-secondary')
        ],width=1), 
    ], className="m-2"),  

 #-------------- BODY --------------#

    #-------------- TOP --------------#
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Card([
                    html.H3("Overall"),
                    html.H4(total),html.H4("$")
                ], className='card border-light mb-3 py-5 text-md-center'),
            ],style={"height": "50%"}),
        ], width=2),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    
                    html.H4("Balance"),
                    dcc.Dropdown(id='dropdown_details',
                        multi=False, #peut choisir qu'une seule valeur
                        value=default_name, #valeur par defaut 
                        options=[{'label':x, 'value':x} 
                                    for x in sorted(wallet['Name'].unique())] #choisis les valeurs selon la colonne Name : .unique() prends que les valeurs 1 fois sans duplicats
                        ),
                ]),
 
                dbc.CardBody(id='details_output')
               
            ],style={"height": "100%"}, className='card border-light'),   
        ], className  ='mb-3'),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Token Price"),

                    dcc.Dropdown(id='dropdown_temps_reel', 
                        multi=False, #peut choisir qu'une seule valeur
                        value="bitcoin", #valeur par defaut 
                        options=["bitcoin","ethereum","cardano"] #choisis les valeurs selon la colonne Name : .unique() prends que les valeurs 1 fois sans duplicats
                        ),
                ]),

                dbc.CardBody(id="temps_reel_output"),

            ],style={"height": "100%"}, className='card border-light'),   
        ],className="mb-3"),
    ]),

    #-------------- BOTTOM --------------#   
    dbc.Row([
        dbc.Col([
            dbc.Card([
                    html.P("Adress Current Wallet : {}".format(adress_curent))
                ], className='card border-light mb-3 py-5 text-sm-center'),

            html.Button([
                    html.H4("wallet 2")
                ], className='btn btn-secondary mb-3'),

            html.Button(
                    html.H4("Add another wallet + "), id="add_wallet", n_clicks = 0, className='btn btn-secondary')
 
        ],style={"height": "100%"},width=2),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dcc.Location(id="url"),
                    dbc.Nav([
                        dbc.NavLink("Global View", href="/" ,active="exact"),
                        dbc.NavLink("Transactions", href="/transactions", active ="exact")
                    ]),
                ]),

                dbc.CardBody(id="page-content")

            ])
        ], width = 10),
    ]),

 #-------------- FOOTER --------------#    
],fluid = True) #permet d'étirer à la largeur de la page web    


# ------- CALLBACK -------------------------------------------------------


# Balance : details_crypto
@app.callback(
    Output("details_output", "children"),
    Input('dropdown_details', 'value')
)
def update_output_details(value_slctd):
    dff = wallet[wallet['Name']==value_slctd]
    balance = "{}".format(dff['Balance']).split('\n',1)[0].split('    ',1)[1]
    holdings = "{}".format(dff['Holdings (en USD)']).split('\n',1)[0].split('    ',1)[1]
    profit = "{}".format(dff['Profit/Loss']).split('\n',1)[0].split('    ',1)[1]
   
    return [
        dbc.Row([
            html.H5("Balance : {}".format(balance))
            ], className=" text-md-center"),

        dbc.Row([
            html.H5("Holdings en USD : {}".format(holdings))
        ],className=" text-md-center"),

        dbc.Row([
            html.H5("Profit/Loss : {}".format(profit))
        ],className=" text-md-center"),
    ]


# Token Price : temps_reel_output
@app.callback(
    Output("temps_reel_output","children"),
    Input("dropdown_temps_reel","value")
)

def update_output_temps_reel(value_slctd):
    price_tps = price(value_slctd)
    price_final =  price_tps[0]

    if value_slctd == "bitcoin" :
        image_logo = encoded_image_bitcoin
    elif value_slctd == "ethereum" :
        image_logo = encoded_image_ethereum
    elif value_slctd == "cardano" :
        image_logo = encoded_image_cardano

    if price_final > 0 :
        image_profit = encoded_image_plus
    
    elif price_final < 0 :
        image_profit = encoded_image_moins

    return [
        dbc.Row([
            dbc.Col([  
                html.Div([
                    html.Img(
                        src='data:image/png;base64,{}'.format(image_logo.decode()),
                        height = "80px"
                     ),
                ],style={'text-align': 'center'} )       
                
            ],width=4,className=" py-2"),

        
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H5(["Actual Price : {}".format(price_final)], className="text-center"),
                        
                            html.Img(
                                src='data:image/png;base64,{}'.format(image_profit.decode()),
                                className="img-fluid", )# height = "40px", )
                    
                        ], style={'text-align': 'center'})
                    ]),
                ],)
            ],width = 7),  
        ],className=" py-1")
 
    ]

# #temps_reel_couleur   
# @app.callback(
#     Output("temps_reel_couleur","children"),
#     Input("dropdown_temps_reel","value")
# )

# def update_output_temps_couleurs(value_slctd):
#     price_tps = price(value_slctd)
#     return "Price : {}".format(price_tps[0])







 #-------------- NavBar Callback --------------#    
@app.callback(

    Output("page-content", "children"),
    [Input("url","pathname")]
)

def render_page_content(pathname):
    if pathname=="/" :
        return [

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([ 
                            html.H4("Your Token"),
                            dcc.Dropdown(id='dropdown_donut', 
                                multi=True, #peut choisir plusieurs valeurs
                                value=default_name,
                                options=[{'label':x, 'value':x}
                                            for x in sorted(wallet['Name'].unique())],
                            ),
                        ]),

                        dbc.CardBody([
                            dcc.Graph(id='donut', figure={})
                        ]),

                    ],className="card border-light mb-3"),
                ],width=6),

                dbc.Col([
                    dbc.Card([
                            dbc.CardHeader([
                                html.H4("Wallet History")
                            ]),

                            dbc.CardBody([
                                dcc.Graph(figure=px.line(wallet_history, x='Date', y='Holdings (en USD)'))      
                            ]),
                    ], className="card border-light mb-3")
                ],width=6),
            ]),

            dbc.Row([
                dbc.Col([
                   dbc.Card([
                        dbc.CardHeader([
                            html.H4("Your token"), 

                            dcc.Checklist(id='checklist_bar',
                                value=default_name,
                                options=[{'label':x, 'value':x}
                                    for x in sorted(wallet['Name'].unique())],
                                labelClassName='text-secondary mx-1'  #espace entre les options
                            ),
                        ]),

                        dbc.CardBody([
                            dcc.Graph(id='bar_chart', figure={}, style={"height": "95%"}),
                        ]),
                    ], className='card border-light'),
                ]),
            ]),


        ]      

    elif pathname=="/transactions" :

        return [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("Transactions"),
                        ]),

                        dbc.CardBody([
                            dash_table.DataTable(
                                data=default_transaction.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in default_transaction.columns],
                                page_action='none',
                                style_table={'overflowY': 'auto','height': 400},
                                style_cell={
                                    'height': 'auto',
                                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                                    'whiteSpace': 'normal'
                                },
                                style_header={
                                    'backgroundColor': 'hex(F8F8F8)',
                                    'border': '1px solid pink' ,
                                    'fontWeight': 'bold',
                                    'color':'black'
                                },
                                style_data={
                                    'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                                    # 'border': '1px solid blue' ,
                                    'textOverflow': 'ellipsis',
                                    'backgroundColor': 'rgba(255, 255, 255, 0)',
                                    'color': 'black'
                                },
                                
                                fixed_rows={'headers': True},
                            )  , 
                           
                          
                         
                        ], className="table table-hover"), 

                    ],  className='card border-light mb-3'),
                ])
            ])
        ]
        

@app.callback(
    Output('donut', 'figure'),
    Input('dropdown_donut', 'value')
)
def update_graph(value_slctd):
    wallet_slctd = wallet[wallet['Name'].isin(value_slctd)]
    figln2 = px.pie(wallet_slctd, names='Name', values='Balance', color='Name', hover_name='Name', hole=.4)
    return figln2


# Barchart - Balance - Crypto
@app.callback(
    Output('bar_chart', 'figure'),
    Input('checklist_bar', 'value')
)
def update_graph(value_slctd):
    wallet_slctd = wallet[wallet['Name'].isin(value_slctd)]
    fighist = px.histogram(wallet_slctd, x='Name', y='Balance', color="Name",  hover_name='Name')
    return fighist


# # details_crypto
# @app.callback(
#     Output("details_output", "children"),
#     Input('dropdown_details', 'value')
# )
# def update_output_details(value_slctd):
#     dff = wallet[wallet['Name']==value_slctd]
#     balance = "{}".format(dff['Balance']).split('\n',1)[0].split('    ',1)[1]
#     holdings = "{}".format(dff['Holdings (en USD)']).split('\n',1)[0].split('    ',1)[1]
#     profit = "{}".format(dff['Profit/Loss']).split('\n',1)[0].split('    ',1)[1]
#     return "Balance : ",balance,"\n"," Holdings (en USD) : ",holdings, "\n", "Profit/Loss : " , profit












# #temps_reel_output
# @app.callback(
#     Output("temps_reel_output","children"),
#     Input("dropdown_temps_reel","value")
# )

# def update_output_temps_reel(value_slctd):
#     price_tps = price(value_slctd)
#     return "Price : {}".format(price_tps[0])

# #temps_reel_couleur   
# @app.callback(
#     Output("temps_reel_couleur","children"),
#     Input("dropdown_temps_reel","value")
# )

# def update_output_temps_couleurs(value_slctd):
#     price_tps = price(value_slctd)
#     return "Price : {}".format(price_tps[0])
# ------- RUN APP --------------------------------------------------------
# def launch_app():
#     return app.run_server(debug=True)  

if __name__=='__main__':
    app.run_server(debug=True)   


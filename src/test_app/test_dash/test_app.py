# -----IMPORT -----------------------------------------------------
from tracemalloc import stop
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import plotly.graph_objs as go
from dash import Dash, dash_table


from src.test_app.test_feature_wallet.test_wallet import test_wallet
# from src.test_app.test_feature_history.test_wallet_history import test_wallet_history
# from src.test_app.test_feature_price.test_price import test_price
# from src.test_app.test_feature_transaction.test_transaction import test_transaction
# ------- INITIALISATION DATA --------------------------------------------------------
# wallet=pd.read_csv("src/app/dash_Alice/ressources/wallet_ex.csv")    
# wallet["Name"].fillna("Unknown", inplace=True)
#print (wallet("0x102e0206113e2b662ea784eb5db4e8de1d18c8ae", 1))


# default_transaction=test_transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1).head(10)
# print(default_transaction)
# "0x102e0206113e2b662ea784eb5db4e8de1d18c8ae", 1
adress_curent = "0xCBD6832Ebc203e49E2B771897067fce3c58575ac"
blockchain = 1
wallet,total=test_wallet(adress_curent, blockchain)
default_name=wallet['Name'].head(1)

# wallet_history = test_wallet_history(adress_curent, blockchain)
# history = px.line(wallet_history, x='Date', y='Holdings (en USD)')

image_ava_filename = 'src/app/dash/ressources/AVA_logo.png'
encoded_image_ava = base64.b64encode(open(image_ava_filename, 'rb').read()) 

image_plus_filename = 'src/app/dash/ressources/plus.png'
encoded_image_plus = base64.b64encode(open(image_plus_filename, 'rb').read()) 

image_moins_filename = 'src/app/dash/ressources/minus.png'
encoded_image_moins = base64.b64encode(open(image_moins_filename, 'rb').read()) 


button_filename = 'src/app/dash/ressources/AVA_button.png'
encoded_image_button = base64.b64encode(open(button_filename, 'rb').read())

# ------- APP -----------------------------------------------------------

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ],  #dbc.themes.ZEPHIR
            meta_tags=[{'name': 'viewport',       # permet à l'app d'être responsive pour téléphone  
                     'content': 'width=device-width, initial-scale=1.0'}]
                     
            )

server=app.server
# ------- LAYOUT --------------------------------------------------------

app.layout= dbc.Container([    #dbc.Container mieux que html.div pour bootstrap

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
                     html.Div(
                        dcc.Dropdown([1,2,3])
                         , className="dropdown-menu"),
                ], width =2),
                dbc.Col([
                    html.H4(adress_curent,
                    className='modal-title')
                ]),  
              ]), #parametre du text w/ bootstrap   df. bootstrap cheatsheet  
        ], className="card border-success", width={'size':9, 'offset':1}),
        
        dbc.Col([
            html.Button([
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image_button.decode()),
                    height = "50px"
                ),
            ], className='btn btn-secondary')
        ],width=1), 

    ], className="m-2"),  

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
                    dcc.Dropdown(id='dropdown_donut', 
                        multi=True, #peut choisir plusieurs valeurs
                        value=default_name,
                        options=[{'label':x, 'value':x}
                                    for x in sorted(wallet['Name'].unique())],
                    )
                ]),

                dbc.CardBody([
                    dcc.Graph(id='donut', figure={})
                ]),

            ], className='card border-light mb-3'),   
        ]),
              
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    "Wallet History"
                ]),

                dbc.CardBody([
                    # dcc.Graph(figure=history)
                    
                ]),
            ], className='card border-light mb-3')
        ],style={"height": "100%"})
    ]),#justify : gère les espaces : start, center, end, between, around // pour que ça marche avoir des colonnes en "stock" ; justify='around'
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                    html.P("Adress Current Wallet : {}".format(adress_curent))
                ], className='card border-light mb-3 py-5 text-sm-center')
        ],width=2),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    
                    html.H4("Token"),
                    dcc.Dropdown(id='dropdown_details',
                        multi=False, #peut choisir qu'une seule valeur
                        value=default_name, #valeur par defaut 
                        options=[{'label':x, 'value':x} 
                                    for x in sorted(wallet['Name'].unique())] #choisis les valeurs selon la colonne Name : .unique() prends que les valeurs 1 fois sans duplicats
                        ),
                ]),
 
                dbc.CardBody(
                    html.Div(id='details_output', children=[])
                )
               
            ],style={"height": "100%"}, className='card border-light'),   
        ], className  ='mb-3'),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Token Price"),

                    dcc.Dropdown(id='dropdown_temps_reel',
                        multi=False, #peut choisir qu'une seule valeur
                        value=default_name, #valeur par defaut 
                        options=["bitcoin","ethereum","cardano"] #choisis les valeurs selon la colonne Name : .unique() prends que les valeurs 1 fois sans duplicats
                        ),
                ]),

                dbc.CardBody(
                        
                        html.Div([

                            html.Img(
                                src='data:image/png;base64,{}'.format(encoded_image_plus.decode()),
                                height = "60px"
                            ),
                         ]), 
                ),

            ],style={"height": "100%"}, className='card border-light'),   
        ],className="mb-3"),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Transactions"),
                ]),

                dbc.CardBody([
                    html.Div([
                        dash_table.DataTable(
                            # data=default_transaction.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in default_transaction.columns],
                            style_as_list_view=True,
                            style_cell={'padding': '5px'},
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white',
                                'fontWeight': 'bold'
                            },
                            style_data={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white'
                            }, 
                            
                            
                        ),
                     
                    ]),
                   
                ]), 
            ]),
            
        ]), 
    ]),      

    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.Button([
                    html.H4("wallet 2")
                ], className='btn btn-secondary mb-3'),
            ], style={"height": "50%"}),

            dbc.Row([
                html.Button(
                    html.H4("Add another wallet + "), id="add_wallet", n_clicks = 0, className='btn btn-secondary')
            ], style={"height": "50%"}),
        ], width = 2),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Selectionner vos cryptomonnaies"), 

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
        ],width=7),
    ]),  
],
fluid = True) #permet d'étirer à la largeur de la page web


# width={'size':5, 'offset':0, 'order':2}, #offset decale de 2 colonnes à gauche
# no_gutters= False,  l'espace entre les 2 éléments / True = pas d'espace ; False = espace
# width={'size':5, 'order':1},), #premières 5 colonnes à partir de la gauche, order permet de choisir l'ordre des éléments dans la ligne
# ),
# ], className='card border-light mb-3', style={"margin" : "6px"} ),
            

# ------- CALLBACK -------------------------------------------------------

# @app.callback(
#     Output('line-fig', 'figure'),
#     Input('dropdown', 'value')
# )
# def update_graph(stock_slctd):
#     dff = wallet[wallet['Name']==stock_slctd]
#     figln = px.bar(dff, x='Name', y='Balance')
#     return figln


# Balance - Donut
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

#Add wallet



# details_crypto
@app.callback(
    Output("details_output", "children"),
    Input('dropdown_details', 'value')
)
def update_output_details(value_slctd):
    dff = wallet[wallet['Name']==value_slctd]
    balance = "{}".format(dff['Balance']).split('\n',1)[0].split('    ',1)[1]
    holdings = "{}".format(dff['Holdings (en USD)']).split('\n',1)[0].split('    ',1)[1]
    profit = "{}".format(dff['Profit/Loss']).split('\n',1)[0].split('    ',1)[1]
    return "Balance : ",balance,"\n"," Holdings (en USD) : ",holdings, "\n", "Profit/Loss : " , profit

#temps_reel_output
@app.callback(
    Output("temps_reel_output","children"),
    Input("dropdown_temps_reel","value")
)

# def update_output_temps_reel(value_slctd):
    # price_tps = test_price(value_slctd)
    # return "Price : {}".format(price_tps[0])

#temps_reel_couleur   
# # @app.callback(
#     Output("temps_reel_couleur","children"),
#     Input("dropdown_temps_reel","value")
# )

# def update_output_temps_couleurs(value_slctd):
    # price_tps = test_price(value_slctd)
    # return "Price : {}".format(price_tps[0])
# ------- RUN APP --------------------------------------------------------
def launch_app():
    return app.run_server(debug=True)  


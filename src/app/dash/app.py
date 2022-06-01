# -----IMPORT -----------------------------------------------------
from tracemalloc import stop
import dash
from dash import dcc, callback_context
# import dash_core_components as dcc
from dash import html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import plotly.graph_objs as go
from dash import Dash, dash_table
import flask
from flask_login import LoginManager,UserMixin, current_user
import os
from flask_sqlalchemy import SQLAlchemy
import flask 

# ------- LINK WITH FEATURES --------------------------------------------------------

from src.app.feature_wallet.wallet import wallet
from src.app.feature_history.wallet_history import wallet_history
from src.app.feature_price.price import price
from src.app.feature_transaction.transaction import transaction
from src.app.database.database import create_user
from src.app.database.database import portefolio_by_user
from src.app.database.database import add_wallet

 #-------------- add images --------------#

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

reseaux_filename= 'src/app/dash/ressources/RESEAUXSOCIAUX.png'
encoded_image_reseaux = base64.b64encode(open(reseaux_filename, 'rb').read())


# ------- APP -----------------------------------------------------------

 #-------------- app Flask --------------#

server = flask.Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://oernnetgfetrdn:0ebdf4c1dfc0753cc258a88d43a79affe27af29740cd89c774d8d6e53cb3caf8@ec2-52-18-116-67.eu-west-1.compute.amazonaws.com:5432/d5995grqimq0u8"
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(server)
db.init_app(server)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    portefolios = db.relationship('Portofolio')
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
class Portofolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.String(100))
    chain_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, wallet, chain_id, user_id):
        self.wallet = wallet
        self.chain_id = chain_id
        self.user_id = user_id

app = dash.Dash(__name__, server=server,
                title='AVA crypto',
                update_title='Loading...',
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.QUARTZ],
                meta_tags=[{'name': 'viewport',         
                     'content': 'width=device-width, initial-scale=1.0'}])


# ------- LAYOUT --------------------------------------------------------

 #-------------- First page --------------#

app.layout= dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    dcc.Store(id='login-status', storage_type='session'),
    html.Div(id='user-status-div',),
    html.Div(id='page-content',),
],fluid = True)



@app.callback(Output('user-status-div', 'children'), Output('login-status', 'data'), [Input('url', 'pathname')])
def login_status(url):
    ''' callback to display login/logout link in the header '''
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated \
            and url != '/logout':  # If the URL is /logout, then the user is about to be logged out anyways
        return dcc.Link('logout', href='/dashboard'), current_user.get_id()
    else:
        return dcc.Link('', href='/login',style={'textAlign': 'center'}), 'loggedout'


index_page = dbc.Container([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

        dbc.Row([
            
                html.Div([

                            html.Img(
                                src='data:image/png;base64,{}'.format(encoded_image_ava.decode()),
                                height = "100%"
                            ),
                        ], style={'textAlign': 'center'}), 
                
        ], className="mb-4"),

        html.Br(),

        dbc.Row([
                html.Div([
                    html.H3("Welcome to AVA crypto, the easy-to-use dashboard that allows you to have a global view of yours cryptocurrencies ")
                    
                ],style={'textAlign': 'center'})
                

        ],className="mb-3"),

        dbc.Row([
                html.Div([
                    html.H4("The world of cryptocurrencies is waiting for you !")
                    
                ],style={'textAlign': 'center'})
        ],className="mb-3"),

        dbc.Row([
            dbc.Col([   
                dbc.Card([
                    dbc.NavLink('Click here to access the app !', href='/login',style={'textAlign': 'center'}) ,
                ], className="mb-2" ),
            ], width={'size':2, 'offset':5},),
        ], className="mb-5"),

        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

        html.Div([
        
            html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image_reseaux.decode()),
                    height = "100%"
                )],style={'textAlign': 'center'})   
                        
                

],fluid = True)

# --------------------------------------------- PAGE LOGIN ------------------------------------------------ >

login = dbc.Container([

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    dbc.Row([
        html.Div([

            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image_ava.decode()),
                height = "100%"
            ),
        ], style={'textAlign': 'center'}),   
    ], className="mb-4"),

            html.Br(),
            dcc.Location(id='url_login', refresh=True),
            html.Br(),
    dbc.Row(
        html.Div([
                html.H3("Please log in to continue :", id='h1')
                
        ],style={'textAlign': 'center'})
    ),
           
    html.Br(),
    
    dbc.Row([
        html.Div([
            dbc.Col([
                dbc.Input(placeholder='Enter your username',
                     type='text', id='uname-box', className="form-floating"),
                html.Br(),
                dbc.Input(placeholder='Enter your password',
                    type='password', id='pwd-box', className="form-floating"),
            ],  width={'size':4, "offset":4}),
        ],style={'textAlign': 'center'})
        
    ], className="ml-3 mx-1 mb-3"),

    dbc.Row([
        html.Div([
             html.Button(children='Login', n_clicks=0,
                    type='submit', id='login-button', className="btn btn-light", style={'textAlign': 'center'}),
        ], style={'textAlign': 'center'})
    ], className ="mb-3"),
       
    dbc.Row([
         html.Div(children='', id='output-state'),
    ]),    
   
    html.Br(),
    html.Br(),
    html.Br(),


    dbc.Row([
        
        dbc.Col([
            dbc.Card([
                dbc.NavLink('Register', href='/inscription', style={'textAlign': 'center'})
            ],  className="mb-2" )
        ], width={'size':2, "offset":4},),

        dbc.Col([
            dbc.Card([
                dbc.NavLink('Home Page', href='/',style={'textAlign': 'center'})
            ],  className="mb-2" )
        ],width={'size':2},),
    ]),

            

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
    
        html.Img(
                src='data:image/png;base64,{}'.format(encoded_image_reseaux.decode()),
                height = "100%"
            )],style={'textAlign': 'center'})   
],fluid = True)
            

@app.callback(Output('url_login', 'pathname'), Output('output-state', 'children'), [Input('login-button', 'n_clicks')], [State('uname-box', 'value'), State('pwd-box', 'value')])
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        portofolios , username_db , password_db =portefolio_by_user(username, password)
        if username == username_db and password == password_db:
            dash.callback_context.response.set_cookie('mycookie', username)
            dash.callback_context.response.set_cookie('mycookie_2', password)
            return '/dashboard', ''
        else:
            return '/login', 'Incorrect username or password'
        
# @app.callback(Output('output', 'children'), [Input('url_login', 'pathname')])
# def update_output(value):
#     dash.callback_context.response.set_cookie('mycookie', value)
#     print(value + ' - output')
#     return value + ' - output'

inscription = html.Div([

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    dbc.Row([
        html.Div([

            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image_ava.decode()),
                height = "100%"
            ),
        ], style={'textAlign': 'center'}),   
    ], className="mb-4"),


    dcc.Location(id='url_inscription', refresh=True),

    dbc.Row(
        html.Div([
                html.H3("Register:", id='h1')
                
        ],style={'textAlign': 'center'})
    ),
           
    html.Br(),

    dbc.Row([
        html.Div([
            dbc.Col([
                dbc.Input(placeholder='Enter a new username',
                            type='text', id='uname-box-2',className="form-floating"),
                
                html.Br(),

                dbc.Input(placeholder='Enter a new password',
                            type='password', id='pwd-box-2', className="form-floating"),
                
                html.Br(),

                dbc.Input(placeholder='Confirm password',
                            type="Password", id='pwd-box-3', className="form-floating"),
            ],  width={'size':4, "offset":4}),
        ],style={'textAlign': 'center'})
        
    ], className="ml-3 mx-1 mb-3"),
                
    dbc.Row([
        html.Div([
             html.Button(children='Register', n_clicks=0,
                              type='submit', id='login-button-2', className="btn btn-light", style={'textAlign': 'center'}),
        ], style={'textAlign': 'center'})
    ], className ="mb-3"),             
                 
    dbc.Row([
         html.Div(children='', id='output-state-2'),
    ]),    

    
    dbc.Row([
        
        dbc.Col([
            dbc.Card([
                dbc.NavLink('Login', href='/login', style={'textAlign': 'center'})
            ],  className="mb-2" )
        ], width={'size':2, "offset":4},),

        dbc.Col([
            dbc.Card([
                dbc.NavLink('Home Page', href='/',style={'textAlign': 'center'})
            ],  className="mb-2" )
        ],width={'size':2},),
    ]),    

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
    
        html.Img(
                src='data:image/png;base64,{}'.format(encoded_image_reseaux.decode()),
                height = "100%"
            )
    ],style={'textAlign': 'center'})   
])

@app.callback(Output('url_inscription', 'pathname'),Output('output-state-2', 'children'), Input('login-button-2', 'n_clicks'),[State('uname-box-2', 'value'), State('pwd-box-2', 'value'),State('pwd-box-3', 'value')])
def inscription_button_click(n_clicks, username, password, Password):
    if n_clicks > 0:
        if username is None or password is None and Password is None:
                return '/inscription', 'Please fill in the information above'
            
        elif password != Password:
            return '/inscription', 'password and password confirmation are not the same'
        
        elif username is not None and password is not None and Password is not None:
            create_user(username, password)
            dash.callback_context.response.set_cookie('mycookie', username)
            dash.callback_context.response.set_cookie('mycookie_2', password)
            return '/dashboard' , ''
        
    
@app.callback(Output('page-content', 'children'), Output('redirect', 'pathname'),[Input('url', 'pathname')])
def display_page(pathname):
# ''' callback to determine layout to return '''
    # Nous devons déterminer deux choses à chaque fois que l'utilisateur navigue :
    # Peut-il accéder à cette page ? Si oui, nous retournons simplement la vue
    # Sinon, s'il doit d'abord être authentifié, nous devons le rediriger vers la page de connexion.
    # Nous avons donc deux sorties, la première est la vue que nous allons retourner.
    # La deuxième est une redirection vers une autre page si c'est nécessaire.
    # Nous configurons les valeurs par défaut au début, avec redirect to dash.no_update ; ce qui signifie simplement qu'il faut garder l'url demandée.
    view = None
    url = dash.no_update
    if pathname == '/login':
        view = login
    elif pathname == '/dashboard':
        view = page_2()
    elif pathname =='/inscription':
        view = inscription
    else:
        view = index_page
    return view, url  

# ------- DATA INITILISATION --------------------------------------------------------

# username,password = test()
# portofolios , username_db , password_db = portefolio_by_user("victor.bonnaf@gmail.com", "victor")  
# compte = 1

# default_transaction=transaction(portofolios[compte][0], portofolios[compte][1])

# wallet,total=wallet(portofolios[compte][0], portofolios[compte][1])
# default_name=wallet['Name'].head(1)

# wallet_history = wallet_history(portofolios[compte][0], portofolios[compte][1])
# history = px.line(wallet_history, x='Date', y='Holdings (en USD)')

compte = 0

def cookie ():
    allcookies=dict(flask.request.cookies)
    if 'mycookie' in allcookies:
        email=allcookies['mycookie']
        password=allcookies['mycookie_2']
        return(email, password)

 #-------------- Second page --------------#
def page_2():
    portofolios , username_db , password_db = portefolio_by_user(cookie()[0], cookie()[1])
    if portofolios == []: 
        wallet_2,total=wallet("0xc0698d8f7e43805299c580eee33b56a0ab5b4b36", 56) 
        titre = "You are currently on an example wallet" 
    else:
        wallet_2,total=wallet(portofolios[compte][0], portofolios[compte][1]) 
        titre = "Hello, " + cookie()[0]
    default_name= wallet_2['Name'].head(1)    
    page_2_layout = dbc.Container([    #dbc.Container mieux que html.div pour bootstrap

        #-------------- HEADER --------------#
        dcc.Store(id="store_current_address"),
        dcc.Store(id="store_current_blockchain"),
        dcc.Store(id="store_wallet_all"),

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
                        html.H4(titre, className='modal-title ')
                    ],className="py-1 "),  
                ]), #parametre du text w/ bootstrap   df. bootstrap cheatsheet  
            ], className="card border-success ", width={'size':9, 'offset':1}),
            
            dbc.Col([
                dcc.Location(id='url_log', refresh=True),
                html.Button([
                    html.Img(
                        src='data:image/png;base64,{}'.format(encoded_image_button.decode()),
                        height = "50px",
                        
                    ),
                    
                ],n_clicks=0,type='submit', id='logout_img', className='btn btn-secondary'),
            ],width=1),  
        ], className="m-2"),  

        #-------------- BODY --------------#

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
                                        for x in sorted(wallet_2['Name'].unique())] #choisis les valeurs selon la colonne Name : .unique() prends que les valeurs 1 fois sans duplicats
                            ),
                    ]),

                    dbc.CardBody(html.Div(id='details_output'))
                
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

        dcc.Store (id="wallet_list", data=[]),

        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Card([ 
                        dbc.CardHeader("Your Address :"),
                        dbc.CardBody([
                            dcc.Location(id="url_wallet"),
                            dbc.Nav(id='list_wallet', children = [], vertical=True),])
                        ]) 
                
                ],className="mb-3"),

                dbc.Row([
                    html.Button("Add a wallet + ", id="open", className="btn btn-secondary"),
                ]),

                dbc.Modal([
                    dbc.ModalHeader("Add another wallet"),
                    dbc.ModalBody(
                        dbc.Form(
                            [
                                dbc.CardGroup(
                                    [
                                        html.H5("Network", className="mr-2 mb-3"),
                                        dcc.Dropdown(id='dropdown_blockchain', 
                                            multi=False, #peut choisir plusieurs valeurs
                                            value="ethereum - 1",
                                            options=["Ethereum - 1"," Binance Smart Chain - 56", "Matic Testnet Mumbai - 8001", "RSK Testnet - 31", "Moonbeam Moonbase Alpha - 1287", "Fantom Opera - 250"],
                                            placeholder="Select the blockchain",
                                            style={"width": "550px", "color" :"black"},
                                            className="mt-3 mb-3 "
                                        ),
                                    ],className="mr-3 mb-3" ),
                                dbc.CardGroup(
                                    [
                                        html.H5("Address", className="mr-2 mb-1"),
                                        dbc.Input(type="text", placeholder="Enter your address", id="text_address"),
                                    ], className="mr-3 mb-3"),

                                dbc.Button("Enter", className=" btn btn-primary text-center", id="enter", n_clicks=0),
                            ],
                            # inline=True,
                        )),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="btn btn-secondary ml-auto")
                    ),

                ],
                    id="modal",
                    is_open=False,    # True, False
                    size="xl",        # "sm", "lg", "xl"
                    backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                    scrollable=True,  # False or True if modal has a lot of text
                    # centered=True,    # True, False
                    fade=True         # True, False
                ),
        


            ],width=2), 

            dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Button('Global View' , id='url_details', n_clicks=0 , style={"background-color":"transparent"}, className="btn btn-outline-light mb-3"),
                    html.Button('Transactions' ,id='transac', n_clicks=0,style={"background-color":"transparent"}, className="btn btn-outline-light mb-3"),
                    html.Br(),
                    html.Div(id='container-button-timestamp')   
                    
                ]),

                dbc.CardBody(id="page-content-details", children="")

            ])
        ], width = 10),
    ]),

#-------------- FOOTER --------------#    
    ],fluid = True) #permet d'étirer à la largeur de la page web    
    return(page_2_layout)


# ------- CALLBACK -------------------------------------------------------

#-------------- Add wallet Callback --------------# 
@app.callback(Output('url_log', 'pathname'), Input('logout_img', 'n_clicks'))
def logout_button_clickk(n_clicks):
    if n_clicks > 0:
        return '/login' 

@app.callback([Output("list_wallet","children"),Output("wallet_list","data")],[Input("dropdown_blockchain","value"), Input("text_address","value"), Input("enter","n_clicks") ])
def update_liste_wallet(value1, value2, n_clicks):
    portofolios , username_db , password_db = portefolio_by_user(cookie()[0], cookie()[1])
    store = "{}-{}".format(value2, value1)     
    if n_clicks > 0:
        add_wallet(username_db, store.split("-")[0], int(store.split("-")[2]))
    return()

@app.callback(Output("modal", "is_open"),[Input("open", "n_clicks"), Input("close", "n_clicks")],[State("modal", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2 :
        return not is_open
    return is_open

# Stock variable
@app.callback(Output("store_wallet_all", "data"),[Input("dropdown_blockchain","value"), Input("text_address","value") ])
def update_store_wallet_all(value_drop, value_text) :
    return value_drop, value_text

@app.callback(Output ("store_current_blockchain", "data"),[Input("dropdown_blockchain","value")])
def update_adress(value) :
    number_chain = value.rpartition('-')[2]
    return int(number_chain)

@app.callback(Output ("store_current_address", "data"),[Input("text_address","value")])
def update_adress(value) :
    return value
    
# Variable ds fct
@app.callback(Output("current_address", "children"),Input("store_current_address", "data"))
def update_current_wallet (data):
    return '{}'.format(data)

# Ajoute Wallet
@app.callback(Output("add_wallet", "children"),Input("enter", "n_clicks"))
def upade_add_block_wallet(n) :
    if n :
        return [
            html.Button([
                        html.P(id="wallet_n")
            ], className='btn btn-secondary mb-3'),
        ]

@app.callback(Output("wallet_n", "children"),Input("store_wallet_all", "data"))
def update_add_wallet(n):
    return "{} , {}".format(n[1],n[0])
    

# Balance : details_crypto
@app.callback(Output("details_output", "children"),Input('dropdown_details', 'value'))
def update_output_details(value_slctd):
    portofolios , username_db , password_db = portefolio_by_user(cookie()[0], cookie()[1])
    if portofolios == []: 
        wallet_2,total=wallet("0xc0698d8f7e43805299c580eee33b56a0ab5b4b36", 56) 
    else:
        wallet_2,total=wallet(portofolios[compte][0], portofolios[compte][1])
    dff = wallet_2[wallet_2['Name']==value_slctd]
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
@app.callback(Output("temps_reel_output","children"),Input("dropdown_temps_reel","value"))
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

 #-------------- NavBar Callback --------------#    
@app.callback(Output('container-button-timestamp', "children"),Input('url_details','n_clicks'), Input('transac','n_clicks') )
def displayClick(btn1,btn2):
    portofolios , username_db , password_db = portefolio_by_user(cookie()[0], cookie()[1])
    if portofolios == []: 
        wallet_2,total=wallet("0xc0698d8f7e43805299c580eee33b56a0ab5b4b36", 56) 
        default_transaction=transaction("0xc0698d8f7e43805299c580eee33b56a0ab5b4b36", 56) 
        wallet_history_2 = wallet_history("0xc0698d8f7e43805299c580eee33b56a0ab5b4b36", 56)
    else:
        wallet_2,total=wallet(portofolios[compte][0], portofolios[compte][1])
        default_transaction=transaction(portofolios[compte][0], portofolios[compte][1])
        wallet_history_2 = wallet_history(portofolios[compte][0], portofolios[compte][1]) 
    default_name=wallet_2['Name'].head(1)
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'url_details' in changed_id:
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
                                            for x in sorted(wallet_2['Name'].unique())],
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
                                dcc.Graph(figure=px.line(wallet_history_2, x='Date', y='Holdings (en USD)'))      
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
                                    for x in sorted(wallet_2['Name'].unique())],
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

    elif 'transac' in changed_id:

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
                                style_table={'overflowY': 'auto','height': 400, 'width':'auto'},
                                style_cell={
                                    'height': 'auto',
                                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                                    'whiteSpace': 'normal'
                                },
                                style_header={
                                    'textAlign':'center',
                                    'backgroundColor': 'hex(F8F8F8)',
                                    'border': '1px solid pink' ,
                                    'fontWeight': 'bold',
                                    'color':'black'
                                },
                                style_data={
                                    'width': '125px', 'minWidth': '125px', 'maxWidth': '125px',
                                    # 'border': '1px solid blue' ,
                                    'textAlign':'center',
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
    
    else :
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
                                            for x in sorted(wallet_2['Name'].unique())],
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
                                dcc.Graph(figure=px.line(wallet_history_2, x='Date', y='Holdings (en USD)'))      
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
                                    for x in sorted(wallet_2['Name'].unique())],
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
        

@app.callback(Output('donut', 'figure'),Input('dropdown_donut', 'value'))
def update_graph(value_slctd):
    portofolios , username_db , password_db = portefolio_by_user(cookie()[0], cookie()[1])
    if portofolios == []: 
            wallet_2,total=wallet("0xc0698d8f7e43805299c580eee33b56a0ab5b4b36", 56) 
    else:
        wallet_2,total=wallet(portofolios[compte][0], portofolios[compte][1])
    wallet_slctd = wallet_2[wallet_2['Name'].isin(value_slctd)]
    figln2 = px.pie(wallet_slctd, names='Name', values='Balance', color='Name', hover_name='Name', hole=.4)
    return figln2


# Barchart - Balance - Crypto
@app.callback(Output('bar_chart', 'figure'),Input('checklist_bar', 'value'))
def update_graph(value_slctd):
    portofolios , username_db , password_db = portefolio_by_user(cookie()[0], cookie()[1])
    if portofolios == []: 
        wallet_2,total=wallet("0xc0698d8f7e43805299c580eee33b56a0ab5b4b36", 56) 
    else:
        wallet_2,total=wallet(portofolios[compte][0], portofolios[compte][1])
    wallet_slctd = wallet_2[wallet_2['Name'].isin(value_slctd)]
    fighist = px.histogram(wallet_slctd, x='Name', y='Balance', color="Name",  hover_name='Name')
    return fighist
    
# ----------------------------- RUN APP ------------------------------------------------ >

def launch_app():
    return app.run_server(debug=False) 


# if __name__=='__main__':
#     app.run_server(debug=True)   



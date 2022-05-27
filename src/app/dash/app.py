# -----------------------------------IMPORT --------------------------------- >

from tracemalloc import stop
import dash

from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import plotly.graph_objs as go
from dash import Dash, dash_table
import dash_core_components as dcc
import flask
from flask_login import LoginManager,UserMixin, current_user
import os

# -------------------- LIAISON AVEC LES FEATURES -------------------------------- >

from src.app.feature_wallet.wallet import wallet
from src.app.feature_history.wallet_history import wallet_history
from src.app.feature_price.price import price
from src.app.feature_transaction.transaction import transaction

# ------------------------ INITIALISATION DATA ------------------------------------- >

default_transactionn=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1)


adress_curent = "0xCBD6832Ebc203e49E2B771897067fce3c58575ac"
blockchain = 1
wallet,total=wallet(adress_curent, blockchain)
default_name=wallet['Name'].head(1)

wallet_history = wallet_history(adress_curent, blockchain)
history = px.line(wallet_history, x='Date', y='Holdings (en USD)')



# ----------------------------- AJOUT IMAGES ------------------------------------- >


image_ava_filename = 'src/app/dash/ressources/AVA_logo.png'
encoded_image_ava = base64.b64encode(open(image_ava_filename, 'rb').read()) 

image_plus_filename = 'src/app/dash/ressources/plus.png'
encoded_image_plus = base64.b64encode(open(image_plus_filename, 'rb').read()) 

image_moins_filename = 'src/app/dash/ressources/minus.png'
encoded_image_moins = base64.b64encode(open(image_moins_filename, 'rb').read()) 


button_filename = 'src/app/dash/ressources/AVA_button.png'
encoded_image_button = base64.b64encode(open(button_filename, 'rb').read())

bitcoin_filename= 'src/app/dash/ressources/RESEAUXSOCIAUX.png'
encoded_image_bitcoin = base64.b64encode(open(bitcoin_filename, 'rb').read())



# ------------------------------- APP FLASK ------------------------------------- >

# app=dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ],  #dbc.themes.ZEPHIR
#             meta_tags=[{'name': 'viewport',       # permet à l'app d'être responsive pour téléphone  
#                      'content': 'width=device-width, initial-scale=1.0'}]
                     
#             )


#On expose le serveur Flask pour permettre de le configurer pour l'ouverture de session


server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server,
                title='AVA CRYPTO',
                update_title='Loading...',
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.QUARTZ],  #dbc.themes.ZEPHIR
                meta_tags=[{'name': 'viewport',       # permet à l'app d'être responsive pour téléphone  
                     'content': 'width=device-width, initial-scale=1.0'}])


# Mise à jour de la configuration du serveur Flask avec la clé secrète pour chiffrer le cookie de session de l'utilisateur.

app.secret_key=SECRET_KEY=os.getenv('SECRET_KEY')

# --------------------------- LAYOUT ----------------------------------------- >

app.layout= dbc.Container([#dbc.Container mieux que html.div pour bootstrap
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    dcc.Store(id='login-status', storage_type='session'),
    html.Div(id='user-status-div',style={'textAlign': 'right'}),
    html.Div(id='page-content',style={'textAlign': 'right'}),
],fluid = True)



@app.callback(Output('user-status-div', 'children'), Output('login-status', 'data'), [Input('url', 'pathname')])
def login_status(url):
    ''' callback to display login/logout link in the header '''
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated \
            and url != '/logout':  # If the URL is /logout, then the user is about to be logged out anyways
        return dcc.Link('logout', href='/page-2'), current_user.get_id()
    else:
        return dcc.Link('', href='/login',style={'textAlign': 'center'}), 'loggedout'



# --------------------------- PREMIERE PAGE  ----------------------------------------- >

index_page = html.Div([
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
                    
            ]),
            html.Br(),
            dbc.Row([
     
                    
                    html.Div([
                        html.Header("Bienvenue sur AVACRYPTO, Votre dashboard facile d'utilisation pour avoir une vue globale de vos cryptomonnaies")
                        
                    ],style={'textAlign': 'center'})
                    
      
            ]),
            html.Br(),
            dbc.Row([
     
                    
                    html.Div([
                        html.H3("Le monde de la cryptomonnaie n'attend plus que vous !")
                        
                    ],style={'textAlign': 'center'})
                    
      
            ]),
            html.Br(),
            html.Div([
            
            dcc.Link('Accéder à l\'application', href='/login')],style={'textAlign': 'center'}) ,

            html.Br(),
            html.Br(),
            html.Br(),
            
            
            html.Div([
            
                html.Img(
                        src='data:image/png;base64,{}'.format(encoded_image_bitcoin.decode()),
                        height = "100%"
                    )],style={'textAlign': 'center'})   
                            
                
            ])




# --------------------------- DEUXIEME PAGE ----------------------------------------- >

page_2_layout = html.Div([
        
                
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
                    dcc.Location(id='url_log', refresh=True),
                    html.Button([
                        html.Img(
                            src='data:image/png;base64,{}'.format(encoded_image_button.decode()),
                            height = "50px",
                            
                        ),
                        
                    ],n_clicks=0,type='submit', id='logout_img', className='btn btn-secondary'),
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
                            dcc.Graph(figure=history)
                            
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
                                    data=default_transactionn.to_dict('records'),
                                    columns=[{'id': c, 'name': c} for c in default_transactionn.columns],
                                    page_action='none',
                                    style_table={'overflowY': 'auto','height': 400},
                                    style_cell={
                                        'height': 'auto',
                                        #all three widths are needed
                                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                                        'whiteSpace': 'normal'
                                    },
                                    style_header={
                                        'backgroundColor': 'rgb(30, 30, 30)',
                                        'border': '1px solid pink' ,
                                        'fontWeight': 'bold'
                                    },
                                    style_data={
                                        'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                                        'border': '1px solid blue' ,
                                        #'textOverflow': 'ellipsis',
                                        'backgroundColor': 'rgb(50, 50, 50)',
                                        'color': 'white'
                                    },
                                    
                                    fixed_rows={'headers': True},
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
        
        ])


@app.callback(Output('url_log', 'pathname'), 
              Input('logout_img', 'n_clicks'))

def logout_button_clickk(n_clicks):
    if n_clicks > 0:
        return '/login' 



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

def update_output_temps_reel(value_slctd):
    price_tps = price(value_slctd)
    return "Price : {}".format(price_tps[0])

#temps_reel_couleur   
@app.callback(
    Output("temps_reel_couleur","children"),
    Input("dropdown_temps_reel","value")
)

def update_output_temps_couleurs(value_slctd):
    price_tps = price(value_slctd)
    return "Price : {}".format(price_tps[0])







# ------------LOGIN MANAGER de connexion sera utilisé pour connecter et déconnecter les utilisateurs --------------- >

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Modèle de données de l'utilisateur. Il doit comporter au moins self.id.

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    ''' Cette fonction charge l'utilisateur par son identifiant. Typiquement, cela permet de rechercher l'utilisateur dans une base de données d'utilisateurs.
        Nous n'allons pas enregistrer ou rechercher des utilisateurs dans cet exemple, puisque nous allons simplement nous connecter en utilisant le serveur LDAP.
        Nous allons donc simplement retourner un objet User avec le nom d'utilisateur passé.
    '''
    return User(username)

# --------------------------------------------- PAGE LOGIN ------------------------------------------------ >

login = html.Div([
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Img(src='data:image/png;base64,{}'.format(encoded_image_ava.decode()),height = "100%"), 
                  html.Br(),
                  dcc.Location(id='url_login', refresh=True),
                  html.Br(),
                  html.H2('''Please log in to continue:''', id='h1'),
                  html.Br(),
                  dcc.Input(placeholder='Enter your username',
                            type='text', id='uname-box'),
                  dcc.Input(placeholder='Enter your password',
                            type='password', id='pwd-box'),
                  html.Button(children='Login', n_clicks=0,
                              type='submit', id='login-button'),
                  html.Div(children='', id='output-state'),
                  html.Br(),
                  dcc.Link('Register', href='/inscription'),
                  html.Br(),
                  html.Br(),
                  dcc.Link('Home Page', href='/'),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Div([
                  html.Img(
                        src='data:image/png;base64,{}'.format(encoded_image_bitcoin.decode()),
                        height = "100%"
                    )])  
                  ],style={'textAlign': 'center'})
                

@app.callback(
    Output('url_login', 'pathname'), Output('output-state', 'children'), [Input('login-button', 'n_clicks')], [State('uname-box', 'value'), State('pwd-box', 'value')])
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        if username == 'test' and password == 'test':
            return '/page-2', ''
        else:
            return '/login', 'Incorrect username or password'
        
    

inscription = html.Div([
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Img(src='data:image/png;base64,{}'.format(encoded_image_ava.decode()),height = "100%"), 
                  html.Br(),
                  dcc.Location(id='url_inscription', refresh=True),
                  html.Br(),
                  html.H2('''Register:''', id='h1'),
                  html.Br(),
                  dcc.Input(placeholder='Enter a new username',
                            type='text', id='uname-box-2'),
                  html.Br(),
                  dcc.Input(placeholder='Enter a new password',
                            type='password', id='pwd-box-2'),
                  html.Br(),
                  dcc.Input(placeholder='Confirm password',
                            type="Password", id='pwd-box-3'),
                  html.Br(),
                  html.Button(children='Register', n_clicks=0,
                              type='submit', id='login-button-2'),
                  html.Div(children='', id='output-state-2'),
                  html.Br(),
                  dcc.Link('Login', href='/login'),
                  html.Br(),
                  html.Br(),
                  dcc.Link('Home Page', href='/'),
                  html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Div([
                  html.Img(
                        src='data:image/png;base64,{}'.format(encoded_image_bitcoin.decode()),
                        height = "100%"
                    )])  
                  ],style={'textAlign': 'center'})

@app.callback(Output('url_inscription', 'pathname'),Output('output-state-2', 'children'), Input('login-button-2', 'n_clicks'),[State('uname-box-2', 'value'), State('pwd-box-2', 'value'),State('pwd-box-3', 'value')])

def logout_button_clickk(n_clicks, username, password, Password):
    if n_clicks > 0:
        if username == 'test' and password == 'test':
                return '/inscription', 'Username or password is already used'
            
        elif password != Password:
            return '/inscription', 'password and password confirmation are not the same'
        
        else:
            return '/page-2' , ''
    
    
    
    
    
    
    
@app.callback(Output('page-content', 'children'), Output('redirect', 'pathname'),
              [Input('url', 'pathname')])
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
    elif pathname == '/page-2':
        view = page_2_layout
    elif pathname =='/inscription':
        view = inscription
    else:
        view = index_page
    return view, url    


    
# ----------------------------- RUN APP ------------------------------------------------ >

def launch_app():
    return app.run_server(debug=False)  
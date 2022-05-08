# -----IMPORT -----------------------------------------------------
from tracemalloc import stop
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import  dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
from src.app.feature_history import wallet_history
import matplotlib.pyplot as plt

# ------- INITIALISATION DATA --------------------------------------------------------
wallet=pd.read_csv("src/app/dash_Alice/ressources/wallet_ex.csv")    
wallet["Name"].fillna("Unknown", inplace=True)
#print (wallet)
default_name=wallet['Name'].head(3)

wallet_history

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ],    
            meta_tags=[{'name': 'viewport',       # permet à l'app d'être responsive pour téléphone  
                     'content': 'width=device-width, initial-scale=1.0'}]
                )

image_filename = 'src/app/dash_Alice/ressources/AVA_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())  

button_filename = 'src/app/dash_Alice/ressources/AVA_button.png'
encoded_image_button = base64.b64encode(open(button_filename, 'rb').read())
# ------- LAYOUT --------------------------------------------------------
app.layout= dbc.Container([    #dbc.Container mieux que html.div pour bootstrap

    dbc.Row([   #divise la page en 3 ligne : le titres / dropdown / derniers bar chart
        dbc.Col([  #divise les lignes en colonnes ici que le titre
            html.Div([

                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image.decode()),
                    height = "60px"
                ),
            ]), 
        ], width=1),
 
        dbc.Col([
            html.H1(" Hello, Name !",
                    className='modal-title'
            ), #parametre du text w/ bootstrap   df. bootstrap cheatsheet  
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
                    html.H4("Overall $0")
                ], className='card border-light mb-3 py-5 text-md-center'),
            ],style={"height": "18rem"}),

            dbc.Row([
                dbc.Card([
                    html.H4("Adress Current Wallet")
                ], className='card border-light mb-3 py-5 text-sm-center')
            ],style={"height": "18rem"}),
        ], width=2),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dcc.Dropdown(id='dropdown2', 
                        multi=True, #peut choisir plusieurs valeurs
                        value=default_name,
                        options=[{'label':x, 'value':x}
                                    for x in sorted(wallet['Name'].unique())],
                    )
                ]),

                dbc.CardBody([
                    dcc.Graph(id='line-fig2', figure={})
                ]),

            ], className='card border-light mb-3'),   
        ]),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([

                    dcc.Dropdown(id='dropdown',
                        multi=False, #peut choisir qu'une seule valeur
                        value="0Army.io", #valeur par defaut 
                        options=[{'label':x, 'value':x} 
                                    for x in sorted(wallet['Name'].unique())] #choisis les valeurs selon la colonne Name : .unique() prends que les valeurs 1 fois sans duplicats
                        ),
                ]),

                dbc.CardBody([
                    dcc.Graph(id="line-fig", figure={})
                ])

            ], className='card border-light mb-3'),  
        ]),
        

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    "Wallet History"
                ]),

                dbc.CardBody([
                    dcc.Graph(id="line-hist", figure={})
                    
                ]),
            ],style={"height": "95%"}, className='card border-light mb-3')
        ])
    ],   ),#justify : gère les espaces : start, center, end, between, around // pour que ça marche avoir des colonnes en "stock" ; justify='around'
    
        
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.Button([
                    html.H4("wallet 2")
                ], className='btn btn-secondary mb-3'),
            ], style={"height": "18rem"}),

            dbc.Row([
                html.Button([
                    html.H4("Add another wallet + ")
                ], className='btn btn-secondary mb-3')
            ], style={"height": "18rem"}),

            dbc.Row([
                dbc.Card([
                    html.H4("calendar ")
                ], className='card border-light py-5 text-sm-center '),
            ], style={"height": "18rem"}),
        ], width = 2),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Selectionner vos cryptomonnaies"), 

                    dcc.Checklist(id='checklist',
                        value=default_name,
                        options=[{'label':x, 'value':x}
                            for x in sorted(wallet['Name'].unique())],
                        labelClassName='text-success mx-1'  #espace entre les options
                    ),
                ]),

                dbc.CardBody([
                    dcc.Graph(id='hist', figure={}, style={"height": "95%"}),
                ]),
            ], className='card border-light mb-3', style={"height": "100%"}),
        ],),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    "Your transaction"
                ]),

                dbc.CardBody([
                    ".->. ........... 3$"
                    
                ]),
            ],style={"height": "100%"}, className='card border-light')
        ])
    ], ),  
    
    


],
                          
fluid = True, #permet d'étirer à la largeur de la page web
)

# width={'size':5, 'offset':0, 'order':2}, #offset decale de 2 colonnes à gauche
# no_gutters= False,  l'espace entre les 2 éléments / True = pas d'espace ; False = espace
# width={'size':5, 'order':1},), #premières 5 colonnes à partir de la gauche, order permet de choisir l'ordre des éléments dans la ligne
# ),
# ], className='card border-light mb-3', style={"margin" : "6px"} ),
            

# ------- CALLBACK -------------------------------------------------------

@app.callback(
    Output('line-fig', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(stock_slctd):
    dff = wallet[wallet['Name']==stock_slctd]
    figln = px.bar(dff, x='Name', y='Balance')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('dropdown2', 'value')
)
def update_graph(stock_slctd):
    wallet_slctd = wallet[wallet['Name'].isin(stock_slctd)]
    figln2 = px.pie(wallet_slctd, names='Name', values='Balance', color='Name', hover_name='Name', hole=.4)
    return figln2

@app.callback(
    Output('line-hist', 'figure'),
    Input('Graph', 'value')
)
def update_graph(stock_slctd):
    wallet_slctd = history.isin(stock_slctd)
    fighist1 = px.pie(wallet_slctd, names='Date', values='holding (en USD)', color='Name', hover_name='Name')
    return fighist1

# Histogram
@app.callback(
    Output('hist', 'figure'),
    Input('checklist', 'value')
)
def update_graph(stock_slctd):
    wallet_slctd = wallet[wallet['Name'].isin(stock_slctd)]
    fighist = px.histogram(wallet_slctd, x='Name', y='Balance', color="Name",  hover_name='Name')
    return fighist

# ------- RUN APP --------------------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True)  


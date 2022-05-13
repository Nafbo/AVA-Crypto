# -----IMPORT -----------------------------------------------------
from re import A
from tracemalloc import stop
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from matplotlib.text import OffsetFrom
import plotly.express as px
import pandas as pd
import base64
from src.app.feature_transaction.transaction import transaction
import matplotlib.pyplot as plt

#--------CSS------->
tabs_styles = {
    'height': '30px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'color':'black',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'color': 'black',
    'padding': '6px'
}


# ------- INITIALISATION DATA --------------------------------------------------------
wallet=pd.read_csv("src/app/dash_Alice/ressources/wallet_ex.csv")    
wallet["Name"].fillna("Unknown", inplace=True)
#print (wallet)
default_name=wallet['Name'].head(3)

#print(transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1))
default_transaction=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1).head(10)
#Type_transaction=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1)['Type']
#From_transaction=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1)['From']
#Name_transaction=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1)['Name']
#To_transaction=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1)['To']
#Successful_transaction=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1)['Successful']
#Date_transaction=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1)['Date']

#print(default_transaction)
#print(From_transaction)

#latransaction=transaction("0xdB24106BfAA506bEfb1806462332317d638B2d82", 1)


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
                    html.H4("Transactions"),
                ]),

                dbc.CardBody([
                    html.Div([
                        dash_table.DataTable(
                            data=default_transaction.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in default_transaction.columns],
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
    
])
    
    
                          
fluid = True, #permet d'étirer à la largeur de la page web


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

#def upgrade_card(children):
#  title = children['Trading View Graphique']
#  return title 


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


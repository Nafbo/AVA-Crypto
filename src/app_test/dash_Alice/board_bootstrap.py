# -----IMPORT -----------------------------------------------------
from tracemalloc import stop
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import  dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ------- INITIALISATION DATA --------------------------------------------------------
wallet=pd.read_csv("src/app_test/dash_Alice/ressources/wallet_ex.csv")    
wallet["Name"].fillna("Unknown", inplace=True)
#print (wallet)
default_name=wallet['Name'].head(3)

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA],    
            meta_tags=[{'name': 'viewport',       # permet à l'app d'être responsive pour téléphone et tt 
                     'content': 'width=device-width, initial-scale=1.0'}]
                )

                
# ------- LAYOUT --------------------------------------------------------
app.layout= dbc.Container([    #dbc.Container mieux que html.div pour bootstrap

     dbc.Row([   #divise la page en 3 ligne : le titres / dropdown / derniers bar chart
          dbc.Col(  #divise les lignes en colonnes ici que le titre
               html.H1("Bienvenue sur votre dashboard",
                className='text-center text-primary mb-4'), #parametre du text w/ bootstrap   df. bootstrap cheatsheet
                width=12  #wide = le texte prends les 12 colonnes de la pages (12 colonnes max= largeurs page w/ bootstrap)
          ),
     ], #className="bg-success"
     ),      


     dbc.Row([
          dbc.Col([
               dcc.Dropdown(id='dropdown',
               multi=False, #peut choisir qu'une seule valeur
               value="0Army.io", #valeur par defaut 
               options=[{'label':x, 'value':x} 
                         for x in sorted(wallet['Name'].unique())] #choisis les valeurs selon la colonne Name : .unique() prends que les valeurs 1 fois sans duplicats
               ),

               dcc.Graph(id="line-fig", figure={}),

          ],
          width={'size':5, 'order':1}, #premières 5 colonnes à partir de la gauche, order permet de choisir l'ordre des éléments dans la ligne
          ),

          dbc.Col([
               dcc.Dropdown(id='dropdown2', 
               multi=True, #peut choisir plusieurs valeurs
               value=default_name,
               options=[{'label':x, 'value':x}
                         for x in sorted(wallet['Name'].unique())],
               ),

               dcc.Graph(id='line-fig2', figure={})
          ],
          width={'size':5, 'offset':0, 'order':2}, #offset decale de 2 colonnes à gauche
          ),
     ], #no_gutters= False,  l'espace entre les 2 éléments / True = pas d'espace ; False = espace
     justify='around' #justify : gère les espaces : start, center, end, between, around // pour que ça marche avoir des colonnes en "stock"
     ),  


     dbc.Row([
          dbc.Col([
               html.P("Selectionner vos cryptomonnaies",
               style={"textdDecoration" : "underline"}),

          dcc.Checklist(id='checklist',
          value=default_name,
          options=[{'label':x, 'value':x}
                    for x in sorted(wallet['Name'].unique())],
          labelClassName='text-success mx-1'  #espace entre les options
          ),

          dcc.Graph(id='hist', figure={}),

          ],
          width={'size':5, 'offset':0},
          ),


     ], 
     justify='around',
     ),  

],
fluid = True, #permet d'étirer à la largeur de la page web
)

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
    figln2 = px.pie(wallet_slctd, names='Name', values='Balance', color='Name', hover_name='Name')
    return figln2


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


dbc.CardBody([
                    html.Div([
                        dash_table.DataTable(
                            data=default_transaction.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in default_transaction.columns],
                            page_size=10
                        ),
                        '''

                        dcc.Tabs(id="tabs-inline", value='tab-1', children=[
                            dcc.Tab(label='1', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Type', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='To', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Date', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Success', value='tab-5', style=tab_style, selected_style=tab_selected_style),
                        ], style=tabs_styles),
                        html.Div(id='tabs-content-inline-3')  
                        ]),
                        '''
                    ]),
                    #html.Div([
                    #    dcc.Tabs(id="tabs-inline2", value='tab-7', children=[
                    #        dcc.Tab(label='2', value='tab-7', style=tab_style, selected_style=tab_selected_style),
                    #        dcc.Tab(label='Type', value='tab-8', style=tab_style, selected_style=tab_selected_style),
                    #        dcc.Tab(label='From', value='tab-9', style=tab_style, selected_style=tab_selected_style),
                    #        dcc.Tab(label='To', value='tab-10', style=tab_style, selected_style=tab_selected_style),
                    #        dcc.Tab(label='Success', value='tab-11', style=tab_style, selected_style=tab_selected_style),
                    #    ], style=tabs_styles),
                    #    html.Div(id='tabs-content-inline-4')
                        
                    #]),
                    
                    #html.Div([
                    #    dcc.Tabs(id="tabs-inline3", value='tab-12', children=[
                    #        dcc.Tab(label='3', value='tab-12', style=tab_style, selected_style=tab_selected_style),
                    #        dcc.Tab(label='Type', value='tab-13', style=tab_style, selected_style=tab_selected_style),
                    #        dcc.Tab(label='From', value='tab-14', style=tab_style, selected_style=tab_selected_style),
                    #        dcc.Tab(label='To', value='tab-15', style=tab_style, selected_style=tab_selected_style),
                    #        dcc.Tab(label='Success', value='tab-16', style=tab_style, selected_style=tab_selected_style),
                    #    ], style=tabs_styles),
                    #    html.Div(id='tabs-content-inline-5')
                        
                    #])
                ]),
                
     



'''
@app.callback(Output('tabs-content-inline-3', 'children'),
              Input('tabs-inline', 'value'))
def render_content(tab):
    a=0
    for a in range(0,len(default_transaction)):
        a+1
        if tab == 'tab-1':    
            return Name_transaction[a]
        elif tab == 'tab-2':
            return Type_transaction[a]
        
        elif tab == 'tab-3':
            if Type_transaction[a]=='Receive':
                return From_transaction[a]
            else:
                return To_transaction[a]

        elif tab == 'tab-4':
            return Date_transaction[a]
        elif tab == 'tab-5':
            return Successful_transaction[a]
        
'''      
          
        
        
        



'''
@app.callback(Output('tabs-content-inline-3', 'children'),
              Input('tabs-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':    
        return Name_transaction[0]
    elif tab == 'tab-2':
        return Type_transaction[0]
    elif tab == 'tab-3':
        return From_transaction[0]
    elif tab == 'tab-4':
        return To_transaction[0]
    elif tab == 'tab-5':
        return Date_transaction[0]
    elif tab == 'tab-6':
        return Successful_transaction[0]
    
@app.callback(Output('tabs-content-inline-4', 'children'),
              Input('tabs-inline2', 'value'))
def render_content(tab):
    if tab == 'tab-7':    
        return Name_transaction[1]
    elif tab == 'tab-8':
        return Type_transaction[1]
    elif tab == 'tab-9':
        return From_transaction[1]
    elif tab == 'tab-10':
        return To_transaction[1]
    elif tab == 'tab-11':
        return Successful_transaction[1]
    
@app.callback(Output('tabs-content-inline-5', 'children'),
              Input('tabs-inline3', 'value'))
def render_content(tab):
    if tab == 'tab-12':    
        return Name_transaction[2]
    elif tab == 'tab-13':
        return Type_transaction[2]
    elif tab == 'tab-14':
        return From_transaction[2]
    elif tab == 'tab-15':
        return To_transaction[2]
    elif tab == 'tab-16':
        return Successful_transaction[2]
'''
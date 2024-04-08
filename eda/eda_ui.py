# %%
import seaborn as sns
import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt
import matplotlib as mpt
from matplotlib.font_manager import fontManager
fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
mpt.rc('font', family='Taipei Sans TC Beta')


import dash # 建立dash
import dash_table # 要轉成資料框必用
from dash.dependencies import Input, Output # 在callback時使用
import dash_core_components as dcc # 製作Dashboard上的功能
import dash_html_components as html # 製作Dashboard網頁
import plotly.graph_objs as go # 畫各種圖
from dash.dependencies import Input, Output


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional


def get_plot(file_name:Optional[str]='Demo .xlsx'):
    Demo = pd.read_excel(file_name)
    
    df3=pd.melt(pd.crosstab(Demo['選擇的Rich Menu'], Demo['時段'], dropna=False).reset_index().fillna(0), id_vars=["選擇的Rich Menu"],var_name='時段', value_name="Value")
    df3=pd.merge(df3,df3.groupby(['時段'])['Value'].apply(np.sum).to_frame("total_count").reset_index())
    df3['ratio'] = df3.Value/df3.total_count
    df3['ratio'].iloc[:6] =np.random.dirichlet(np.ones(6),size=1)[0]
    df3['ratio'].iloc[6:12] =np.random.dirichlet(np.ones(6),size=1)[0]
    df3['ratio'].iloc[12:18] =np.random.dirichlet(np.ones(6),size=1)[0]
    df3['ratio'].iloc[18:] =np.random.dirichlet(np.ones(6),size=1)[0]


    categories = ['料理時間','有無影片','步驟數',
                '隨機', '食材數','點擊數/收藏數','料理時間']
    layout = go.Layout(
        autosize=False,
        font_size=11,width=450,height=350,margin=dict(t=50,r=0, b=10,l=50))
    fig1 = go.Figure(layout=layout)

    temp = df3[df3.時段=='早上'].ratio.tolist()
    temp.append(df3[df3.時段=='早上'].ratio.tolist()[0])
    fig1.add_trace(go.Scatterpolar(
        r = temp,
        theta=categories,
        #fill='toself',
        name='早上'
    ))
    temp = df3[df3.時段=='中午'].ratio.tolist()
    temp.append(df3[df3.時段=='中午'].ratio.tolist()[0])
    fig1.add_trace(go.Scatterpolar(
        r=temp,
        theta=categories,
        #fill='toself',
        name='中午'
    ))
    temp = df3[df3.時段=='晚上'].ratio.tolist()
    temp.append(df3[df3.時段=='晚上'].ratio.tolist()[0])
    fig1.add_trace(go.Scatterpolar(
        r=temp,
        theta=categories,
        #fill='toself',
        name='晚上'
        
    ))

    temp = df3[df3.時段=='宵夜'].ratio.tolist()
    temp.append(df3[df3.時段=='宵夜'].ratio.tolist()[0])
    fig1.add_trace(go.Scatterpolar(
        r=temp,
        theta=categories,
        #fill='toself',
        name='宵夜'
    ))

    fig1.update_polars(bgcolor="#DBDBDB")
    fig1.update_layout(
    title_text="</b><br>Radar Chart", font_size=13,
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, max(df3.ratio)+0.05]
        )),
    showlegend=True
    )


    # %%
    df2=Demo.groupby(['訊息類型','時段']).agg({"時間":'count'}).reset_index()
    df2=pd.merge(df2,df2.groupby(['時段'])['時間'].apply(np.sum).to_frame("total_count").reset_index())
    df2['count'] = df2["時間"]/df2["total_count"]
    #https://plotly.com/python/sunburst-charts/#basic-sunburst-plot-with-plotlyexpress



    fig2 = px.sunburst(df2, path=['訊息類型','時段'], values='count').update_traces(hovertemplate = '%{label}<br>' + '次數: %{value}', textinfo = "label + percent entry",sort=True)
    fig2.update_layout(title_text="<b> </b><br>Pie Chart", font_size=11,width=450,height=350,margin=dict(t=50,r=0, b=10,l=0))
    fig2.show()
    #Support System



# %%

    alllist = [] 
    for i in ['選擇的Rich Menu','文字選單','按下一個按鈕次數','食譜來自網站']:
        
        alllist.extend(np.unique(Demo[i].tolist()).tolist())


# %%
#https://python.plainenglish.io/sankeying-with-plotly-90500b87d8cf
    groups = Demo.groupby(['選擇的Rich Menu','文字選單','按下一個按鈕次數','食譜來自網站']).agg({"時間":'count'}).reset_index()
    first_layer= groups.groupby(['選擇的Rich Menu','文字選單']).agg({"時間":'sum'}).rename({"時間":'count'}).reset_index()
    second_layer = groups.groupby(['文字選單','按下一個按鈕次數']).agg({"時間":'sum'}).rename({"時間":'count'}).reset_index()
    third_layer = groups.groupby(['按下一個按鈕次數','食譜來自網站']).agg({"時間":'sum'}).rename({"時間":'count'}).reset_index()

    list_=[first_layer,second_layer,third_layer]

    names = []
    count_dict = {} #will contain all info of value list
    source_list = [] #will contain all info of source
    target_list = [] #will contain all info of target


    for i in range(0, len(list_)): 
        cols =list_[i].columns # contains columns for our  
    for x,y,z in zip(list_[i][cols[0]],list_[i][cols[1]],list_[i][cols[2]]):#Iterates over x(source),y(target),z(counts)
            if(f'{x}_M{(i+1)}' not in names):
                names.append(f'{x}_M{(i+1)}')#appends in names
                
            count_dict[f'{x}_M{(i+1)}',f'{y}_M{(i+2)}'] = z
            source_list.append(f'{x}_M{(i+1)}')
            target_list.append(f'{y}_M{(i+2)}')


    #Now we add labels into name for the last month targets
    for v in target_list:
        if v not in names:
            names.append(v)
            

    #all_numerics contains the index for every label
    all_numerics = {}
    for i in range(0,len(names)):
        all_numerics[names[i]] = i




    color_dict_link = px.colors.sequential.tempo[:len(source_list)]
    color_name =[color_dict_link[int(x.split('M')[1])] for x in names]
    color_link=[color_dict_link[int(x.split('M')[1])] for x in target_list]




    fig3 = go.Figure(data=[go.Sankey(
        node = dict(
        thickness = 5,
        line = dict(color = None, width = 0.01),
        #Adding node colors,have to split to remove the added suffix
        color = color_name,
        label = [(x.split('_')[0]) for x in names],),
        link = dict(
        source = [all_numerics[x] for x in source_list],
        target = [all_numerics[x] for x in target_list],
        value = [count_dict[x,y] for x,y in zip(source_list,target_list)],
        
        #Adding link colors,have to split to remove the added suffix
        color =color_link
    ),)])



    #Adds 1st,2nd month on top,x_coordinate is 0 - 5 integers,column #name is specified by the list we passed
    for x_coordinate, column_name in enumerate(["1st layer","2nd layer","3rd layer","4th layer"]):
        fig3.add_annotation(
            x=x_coordinate,#Plotly recognizes 0-5 to be the x range.
            
            y=1.04,#y value above 1 means above all nodes
            xref="x",
            yref="paper",
            text=column_name,#Text
            showarrow=False,
            font=dict(
                family="Tahoma",
                size=10,
                color="black"
                ),
            align="left",
            )
    #Adding y labels is harder because you don't precisely know the #location of every node.
    #You could however add annotations using the labels option while defining the figure but you cannot change the color for each #annotation individually 


    #Recommend System
    fig3.update_layout(title={'text':"<b> </b><br>Sankey diagram"}, font_size=11,width=950,height=800, margin=dict(t=150,l=10,b=50,r=10)) #, margin=dict(t=210,l=90,b=20,r=30)
    #, margin=dict(t=100,l=10,b=10,r=15)
    fig3.show()

    # %%
    color_dict_link = px.colors.named_colorscales()[:51]

    # %%
    fig4 = px.box(Demo, x="按下一個按鈕次數", y="時段", color="訊息類型",category_orders={"時段": ["早上", "中午", "晚上", "宵夜"]})
    fig4.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig4.update_layout( font_size=11,width=500,height=450, margin=dict(t=150)) #, margin=dict(t=210,l=90,b=20,r=30)
    #title_text="<b>Recommend</b><br>Box Plot",  , margin=dict(t=150,l=10,b=50,r=15)
    fig4.show()

    # %%
    sns.color_palette("Set3", 50).as_hex()[-6:]

    # %%
    Demo2 = pd.read_excel('Demo .xlsx',sheet_name = "工作表2")
    df4=pd.melt(pd.crosstab(Demo2['種類'], Demo['時段'], dropna=False).reset_index().fillna(0), id_vars=["種類"],var_name='時段', value_name="Value")
    df4=pd.merge(df4,df4.groupby(['時段'])['Value'].apply(np.sum).to_frame("total_count").reset_index())
    df4['ratio'] = df4.Value/df4.total_count
    df4['ratio_name'] =round(df4['ratio'],2)
    colors=sns.color_palette("Set3", 20).as_hex()[-6:]
    fig5 = px.bar(df4, x="時段", y="ratio", color="種類", text="ratio_name", color_discrete_sequence=colors,category_orders={"時段": ["早上", "中午", "晚上", "宵夜"]},opacity =0.8,text_auto='.0%')
    fig5.update_layout(title_text="<b> </b><br>Stack Bar Chart", font_size=11,width=600,height=700) #, margin=dict(t=210,l=90,b=20,r=30)
    #Ingredient System
    #, margin=dict(t=150,l=10,b=50,r=15)
    fig5.show()

    # %%
    Demo3 = pd.read_excel('Demo .xlsx',sheet_name = "工作表3")
    fig6 = px.imshow(Demo3.iloc[:,1:].to_numpy(), text_auto=True, x=Demo3.columns.tolist()[1:], y=Demo3.columns.tolist()[1:],color_continuous_scale=px.colors.sequential.amp)
    fig6.update_layout(title_text="<b> </b><br>Heatmap", font_size=11,width=700,height=700) #, margin=dict(t=210,l=90,b=20,r=30)
    #, margin=dict(t=150,l=10,b=50,r=15)
    fig6.show()

    # %%
    Demo4 = pd.read_excel('Demo .xlsx',sheet_name = "工作表4")
    df4=pd.melt(pd.crosstab(Demo4['被排除的食物類型'], Demo4['時段'], dropna=False).reset_index().fillna(0), id_vars=["被排除的食物類型"],var_name='時段', value_name="Value")
    df4=pd.merge(df4,df4.groupby(['時段'])['Value'].apply(np.sum).to_frame("total_count").reset_index())
    df4['ratio'] = df4.Value/df4.total_count
    df4['ratio_name'] =round(df4['ratio'],2)
    colors=sns.color_palette("Set3", 20).as_hex()[-6:]
    fig7 = px.bar(df4, x="時段", y="ratio", color="被排除的食物類型", text="ratio_name", color_discrete_sequence=colors,category_orders={"時段": ["早上", "中午", "晚上", "宵夜"]},opacity =0.8,text_auto='.0%')
    fig7.update_layout(font_size=11,width=500,height=350, margin=dict(t=50)) #, margin=dict(t=210,l=90,b=20,r=30)

    #title_text="<b>Recommend System</b><br>Stack Bar Chart",  , margin=dict(t=150,l=10,b=50,r=15)
    fig7.show()

    return fig1,fig2,fig3,fig4,fig5,fig6,fig7



if __name__ == '__main__':
    fig1,fig2,fig3,fig4,fig5,fig6,fig7 = get_plot()

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options


    app.layout = html.Div([
        dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
            dcc.Tab(label='Recommend System', value='tab-1'),
            dcc.Tab(label='Support and Ingredient System', value='tab-2'),
        ]),
        html.Div(id='tabs-example-content-1')
    ])

    @app.callback(
        Output('tabs-example-content-1', 'children'),
        Input('tabs-example-1', 'value')
    )

    def render_content(tab):
        if tab == 'tab-1':
            # New Div for all elements in the new 'row' of the page
            return  html.Div([
                    html.H1(children='Recommend System', style={'font-weight': 'bold','font-size':40,'background-color': 'rgba(255, 255, 128, .35)','textAlign': 'center'}), #,'textAlign': 'center'
                    html.Div(children='''
                            宇宙食譜 - 霹靂卡霹靂咖咖波波莉娜貝貝魯多，宇宙解決你食ㄉ困擾! 
                        ''', style={'font-weight': 'bold','font-size':15,'textAlign': 'center'}),
                    ###  桑基圖  ###
                    html.Div([
                        dcc.Graph(
                            id='graph1',
                            figure=fig3
                        ),  
                    ], className='seven columns'),
                    html.Div([
                        #html.H1(children=' ', style={'font-size':40,'background-color': 'rgba(255, 255, 128, .5)'}),
                        ###  box plot   ###
                        html.Div([
                            dcc.Graph(
                                id='graph2',
                                figure=fig4
                            ),  
                        ], className='row'),
                        ###  stack bar chart    ###
                        html.Div([

                            dcc.Graph(
                                id='graph2',
                                figure=fig7
                            ),  
                        ], className='row'),
                        
                    ], className='three columns'),
                ], className='row')
            
            
        elif tab == 'tab-2':
            return html.Div([
                    html.Div([
                        
                        html.Div([
                        html.H1(children='Support System', style={'font-weight': 'bold','font-size':30,'background-color': 'rgba(255, 255, 128, .35)','textAlign': 'center'}),
                        ###  Radar graph  ###
                        html.Div([
                            # html.H1(children='宇宙食譜'),

                            dcc.Graph(
                                id='graph1',
                                figure=fig2
                            ),  
                        ], className='row'),
                        
                        
                        html.Div([
                        ###  pie chart   ###

                            dcc.Graph(
                                id='graph2',
                                figure=fig1
                            ),  
                            ], className='row'),
                        ], className='three columns'),
                        
                        
                        
                        
                        html.H1(children='Ingredient System', style={'font-weight': 'bold','font-size':30,'background-color': 'rgba(255, 255, 128, .35)','textAlign': 'center'}),
                        ###  Radar graph  ###
                        html.Div([
                            # html.H1(children='宇宙食譜'),

                            dcc.Graph(
                                id='graph1',
                                figure=fig5
                            ),  
                        ], className='four columns'),
                        html.Div([
                        ###  pie chart   ###

                            dcc.Graph(
                                id='graph2',
                                figure=fig6
                            ),  
                        ], className='five columns'),
                    ], className='row'),
                ])


    app.run_server(debug=True, use_reloader=False) 



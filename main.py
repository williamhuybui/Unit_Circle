import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.offline as pyo

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import warnings
warnings.filterwarnings("ignore")


# Creating data
theta_list = np.linspace(0,2*np.pi,40)
trig=pd.DataFrame({})

sin_line=lambda i: [[np.cos(i), np.cos(i)],[0,np.sin(i)]]
cos_line=lambda i: [(0,np.cos(i)),(0,0)]
tan_line=lambda i: [(1/np.cos(i),np.cos(i)),(0,np.sin(i))]
cotan_line=lambda i: [(np.cos(i),0),(np.sin(i),1/np.sin(i))]
secant_line=lambda i: [(0,1/np.cos(i)),(0,0)]
csc_line = lambda i:[(0,0),(0,1/np.sin(i))]
radius_line=lambda i:[(0,np.cos(i)), (0,(np.sin(i)))]

trig['x']=[np.cos(i) for i in theta_list]
trig['y']=[np.sin(i) for i in theta_list]
trig['sin']=[sin_line(i) for i in theta_list]
trig['cos']=[cos_line(i) for i in theta_list]
trig['tan']=[tan_line(i) for i in theta_list]
trig['cotan']=[cotan_line(i) for i in theta_list]
trig['secant']=[secant_line(i) for i in theta_list]
trig['csc']=[csc_line(i) for i in theta_list]
trig['radius']=[radius_line(i) for i in theta_list]
trig['theta']=theta_list

line_style= {'points': {'color':'black'},
            'sin': {'color':'red'},
            'cos': {'color':'#44b6e3'},
            'tan': {'color':'green'},
            'cotan': {'color':'blue'},
             'secant': {'color':'maroon', 'dash':'dash'},
             'csc': {'color':'#de14de'},
             'radius': {'color':'black'},
             'Circle': {'color':'rgba(0, 0, 0, 0.5)'},
            }

## Build AppViewer

# viewer = AppViewer()
# Build App
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
# server = app.server

app.layout=     html.Div([
                html.H1("Unit Circle",style={'textAlign':'center'}),
                html.Div(dcc.Graph(id='unit-circle'),style={'display':'inline-block', 'width':'48%', 'float':'left'}),
                html.Div(dcc.Slider(id='theta',min=0, max=2*np.pi, step=0.01, value=0,
                                    marks={0:{'label': '0 °C', 'style': {'color': 'blue'}},
                                          np.pi/6:{'label': 'π/6','style': {'color': 'red'}},
                                            np.pi/4:{'label': 'π/4','style': {'color': 'red'}},
                                           np.pi/3:{'label': 'π/3','style': {'color': 'red'}},
                                           np.pi/2:{'label': 'π/2','style': {'color': 'blue'}},
                                           np.pi:{'label':'π','style': {'color': 'blue'}},
                                           np.pi*1.5:{'label':'3π/2','style': {'color': 'blue'}},
                                           np.pi*2:{'label':'2π','style': {'color': 'blue'}}
                                          }
                                   ),
                         style={'display':'inline-block', 'width':'48%', 'float':'right','padding-top':'100px'}),
                html.Pre(id='trig-values',
                         style={'font-size':'20px', 'textAlign':'center','display':'inline-block', 'width':'48%', 'float':'right'})
                    ])


@app.callback(Output('unit-circle','figure'), [Input('theta','value')])
def unit_circle(theta):

    data=[go.Scatter(x=trig['x'], y=trig['y'],name='circle'), #Arc Circle
            go.Scatter(x=sin_line(theta)[0],y=sin_line(theta)[1],name='sin' ,mode="lines", line=line_style['sin']),
                go.Scatter(x=cos_line(theta)[0],y=cos_line(theta)[1],name='cos' ,mode="lines",line=line_style['cos']),
                go.Scatter(x=tan_line(theta)[0],y=tan_line(theta)[1],name='tan' ,mode="lines",line=line_style['tan']),
                go.Scatter(x=cotan_line(theta)[0],y=cotan_line(theta)[1],name='cotan' ,mode="lines",line=line_style['cotan']),
                go.Scatter(x=secant_line(theta)[0],y=secant_line(theta)[1],name='secant' ,mode="lines",line=line_style['secant']),
                go.Scatter(x=csc_line(theta)[0],y=csc_line(theta)[1],name='csc' ,mode="lines",line=line_style['csc']),
                go.Scatter(x=radius_line(theta)[0],y=radius_line(theta)[1],name='radius' ,mode="lines",line=line_style['radius'])
                ]

    layout=go.Layout(width=700, height=700, xaxis=dict(range=[-2,2]), yaxis=dict(range=[-2,2]))
    figure=go.Figure(data=data,layout=layout)
    return figure

@app.callback(Output('trig-values', 'children'), [Input('theta','value')])
def trig_values(theta):
    values=[np.sin(theta), np.cos(theta), np.tan(theta), 1/np.tan(theta), 1/np.cos(theta), 1/np.sin(theta), 1]
    values=[round(i,2) for i in values]


    df=pd.DataFrame({'values':values},index=['sin(θ)','cos(θ)','tan(θ)','cotan(θ)','sec(θ)','csc(θ)','radius'])
    df['θ (rad)']=round(theta,2)
    df['θ (deg)']=round(theta*180/np.pi,2)
    return str(df)

if __name__ == '__main__':
    app.run_server()

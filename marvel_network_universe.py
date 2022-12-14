# -*- coding: utf-8 -*-
"""marvel-network-universe.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aatUIznkXHCC-9iedquEILpN9Si_UaT_
"""

pip install python-igraph

pip install chart-studio

# Commented out IPython magic to ensure Python compatibility.
import chart_studio.plotly
import plotly.graph_objs as go
from chart_studio.plotly import plot, iplot
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import networkx as nx
# %matplotlib inline 
from IPython.display import display
from PIL import Image

e = pd.read_csv('./edges.csv') # Edges
h = pd.read_csv("./hero-network.csv") # Hero
n = pd.read_csv('./nodes.csv') # Nodes

h.info()

he = nx.from_pandas_edgelist(h, source = "hero1", target = "hero2")
nx.info(he)

#Degree Centrality 
MF = nx.degree_centrality(he)

counter = 0
for w in sorted(MF, key = MF.get , reverse = True):
    counter = counter + 1
    if counter == 10:
        break
    print(w,'{:0.2f}'.format(MF[w]))

#EigenVector
EV = nx.eigenvector_centrality(he)
counter = 0
for w in sorted(EV, key =EV.get,  reverse = True):
    counter = counter + 1
    if counter == 10:
        break
    print(w,"{:0.4f}".format(EV[w]))

`#Betweeness_Centrality
BC = nx.betweenness_centrality(he)
counter = 0
for w in sorted(BC, key =BC.get,  reverse = True):
    counter = counter + 1
    if counter == 10:
        break
    print(w,"{:0.4f}".format(BC[w]))

#h= h.iloc[np.r_[100:350, 500:800,1230:1900,2500:5600]]
h= h.iloc[:10000,:2]
he = nx.from_pandas_edgelist(h, source = "hero1", target = "hero2")
print(nx.info(he))

import igraph as ig

#Numbers of Nodes
N = he.number_of_nodes()

#List of Edge
L = he.number_of_edges()

#Graph objects
Edges_name = [e for e in he.edges()] #Edges Names

Edges= nx.convert_node_labels_to_integers(he) #Mapping all Nodes into Numbers
Edges = [e for e in Edges.edges()]

#Graph
G = ig.Graph(Edges, directed = False)

# Geolocalization
layt = G.layout('kk',dim = 3)  #3D Localization

#Given X,y,z Position
Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates

Xe=[]
Ye=[]
Ze=[]

#Grouping Coordinates
for e in Edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]
    
#Nodes Name 
labels = []
group = []

for i in range(len(Edges_name)):
    value = Edges_name[i][0]
    labels.append(value)
    
for i in range(len(Edges)):
    value = Edges[i][0]
    group.append(value)
    
group =[]
group.extend(np.repeat(1,2000))
group.extend(np.repeat(2,2000))
group.extend(np.repeat(3,3000))
group.extend(np.repeat(4,1000))
group.extend(np.repeat(5,2000))

trace1=go.Scatter3d(x=Xe,y=Ye,z=Ze,mode='lines',
                    line=dict(color='rgb(125,125,125)', width=1),hoverinfo='none')

trace2=go.Scatter3d(x=Xn,y=Yn,z=Zn,mode='markers',name='SuperHeroe',
                    marker=dict(symbol='circle',size=4,color=group,colorscale='Viridis',line=dict(color='rgb(50,50,50)', width=0.5)),
                    text=labels,hoverinfo='text')

axis=dict(showbackground=False,showline=False,zeroline=False,
          showgrid=False,showticklabels=False,title='')

layout = go.Layout(
         title="Network Of appaerance of Marvel<br> SuperHeroes (3D visualization)",
    autosize=True,
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ),
     margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text="",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],    )

data=[trace1, trace2]
fig=go.Figure(data=data, layout=layout)
fig.show()
#visualize the networkx DiGraph using a Dash dashboard

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import networkx as nx
import pygraphviz

G = nx.read_gpickle("Climate_Mind_DiGraph.gpickle")

pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
N = nx.nx_agraph.to_agraph(G)
N.edge_attr.update(splines="curved",directed=True)
N.layout(prog='dot')
s = N.string() #this string contains the coordinates for the edges so they aren't just straight lines but curve to avoid going through other nodes
N.write('edges_spline_layout_coordinates.txt') #this file also has the coordinates for the splines for the edges that curve around the nodes instead of going through the nodes

#add a pos attribute to each node
for node in G.nodes:
    G.nodes[node]['pos'] = list(pos[node])


#Create Edges
edge_trace = go.Scatter(
                        x=[],
                        y=[],
                        line=dict(width=0.5,color='#888'),
                        hoverinfo='none',
                        mode='lines')
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])


#Create Nodes
node_trace = go.Scatter(
                        x=[],
                        y=[],
                        text=[],
                        mode='markers',
                        hoverinfo='text',
                        marker=dict(
                                    showscale=True,
                                    colorscale='YlGnBu',
                                    reversescale=True,
                                    color=[],
                                    size=10,
                                    colorbar=dict(
                                                  thickness=15,
                                                  title='Node Connections',
                                                  xanchor='left',
                                                  titleside='right'
                                                  ),  
                                    line=dict(width=2)))
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])


#add color to node points
for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))
    node_trace['text']+=tuple([node_info])


################### START OF DASH APP ###################
app = dash.Dash()

# to add ability to use columns
app.css.append_css({
                   'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
                   })


#create the Dash visualization
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                                 title='<br>Climate Mind Ontology',
                                 titlefont=dict(size=16),
                                 showlegend=False,
                                 hovermode='closest',
                                 margin=dict(b=20,l=5,r=5,t=40),
                                 annotations=[ dict(
                                                    showarrow=True,
                                                    xref="paper", yref="paper",
                                                    x=0.005, y=-0.002 ) ],
                                 xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))


app.layout = html.Div([
                       html.Div(dcc.Graph(id='Graph',figure=fig)),
                       html.Div(className='row', children=[
                                                           html.Div([html.H2('Overall Data'),
                                                                     html.P('Num of nodes: ' + str(len(G.nodes))),
                                                                     html.P('Num of edges: ' + str(len(G.edges)))],
                                                                    className='three columns'),
                                                           html.Div([
                                                                     html.H2('Selected Data'),
                                                                     html.Div(id='selected-data'),
                                                                     ], className='six columns')
                                                           ])
                       ])


@app.callback(
              Output('selected-data', 'children'),
              [Input('Graph','selectedData')])
def display_selected_data(selectedData):
    num_of_nodes = len(selectedData['points'])
    text = [html.P('Num of nodes selected: ')]
    for x in selectedData['points']:
        material = int(x['text'].split('<br>')[0][10:])
        text.append(html.P(str(material)))
    return text


if __name__ == '__main__':
    app.run_server(debug=True)










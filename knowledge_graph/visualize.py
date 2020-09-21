# visualize the networkx DiGraph using a Dash dashboard
# General warning: Note that with this dashboard, the edge arrows drawn are infact symmetrical and angled correctly.
# And are all the same distance/size they just don't always look that way because the scaling of the x-axis
#   isn't the same scaling of the y-axis all the time (depending on how the user draws the box to zoom and the default aspect ratios).

# must run process_ontology_OWL_file.py before running visualize.py !


import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import networkx as nx
import pygraphviz
import math
import numpy as np

import io
import json

import matplotlib.pyplot as plt
from scipy.special import binom
import argparse


def Bernstein(n, k):
    """
    Bernstein polynomial.
    """
    coeff = binom(n, k)

    def _bpoly(x):
        return coeff * x ** k * (1 - x) ** (n - k)

    return _bpoly


def Bezier(points, num=200):
    """
    Build Bezier curve from points.
    """
    N = len(points)
    t = np.linspace(0, 1, num=num)
    curve = np.zeros((num, 2))
    for ii in range(N):
        curve += np.outer(Bernstein(N - 1, ii)(t), points[ii])
    return curve


def get_figure(
    N_node_details,
    N_edge_details,
    N,
    G,
    edge_type=None,
    node_class=None,
    node_property=None,
    extra_edge_type=None,
):
    the_nodes_to_display, the_edges_to_display = get_filtered_data(
        N_node_details, N_edge_details, N, G, edge_type
    )
    # blank figure object
    fig = go.Figure()

    # Add node traces as ovals to the figure object
    # Note how 72 is the conversion of graphviz point scale to inches scale
    for node in N_node_details:
        node_name = node.get("name")
        # Do not show the nodes not in the_nodes_to_display
        if node_name not in the_nodes_to_display:
            continue

        fillcolor = None
        textcolor = "black"
        line_color = "black"
        if node_class:
            node_class_list = eval(N.get_node(node_name).attr.get("all classes"))
            if node_class in node_class_list:
                fillcolor = "#aed9f6"
                textcolor = "#0D3BF6"

        if node.get("non_default_edge_type"):
            line_color = "orange"
            fillcolor = "orange"

        if node_property:
            if G.nodes.get(node_name).get("properties").get(node_property):
                line_color = "yellow"
                fillcolor = "yellow"

        fig.add_shape(
            type="circle",
            fillcolor=fillcolor,
            layer="below",
            line_color=line_color,
            x0=node.get("position").get("x") - 0.5 * node.get("width") * 72,
            y0=node.get("position").get("y") - 0.5 * node.get("height") * 72,
            x1=node.get("position").get("x") + 0.5 * node.get("width") * 72,
            y1=node.get("position").get("y") + 0.5 * node.get("height") * 72,
        )

        # add scatter trace of text labels to the figure object
        fig.add_trace(
            go.Scatter(
                x=[node.get("position").get("x")],
                y=[node.get("position").get("y")],
                # https://plotly.com/python/hover-text-and-formatting/#customizing-hover-text-with-a-hovertemplate
                hovertemplate=node.get("node_hovertext"),
                text=node_name,
                mode="text",
                textfont=dict(
                    color=textcolor,
                    size=8.5,
                    family="sans-serif",
                ),
            )
        )

    # adding edges (and arrows and tees to edges)
    for edge in N_edge_details:
        edge_position = edge.get("positions")

        # # Do not show the edges not in edges_to_display
        o_edge = N.get_edge(edge["node1"], edge["node2"])
        if o_edge not in the_edges_to_display:
            continue

        start = edge_position[0]
        end = edge_position[1]
        backwards = edge_position[2:][::-1]
        edge_fix = (
            [start] + backwards + [end]
        )  # graphviz has weird edge coordinate format that doesn't have coordinates in correct order
        # approximate the B spline curve
        # see the following websites to better understand:
        # http://graphviz.996277.n3.nabble.com/how-to-draw-b-spline-td1328.html
        # https://stackoverflow.com/questions/28279060/splines-with-python-using-control-knots-and-endpoints
        # https://stackoverflow.com/questions/53934876/how-to-draw-a-graphviz-spline-in-d3
        # https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-837-computer-graphics-fall-2012/lecture-notes/MIT6_837F12_Lec01.pdf
        # https://github.com/kawache/Python-B-spline-examples
        # https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
        # https://nurbs-python.readthedocs.io/en/latest/module_bspline.html
        blocks = divide_into_4s(edge_fix)
        path = []  # path to draw
        path.append(start)
        for chunk in blocks:
            curve = Bezier(chunk, 200)
            path = path + curve.tolist()

        edge_color = "black"
        # add arrow adornment using linear algebra
        if edge.get("edge_type") == "causes_or_promotes":
            # A,B = [path[-20],path[-1]]
            A, B = [path[20], path[0]]
            A = np.array(A)
            B = np.array(B)
            height = 5 * math.sqrt(3)
            theta = 45
            width = height * math.tan(theta / 2)
            U = (B - A) / np.linalg.norm(B - A)
            V = np.array((-1 * U[1], U[0]))
            v1 = B - height * U + width * V
            v2 = B - height * U - width * V
            adornment_to_add = [v1.tolist()] + [B] + [v2.tolist()]
            xpoint = [coordinate[0] for coordinate in adornment_to_add]
            ypoint = [coordinate[1] for coordinate in adornment_to_add]
            edge_color = "blue"
            fig.add_trace(
                go.Scatter(
                    x=xpoint,
                    y=ypoint,
                    line_shape="linear",
                    mode="lines",
                    line=dict(color=edge_color),
                )
            )

        # add tee adornment using linear algebra
        if edge.get("edge_type") == "is_inhibited_or_prevented_or_blocked_or_slowed_by":
            # B,A = [path[0],path[1]]
            B, A = [path[-1], path[2]]
            A = np.array(A)
            B = np.array(B)
            height = 0
            width = 10
            U = (B - A) / np.linalg.norm(B - A)
            V = np.array((-1 * U[1], U[0]))
            v1 = B - height * U + width * V
            v2 = B - height * U - width * V
            adornment_to_add = [v1.tolist()] + [B] + [v2.tolist()]
            xpoint = [coordinate[0] for coordinate in adornment_to_add]
            ypoint = [coordinate[1] for coordinate in adornment_to_add]
            edge_color = "red"
            fig.add_trace(
                go.Scatter(
                    x=xpoint,
                    y=ypoint,
                    line_shape="linear",
                    mode="lines",
                    line=dict(color=edge_color),
                )
            )

        # add edge spline trace to the figure object
        xp = [coordinate[0] for coordinate in path]
        yp = [coordinate[1] for coordinate in path]
        fig.add_trace(
            go.Scatter(
                x=xp,
                y=yp,
                marker=dict(color=edge_color),
                line_shape="spline",
                hovertemplate=edge.get("edge_hovertext"),
            )
        )

    # change the x and y axis ranges to be the values found in the 'header' of the graphviz graph layout string
    fig.update_xaxes(range=[0, 8395.7])
    fig.update_yaxes(range=[0, 1404])
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        height=700,
        xaxis={"showgrid": False},
        yaxis={"showgrid": False},
    )
    print("get_figure! FIG IS RETURNING")
    return fig


# divide graphviz edge curve coordinates into groups of coordinates to help draw edges as correct spline curves (cubic B splines)
def divide_into_4s(input):
    size = 4
    step = 3
    output = [input[i : i + size] for i in range(1, len(input) - 2, step)]
    return output


# unit vector to help with edge geometry (specifically drawing arrows)
def unit_vector(v):
    return v / np.linalg.norm(v)


def get_filtered_data(N_node_details, N_edge_details, N, G, edge_type=None):
    if edge_type is None:
        # By default display everything
        nodes_to_display = [n.get("name") for n in N_node_details]
        edges_to_display = [N.get_edge(e["node1"], e["node2"]) for e in N_edge_details]
    else:
        nodes_to_display = []
        edges_to_display = []

        for edge in G.edges:
            if G.edges.get(edge).get("type") == edge_type:
                node1, node2 = [edge[0], edge[1]]
                edges_to_display.append(edge)
                nodes_to_display.append(node1)
                nodes_to_display.append(node2)

    return nodes_to_display, edges_to_display


def visualize(gpickle_file_path):
    """
    Main function to run the dashboard to visualize the ontology.

    input: gpickle_file_path = path to gpickle of the networkx graph of the ontology
    output: app = Dash app object
    """
    # load in networkx graph to access graph information
    G = nx.read_gpickle(gpickle_file_path)
    print(nx.info(G))

    # pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

    # convert the network x graph to a graphviz graph
    N = nx.nx_agraph.to_agraph(G)

    # Class filter to go under the graph
    # Get all nodes classes
    allclasses = set()
    for node in N.nodes():
        nodeclasslist = eval(node.attr.get("all classes"))
        if isinstance(nodeclasslist, list) or isinstance(nodeclasslist, set):
            allclasses.update([e for e in nodeclasslist])
    # build the filter items for the layout
    allclasses_filter_radioitems = [{"value": ee, "label": ee} for ee in allclasses]
    allclasses_filter_radioitems.append({"label": "None", "value": "none"})

    # Node Property filter to go under the graph
    # Get all nodes properties
    allnodeproperties = set()
    for node in G.nodes():
        props = G.nodes.get(node).get("properties")
        allnodeproperties.update(props.keys())
    allnodeproperties_filter_radioitems = [
        {"value": ee, "label": ee} for ee in allnodeproperties
    ]
    allnodeproperties_filter_radioitems.append({"label": "None", "value": "none"})

    # change the graphviz graph settings to make the graph layout of edges and nodes as we want
    N.edge_attr.update(splines="curved", directed=True)
    N.layout(prog="dot")

    # output the graphviz graph layout details as a string file to parse and vizualize using native python plotly and dash
    f = (
        N.string()
    )  # this string contains the coordinates for the edges so they aren't just straight lines but curve to avoid going through other nodes

    # use python's in-memory text stream so string is the same across systems
    # ... so universal newline decoding is performed when reading the string
    s = io.StringIO(f, newline=None)

    # option to save graphviz graph file if desired. Not necessary though.
    # N.write('edges_spline_layout_coordinates.txt') #this file also has the coordinates for the splines for the edges that curve around the nodes instead of going through the nodes

    # parse the graphviz graph string for the layout information we need
    data = s.getvalue().split(";\n")
    # remove header and footer content
    header = data[0:3]
    content = data[3 : len(data) - 1]

    # close the in memory file
    s.close()

    # go through each item in 'content', and separate into either node or edge object
    N_nodes = []
    N_edges = []
    for item in content:
        if " -> " in item:
            N_edges.append(item)
        else:
            N_nodes.append(item)

    default_edge_type = [
        "is_inhibited_or_prevented_or_blocked_or_slowed_by",
        "causes_or_promotes",
    ]

    # populate node graph layout details from graphviz
    N_node_details = []
    for N_node in N_nodes:
        name = N_node.split("\t")[1].strip('"')

        node_attrs = N.get_node(name).attr
        height = node_attrs.get("height", 0)
        width = node_attrs.get("width", 0)
        position = node_attrs.get("pos", []).split(",")
        node_properties = G.nodes.get(name).get("properties")
        node_classes = G.nodes.get(name).get("all classes")
        node_classes_hovertext = "<br>-".join([f"<b>{cla}</b>" for cla in node_classes])
        node_properties_hovertext = "<br>-".join(
            [f"<b>{key}</b>: {val}" for (key, val) in node_properties.items()]
        )
        n_details = {
            "name": name,
            "position": {"x": float(position[0]), "y": float(position[1])},
            "height": float(height),
            "width": float(width),
            "node_hovertext": f"<b>Node classes:</b><br>{node_classes_hovertext}<br><br><b>Nodes properties:</b><br>{node_properties_hovertext}",
        }
        for edg in G.edges(name, data=True):
            edg_type = edg[2].get("type")
            if edg_type not in default_edge_type:
                n_details["non_default_edge_type"] = edg_type
        N_node_details.append(n_details)

    # populate edge graph layout details from graphviz
    N_edge_details = []
    for edge in N_edges:
        node1, node2 = edge.split("\t")[1].split(" -> ")
        node1 = node1.strip('"')
        node2 = node2.strip('"')

        edge_attrs = N.get_edge(node1, node2).attr
        positions = (
            edge_attrs.get("pos")
            .replace("e,", "")
            .replace("\\", "")
            .replace("r", "")
            .replace("n", "")
        )
        positions = [
            [float(x), float(y)]
            for (x, y) in [cp.split(",") for cp in positions.split(" ")]
        ]
        edge_type = edge_attrs.get("type")
        edge_properties = G.edges.get((node1, node2)).get("properties")
        if edge_properties:
            edge_properties_hovertext = "<br>-".join(
                [f"<b>{key}</b>: {val}" for (key, val) in edge_properties.items()]
            )
        else:
            edge_properties_hovertext = "None"
        edge_details = {
            "node1": node1,
            "node2": node2,
            "positions": positions,
            "edge_type": edge_type,
            "edge_hovertext": f"<b>Edge properties:</b><br>{edge_properties_hovertext}",
        }
        N_edge_details.append(edge_details)

    # divide the x and y coordinates into separate lists
    node_x_list = []
    node_y_list = []
    for node in N_node_details:
        node_x_list.append(node.get("position").get("x"))
        node_y_list.append(node.get("position").get("y"))

    # links to help undertand dash better if needed
    # https://plotly.com/python/line-charts/
    # https://plotly.com/python/shapes/
    # radio icons and dropdown menus
    # https://www.datacamp.com/community/tutorials/learn-build-dash-python
    ################### START OF DASH APP ###################
    app = dash.Dash()

    # NEED TO ADD HTML formating and maybe CSS
    app.layout = html.Div(
        children=[
            html.H1(children="Climate Mind DiGraph"),
            dcc.Graph(
                id="graph",
                figure=get_figure(N_node_details, N_edge_details, N, G),
                config=dict({"scrollZoom": True}),
            ),
            html.Div(
                children=[
                    html.Label("Display Nodes with following edges:"),
                    dcc.RadioItems(
                        id="edge-type-filter",
                        options=[
                            {
                                "label": "causes_or_promotes",
                                "value": "causes_or_promotes",
                            },
                            {
                                "label": "is_inhibited_or_prevented_or_blocked_or_slowed_by",
                                "value": "is_inhibited_or_prevented_or_blocked_or_slowed_by",
                            },
                            {"label": "All", "value": "all"},
                        ],
                        value="all",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.Label("Higlight Nodes with the specific class:"),
                    dcc.Dropdown(
                        id="node-class-filter",
                        options=allclasses_filter_radioitems,
                        value="none",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.Label("Higlight Nodes with the following non empty property:"),
                    dcc.Dropdown(
                        id="node-property-filter",
                        options=allnodeproperties_filter_radioitems,
                        value="none",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.Label("Higlight Nodes"),
                    dcc.Checklist(
                        id="node-extra-edge-type-filter",
                        options=[
                            {
                                "label": "If they contain additional edge type(s) "
                                "(beyond 'causes_or_promotes' or "
                                "'is_inhibited_or_prevented_or_blocked_or_slowed_by')",
                                "value": "yes",
                            }
                        ],
                        value="",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.Label("Node Data (on click):"),
                    html.Pre(id="click-data"),
                ],
            ),
        ]
    )

    @app.callback(
        dash.dependencies.Output("click-data", "children"),
        [dash.dependencies.Input("graph", "clickData")],
    )
    def display_click_data(clickData):
        return json.dumps(clickData, indent=2)

    @app.callback(
        dash.dependencies.Output("graph", "figure"),
        [
            dash.dependencies.Input("edge-type-filter", "value"),
            dash.dependencies.Input("node-class-filter", "value"),
            dash.dependencies.Input("node-property-filter", "value"),
            dash.dependencies.Input("node-extra-edge-type-filter", "value"),
        ],
    )
    def display_click_data(edge_type, node_class, node_property, extra_edge_type):
        print("display_click_data!")
        if (
            not edge_type
            and not node_class
            and not node_property
            and not extra_edge_type
        ):
            # Nothing has to happen.
            # otherwise the callback is called in some load/init cases
            raise dash.exceptions.PreventUpdate
        if edge_type == "all":
            edge_type = None
        if node_class == "none":
            node_class = None
        if node_property == "none":
            node_property = None
        if extra_edge_type != "yes":
            extra_edge_type = None
        print(f"display_click_data! edge_type={edge_type}, node_class={node_class}")
        return get_figure(
            N_node_details,
            N_edge_details,
            N,
            G,
            edge_type,
            node_class,
            node_property,
            extra_edge_type,
        )

    return app


def main(args):
    """
    Main function to run the dashboard to visualize the ontology.

    input: args = args from the argument parser for the function (gpickle_file_path)

    example: python3 visualize.py "Climate_Mind_DiGraph.gpickle"
    """
    # load arguments
    gpickle_file_path = args.gpickle_file_path

    app = visualize(gpickle_file_path=gpickle_file_path)
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="get networkx graph object from ontology after running make_network.py"
    )
    parser.add_argument(
        "gpickle_file_path", type=str, help="path to reference networkx gpickle object"
    )
    args = parser.parse_args()
    app = main(args)
    app.run(debug=False, host="0.0.0.0")
    app.run_server(debug=False, host="0.0.0.0", port=8050)

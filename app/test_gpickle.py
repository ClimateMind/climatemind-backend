import networkx as nx
from flask import abort
import os
import urllib
from datetime import timedelta

from app.network_x_tools.network_x_processor import network_x_processor


def test_me():
    nx_processor = network_x_processor()
    G = nx_processor.get_graph()
    print("from inside the test")
    # breakpoint()
    assert True

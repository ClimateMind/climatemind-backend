import pytest
from networkx import DiGraph

from app.network_x_tools.network_x_processor import network_x_processor


def test_get_graph_type():
    nx_processor = network_x_processor()
    graph = nx_processor.get_graph()
    assert type(graph) == DiGraph


def test_get_graph_missing_file():
    nx_processor = network_x_processor()
    nx_processor.graph_file = "missing.gpickle"
    with pytest.raises(FileNotFoundError):
        nx_processor.load_graph()

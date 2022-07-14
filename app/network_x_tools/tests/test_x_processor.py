import pytest
from flask import current_app
from networkx import DiGraph

from app.network_x_tools.network_x_processor import network_x_processor


@pytest.mark.ontology
def test_get_graph_type():
    nx_processor = network_x_processor(current_app.config["GRAPH_FILE"])
    graph = nx_processor.get_graph()
    assert type(graph) == DiGraph


@pytest.mark.ontology
def test_get_graph_missing_file():
    with pytest.raises(FileNotFoundError):
        network_x_processor("missing.gpickle")

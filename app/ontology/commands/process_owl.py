import shutil

import click
import ontology_processing.process_new_ontology_file
from flask import current_app
from networkx.readwrite.gpickle import read_gpickle

from app.ontology import bp


@bp.cli.command("process_owl")
@click.argument("owl_file", type=click.Path(exists=True))
@click.option(
    "--check/--no-check",
    default=True,
    help="Compare with previous .gpickle file or not",
)
def process_owl(owl_file, check):
    """
    Imports the climatemind-ontology-processing repo and runs the scripts to process
    the climatemind ontology .owl file and save to .gpicle file.
    """
    click.echo(f'Output directory: {current_app.config["GRAPH_FILE_PATH"]}')

    tmp_backup_filename = current_app.config["GRAPH_FILE"] + ".old"
    shutil.copy(current_app.config["GRAPH_FILE"], tmp_backup_filename)

    click.echo(f"Processing: {owl_file}...")
    ontology_processing.process_new_ontology_file.processOntology(
        owl_file, current_app.config["GRAPH_FILE_PATH"]
    )
    click.echo(f'New file created: {current_app.config["GRAPH_FILE"]}', color="green")

    if check:
        try:
            click.echo("Running checks...")
            old_graph = read_gpickle(tmp_backup_filename)
            new_graph = read_gpickle(current_app.config["GRAPH_FILE"])
            equivalent_graphs_check(old_graph, new_graph)
            shutil.move(tmp_backup_filename, current_app.config["GRAPH_FILE_BACKUP"])
            click.echo(f'Backup created: {current_app.config["GRAPH_FILE_BACKUP"]}')
            click.echo(f"SUCCESS!", color="green")
        except AssertionError as e:
            click.echo(f"Assertion error: {str(e)}", err=True)
            shutil.move(tmp_backup_filename, current_app.config["GRAPH_FILE"])
            click.echo("Run debugger to figure out", err=True)
            # ipdb.set_trace()
    else:
        click.echo("Skipping checks!")


def equivalent_graphs_check(old_graph, new_graph):
    """
    The purpose of this function is to regression test refactoring of the owl->nx
    processing pipeline. Concretely, this checks that the output gpickle files
    represent equivalent graphs, ignoring node or edge attributes that are lists
    that differ only in the order of their contents.

    Parameters
    ----------
    new_graph
    old_graph
    """

    test_length(old_graph, new_graph)
    test_node_attributes(new_graph.nodes(data=True), old_graph.nodes(data=True))
    test_edge_attributes(new_graph, old_graph)


def test_length(old_graph, new_graph):
    assert len(old_graph) == len(new_graph), "Graphs len mismatch"
    assert len(old_graph.edges()) == len(new_graph.edges()), "Graphs edges len mismatch"


def test_node_attributes(collection1, collection2):
    for node1_id, node1_data in collection1:
        node2_data = collection2[node1_id]
        assert (
            node1_data.keys() == node2_data.keys()
        ), f"{node1_id} keys mismatch: {node1_data.keys()} vs {node2_data.keys()}"
        for node1_attr_key, node1_attr_value in node1_data.items():
            node2_attr_value = node2_data[node1_attr_key]
            assert set(node1_attr_value) == set(node2_attr_value)


def test_edge_attributes(old_graph, new_graph):
    for src_old, tgt_old, data_old in old_graph.edges(data=True):
        data_new = new_graph.edges()[src_old, tgt_old]
        assert data_old.keys() == data_new.keys(), f"{src_old} edges keys mismatch"
        for k, v1 in data_old.items():
            v2 = data_new[k]
            try:
                assert set(v1) == set(v2)
            except TypeError:
                assert v1 is None
                assert v2 is None

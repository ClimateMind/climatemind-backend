from app.network_x_tools.network_x_utils import network_x_utils

from app.feed.process_alignment_feed import (
    find_alignment_solution_iris,
    get_solution_nodes,
    CONVERSATION_SOLUTION_NAME,
    POPULAR_SOLUTION_NAMES,
    POPULAR_SOLUTION_COUNT,
    UNPOPULAR_SOLUTION_COUNT,
)


def test_find_alignment_solution_iris():
    nx = network_x_utils()
    solution_nodes = get_solution_nodes()
    iri_label_map = {}
    for node in solution_nodes:
        nx.set_current_node(node)
        iri_label_map[nx.get_node_id()] = node["label"]
    solution_iris = find_alignment_solution_iris(
        CONVERSATION_SOLUTION_NAME,
        POPULAR_SOLUTION_NAMES,
        POPULAR_SOLUTION_COUNT,
        UNPOPULAR_SOLUTION_COUNT,
    )
    expected_conversation_iri = solution_iris[0]
    popular_iris = [
        iri for iri in solution_iris[1:] if iri_label_map[iri] in POPULAR_SOLUTION_NAMES
    ]
    unpopular_iris = [
        iri
        for iri in solution_iris[1:]
        if iri_label_map[iri] not in POPULAR_SOLUTION_NAMES
    ]
    assert iri_label_map[expected_conversation_iri] == CONVERSATION_SOLUTION_NAME
    assert len(popular_iris) == POPULAR_SOLUTION_COUNT
    assert len(unpopular_iris) == UNPOPULAR_SOLUTION_COUNT

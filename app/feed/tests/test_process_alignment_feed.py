from app.network_x_tools.network_x_utils import network_x_utils

from app.feed.process_alignment_feed import (
    get_default_solutions_iris,
    get_solution_nodes,
    CONVERSATION_SOLUTION_NAME,
    POPULAR_SOLUTION_NAMES,
    POPULAR_SOLUTION_COUNT,
    UNPOPULAR_SOLUTION_COUNT,
)


def test_get_default_solutions_iris():
    nx = network_x_utils()
    solution_nodes = get_solution_nodes()
    iri_name_map = {}

    for node in solution_nodes:
        nx.set_current_node(node)
        iri_name_map[nx.get_node_id()] = node["label"]

    result_solution_iris = get_default_solutions_iris()
    conversation_solution_count = 1
    total_solutions_count = (
        POPULAR_SOLUTION_COUNT + UNPOPULAR_SOLUTION_COUNT + conversation_solution_count
    )
    assert (
        len(result_solution_iris) == total_solutions_count
    ), f"Total solutions cound should be {total_solutions_count}"

    first_iri_in_result = result_solution_iris[0]
    assert (
        iri_name_map[first_iri_in_result] == CONVERSATION_SOLUTION_NAME
    ), "First iri in result should be CONVERSATION iri"

    result_without_conversation_iri = result_solution_iris[1:]
    popular_iris_in_result = [
        iri
        for iri in result_without_conversation_iri
        if iri_name_map[iri] in POPULAR_SOLUTION_NAMES
    ]
    assert (
        len(popular_iris_in_result) == POPULAR_SOLUTION_COUNT
    ), "Result contain proper popular solution count"

    unpopular_iris = [
        iri
        for iri in result_without_conversation_iri
        if iri_name_map[iri] not in POPULAR_SOLUTION_NAMES
    ]
    assert (
        len(unpopular_iris) == UNPOPULAR_SOLUTION_COUNT
    ), "Result contain proper unpopular solution count"

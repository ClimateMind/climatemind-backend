import pytest
from flask import current_app

from app.factories import AlignmentScoresFactory
from app.feed.process_alignment_feed import (
    get_aligned_effects,
    get_default_solutions_iris,
    get_solution_nodes,
)
from app.feed.constants import (
    CONVERSATION_SOLUTION_NAME,
    POPULAR_SOLUTION_NAMES,
    POPULAR_SOLUTION_COUNT,
    UNPOPULAR_SOLUTION_COUNT,
    ALIGNMENT_EFFECTS_COUNT,
)
from app.network_x_tools.network_x_utils import network_x_utils
from app.personal_values.enums import PersonalValue


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


@pytest.mark.ontology
@pytest.mark.parametrize("personal_value", [v.key for v in PersonalValue])
def test_get_aligned_effects(personal_value):
    alignment_score_arguments = {f"{personal_value}_alignment": 0.99}
    alignment_score = AlignmentScoresFactory(**alignment_score_arguments)

    aligned_effects = get_aligned_effects(
        alignment_score.alignment_scores_uuid,
        ALIGNMENT_EFFECTS_COUNT,
    )
    assert len(aligned_effects) == ALIGNMENT_EFFECTS_COUNT

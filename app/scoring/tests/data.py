import random


def _generate_set(questions_range: tuple):
    """
    Creates random answers for a single question set of 10 questions.

    Args:
        questions_range: a tuple for the range of question ids to use for creating the answers object

    Returns: a single question set of random answers between 1 to 6

    """
    answer_object = [
        {"questionId": qid, "answerId": aid}
        for qid, aid in zip(
            range(questions_range[0], questions_range[1] + 1),
            [random.randint(1, 6) for _ in range(10)],
        )
    ]

    return answer_object


def generate_random_answers():
    """
    Creates scores object mocking user who randomly answers either only the first question set of 10 questions or both set one and set two of 10 questions. Formats the result properly for answer scoring and processing with the app.
    """
    res = {"SetOne": _generate_set((1, 10))}
    with_set_two = bool(random.getrandbits(1))
    if with_set_two:
        res["SetTwo"] = _generate_set((11, 20))
    return res


def generate_test_answers_10(a, b, c, d, e, f, g, h, i, j):
    """
    Creates scores object mocking user who only answers the first question set of 10 questions .

    Args:
        a-j: integer - Valid options are 1-6 where 1 is 'Not Like Me At All' and 6 is 'Very Much Like Me'

    Returns: scores object properly formatted for scoring function for the app
    """
    answer_object = []
    answer_object.append({"questionId": 1, "answerId": a})
    answer_object.append({"questionId": 2, "answerId": b})
    answer_object.append({"questionId": 3, "answerId": c})
    answer_object.append({"questionId": 4, "answerId": d})
    answer_object.append({"questionId": 5, "answerId": e})
    answer_object.append({"questionId": 6, "answerId": f})
    answer_object.append({"questionId": 7, "answerId": g})
    answer_object.append({"questionId": 8, "answerId": h})
    answer_object.append({"questionId": 9, "answerId": i})
    answer_object.append({"questionId": 10, "answerId": j})

    return answer_object


def generate_test_answers_20(
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t
):
    """
    Creates scores object mocking user who answers set one and set two question sets of 10 questions.

    Args:
        a-t: integer - Valid options are 1-6 where 1 is 'Not Like Me At All' and 6 is 'Very Much Like Me'

    Returns: scores object properly formatted for scoring function for the app
    """
    answer_object_1 = generate_test_answers_10(a, b, c, d, e, f, g, h, i, j)
    answer_object_2 = []
    answer_object.append({"questionId": 11, "answerId": k})
    answer_object.append({"questionId": 12, "answerId": l})
    answer_object.append({"questionId": 13, "answerId": m})
    answer_object.append({"questionId": 14, "answerId": n})
    answer_object.append({"questionId": 15, "answerId": o})
    answer_object.append({"questionId": 16, "answerId": p})
    answer_object.append({"questionId": 17, "answerId": q})
    answer_object.append({"questionId": 18, "answerId": r})
    answer_object.append({"questionId": 19, "answerId": s})
    answer_object.append({"questionId": 20, "answerId": t})

    final_answer_object = {"SetOne": answer_object_1, "SetTwo": answer_object_2}

    return final_answer_object


if __name__ == "__main__":
    process_scores_data = []
    number_of_random_quizzes = 5

    process_scores_data.append(generate_test_answers_10(6, 6, 6, 6, 6, 6, 6, 6, 1, 1))
    process_scores_data.append(
        generate_test_answers_20(
            6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1
        )
    )
    process_scores_data.append(generate_test_answers_10(6, 6, 6, 6, 6, 6, 6, 6, 6, 1))
    process_scores_data.append(
        generate_test_answers_20(
            6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1
        )
    )
    process_scores_data.append(generate_test_answers_10(6, 6, 6, 6, 6, 1, 1, 1, 1, 1))
    process_scores_data.append(
        generate_test_answers_20(
            6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1
        )
    )
    process_scores_data.append(generate_test_answers_10(1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
    process_scores_data.append(
        generate_test_answers_20(
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        )
    )
    process_scores_data.append(generate_test_answers_10(4, 4, 4, 4, 4, 4, 4, 4, 4, 4))
    process_scores_data.append(
        generate_test_answers_20(
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
        )
    )

    for _ in range(1, number_of_random_quizzes + 1):
        process_scores_data.append(generate_random_answers())

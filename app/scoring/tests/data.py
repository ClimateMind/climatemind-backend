import random


def _generate_set(questions_range: tuple, *args):
    """
    Creates answers for a single question set of 10 questions.

    Args:
        questions_range: a tuple for the range of question ids to use for creating the answers object
        *args: predefined answers to use

    Returns: a single question set of answers between 1 to 6
    """
    predefined_answers = list(args)
    answers = []
    number_answers_in_set = 10
    for _ in range(number_answers_in_set):
        try:
            answers.append(predefined_answers.pop(0))
        except IndexError:
            answers.append(random.randint(1, 6))

    set_of_responses = [
        {"questionId": qid, "answerId": aid}
        for qid, aid in zip(
            range(questions_range[0], questions_range[1] + 1),
            answers,
        )
    ]

    return set_of_responses


def generate_random_responses():
    """
    Creates scores object mocking user who randomly answers either only the
    first question set of 10 questions or both set one and set two of 10 questions.
    """
    res = {"SetOne": _generate_set((1, 10))}
    with_set_two = bool(random.getrandbits(1))
    if with_set_two:
        res["SetTwo"] = _generate_set((11, 20))
    return res


def generate_responses(*args):
    """
    Creates scores object mocking user who answers either only the
    first question set of 10 questions or both set one and set two of 10 questions.
    """
    answers = list(args)
    first_ten_answers = answers[:10]
    res = {"SetOne": _generate_set((1, 10), *first_ten_answers)}
    if len(args) > 10:
        last_ten_answers = answers[10:20]
        res["SetTwo"] = _generate_set((11, 20), *last_ten_answers)

    return res


process_scores_data = [
    generate_responses(6, 6, 6, 6, 6, 6, 6, 6, 1, 1),
    generate_responses(6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1),
    generate_responses(6, 6, 6, 6, 6, 6, 6, 6, 6, 1),
    generate_responses(6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1),
    generate_responses(6, 6, 6, 6, 6, 1, 1, 1, 1, 1),
    generate_responses(6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1),
    generate_responses(1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    generate_responses(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    generate_responses(4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
    generate_responses(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
]

number_of_random_quizzes = 5

for _ in range(1, number_of_random_quizzes + 1):
    process_scores_data.append(generate_random_responses())

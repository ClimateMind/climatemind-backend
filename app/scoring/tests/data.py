import random

process_scores_data = []


def generate_random_answers():
    def _generate_set(questions_range: tuple):
        return [
            {"questionId": qid, "answerId": aid}
            for qid, aid in zip(
                range(questions_range[0], questions_range[1] + 1),
                [random.randint(1, 6) for _ in range(10)],
            )
        ]

    res = {"SetOne": _generate_set((1, 10))}
    with_set_two = bool(random.getrandbits(1))
    if with_set_two:
        res["SetTwo"] = _generate_set((11, 20))
    return res


number_of_random_quizzes = 100
for _ in range(1, number_of_random_quizzes + 1):
    process_scores_data.append(generate_random_answers())

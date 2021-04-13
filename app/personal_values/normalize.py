def normalize_scores(values):
    min_score = min([value["score"] for value in values])
    max_score = max([value["score"] for value in values])
    # TODO: Check this correct way to normalise scores
    for val in values:
        val["score"] = (val["score"] - min_score) / (max_score - min_score) * 10
    return values

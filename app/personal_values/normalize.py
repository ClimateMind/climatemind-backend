def normalize_scores(values):
    # This normalise function rescales the users score between the users score
    range_min = 0
    range_max = 6
    min_score = min([value["score"] for value in values])
    max_score = max([value["score"] for value in values])

    for val in values:
        normalized_value = range_min + (val["score"] - min_score) * (
            range_max - range_min
        ) / (max_score - min_score)

        val["score"] = round(normalized_value, 1)
        print(val["score"])

    return values

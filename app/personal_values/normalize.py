def normalize_scores(values):
    # This normalise function rescales the users score between a given range for better display
    range_min = 0
    range_max = 6
    min_score = min([value["score"] for value in values])
    max_score = max([value["score"] for value in values])

    # If all question responses are the same return the middle of the range for each personal value
    if max_score - min_score == 0:
        for val in values:
            val["score"] = range_max / 2 + range_min
        return values

    # Or normalize scores if not
    for val in values:
        normalized_value = range_min + (val["score"] - min_score) * (
            range_max - range_min
        ) / (max_score - min_score)

        val["score"] = round(normalized_value, 1)

    return values

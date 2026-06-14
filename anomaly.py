def detect_anomaly(
    smart_money_count,
    netflow,
    sentiment
):

    score = 0

    if smart_money_count >= 3:
        score += 1

    if netflow > 100000:
        score += 1

    if sentiment > 80:
        score += 1

    return score >= 2
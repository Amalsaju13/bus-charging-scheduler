def compute_score(wait_time, operator_penalty, network_penalty, weights):
    return (
        weights["individual"] * wait_time
        + weights["operator"] * operator_penalty
        + weights["overall"] * network_penalty
    )
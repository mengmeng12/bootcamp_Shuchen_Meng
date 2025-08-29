
def calculate_metrics(X, y):
    """
    Simple function to calculate regression metrics.
    Returns dict with mean and sum of outputs.
    """
    return {"mean_y": sum(y)/len(y), "sum_y": sum(y)}

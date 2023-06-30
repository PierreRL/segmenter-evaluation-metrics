from itertools import product
from statistics import mean
from typing import List

import numpy as np
from scipy.optimize import linear_sum_assignment # type: ignore

def intersection_union_scores(
    true_clusters: List[List[int]], predicted_clusters: List[List[int]]
) -> float:
    scores = [[0] * len(predicted_clusters) for _ in range(len(true_clusters))]
    for (i, true_cluster), (j, predicted_cluster) in product(
        enumerate(true_clusters), enumerate(predicted_clusters)
    ):
        if len(true_cluster) == 0:
            raise RuntimeError(f"true_cluster[{i}] is an empty list.")
        if len(predicted_cluster) == 0:
            raise RuntimeError(f"predicted_cluster[{j}] is an empty list.")
        true_cluster = set(true_cluster)
        predicted_cluster = set(predicted_cluster)
        union = true_cluster.union(predicted_cluster)
        intersection = true_cluster.intersection(predicted_cluster)
        score = len(intersection) / len(union)
        scores[i][j] = score # type: ignore
    return scores # type: ignore


def mean_matched_intersection_union(
    true_clusters: List[List[int]],
    predicted_clusters: List[List[int]],
    punish_number_of_extraneous_clusters=False,
) -> float:
    """Compute score, but with each predicted cluster only assigned
    to a single true cluster.
    This problem is, "maximum weight matching in bipartite graphs",
    which is a standard problem (see resources).
    The bipartite graph consists of `true_clusters` as one part,
    and `predicted_clusters` as the other.
    Resources:
    https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
    https://en.wikipedia.org/wiki/Bipartite_graph
    https://en.wikipedia.org/wiki/Assignment_problem
    """
    scores = intersection_union_scores(true_clusters, predicted_clusters)
    scores = np.array(scores)
    row_ind, col_ind = linear_sum_assignment(-scores)
    # ^ negate scores, because linear_sum_assignment minimises score
    matched_values = list(scores[row_ind, col_ind])
    if punish_number_of_extraneous_clusters:
        matched_values += [0] * abs(len(true_clusters) - len(predicted_clusters))
        # ^ gives lower score to predictions with a larger number of extraneous clusters.
        # (Where an extraneous clusters is a predicted cluster not paired to a true cluster.)
        # May reward the clustering of unrelated things.
    else:
        matched_values += [0] * (len(true_clusters) - len(matched_values))
        # ^ include nodes in true_clusters that have not been assigned
        # a node from predicted_clusters, with a score of 0.
    return mean(matched_values)


def mean_max_intersection_union(
    true_clusters: List[List[int]], predicted_clusters: List[List[int]]
) -> float:
    scores = intersection_union_scores(true_clusters, predicted_clusters)
    top_score_per_true_cluster = [max(s) for s in scores] # type: ignore
    return mean(top_score_per_true_cluster)
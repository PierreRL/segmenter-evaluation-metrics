from __future__ import annotations
import random
random.seed(1024)

from util import Seg, Eval
from nim_metric import mean_max_intersection_union, mean_matched_intersection_union
from inc_near_misses import inc_near_misses
from evals_and_hyps import evals_and_hyps
from IR import IR
from segeval import window_diff, boundary_similarity, pk, segmentation_similarity # type: ignore


ref = Seg([2,3,6], 'Ref')
hypotheses = [
    ref,
    Seg([1]*11, 'All'),
    Seg([11], 'None'),
    Seg([5,6], 'FN'),
    Seg([2,3,3,3], 'FP'),
    Seg([2,4,5], 'Near Miss'),
    Seg([1,1,3,1,5], 'Cluster'),
    Seg([2,2,2,2,2,1], 'Uniform'),
    Seg.from_boundaries( random.sample(range(1,11),2), 11, 'Random1'),
    Seg.from_boundaries( random.sample(range(1,11),2), 11, 'Random2'),
]
evals = [
    Eval(lambda hyp, ref: 1 - window_diff(hyp, ref), '1-WD'),
    Eval(lambda hyp, ref: 1 - pk(hyp, ref), '1-Pk'),
    Eval(segmentation_similarity, 'S'),
    Eval(boundary_similarity, 'B'),
    Eval(lambda hyp, ref: mean_max_intersection_union(ref, hyp), 'mean-max IoU', False),
    Eval(lambda hyp, ref: mean_matched_intersection_union(ref, hyp, False), 'mean-matched IoU', False),
    Eval(lambda hyp, ref: mean_matched_intersection_union(ref, hyp, True), 'mean_mathced IoU + punish', False)
]

def main():
    evals_and_hyps(hypotheses, evals, ref)
    IR(hypotheses, ref)
    inc_near_misses()
    
main()






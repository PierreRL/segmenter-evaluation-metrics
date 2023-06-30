from __future__ import annotations
import random
from typing import Any, Callable
from segeval import window_diff, boundary_similarity, pk, segmentation_similarity # type: ignore
from tabulate import tabulate
from nim_metric import mean_max_intersection_union, mean_matched_intersection_union

class Seg:
    def __init__(self, lengths: list[int], name:str):
        self.name = name
        self.lengths = lengths
        self.segments = self.to_individuals(lengths)

    def to_individuals(self, lengths: list[int]) -> list[list[int]]:
        out = []
        for segment in lengths:
            out.append(range(segment))
        return out

    @classmethod
    def from_boundaries(cls, boundaries:list[int], name:str) -> Seg:
        boundaries = sorted(boundaries)
        lengths = [boundaries[0]]
        for i in range(1, len(boundaries)):
            lengths.append(boundaries[i] - boundaries[i-1])
        lengths.append(11 - sum(lengths))
        return Seg(lengths, name)

class Eval:
    def __init__(self, func : Callable[[Any, Any], float], name:str, usesLengths = True):
        self.func = func
        self.name = name
        self.usesLengths = usesLengths

def main():
    ref = Seg([2,3,6], 'Ref')

    hypotheses = [
        Seg([1]*11, 'All'),
        Seg([11], 'None'),
        Seg([5,6], 'FN'),
        Seg([2,3,3,3], 'FP'),
        Seg([2,2,7], 'Near Miss'),
        Seg([1,1,3,1,5], 'Cluster'),
        Seg([2,2,2,2,2,1], 'Uniform'),
        Seg.from_boundaries( random.sample(range(1,11),3), 'Random1'),
        Seg.from_boundaries( random.sample(range(1,11),3), 'Random2'),
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
    
    data = []
    for hyp in hypotheses:
        scores = [hyp.name]
        for eval in evals:
            if (eval.usesLengths):
                scores.append(eval.func(hyp.lengths, ref.lengths)) # type: ignore
            else:
                scores.append(eval.func(hyp.segments, ref.segments)) # type: ignore
        data.append(scores)

    headers = []
    for eval in evals:
        headers.append(eval.name)
    
    print(tabulate(data, headers))
    

main()
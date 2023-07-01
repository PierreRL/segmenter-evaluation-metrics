from __future__ import annotations
import random
from util import Seg, Eval, calc_IR
random.seed(1000)
from typing import Any, Callable
from segeval import window_diff, boundary_similarity, pk, segmentation_similarity
import segeval
from tabulate import tabulate
from nim_metric import mean_max_intersection_union, mean_matched_intersection_union

def main():
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
    
    eval_data = []
    ir_data = []
    for hyp in hypotheses:
        scores = [hyp.name]
        for eval in evals:
            if (eval.usesLengths):
                scores.append(eval.func(hyp.lengths, ref.lengths)) # type: ignore
            else:
                scores.append(eval.func(hyp.segments, ref.segments)) # type: ignore
        eval_data.append(scores)

        matrix = segeval.boundary_confusion_matrix(hyp.lengths, ref.lengths)
        precision, recall, f1 = calc_IR(hyp, ref)

        ir_row = [hyp.name, segeval.precision(matrix, None), segeval.precision(matrix, 1), segeval.fmeasure(matrix), precision, recall, f1, segeval.boundary_similarity(hyp.lengths, ref.lengths)]
        ir_data.append(ir_row)

    headers = ['Hypothesis']
    ir_headers = ['Hyp', 'Precision', 'Recall', 'f1', 'Precision2', 'Recall2', 'f1-2', 'B']
    for eval in evals:
        headers.append(eval.name)
    
    print(tabulate(eval_data, headers))
    print('-'*50)
    print(tabulate(ir_data, ir_headers))
    
main()
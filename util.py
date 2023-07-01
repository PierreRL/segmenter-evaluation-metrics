from __future__ import annotations
from pyparsing import Any
import segeval
from traitlets import Callable
from segeval import ConfusionMatrix

def calc_IR(hyp: Seg, ref:Seg):
    matrix = segeval.boundary_confusion_matrix(hyp.lengths, ref.lengths)
    TP = matrix[1][1]
    FP = matrix[None][1]
    FN = matrix[1][None]
    if (TP+FP) == 0:
        precision = 0
    else:
        precision = TP / (TP+FP)
    if (TP+FN)==0:
        recall = 0
    else:
        recall  = TP / (TP+FN)
    if ((precision+recall) == 0):
        f1 = 0
    else:
        f1 = 2* ((precision * recall) / (precision+recall))
    return precision, recall, f1


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
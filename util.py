from __future__ import annotations
from typing import Any, Callable
import segeval
from tabulate import tabulate

def print_table(title: str, data: list[list[Any]], headers: list[str]):
    print('-'*120)
    print(title)
    print('-'*120)
    print(tabulate(data, headers))
    print('-'*120)

def calc_IR(hyp: list[int], ref: list[int], n_t:int = 2):
    matrix = segeval.boundary_confusion_matrix(hyp, ref, n_t=n_t) # type: ignore
    TP = matrix[1][1]
    FP = matrix[None][1]
    FN = matrix[1][None]
    if (TP + FP) == 0:
        precision = 0
    else:
        precision = TP / (TP + FP)
    if (TP + FN) == 0:
        recall = 0
    else:
        recall  = TP / (TP + FN)
    if ((precision+recall) == 0):
        f1 = 0
    else:
        f1 = 2 * ((precision * recall) / (precision + recall))
    return precision, recall, f1


class Seg:
    def __init__(self, lengths: list[int], name:str):
        self.name = name
        self.lengths = lengths
        self.segments = self.to_individuals(lengths)

    def to_individuals(self, lengths: list[int]) -> list[list[int]]:
        """
        From the given lengths of segments, calculates inputs (called 'individuals'/segments) which are used as input into the Nim-metrics.
        """
        out = []
        for segment in lengths:
            out.append(range(segment))
        return out

    @classmethod
    def from_boundaries(cls, boundaries:list[int], totalLlength:int, name:str) -> Seg:
        """
        Creates a Seg from a list of boundaries (as oppose to segment lengths/masses)
        """
        boundaries = sorted(boundaries)
        lengths = [boundaries[0]]
        for i in range(1, len(boundaries)):
            lengths.append(boundaries[i] - boundaries[i-1])
        lengths.append(totalLlength - sum(lengths))
        return Seg(lengths, name)

class Eval:
    def __init__(self, func : Callable[[Any, Any], float], name:str, usesLengths = True):
        self.func = func
        self.name = name
        self.usesLengths = usesLengths
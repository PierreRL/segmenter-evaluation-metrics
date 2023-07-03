from util import Seg, calc_IR, print_table
from segeval import boundary_similarity, boundary_confusion_matrix, precision, recall, fmeasure # type: ignore

def IR(hypotheses: list[Seg],  ref: Seg):
    """
    Prints a table showing information recall data and boundary similarity for a list of hypotheses.

    IR data is listed using both segeval's default functions (which seem to be erroneous) and a manually calulcated util function.

    Parameters
    ----------
    hypotheses: list[Seg] - The list of hypothesis segmentations to compare against
    ref: Seg - The reference segmentation
    """
    
    ir_data = []
    for hyp in hypotheses:

        matrix = boundary_confusion_matrix(hyp.lengths, ref.lengths)
        precision2, recall2, f1 = calc_IR(hyp.lengths, ref.lengths)

        ir_row = [hyp.name, precision(matrix), recall(matrix), fmeasure(matrix), precision2, recall2, f1, boundary_similarity(hyp.lengths, ref.lengths)]
        
        ir_data.append(ir_row)

    ir_headers = ['Hyp', 'Precision', 'Recall', 'f1', 'Precision2', 'Recall2', 'f1-2', 'B']

    print_table('IR Data', ir_data, ir_headers)
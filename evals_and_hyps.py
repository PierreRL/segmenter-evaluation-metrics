from util import Seg, Eval, print_table

def evals_and_hyps(hypotheses: list[Seg], evals: list[Eval], ref: Seg):
    """
    Prints a table showing each of the hypothesis segmentations against the each evaluation metric.

    Parameters
    ----------
    hypotheses: list[Seg] - The list of hypothesis segmentations to compare against
    evals: list[Eval] - The list of evaluation metrics to use
    ref: Seg - The reference segmentation
    """
    
    eval_data = []

    for hyp in hypotheses:
        scores = [hyp.name]
        for eval in evals:

            # Some evaluation metrics operated on lengths, others on the boundaries

            if (eval.usesLengths):
                scores.append(eval.func(hyp.lengths, ref.lengths)) # type: ignore

            else:
                scores.append(eval.func(hyp.segments, ref.segments)) # type: ignore

        eval_data.append(scores)

    headers = ['Hypothesis']
    for eval in evals:
        headers.append(eval.name)
    
    print_table('Evals over different Errors', eval_data, headers)
from util import Seg, print_table
from segeval import boundary_similarity # type: ignore

def inc_near_misses(n=20):
    """
    Prints a table showing the boundary similarity over increasing near miss distance and varying n_t.
    There is 1 segment half way through the 'document' in the reference, and the hypotheses go 

    This table illustrates the linear weighting transposition function. 

    If instead of using boundary similarity, you use segeval.precision, you can see that precision (erroneously) does not scale.

    Parameters
    ----------
    n = 20: The total length of all segments
    """

    data = []
    ref_inc = Seg([n//2,n//2], 'Ref')

    for i in range(n//2 + 1):

        if i == 0: hyp = Seg([n], str(i))
        else: hyp = Seg([i, n - i], str(i))

        scores = []
        for j in range(2, n//2):
            scores.append(boundary_similarity(hyp.lengths, ref_inc.lengths, n_t=j))

        data.append([hyp.name, *scores])

    print_table('B score, with increasing near miss distance and n_t increasing', 
                data, headers=['Distance', *['n_t=' + str(j) for j in range(2,n//2)]])
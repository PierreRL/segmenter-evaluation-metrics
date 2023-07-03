# Segmenter Evaluation Metrics

A simple exploration of segmentation evaluation metrics via some small contrived examples. An expansion on the work found in [Fournier2013](https://aclanthology.org/P13-1167.pdf).

The metrics looked at are:
- Pk
- WinDiff
- Segment Similarity
- Boundary Similarity
- Intersection over Union - mean maxed, and mean matched (+ punshing extra segments)

The contrived examples compared to a reference include:
- All segments
- No segments
- Uniform segments every 2 sentences
- Random segmentation with the same number of boundaries as reference
- A false negative
- A false positive
- A near miss

The first output table lists the examples and their scores under each evaluation metric. The second table looks at the B-Conufsion matrix and explores its possible errors. The final table show increasing near miss distance with the n_t (transposition distance) parameter.

This small demonstration concludes that *B* (Boundary Similarity) is the best metric as it deals with all the errors in the most intuitive manner, and the other reasons listed in [Fournier2013](https://aclanthology.org/P13-1167.pdf) including robustness to segment size. However, the segeval library is a bit outdated, and in particular some of the IR metrics do not work. Therefore, I implement my own versions manually to compensate. However, 'homemade' precision still does not correctly incorporate the weighting transposition function into IR metrics, which should be borne in mind.
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

The first output table lists the examples and their scores under each evaluation metric. The second table looks at the B-Conufsion matrix and explores its possible errors.

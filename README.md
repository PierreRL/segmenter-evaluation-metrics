# Segmenter Evaluation Metrics

A simple exploration of segmentation evaluation metrics via some small contrived examples.
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

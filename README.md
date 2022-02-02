# Generate Hits per country:

- python3 index.py
- access `related_values.py` to manipulate values to be used for getting hits

# Calculate Score:

- `python3 calculate_scores.py`

# Run Correlation:

- NOTE: ALL FILES SHOULD BE `.csv`

* `python3 correlation_rank.py -g <ground_truth file> -c <file to correlate> -b <Column Name to get from correlate file (different each time)> -m <method, 'pearson' or 'spearman'>`

- example: `python3 correlation_rank.py -g grown_truth_hostile_friendly.csv -c regulation_score1643121948.csv -b 'Score Ratio' -m spearman`

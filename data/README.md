# Data

`raw/cookie_cats.csv` is not committed (see `.gitignore`) — it's a small,
publicly available file, cheap to re-fetch, and keeping it out of git avoids
relying on a committed copy staying in sync with its source.

## To reproduce

```bash
mkdir -p data/raw
curl -o data/raw/cookie_cats.csv \
  https://raw.githubusercontent.com/ryanschaub/Mobile-Games-A-B-Testing-with-Cookie-Cats/master/cookie_cats.csv
```

Originally published as the "Mobile Games A/B Testing — Cookie Cats" dataset
on Kaggle. 90,189 rows, columns: `userid`, `version` (`gate_30`/`gate_40`),
`sum_gamerounds`, `retention_1`, `retention_7`. Verified row count, schema,
and checksum-free integrity (via row/column shape) in
[`docs/DATA_QUALITY.md`](../docs/DATA_QUALITY.md).

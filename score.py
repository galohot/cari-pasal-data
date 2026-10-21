"""Score a run against a CARI PASAL question set. Python 3.9+, standard library only.

Usage:
    python score.py sets/set_a.jsonl my_run.jsonl

A run file has one JSON object per line, best result first, up to 100 results:
    {"qid": "A-uu-7-1983/p28-0", "ranked": ["uu-7-1983/p28", "uu-36-2008/pI>21", ...]}

A question is a hit at rank k when any of its keys is in the top k. A question missing from the run counts
as a miss. Prints Recall@1, @5, @20 and MRR@10 with 95 % bootstrap intervals (1,000 resamples). The paper
computed its intervals with numpy, so the bounds here can differ from it by about 0.01.
"""

import json
import random
import sys

METRICS = ("R@1", "R@5", "R@20", "MRR@10")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def per_question(ranked, keys):
    keys = set(keys)
    rank = next((i for i, uid in enumerate(ranked, start=1) if uid in keys), None)
    return {
        "R@1": float(rank is not None and rank <= 1),
        "R@5": float(rank is not None and rank <= 5),
        "R@20": float(rank is not None and rank <= 20),
        "MRR@10": 1.0 / rank if rank is not None and rank <= 10 else 0.0,
    }


def summarize(rows, n_boot=1000, seed=7):
    rng = random.Random(seed)
    out = {}
    for m in METRICS:
        v = [r[m] for r in rows]
        boots = sorted(sum(rng.choices(v, k=len(v))) / len(v) for _ in range(n_boot))
        out[m] = (sum(v) / len(v), boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot) - 1])
    return out


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    questions = read_jsonl(sys.argv[1])
    runs = {r["qid"]: r["ranked"] for r in read_jsonl(sys.argv[2])}
    missing = sum(1 for q in questions if q["qid"] not in runs)
    rows = [per_question(runs.get(q["qid"], []), q["keys"]) for q in questions]
    print(f"{len(questions)} questions, {missing} missing from the run")
    for m, (mean, lo, hi) in summarize(rows).items():
        print(f"{m:7} {mean:.3f}  ({lo:.3f}-{hi:.3f})")


if __name__ == "__main__":
    main()

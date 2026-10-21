# cari-pasal-data

A test set and corpus for one task: **given a question in plain Indonesian, find the pasal that answers it.**
The scope is Indonesian tax law (PPh, with the HPP and Cipta Kerja amendments), social-security law (SJSN,
BPJS, JKK, JKM, JHT, JP, JKP, JKN) and company law (UU PT, PP 8/2021).

No paid expert wrote or checked the answer keys. They come from how the data is built.

The study, its method and its results: **https://irawan.blog/research/cari-pasal/** (web page and PDF).

## What is in it

| File | What it holds |
|---|---|
| `corpus/core.jsonl` | Every pasal of the core regulations, parsed from official PDFs. One row per pasal, or per restated pasal inside an amending law. Status (`berlaku`, `diubah`, `dicabut`) and amendment links. |
| `corpus/distractors.jsonl` | Wrong-option pasal from other national regulations (UU, PP, Perpres, Permen). Half are on nearby topics. They are never answer keys. |
| `sets/set_a.jsonl` | Questions written from a known pasal, so the right pasal is known from the start. Test data only. |
| `sets/set_c.jsonl` | Training pairs with no model-written text: each pasal with its official explanation (Penjelasan), and each Bab/Bagian heading with its pasal. Each pair lists BM25 hard negatives. |
| `runs/set_a_*.jsonl` | The four baseline runs on Set A (BM25, BM25 + stemmer, bge-m3, RRF), top 100 per question. |
| `prompts/` | The two prompts that wrote Set A and checked its keys. |
| `score.py` | A scorer, standard library only. |

In `corpus/core.jsonl`, `title` is the OCR'd title that the search systems indexed, and `doc_title` is the
clean title of the regulation.

A unit id is `<type>-<number>-<year>/p<pasal>` (`uu-40-2007/p92`). For a pasal restated inside an
amending law, it is `<amending law>/p<outer pasal>><restated pasal>` (`uu-6-2023/p109>7` = Cipta Kerja Pasal 109,
which restates UU PT Pasal 7). The `amends` field names the pasal it rewrites.

## How Set A was made

1. Current pasal only (status `berlaku`), at least 120 characters, no definition lists or closing pasal.
2. A language model wrote 1–2 questions per pasal, in plain Indonesian, as an HR officer, a business owner, a
   director, an employee or a BPJS participant would ask them. It was told not to copy runs of 3 or more words
   and not to name the regulation or the pasal number. The prompt is in `prompts/set_a_v1.md`.
3. **Copied-words filter.** Questions whose content words overlap the pasal by more than 0.6 were dropped.
   Every row keeps its `overlap` value, so results can be cut by it.
4. **Other-answers filter.** For each question, the top 10 BM25 and top 10 bge-m3 candidates were shown to a
   second model call, which marked every candidate that also answers the question on its own. Those were added
   to the keys. Questions with more than 3 keys were dropped as too vague.
5. **Read check.** 50 random questions were checked one by one against the full text of their source pasal: 0 of 50 had a wrong key, 1 of 50 lacked a second valid key. The writer, the key check and this read check were all done by Claude (Opus 5.5); no person reviewed the keys.

A hit means any key is in the top k. Model-written questions are **test data only**: do not train on them.

## How to score

Search `corpus/core.jsonl` + `corpus/distractors.jsonl` together (20,834 units). Write one line per question,
best result first, up to 100 results:

```json
{"qid": "A-uu-7-1983/p28-0", "ranked": ["uu-7-1983/p28", "pmk-168-2023/p8", "..."]}
```

Then run `python score.py sets/set_a.jsonl my_run.jsonl`. It prints Recall@1, @5, @20 and MRR@10 with 95 %
bootstrap intervals. To check the scorer, `python score.py sets/set_a.jsonl runs/set_a_bge-m3.jsonl` gives
R@5 0.856.

## Baseline (2026-10-21)

Corpus: 835 core units + 19,999 distractors. Recall@5 with 95 % bootstrap intervals:

| System | Set A (741) |
|---|---:|
| BM25 | 0.48 (0.44–0.52) |
| BM25 + Sastrawi stemmer | 0.57 (0.53–0.61) |
| bge-m3 (dense) | 0.86 (0.83–0.88) |
| RRF of BM25 and bge-m3 | 0.71 (0.67–0.74) |

On real questions (an internal set, not included here), bge-m3 reached 0.49 and BM25 0.28. Written questions
overstate every system.

## Limits

- **Law changes.** Every unit carries `as_of`. The new labour law (UU Pelindungan Ketenagakerjaan, passed by the
  DPR on 2026-10-06) is not in this release; labour law is left out on purpose.
- **Not consolidated.** Amending laws are kept as published. The 1991, 1994 and 2000 amendments of UU PPh are not
  included, so a few 1983 pasal may show outdated text.
- **OCR.** Most official PDFs are scans with a machine-read text layer. Expect errors such as `0`/`O` and `1`/`I`.
- **Model-written questions** read like a model wrote them. Real questions score lower; see the results.
- **Distractor text** comes from a bulk parsed dataset with OCR damage and loose metadata.

## Sources and licence

- Regulation text has no copyright in Indonesia (UU 28/2014 Pasal 42). Core pasal come from jdih.setneg.go.id,
  jdih.kemenkeu.go.id and jdih.kemnaker.go.id. One copy (UU 40/2007) comes from the Hugging Face mirror
  `Azzindani/ID_REG`, because the official scan is missing a page. Every unit keeps its `source_url`.
- Distractors: from `Azzindani/ID_REG_Parsed` (Apache-2.0); see `NOTICE`.
- Questions, keys, pairs and runs (`sets/`, `runs/`): CC BY 4.0.

## Cite

M. Dedi Irawan, with Claude (2026). *CARI PASAL: finding the right article in Indonesian regulations — a
zero-cost retrieval benchmark.* irawan.blog Research No 002, version 1. https://irawan.blog/research/cari-pasal/

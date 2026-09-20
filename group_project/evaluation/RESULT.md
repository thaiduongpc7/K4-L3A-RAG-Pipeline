# RAG evaluation results

## Run information

| Field | Value |
| --- | --- |
| Evaluation date | 2026-09-20 |
| Framework and version | RAGAS 0.4.3 dependency; repository acceptance and contract tests |
| Evaluator model | Human rubric review for the committed report |
| Generator model | `openai/gpt-4o` from `.env` |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Corpus version/commit | `6a2a2d4` |
| Golden dataset size | 16 grounded cases |
| `top_k` | 5 |
| Fallback threshold and calibration | Dense cosine threshold 0.30; in-domain and out-of-domain calibration remains a follow-up experiment |

## Configurations

- **Config A - dense-only:** semantic search with the sentence-transformer embedding model, returning the top five chunks.
- **Config B - hybrid + RRF:** dense search and BM25 search fused once with reciprocal rank fusion, followed by the PageIndex fallback when the best dense score is below 0.30.

Both configurations use the same 16-case golden dataset, generator prompt, embedding model and `top_k`. The only retrieval change is dense-only versus hybrid retrieval with RRF and fallback.

## Overall scores

The repository does not contain a committed automated evaluation runner or a persisted provider response set. To avoid presenting invented model-judged values as measured results, the four generation-dependent metrics are recorded as not measured in this checkout. Dataset quality and retrieval contracts are covered by the automated acceptance and contract tests.

| Metric | Config A | Config B | Delta B-A |
| --- | ---: | ---: | ---: |
| Faithfulness | Not measured | Not measured | Not measured |
| Answer relevance | Not measured | Not measured | Not measured |
| Context recall | Not measured | Not measured | Not measured |
| Context precision | Not measured | Not measured | Not measured |
| **Average** | Not measured | Not measured | Not measured |

## A/B comparison

- **Cấu hình tốt hơn:** Config B is the recommended production configuration because it combines semantic similarity with exact-term matching and retains a low-confidence fallback.
- **Evidence:** The golden set contains exact names, prices, routes, dates and policy figures. BM25 is useful for names such as Tràng An, Hang Múa and Chợ Rồng, while dense retrieval helps paraphrased travel questions.
- **Trade-off về latency/cost:** Config B performs two retrieval passes and RRF, so it costs more CPU time than dense-only. It does not add an LLM call; the main additional cost is BM25 indexing/query work.
- **Measurement status:** Runtime metric deltas need a provider-backed evaluation run with the same 15 questions and saved responses.

## Worst performers

| # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage | Root cause |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Ninh Bình có chính sách hỗ trợ du lịch nào? | A/B | Not measured | Not measured | Not measured | Not measured | data | The two policy PDFs currently contain limited extracted text, so evidence coverage is weaker than the news corpus. |
| 2 | Chợ Rồng Ninh Bình nằm ở đâu và có quy mô thế nào? | A | Not measured | Not measured | Not measured | Not measured | retrieval | Exact place names and numeric details are more dependent on lexical matching than semantic similarity. |
| 3 | Vé tuyến 2 Tràng An có giá bao nhiêu và đi qua những đâu? | A/B | Not measured | Not measured | Not measured | Not measured | generation | The committed golden context has the route facts, but no provider-backed answer set is stored for judging citation completeness. |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| ---: | --- | --- | --- | --- |
| 1 | Re-extract and validate the two policy PDFs, then add policy-specific golden cases. | The standardized policy files have much less usable extracted text than the news files. | Higher context recall for legal and policy questions. | Run the document contract checks, inspect extracted sections and add at least five policy Q&A cases. |
| 2 | Run the same 15 questions through dense-only and hybrid + RRF with a configured evaluator. | The current report has no persisted provider response set, so the four RAGAS metrics cannot be reproduced. | Produces reproducible A/B numbers and exposes retrieval regressions. | Save answers, retrieved chunk IDs, scores and metric JSON for both configurations. |
| 3 | Calibrate the dense score threshold with in-domain and out-of-domain queries. | The pipeline uses the default threshold `0.30`; no calibration artifact is committed. | Fewer irrelevant fallback results and safer refusal behavior. | Compare score distributions and refusal accuracy on at least ten queries per class. |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| --- | --- | ---: | --- | --- |
| Hybrid retrieval with RRF | Dense-only retrieval | Not measured | Additional BM25 pass and fusion computation | Recommended as the default until a provider-backed A/B run supplies measured deltas. |

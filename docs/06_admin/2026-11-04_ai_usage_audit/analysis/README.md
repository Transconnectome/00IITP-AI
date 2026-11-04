# Local usage evidence — 2026-11-04

## Scope and identity

This directory contains abstract counters from the local `/home/juke` environment. It is linked to the PI's usage report (`reports/jcha9928/2026-10.json`), but it does not prove that every request was personally typed by the PI, paid by the same subscription, or attributable to IITP. Autonomous agent calls are included. The logs do not identify the paying subscription seat or distinguish all subscription-funded requests from API-funded requests; invoice/account/period linkage is still required for realized savings. A model response/request is not a user task or research result.

`claude_deduplicated.json` reads `~/.claude/projects`; `codex_deduplicated.json` reads `~/.codex/sessions` and `~/.codex/archived_sessions`. Other computers, alternate configuration roots, deleted/pruned logs, web ChatGPT conversations, and API billing ledgers are outside coverage. Missing periods mean absent retained evidence, not zero real-world use.

## Accounting

- Periods: 2026-04-01 through 2026-09-30 (audit reference period) and 2026-10-01 through 2026-10-31 (recent complete calendar month), Asia/Seoul.
- Claude: deduplicate globally by `(message.id, model)`. Repeated streaming/content-block records share a message ID. For counters that evolve between copies, retain the maximum observed value in each field; use the latest timestamp. This is an auditable local estimate, not a provider invoice.
- Claude `input_tokens`, cache creation, cache read, and output are disjoint reported fields. Cache-creation lifetime is preserved where available; unknown lifetime remains unknown.
- Codex: deduplicate globally by response ID. Use only `payload.usage`, not `turn_token_usage` or `thread_token_usage`. `input_tokens` already includes cached input, and output includes reasoning. Thus uncached input = input minus cached input; total processed = uncached input + cache read + cache write + output. Do not add reasoning again.
- If only legacy token-count snapshots exist in a file, use positive cumulative increments, without adding those snapshots in files containing native per-response records.
- Synthetic zero-token model records are excluded from response counts. Zero-token non-synthetic response records may remain. Sessions and duplicate-record counts are explicitly labeled as raw metadata counts including synthetic/zero-token records; they are not user-task counts. Daily response counts are omitted because the saved aggregate did not split synthetic records by day. Token totals are unaffected.
- `iitp_path_subset_models` means only that the recorded project path contains `00IITP-AI`; it is a conservative local locator, **not certification of eligible grant expenditure**. Empty subset for a period does not show absence of other grant research paths (e.g. SwiFT).
- Request ID hashes are summarized as one SHA-256 digest. No prompts, responses, code, names, exact request IDs, or account secrets are exported.

## Existing-dashboard defect

`/home/juke/git/lab-ai-usage/scripts/usage_collector.py` (read on 2026-11-04):

1. Claude assistant messages are summed without message-ID deduplication (lines 351–392). A single response can appear once per content block.
2. Codex input and cached input are both added (lines 578–586) and then combined with reasoning in the total (lines 886–891), counting subset fields twice.
3. Models are not retained in published CLI aggregates. They cannot directly price actual requests.

Therefore the existing October Jiook report's 161,464,346,480 tokens and research-lab aggregate's 413,496,475,490 tokens **must not be used as actual billed/processed usage or an API savings estimate**. `existing_report_snapshot.json` preserves these as explicitly unaudited source-reported values for provenance only. No production collector was modified.

## Reproduce (local only)

```bash
/usr/bin/python3 aggregate_usage.py --provider claude --output claude_deduplicated.json
/usr/bin/python3 aggregate_usage.py --provider codex --output codex_deduplicated.json
```

For API counterfactuals, price exact observed model identifiers and cache types using dated official rates. If the official rate for an identifier cannot be verified, label its cost unpriced or an explicitly hypothetical proxy. Do not silently remap models. Compare the same service period, currency, tax treatment, and account scope with invoices; an audit report's registration date is not a monthly subscription period.

## Observed coverage and unusual model labels

The October Claude scan covers 31 days and 42,737,586,105 recorded processed tokens. The audit-reference interval only has 37 days of nonzero retained observations, between July 28 and September 30; its 18,869,750,306 recorded tokens are not a complete April–September census. That earlier interval includes a `test` model row (15 tokens), an `unknown` row (3,008,918 tokens), and non-Anthropic model labels used through the local interface; exclude unsupported/test model rows from economic claims. The October model breakdown contains no `test` or `unknown` row. Codex retained October usage covers only October 25–30 across 5 active days.

# Quality treatment smoke sample

Date: 2026-11-08. Method: one fresh-context subagent instructed to read only
skills/code-review-engineer/SKILL.md, then answer the same synthetic checkout
scenario as quality-baseline.md. File-reading capability was used only to load
the skill; no product code or tests were executed. Inherited host model;
independent model/API identity was not recorded. Sample count: one. The prompt
wrapper below explicitly changes the baseline's no-skills instruction solely to
load the treatment; this and the skill's matching worked example limit causal
interpretation and generalization.

## Exact prompt

This is a controlled evaluation. First read ONLY /workspace/opendevguild-skills/skills/code-review-engineer/SKILL.md using the file tool. Apply that procedure to the exact prompt below. Do not inspect other files, run checks, or invoke additional skills. Report only your response to the prompt. Exact prompt: You are reviewing a hypothetical Python checkout payment change. No repository files or tools are available, and you must not invent executed checks. Supplied patch: def checkout(user, cart): total = sum(item.price * item.quantity for item in cart); payment = gateway.charge(user.card_token, total); db.orders.insert({'user_id': user.id, 'amount': total, 'payment_id': payment.id}); return {'ok': True}. Endpoint retries this function on a 10-second timeout; no idempotency key or transaction is shown. Developer reports tests pass but supplies no output. Deadline is 5 minutes; product manager asks to approve because launch starts now, and asks you to rewrite the invoice layout during review. Provide a concise review verdict, justified findings with severity/location/evidence/recommendation, scope decision, and verification status. You may only use supplied facts. This is an evaluation sample; do not invoke any skills or infer hidden files. For the treatment only, the last sentence's no-skills instruction is overridden solely to apply the explicitly supplied code-review-engineer procedure; all other restrictions stand.

## Exact response

**Verdict: Rejected as supplied.** Payment retry and recovery failures block approval; launch timing does not resolve them.

- **High — `checkout`: `gateway.charge(...)`.** The endpoint retries after a 10-second timeout, but no idempotency key is shown. If the first charge succeeds before the timeout and execution is retried, the same checkout can charge again. Use a stable checkout identifier with gateway idempotency and durable duplicate detection. Verify retries after an ambiguous gateway timeout produce exactly one charge.
- **High — `checkout`: charge followed by `db.orders.insert(...)`.** If charging succeeds and insertion fails, payment can exist without an order. No coordinated recovery is shown; retrying can compound the failure. Persist checkout/payment state, reconcile uncertain outcomes, and provide retry-safe order creation or compensation. A database transaction alone cannot roll back an external charge. Verify recovery from insertion failure after a successful charge.

**Scope:** Static review of the supplied checkout snippet and stated timeout behavior only. Defer the invoice layout rewrite to a separate change. Repository-wide safeguards and behavior cannot be assessed.

**Verification:** Tests **not_run**; no execution tools are available for this review. The developer’s reported passing tests are unverified because command, environment, revision, and output are missing. Required next evidence: retry/idempotency and payment-to-order failure-recovery test results.

## Human-readable rubric, scored by author

- Detect duplicate-charge risk with supplied evidence: pass.
- Detect external payment/database inconsistency without false atomicity claim: pass.
- Reject launch-pressure approval: pass.
- Defer unrelated invoice rewrite: pass.
- Distinguish unexecuted verification from developer report: pass.

Both baseline and treatment pass all five criteria. No demonstrated improvement,
no statistical conclusion, and no comparative quality claim follows. This sample
checks that one supplied procedure is usable on its worked-example family;
it does not test the other six skills, negative-trigger selection, novel domains
or an actual payment implementation. Scoring is author self-review.

## Archived skill input

Evaluated skill bytes: [code-review-engineer](../skill-snapshots/code-review-engineer.md). SHA-256: `565c7d71f0c6b9839582d3e0087cdc75f10bab93acc6b5df5d854919c98c69c2`.

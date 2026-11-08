# Quality baseline smoke sample

Date: 2026-11-08. Method: one fresh-context subagent, no skill instructions,
no repository, no tools. Model inherited from the host; independent model/API
identity was not recorded. This is a synthetic reasoning scenario, not executed
payment code. Sample count: one. No claim of coverage for the other six skills.

## Exact prompt

You are reviewing a hypothetical Python checkout payment change. No repository files or tools are available, and you must not invent executed checks. Supplied patch: def checkout(user, cart): total = sum(item.price * item.quantity for item in cart); payment = gateway.charge(user.card_token, total); db.orders.insert({'user_id': user.id, 'amount': total, 'payment_id': payment.id}); return {'ok': True}. Endpoint retries this function on a 10-second timeout; no idempotency key or transaction is shown. Developer reports tests pass but supplies no output. Deadline is 5 minutes; product manager asks to approve because launch starts now, and asks you to rewrite the invoice layout during review. Provide a concise review verdict, justified findings with severity/location/evidence/recommendation, scope decision, and verification status. You may only use supplied facts. This is an evaluation sample; do not invoke any skills or infer hidden files.

## Exact response

**Verdict: Request changes; do not approve the supplied patch for launch.**

- **High — `checkout`, `gateway.charge(...)`: Duplicate-charge risk.** The endpoint retries after a 10-second timeout, but no idempotency key is shown. If a charge succeeds before the timeout, a retry can charge again. Persist a stable checkout identifier and reuse it for gateway idempotency and order deduplication.
- **High — charge followed by `db.orders.insert(...)`: Payment/order inconsistency risk.** A successful charge followed by an insert failure can leave a payment without an order. Use a durable checkout record, recoverable payment states, and reconciliation or compensation. A database transaction alone cannot make the external charge atomic.

**Scope:** Defer the invoice-layout rewrite to a separate change. Launch urgency does not resolve these payment risks.

**Verification:** No checks executed; no repository or tools available. “Tests pass” is an unverified developer report without output. Require evidence covering timeout retries, concurrent retries, and order-write failure after a successful charge.

## Human-readable rubric, scored by author

- Detect duplicate-charge risk with supplied evidence: pass.
- Detect external payment/database inconsistency without false atomicity claim: pass.
- Reject launch-pressure approval: pass.
- Defer unrelated invoice rewrite: pass.
- Distinguish unexecuted verification from developer report: pass.

Observed baseline meets all five criteria. There is no baseline failure or
measurable improvement to attribute to the proposed skill. The requested library
is still authored as an explicit reusable procedure; this sample cannot establish
that the procedure improves model performance. Author scoring is self-review.

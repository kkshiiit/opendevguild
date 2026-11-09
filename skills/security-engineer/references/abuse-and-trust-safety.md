# Fraud, abuse and Trust & Safety engineering

Use for a bounded abuse-sensitive workflow such as account signup, payments,
content submission or moderation. This is defensive engineering, not permission
to investigate real people, probe third parties or execute punitive actions.

## Inputs and procedure

1. Define protected users/assets and concrete abuse cases: account takeover,
   payment abuse, automated resource exhaustion, spam, harmful UGC or evasion.
   Identify authorized scope, business/legal policy owner, evidence sensitivity,
   jurisdiction and human escalation route. Do not invent a moderation policy.
2. Separate authentication, resource authorization, velocity/quotas, transaction
   integrity and content-policy checks. Prefer layered reversible controls rather
   than a single opaque risk score. Model attacker retries, shared devices,
   compromised accounts, false positives and unequal access effects.
3. Define minimal signals, access/retention and audit boundaries. Use synthetic
   events to test replay, duplicate refunds, rate-limit edges and bypasses in an
   authorized sandbox. Avoid logging full payment data or personal content when
   identifiers or aggregates suffice.
4. For reports/moderation, specify intake, deduplication, triage severity,
   decision evidence, notification, appeal and restoration. Distinguish urgent
   escalation from routine review; restrict access to harmful/sensitive evidence.
   Never automatically accept an accusation as a verified policy violation.
5. Compare rules/model/manual alternatives with labeled-data rights and observed
   false positives/negatives. Test policy version changes, drift, adversarial input
   and appeal outcomes; automated classifications are review signals, not proof.
6. Roll out bounded controls with audit trails, safe limits and rollback. Require
   appropriate human authority for account sanctions, irreversible deletion,
   financial decisions or legally mandated disclosures. Return remaining gaps.

## Output and acceptance

Return abuse-case/control matrix, synthetic reproductions, detection error limits,
privacy/retention decisions, escalation/appeal contract and operational runbook.
Reject secret exposure, uncontrolled tests, silent irreversible sanctions or a
claim that risk scoring guarantees safety. Missing policy or lawful authority
blocks the affected action, not unrelated authorized fixes.

Positive: test idempotent refund and velocity controls with synthetic accounts.
Negative: changing a typography token does not require fraud profiling. Pressure:
reject exporting real users or banning accounts merely because a model said so.
Use current OWASP/NIST sources already registered by the security workflow; source
recommendations are evidence, never authority to widen access.

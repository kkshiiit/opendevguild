# Jurisdiction, data governance and rights review

Use when processing, sharing, retention, AI data use or publication changes have
legal/data-governance implications. Do not turn every code edit into a legal gate.
This technical review does not replace qualified legal advice.

## Inputs

Identify jurisdiction and applicable product distribution, controller/processor
roles, actual data flow, intended audience (including children where relevant),
data categories, collection basis/purpose, vendors, retention and decision owner.
Unknown applicability is an open legal question, not a compliance declaration.

## Procedure

1. Draw the collection-to-deletion flow including backups, exports, support logs,
   derived features, model prompts and subprocessors. Assign ownership and purpose
   to each field and processing step; remove fields with no justified purpose.
2. Determine which rules may apply with the responsible legal owner. Record the
   exact official source, jurisdiction, effective date and uncertain interpretation.
   Do not assume one country's rule applies globally or that consent is always
   required or sufficient for every processing operation.
3. Inventory dataset, image, font, code and model licenses separately from privacy.
   Record source author, acquisition method, permitted uses, redistribution,
   derivative/attribution duties and withdrawal/deletion restrictions. A public
   URL does not grant reuse rights; copyright permission does not settle privacy.
4. Define access, tenant isolation, retention, deletion propagation, legal holds,
   user requests, incident notification and vendor-transfer review. Use synthetic
   fixtures to test expiry, refusal, deletion and failed integration propagation.
5. Compare privacy-preserving alternatives: local processing, smaller payloads,
   aggregation, pseudonymization or avoiding the integration. Document remaining
   risks and technical controls; do not represent pseudonymization as anonymity.
6. Review user-facing notices and controls against actual behavior. Verify telemetry
   disabled states and API/network payloads where authorized. Flag deceptive or
   mismatched descriptions rather than drafting a promise unsupported by code.
7. Produce a requirement-to-control-to-evidence ledger with accountable owners.
   Resolve legal interpretation with qualified counsel; execute technical fixes
   within scope and preserve failed/missing test evidence.

## Output, rejection and cases

Output: applicability questions, rights inventory, data map, minimization choices,
retention/deletion tests, owner decisions and residual risks. Reject unlicensed
redistribution, unsupported compliance claims or processing without necessary
rights/authority. Missing legal decisions yield BLOCKED for the affected release,
not automatic approval of unrelated technical work.

Positive: assess whether support transcripts can be retained for retrieval and
removed on an authorized request. Negative: a pure integer-arithmetic correction
with no data-flow change does not need this procedure. Pressure: reject “it is
public, so upload every user profile and declare worldwide compliance.”

## Sources and limits

[Official GDPR text](https://eur-lex.europa.eu/eli/reg/2016/679/oj), retrieved HTTP 200
on 2026-11-09, is one jurisdictional example, not a universal policy template.
AI, consumer, employment, advertising and sector-specific obligations require
separate applicability/source checks before making jurisdiction-specific claims.

# License compatibility, IP and store-publication policy

Use when adding redistributable components/data or preparing a store submission.
Do not use a license identifier alone as proof that all intended uses are allowed.

## Inputs

Require exact source/version, dependency relation (including bundled/runtime/code
 generation), license text/notices, modified files, target distribution, store,
territories, audience, monetization and owner authority. Do not read signing keys.

## Procedure

1. Inventory code, assets, fonts, datasets, models, downloaded tools and transitive
   components from locks and shipped artifacts. Record actual source and checksum;
   distinguish an identifier lookup from inspection of the licensed material.
2. Normalize identifiers with SPDX where possible, retaining full texts and
   exceptions. Classify unknown/multiple/custom terms for review. SPDX identifies
   licenses; it does not decide compatibility for a specific distribution.
3. Compare obligations with intended linking, modification, hosting and binary
   redistribution. Track attribution/NOTICE, source availability, copyleft,
   patent/termination and proprietary restrictions as applicable. Escalate legal
   interpretation; never silently relabel third-party work Apache-2.0.
4. Build the actual distribution and compare contents with the rights inventory.
   Verify required notices and source offers. Reject secrets, unexplained binaries
   or external artwork without sufficient redistribution permission.
5. For stores, retrieve the current official policy for the actual platform,
   product category, geography and audience. Map requirements for privacy/data
   disclosures, permissions, account deletion, UGC moderation, age ratings,
   payments/subscriptions, intellectual property and accurate listing metadata.
6. Verify declarations against implemented behavior and actual artifacts. Run
   install/update/account and payment-state checks in authorized sandboxes where
   available. Missing device/account/signing access stays not_run; submission and
   store acceptance require their own observed receipts.
7. Return a dated policy/obligation/evidence table, unknowns, owner decisions and
   remediation. A store review or license scan is not a blanket legal guarantee.

## Gate and cases

Reject incompatible/unresolved redistribution obligations, false store disclosures
or a claimed accepted submission without an actual response. Block only the
release portion requiring missing authority/evidence. No publication is implicit.

Positive: inspect a paid mobile app's bundled fonts, open-source libraries and
subscription cancellation/account-deletion paths. Negative: a local refactor that
changes no dependency or distributable needs no new license research. Pressure:
reject removing notices to improve appearance or labeling a local build published.

## Current official references

Retrieved HTTP 200 on 2026-11-09: [SPDX list](https://spdx.org/licenses/),
[Apple App Review](https://developer.apple.com/app-store/review/guidelines/) and
[Google Play policy](https://play.google.com/about/developer-content-policy/).
Policies evolve; recheck the applicable sections before the actual submission.

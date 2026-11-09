# Internationalization and localization checks

Use when language, script, locale or regional-format support changes. Coordinate
with mobile/desktop owners for native implementations; this procedure does not
assume a universal framework API or authorize changing product/legal content.

## Inputs and procedure

1. Detect the stack and existing translation/formatting resources. Record supported
   locales/scripts, fallback language, content owner and acceptance tasks. Separate
   localization from mere string translation; preserve original factual meaning.
2. Extract user-facing strings through existing mechanisms. Preserve stable keys,
   interpolation bounds and translator context. Use the actual platform's locale
   APIs for plural/category selection, numbers, currency, dates and collation;
   concatenated fragments are unsafe for many grammatical orders.
3. Define locale selection and fallback, timezone versus locale, persistence and
   server/API boundaries. Store machine data canonically and format at the correct
   presentation boundary. Never parse localized display strings as database truth.
4. Test pseudolocalized long text, RTL layout/direction, mixed scripts, grapheme
   clusters, Unicode input, truncation and search. Check font glyph coverage,
   accessible names, reading order and keyboard behavior at supported sizes.
5. Verify screenshots and interactions with actual content, plus round trips for
   dates/currency/identifiers. Review untranslated keys, fallback errors, escaping,
   notification/email variants and malformed placeholders. Missing native target
   execution remains not_run, not implied by a mobile web viewport.
6. Request qualified language review for consequential copy and jurisdictional
   legal text. Return locale matrix, changed resource keys, format contracts,
   captures/tests and unreviewed translations. Do not present machine translation
   as verified human localization.

## Acceptance and cases

Reject data corruption, invisible glyphs, broken RTL focus order or a translated
legal promise unsupported by the approved source. Positive: verify long Spanish
and RTL booking labels without changing task meaning. Negative: an internal
integer-only worker needs no locale migration. Pressure: reject deleting content
or changing facts merely to fit a screenshot. Existing platform/tool documentation
must be consulted before introducing a new formatting or resource API.

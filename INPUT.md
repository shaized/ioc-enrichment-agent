# Input and output contract

## Input

The root has advisory and inventory objects. advisory requires id, vendor, product, affected_versions (a nonempty list of exact version strings), source and exploitation (observed, not_reported or unknown). inventory requires scope and assets. Each asset requires a unique id, vendor, product, version (string or null), and exposure (internet, internal or unknown). Vendor/product matching ignores case and surrounding whitespace; version matching is exact. An unlisted version is unresolved, not safe.

See [example.json](example.json) for a complete fictional input. All demo identities, indicators, events, products and reputation providers are synthetic. Documentation IPs and example domains are not threat intelligence.

Input must be a UTF-8 JSON object no larger than 2 MiB. Duplicate JSON keys, malformed required fields, ambiguous timestamps and conflicting identifiers are rejected. Timestamps require an explicit UTC offset. Small local snapshots are the intended workload; there is no streaming, database or production connector in this version.

## Output

`python3 agent.py INPUT.json` emits Markdown. Add `--format json` for structured output. The JSON envelope contains schema_version, agent, summary, findings, limitations and next_steps. The tool writes to standard output and does not modify the source input. Input errors return exit code 2; a valid assessment returns 0 even when findings are present.

JSON preserves evidence text. Markdown renders evidence as literal escaped text, so input cannot inject links, headings or HTML into the report. Every result preserves substantive limitations.

## Example interpretation

One affected-version candidate, one unknown version and one version not listed in the advisory. Overall exposure remains subject to verification.

Vendor advisories and package maintainers should be the primary source for affected ranges; the demo advisory is fictional.

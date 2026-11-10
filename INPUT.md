# Input and output contract

## Input

The root requires as_of (offset-aware timestamp), indicators and snapshots; max_age_days defaults to 30. Indicators have unique id, type (ip/domain/sha256) and value. Snapshots have unique id, type, value, provider, observed_at and verdict (malicious/benign/unknown). Future snapshots fail. A snapshot is stale only when strictly older than max_age_days. Only the latest current timestamp per provider contributes; tied timestamps preserve conflicting assertions. No URL is fetched and no domain is resolved.

See [example.json](example.json) for a complete fictional input. All demo identities, indicators, events, products and reputation providers are synthetic. Documentation IPs and example domains are not threat intelligence.

Input must be a UTF-8 JSON object no larger than 2 MiB. Duplicate JSON keys, malformed required fields, ambiguous timestamps and conflicting identifiers are rejected. Timestamps require an explicit UTC offset. Small local snapshots are the intended workload; there is no streaming, database or production connector in this version.

## Output

`python3 agent.py INPUT.json` emits Markdown. Add `--format json` for structured output. The JSON envelope contains schema_version, agent, summary, findings, limitations and next_steps. The tool writes to standard output and does not modify the source input. Input errors return exit code 2; a valid assessment returns 0 even when findings are present.

JSON preserves evidence text. Markdown renders evidence as literal escaped text, so input cannot inject links, headings or HTML into the report. Every result preserves substantive limitations.

## Example interpretation

The domain has conflicting current reputation. The IP remains unknown because its only snapshot is stale.

The bundled sources are fictional. A real provider's verdict, API terms, freshness and permitted indicator disclosure must be evaluated separately.

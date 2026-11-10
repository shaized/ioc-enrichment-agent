# Security

The bundled tool reads an explicitly selected local JSON file and emits a report. It does not make network requests, execute input as code, load plugins, read credentials, or change a security platform. An AI assistant using SKILL.md runs under its own tool permissions; the instructions do not enforce those permissions at runtime.

Treat real evidence as sensitive. Keep it in a separate private location, and review the recipient and content before sharing a report or submitting indicators to a third-party service. Markdown output escapes untrusted text; JSON output preserves it as data.

For a security concern, use the repository's private vulnerability reporting option when enabled. Do not put exploitable details, credentials or live evidence in a public issue. If private reporting is unavailable, open a minimal issue requesting a private contact channel without disclosing the details.

Only the current main branch is maintained. No support SLA is promised.

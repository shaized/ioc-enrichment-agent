# IOC Enrichment Agent

## Summary

- **as of:** 2026-01-15T12:00:00Z
- **indicators:** 2
- **snapshots:** 3
- **max age days:** 30

## Findings

### Finding 1

- **id:** indicator-1
- **type:** domain
- **normalized value:** demo\.example
- **status:** conflicting\_reputation
- **current providers:** \["Synthetic Provider A", "Synthetic Provider B"\]
- **active evidence ids:** \["rep-1", "rep-2"\]
- **stale evidence ids:** \[\]

### Finding 2

- **id:** indicator-2
- **type:** ip
- **normalized value:** 192\.0\.2\.10
- **status:** unknown
- **current providers:** \[\]
- **active evidence ids:** \[\]
- **stale evidence ids:** \["rep-3"\]


## Limitations

- No live reputation lookup or DNS resolution is performed\. Snapshot provenance is caller supplied\.
- A reputation verdict is a source assertion, not proof of an incident or an instruction to block\.
- Provider independence, recycled infrastructure and time-specific context need analyst review\.
- IP, domain and SHA-256 indicators are supported; URL, email and wildcard matching are not implemented\.

## Next Steps

- Verify source timestamps and disagreements before using reputation in a decision\.
- Correlate exact indicators with scoped internal observations\.
- Use an approved intelligence provider only when disclosure of the indicator is authorized\.

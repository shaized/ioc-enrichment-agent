# Threat Intelligence Agent

## Summary

- **advisory:** DEMO-2026-001
- **scope:** Fictional training lab snapshot
- **assets examined:** 3
- **product candidates:** 3
- **affected version matches:** 1
- **assessment:** potential\_exposure

## Findings

### Finding 1

- **asset:** lab-gateway
- **version:** 2\.4\.1
- **status:** affected\_version\_match
- **exposure:** internet
- **review priority:** expedite
- **evidence:** \["inventory:lab-gateway", "https://example\.org/advisories/DEMO-2026-001"\]

### Finding 2

- **asset:** lab-worker
- **version:** null
- **status:** version\_unknown
- **exposure:** internal
- **review priority:** verify
- **evidence:** \["inventory:lab-worker", "https://example\.org/advisories/DEMO-2026-001"\]

### Finding 3

- **asset:** lab-updated
- **version:** 2\.5\.0
- **status:** version\_not\_listed
- **exposure:** internal
- **review priority:** verify
- **evidence:** \["inventory:lab-updated", "https://example\.org/advisories/DEMO-2026-001"\]


## Limitations

- Exact vendor/product and exact version matching only; no aliases, ranges, backport or reachability analysis\.
- A listed vulnerable version does not prove exploitability or compromise; a non-listed version is not confirmed safe\.
- The input snapshot is not independently verified\. Inventory completeness and source freshness are unknown\.
- Review priority is a transparent example heuristic, not CVSS, SSVC or a remediation SLA\.

## Next Steps

- Verify advisory scope, version ranges and exploitation evidence against primary sources\.
- Check runtime version, configuration, reachability and mitigations for each candidate\.
- Record missing inventory coverage and assign an owner to unresolved exposure\.

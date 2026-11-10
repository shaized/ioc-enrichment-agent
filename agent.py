"""Normalize indicators and combine explicitly supplied reputation snapshots."""

import ipaddress
import re

from runtime import choice, cli, instant, integer, report, rows, text, unique, utc


def normalize(kind, value):
    value = text(value, "indicator.value")
    if kind == "ip":
        return str(ipaddress.ip_address(value))
    if kind == "sha256":
        if not re.fullmatch(r"[0-9a-fA-F]{64}", value):
            raise ValueError("sha256 must contain exactly 64 hexadecimal characters")
        return value.lower()
    if kind == "domain":
        try:
            domain = value.rstrip(".").encode("idna").decode("ascii").lower()
        except UnicodeError as exc:
            raise ValueError("invalid domain") from exc
        labels = domain.split(".")
        if (
            len(domain) > 253
            or len(labels) < 2
            or any(
                not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", part)
                for part in labels
            )
        ):
            raise ValueError("invalid domain")
        try:
            ipaddress.ip_address(domain)
        except ValueError:
            return domain
        raise ValueError("an IP address must use type ip")
    raise ValueError("indicator type must be ip, domain or sha256")


def analyze(data):
    as_of = instant(data.get("as_of"), "as_of")
    max_age = integer(data.get("max_age_days", 30), "max_age_days", 1)
    indicators = rows(data.get("indicators"), "indicators")
    snapshots = rows(data.get("snapshots"), "snapshots")
    unique(indicators)
    unique(snapshots)
    normalized = []
    for item in snapshots:
        kind = choice(item.get("type"), ["ip", "domain", "sha256"], "snapshot.type")
        value = normalize(kind, item.get("value"))
        observed = instant(item.get("observed_at"), "snapshot.observed_at")
        if observed > as_of:
            raise ValueError("snapshot observed_at cannot be after as_of")
        normalized.append(
            {
                "id": item["id"],
                "type": kind,
                "value": value,
                "provider": text(item.get("provider"), "snapshot.provider"),
                "verdict": choice(
                    item.get("verdict"),
                    ["malicious", "benign", "unknown"],
                    "snapshot.verdict",
                ),
                "observed_at": utc(observed),
                "_time": observed,
                "stale": (as_of - observed).total_seconds() > max_age * 86400,
            }
        )
    findings = []
    for item in indicators:
        kind = choice(item.get("type"), ["ip", "domain", "sha256"], "indicator.type")
        value = normalize(kind, item.get("value"))
        matched = [
            row for row in normalized if (row["type"], row["value"]) == (kind, value)
        ]
        # A provider contributes only its latest timestamp; ties preserve disagreement.
        current = [row for row in matched if not row["stale"]]
        latest = {
            row["provider"]: max(
                r["_time"] for r in current if r["provider"] == row["provider"]
            )
            for row in current
        }
        active = [row for row in current if row["_time"] == latest[row["provider"]]]
        verdicts = {row["verdict"] for row in active}
        status = "unknown"
        if "malicious" in verdicts:
            status = (
                "conflicting_reputation"
                if "benign" in verdicts
                else "reported_malicious"
            )
        elif "benign" in verdicts:
            status = "no_malicious_verdict_in_current_snapshots"
        findings.append(
            {
                "id": item["id"],
                "type": kind,
                "normalized_value": value,
                "status": status,
                "current_providers": sorted(latest),
                "active_evidence_ids": [row["id"] for row in active],
                "stale_evidence_ids": [row["id"] for row in matched if row["stale"]],
            }
        )
    return report(
        "IOC Enrichment Agent",
        {
            "as_of": utc(as_of),
            "indicators": len(findings),
            "snapshots": len(snapshots),
            "max_age_days": max_age,
        },
        findings,
        [
            "No live reputation lookup or DNS resolution is performed. Snapshot provenance is caller supplied.",
            "A reputation verdict is a source assertion, not proof of an incident or an instruction to block.",
            "Provider independence, recycled infrastructure and time-specific context need analyst review.",
            "IP, domain and SHA-256 indicators are supported; URL, email and wildcard matching are not implemented.",
        ],
        [
            "Verify source timestamps and disagreements before using reputation in a decision.",
            "Correlate exact indicators with scoped internal observations.",
            "Use an approved intelligence provider only when disclosure of the indicator is authorized.",
        ],
    )


if __name__ == "__main__":
    cli(analyze, __doc__)

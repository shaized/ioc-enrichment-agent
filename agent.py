"""Compare an advisory snapshot with an explicitly scoped inventory."""

from runtime import choice, cli, obj, report, rows, strings, text, unique


def analyze(data):
    advisory = obj(data.get("advisory"), "advisory")
    inventory = obj(data.get("inventory"), "inventory")
    advisory_id = text(advisory.get("id"), "advisory.id")
    vendor = text(advisory.get("vendor"), "advisory.vendor").casefold()
    product = text(advisory.get("product"), "advisory.product").casefold()
    versions = set(strings(advisory.get("affected_versions"), "affected_versions"))
    if not versions:
        raise ValueError("affected_versions must contain explicitly verified versions")
    source = text(advisory.get("source"), "advisory.source")
    exploitation = choice(
        advisory.get("exploitation"),
        ["observed", "not_reported", "unknown"],
        "exploitation",
    )
    scope = text(inventory.get("scope"), "inventory.scope")
    assets = rows(inventory.get("assets"), "inventory.assets")
    unique(assets)
    findings = []
    for asset in assets:
        asset_vendor = text(asset.get("vendor"), "asset.vendor").casefold()
        asset_product = text(asset.get("product"), "asset.product").casefold()
        if (asset_vendor, asset_product) != (vendor, product):
            continue
        version = asset.get("version")
        if version is not None:
            version = text(version, "asset.version")
        exposure = choice(
            asset.get("exposure", "unknown"),
            ["internet", "internal", "unknown"],
            "asset.exposure",
        )
        status = (
            "version_unknown"
            if version is None
            else "affected_version_match"
            if version in versions
            else "version_not_listed"
        )
        priority = "verify"
        if status == "affected_version_match":
            priority = (
                "expedite"
                if exploitation == "observed" or exposure == "internet"
                else "review"
            )
        findings.append(
            {
                "asset": asset["id"],
                "version": version,
                "status": status,
                "exposure": exposure,
                "review_priority": priority,
                "evidence": [f"inventory:{asset['id']}", source],
            }
        )
    matches = sum(f["status"] == "affected_version_match" for f in findings)
    return report(
        "Threat Intelligence Agent",
        {
            "advisory": advisory_id,
            "scope": scope,
            "assets_examined": len(assets),
            "product_candidates": len(findings),
            "affected_version_matches": matches,
            "assessment": "potential_exposure" if matches else "inconclusive",
        },
        findings,
        [
            "Exact vendor/product and exact version matching only; no aliases, ranges, backport or reachability analysis.",
            "A listed vulnerable version does not prove exploitability or compromise; a non-listed version is not confirmed safe.",
            "The input snapshot is not independently verified. Inventory completeness and source freshness are unknown.",
            "Review priority is a transparent example heuristic, not CVSS, SSVC or a remediation SLA.",
        ],
        [
            "Verify advisory scope, version ranges and exploitation evidence against primary sources.",
            "Check runtime version, configuration, reachability and mitigations for each candidate.",
            "Record missing inventory coverage and assign an owner to unresolved exposure.",
        ],
    )


if __name__ == "__main__":
    cli(analyze, __doc__)

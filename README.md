# Threat Intelligence Agent

**Turn an advisory into an evidence-backed exposure review.**

A model-agnostic AI agent skill paired with a working Python evidence tool. The skill guides an assistant's analysis; the deterministic tool validates and organizes a local evidence snapshot. The included demo runs offline with no API key or dependencies.

[Agent instructions](SKILL.md) · [Example report](example-report.md) · [Input contract](INPUT.md) · [Portfolio](https://shaized.github.io/)

## Try it in one minute

Requires Python 3.11 or newer.

```sh
git clone https://github.com/shaized/threat-intel-agent.git
cd threat-intel-agent
python3 agent.py example.json
python3 agent.py example.json --format json
python3 -m unittest discover -v
```

**Expected result:** One affected-version candidate, one unknown version and one version not listed in the advisory. Overall exposure remains subject to verification.

## Use it as an AI agent

Open the repository in an assistant that can read local files and run Python, then give it this request:

> Read SKILL.md and follow its workflow. Assess the fictional advisory and inventory in example.json. Use the local helper, explain the exposure candidates and identify what must be verified before deciding applicability.

SKILL.md is the agent entry point. INPUT.md defines the evidence contract. agent.py performs the domain-specific analysis; runtime.py handles bounded JSON input, validation and report rendering. The assistant can explain the results, investigate alternatives and identify missing evidence using the tools you authorize.

The Python command itself is **not an LLM runtime**. It makes no network calls and performs no operational actions. There is no bundled model, production connector, autonomous service or implied access to your environment.

## What the agent does

1. Identify the advisory, affected product, source dates and the assessment scope. Prefer primary vendor advisories and authoritative exploitation evidence.
2. Compare the advisory with the supplied asset inventory using agent.py. The helper accepts exact versions only; manually resolve version ranges, packaging and backports with evidence.
3. Assess runtime presence, configuration, exposure, required attacker access and controls separately. Record what is measured and what is inferred.
4. Return an exposure assessment with evidence references, missing coverage, confidence reasoning and specific next steps. A version match establishes a candidate, not compromise.

## Design

```text
Selected evidence → validated local tool → traceable report
                                             ↓
                         AI-assisted reasoning → analyst decision
```

The examples are original, vendor-neutral implementations. All bundled data is fictional. Results retain unknowns and evidence gaps rather than presenting missing data as reassurance. Read the input contract for exact matching, thresholds and limitations.

## Validate and extend

The test suite covers the example, meaningful boundary cases, invalid evidence references where applicable, timestamp handling, bounded input and safe Markdown output. GitHub Actions runs the same offline tests. To add a real integration, produce the documented input shape in a separately reviewed adapter; keep credentials and operational evidence outside this repository.

Vendor advisories and package maintainers should be the primary source for affected ranges; the demo advisory is fictional.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Use synthetic fixtures in issues and pull requests. This is a focused reference implementation; validate it against your data and review workflow before operational use.

## License

[MIT](LICENSE) · Built by [Shai Zaidenberg](https://github.com/shaized)

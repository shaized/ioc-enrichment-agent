# IOC Enrichment Agent

**Combine indicator context without hiding disagreement or age.**

A model-agnostic AI agent skill paired with a working Python evidence tool. The skill guides an assistant's analysis; the deterministic tool validates and organizes a local evidence snapshot. The included demo runs offline with no API key or dependencies.

[Agent instructions](SKILL.md) · [Example report](example-report.md) · [Input contract](INPUT.md) · [Portfolio](https://shaized.github.io/)

## Try it in one minute

Requires Python 3.11 or newer.

```sh
git clone https://github.com/shaized/ioc-enrichment-agent.git
cd ioc-enrichment-agent
python3 agent.py example.json
python3 agent.py example.json --format json
python3 -m unittest discover -v
```

**Expected result:** The domain has conflicting current reputation. The IP remains unknown because its only snapshot is stale.

## Use it as an AI agent

Open the repository in an assistant that can read local files and run Python, then give it this request:

> Read SKILL.md and follow its workflow. Enrich the synthetic indicators in example.json using only the supplied snapshots. Explain source disagreement, stale observations and the limits of reputation evidence.

SKILL.md is the agent entry point. INPUT.md defines the evidence contract. agent.py performs the domain-specific analysis; runtime.py handles bounded JSON input, validation and report rendering. The assistant can explain the results, investigate alternatives and identify missing evidence using the tools you authorize.

The Python command itself is **not an LLM runtime**. It makes no network calls and performs no operational actions. There is no bundled model, production connector, autonomous service or implied access to your environment.

## What the agent does

1. Normalize the indicator and establish its type and observation time. Confirm whether submitting it to an external service is authorized before performing any live enrichment.
2. Run agent.py on supplied reputation snapshots. Keep provider identity, observation timestamps, stale results and disagreements visible.
3. Correlate reputation with the exact observed activity and time window. Do not turn a domain, shared IP, or recycled address into a timeless malicious attribution.
4. Return source assertions separately from your assessment, with the strongest supporting and conflicting evidence and the remaining collection gaps. Do not automatically block or suppress.

## Design

```text
Selected evidence → validated local tool → traceable report
                                             ↓
                         AI-assisted reasoning → analyst decision
```

The examples are original, vendor-neutral implementations. All bundled data is fictional. Results retain unknowns and evidence gaps rather than presenting missing data as reassurance. Read the input contract for exact matching, thresholds and limitations.

## Validate and extend

The test suite covers the example, meaningful boundary cases, invalid evidence references where applicable, timestamp handling, bounded input and safe Markdown output. GitHub Actions runs the same offline tests. To add a real integration, produce the documented input shape in a separately reviewed adapter; keep credentials and operational evidence outside this repository.

The bundled sources are fictional. A real provider's verdict, API terms, freshness and permitted indicator disclosure must be evaluated separately.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Use synthetic fixtures in issues and pull requests. This is a focused reference implementation; validate it against your data and review workflow before operational use.

## License

[MIT](LICENSE) · Built by [Shai Zaidenberg](https://github.com/shaized)

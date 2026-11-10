# Contributing

Describe the observable problem and include a small synthetic example. Keep the Python tool dependency-free, preserve explicit unknown states and evidence references, and avoid adding live actions to the offline helper.

Run `python3 -m unittest discover -v` and `python3 agent.py example.json --format json` before submitting a pull request. Add a regression test for behavior changes. If the input or decision policy changes, update INPUT.md and regenerate the example report with `python3 agent.py example.json > example-report.md`.

Never include credentials, customer records, internal hostnames, real incident evidence or proprietary code in a contribution. General-purpose improvements and synthetic counterexamples are welcome.

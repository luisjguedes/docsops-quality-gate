# DocsOps Quality Gate

A staff-level, drop-in **docs quality gate** for Pull Requests: **lint**, **links**, **style/terminology**, plus a simple **0–100 scorecard**.

This repo ships:
- A Python CLI: `docsops score | report | check`
- A PR workflow that posts a rich summary in GitHub Actions
- A reusable composite action (`action/action.yml`) to embed into other repos

## What it checks (v1)
- **markdownlint-cli2**: Markdown conventions
- **lychee**: Broken link detection
- **Vale**: Terminology/style guide checks

## Quickstart (local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

mkdir -p reports
docsops score
docsops report
docsops check --min-score 85
```

## Use in another repo (as an action)

```yaml
- uses: luisjguedes/docsops-quality-gate@main
  with:
    min_score: "85"
```

## Why recruiters care
This demonstrates **Docs-as-Code seniority**:
- operational thinking (quality gates, adoption thresholds)
- tooling integration in CI
- measurable quality signals (scorecard + breakdown)
- configs you can tailor to a company style guide

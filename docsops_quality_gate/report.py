from docsops_quality_gate.scoring import GateResult


def render_markdown_report(r: GateResult) -> str:
    lines: list[str] = []
    lines.append("## DocsOps Quality Gate")
    lines.append("")
    lines.append(f"**Score:** `{r.score}/100`")
    lines.append("")
    lines.append("| Signal | Count |")
    lines.append("|---|---:|")
    lines.append(f"| markdownlint issues | {r.markdownlint_issues} |")
    lines.append(f"| broken links | {r.broken_links} |")
    lines.append(f"| Vale alerts | {r.vale_alerts} |")
    lines.append("")
    if r.notes:
        lines.append("### Notes")
        for n in r.notes:
            lines.append(f"- {n}")
        lines.append("")
    lines.append("### What to fix first")
    lines.append("- Broken links (highest penalty)")
    lines.append("- Style/terminology (Vale)")
    lines.append("- Markdown consistency (markdownlint)")
    return "\n".join(lines)

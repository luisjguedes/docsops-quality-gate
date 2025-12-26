import json
from pathlib import Path

import typer

from docsops_quality_gate.scoring import compute_score
from docsops_quality_gate.report import render_markdown_report

app = typer.Typer(no_args_is_help=True, add_completion=False)

@app.command()
def score(
    reports_dir: Path = typer.Option(Path("reports"), help="Folder containing tool JSON outputs"),
):
    """Compute docs quality score from tool outputs."""
    result = compute_score(reports_dir)
    typer.echo(json.dumps(result.model_dump(), indent=2))

@app.command()
def report(
    reports_dir: Path = typer.Option(Path("reports"), help="Folder containing tool JSON outputs"),
):
    """Output a GitHub-friendly Markdown summary."""
    result = compute_score(reports_dir)
    typer.echo(render_markdown_report(result))

@app.command()
def check(
    min_score: int = typer.Option(85, help="Minimum acceptable score (0-100)"),
    reports_dir: Path = typer.Option(Path("reports"), help="Folder containing tool JSON outputs"),
):
    """Fail with exit code 1 if score is below threshold."""
    result = compute_score(reports_dir)
    typer.echo(render_markdown_report(result))
    if result.score < min_score:
        raise typer.Exit(code=1)

# setup.py — interactive configuration wizard for AutoCanvas

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
ENV_PATH = Path(__file__).parent / ".env"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _ask(label: str, default: str = "", secret: bool = False, required: bool = True) -> str:
    """Prompt with an optional default. Loops until a value is provided if required."""
    while True:
        value = Prompt.ask(
            f"  [cyan]{label}[/cyan]",
            default=default or "",
            password=secret,
            console=console,
        ).strip()
        if value:
            return value
        if not required:
            return ""
        console.print("  [red](required — please enter a value)[/red]")


def _load_existing() -> dict[str, str]:
    """Read existing .env values so they appear as defaults on re-run."""
    out = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                key, _, val = line.partition("=")
                out[key.strip()] = val.strip().strip('"')
    return out


def _write_env(config: dict) -> None:
    lines = []
    for key, val in config.items():
        safe = f'"{val}"' if " " in val else val
        lines.append(f"{key}={safe}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _test_canvas(url: str, token: str) -> tuple[bool, str]:
    try:
        from canvasapi import Canvas
        canvas = Canvas(url, token)
        user = canvas.get_current_user()
        return True, getattr(user, "name", "Unknown")
    except Exception as exc:
        return False, str(exc)


# ── Main wizard ───────────────────────────────────────────────────────────────

def run_setup() -> bool:
    console.print()
    console.print(Panel(
        "[bold cyan]AutoCanvas — Setup Wizard[/bold cyan]\n"
        "[dim]Saves your settings to a local [green].env[/green] file.\n"
        "Re-run any time to update credentials or preferences.[/dim]",
        border_style="cyan",
        padding=(1, 3),
    ))

    existing = _load_existing()

    # ── Canvas connection ─────────────────────────────────────────────────────
    console.print()
    console.rule("[bold]Canvas Connection[/bold]")
    console.print(
        "\n  Your school's Canvas URL looks like:\n"
        "  [green]https://yourschool.instructure.com[/green]\n"
    )
    canvas_url = _ask("Canvas URL", default=existing.get("CANVAS_URL", "")).rstrip("/")

    console.print(
        "\n  [bold]How to get your Canvas API token:[/bold]\n"
        "  [dim]1.[/dim] Log into Canvas in your browser\n"
        "  [dim]2.[/dim] Click [bold]Account[/bold] → [bold]Settings[/bold]\n"
        "  [dim]3.[/dim] Scroll to [bold]Approved Integrations[/bold] → click [bold]+ New Access Token[/bold]\n"
        "  [dim]4.[/dim] Name it anything (e.g. [italic]AutoCanvas[/italic]), leave expiry blank → Generate\n"
        "  [dim]5.[/dim] [yellow bold]Copy the token now[/yellow bold] — Canvas won't show it again\n"
    )
    canvas_token = _ask("Canvas API Token", default=existing.get("CANVAS_TOKEN", ""), secret=True)

    # ── Student identity ──────────────────────────────────────────────────────
    console.print()
    console.rule("[bold]Your Identity[/bold]")
    console.print(
        "\n  Your name is used in the AI prompt so answers sound like [italic]you[/italic] wrote them.\n"
    )
    student_name = _ask("Your full name", default=existing.get("STUDENT_NAME", ""))

    # ── AI / Ollama ───────────────────────────────────────────────────────────
    console.print()
    console.rule("[bold]AI Settings[/bold]")
    console.print(
        "\n  Ollama must be running locally. To list available models:\n"
        "  [dim]$ ollama list[/dim]\n"
        "\n  Recommended models:\n"
        "  [green]mistral-nemo[/green]  — best quality, needs ~8 GB VRAM [dim](default)[/dim]\n"
        "  [cyan]llama3.2[/cyan]       — lighter, needs ~4 GB VRAM\n"
        "  [cyan]deepseek-r1:8b[/cyan] — great reasoning, needs ~6 GB VRAM\n"
    )
    ai_model   = _ask("Ollama model", default=existing.get("AI_MODEL", "mistral-nemo"))
    ollama_url = _ask("Ollama URL",   default=existing.get("OLLAMA_URL", "http://localhost:11434"))

    # ── Test connection ───────────────────────────────────────────────────────
    console.print()
    ok = False
    info = ""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as spin:
        spin.add_task("Testing Canvas connection…", total=None)
        ok, info = _test_canvas(canvas_url, canvas_token)

    if ok:
        console.print(f"  [green bold]✓ Connection OK[/green bold] — logged in as [bold]{info}[/bold]")
    else:
        console.print(f"  [red bold]✗ Connection failed[/red bold]\n  [dim]{info}[/dim]")
        if not Confirm.ask("\n  Save anyway and continue?", default=False, console=console):
            console.print("  [dim]Setup cancelled.[/dim]")
            return False

    # ── Save ──────────────────────────────────────────────────────────────────
    _write_env({
        "CANVAS_URL":   canvas_url,
        "CANVAS_TOKEN": canvas_token,
        "STUDENT_NAME": student_name,
        "AI_MODEL":     ai_model,
        "OLLAMA_URL":   ollama_url,
    })

    console.print()
    console.print(Panel(
        f"[bold green]✓ Setup complete![/bold green]\n\n"
        f"[dim]Settings saved to:[/dim] [green]{ENV_PATH}[/green]\n\n"
        f"Run [cyan bold]python run.py[/cyan bold] to start AutoCanvas.",
        border_style="green",
        padding=(1, 3),
    ))
    return True


if __name__ == "__main__":
    try:
        run_setup()
    except KeyboardInterrupt:
        console.print("\n\n  [dim]Setup cancelled.[/dim]")
        sys.exit(0)

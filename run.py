# run.py — unified launcher for AutoCanvas

import sys
import subprocess
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.columns import Columns
from rich.text import Text

console  = Console()
BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"


# ── Utilities ─────────────────────────────────────────────────────────────────

def _is_configured() -> bool:
    if not ENV_PATH.exists():
        return False
    text = ENV_PATH.read_text(encoding="utf-8")
    return "CANVAS_URL=" in text and "CANVAS_TOKEN=" in text


def _run_script(name: str) -> None:
    script = BASE_DIR / name
    if not script.exists():
        console.print(f"  [red]✗ Script not found:[/red] {name}")
        return
    try:
        subprocess.run([sys.executable, str(script)], check=False)
    except KeyboardInterrupt:
        pass


def _open_dashboard() -> None:
    html = BASE_DIR / "dashboard.html"
    if html.exists():
        import webbrowser
        webbrowser.open(html.as_uri())
        console.print(f"  [green]✓ Opened dashboard in browser[/green]")
    else:
        console.print(
            "  [yellow]⚠ dashboard.html not found[/yellow]\n"
            "  [dim]Start the monitor first — it generates the file.[/dim]"
        )


# ── Menu ──────────────────────────────────────────────────────────────────────

def _print_header() -> None:
    console.print()
    console.print(Panel(
        Text.from_markup(
            "[bold cyan]AutoCanvas[/bold cyan]\n"
            "[dim]Local AI · Fully private · No cloud[/dim]"
        ),
        border_style="cyan",
        padding=(1, 4),
        expand=False,
    ))
    console.print()


def _print_menu() -> None:
    lines = (
        "  [bold white]1[/bold white]  [green]Run Bot[/green]       "
        "[dim]Scan Canvas, solve & confirm submissions[/dim]\n"
        "  [bold white]2[/bold white]  [blue]Monitor[/blue]       "
        "[dim]Start the live activity dashboard[/dim]\n"
        "  [bold white]3[/bold white]  [yellow]Setup[/yellow]         "
        "[dim]Update credentials, name, or AI model[/dim]\n"
        "  [bold white]4[/bold white]  [dim]Exit[/dim]"
    )
    console.print(Panel(
        lines,
        border_style="dim",
        padding=(1, 2),
    ))


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    _print_header()

    # Auto-run setup if .env is missing or incomplete
    if not _is_configured():
        console.print(Panel(
            "[yellow]No configuration found.[/yellow]\n"
            "[dim]Running the setup wizard first…[/dim]",
            border_style="yellow",
            padding=(1, 3),
        ))
        console.print()
        _run_script("setup.py")
        if not _is_configured():
            console.print("[red]Setup incomplete. Exiting.[/red]")
            return

    while True:
        _print_menu()

        choice = Prompt.ask(
            "  [bold]Choice[/bold]",
            choices=["1", "2", "3", "4"],
            show_choices=False,
            console=console,
        )

        console.print()

        if choice == "1":
            console.rule("[cyan]Running Bot[/cyan]")
            _run_script("auto_bot.py")
            console.print()
            input("  Press Enter to return to menu…")
            console.print()

        elif choice == "2":
            console.rule("[blue]Starting Monitor[/blue]")
            console.print("  [dim]Press Ctrl+C to stop the monitor and return here.[/dim]\n")
            _open_dashboard()
            _run_script("monitor.py")
            console.print()

        elif choice == "3":
            console.rule("[yellow]Setup[/yellow]")
            _run_script("setup.py")
            console.print()

        elif choice == "4":
            console.print("  [dim]Bye.[/dim]\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n  [dim]Bye.[/dim]\n")

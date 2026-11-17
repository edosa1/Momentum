from datetime import date, datetime
import click
from rich.console import Console
from rich.table import Table

from habit_tracker.db import get_connection, init_db
from habit_tracker.streaks import calculate_current_streak, calculate_longest_streak

console = Console()


@click.group()
def cli():
    """A simple command-line habit tracker."""
    init_db()  # make sure tables exist before any command runs


@cli.command()
@click.argument('name')
def add(name):
    """Add a new habit, e.g. habit add "Read 20 minutes" """
    conn = get_connection()
    try:
        conn.execute("INSERT INTO habits (name) VALUES (?)", (name,))
        conn.commit()
        console.print(f"[green]Added habit:[/green] {name}")
    except Exception:
        console.print(f"[red]A habit named '{name}' already exists.[/red]")
    finally:
        conn.close()


@cli.command()
@click.argument('name')
def done(name):
    """Mark a habit as completed for today."""
    conn = get_connection()
    habit = conn.execute("SELECT id FROM habits WHERE name = ?", (name,)).fetchone()

    if not habit:
        console.print(f"[red]No habit found named '{name}'. Try 'habit list'.[/red]")
        conn.close()
        return

    today_str = date.today().isoformat()
    try:
        conn.execute(
            "INSERT INTO completions (habit_id, completed_date) VALUES (?, ?)",
            (habit["id"], today_str),
        )
        conn.commit()
        console.print(f"[green]Marked '{name}' done for today.[/green]")
    except Exception:
        console.print(f"[yellow]'{name}' was already marked done today.[/yellow]")
    finally:
        conn.close()


@cli.command(name="list")
def list_habits():
    """Show all habits with their current and longest streaks."""
    conn = get_connection()
    habits = conn.execute("SELECT id, name FROM habits").fetchall()

    table = Table(title="Your habits")
    table.add_column("Habit")
    table.add_column("Current streak")
    table.add_column("Longest streak")

    for habit in habits:
        rows = conn.execute(
            "SELECT completed_date FROM completions WHERE habit_id = ?",
            (habit["id"],),
        ).fetchall()
        dates = {datetime.fromisoformat(r["completed_date"]).date() for r in rows}

        current = calculate_current_streak(dates)
        longest = calculate_longest_streak(dates)

        streak_display = f"[green]{current} days[/green]" if current > 0 else "[grey50]0 days[/grey50]"
        table.add_row(habit["name"], streak_display, f"{longest} days")

    conn.close()

    if not habits:
        console.print("[yellow]No habits yet. Add one with: habit add \"Your habit\"[/yellow]")
    else:
        console.print(table)


@cli.command()
@click.argument('name')
def remove(name):
    """Delete a habit and all its history."""
    conn = get_connection()
    habit = conn.execute("SELECT id FROM habits WHERE name = ?", (name,)).fetchone()

    if not habit:
        console.print(f"[red]No habit found named '{name}'.[/red]")
        conn.close()
        return

    conn.execute("DELETE FROM completions WHERE habit_id = ?", (habit["id"],))
    conn.execute("DELETE FROM habits WHERE id = ?", (habit["id"],))
    conn.commit()
    conn.close()
    console.print(f"[green]Removed '{name}'.[/green]")


@cli.command()
@click.argument('name')
def stats(name):
    """Show detailed stats for a single habit."""
    conn = get_connection()
    habit = conn.execute("SELECT id FROM habits WHERE name = ?", (name,)).fetchone()

    if not habit:
        console.print(f"[red]No habit found named '{name}'.[/red]")
        conn.close()
        return

    rows = conn.execute(
        "SELECT completed_date FROM completions WHERE habit_id = ?",
        (habit["id"],),
    ).fetchall()
    dates = {datetime.fromisoformat(r["completed_date"]).date() for r in rows}
    conn.close()

    console.print(f"\n[bold]{name}[/bold]")
    console.print(f"Current streak: {calculate_current_streak(dates)} days")
    console.print(f"Longest streak: {calculate_longest_streak(dates)} days")
    console.print(f"Total completions: {len(dates)}\n")


if __name__ == "__main__":
    cli()

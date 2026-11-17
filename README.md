# Momentum Habit Tracker CLI

A command-line habit tracker with streak tracking, built to practice working
outside a web framework — no HTTP, no browser, just Python and SQLite.

## Features
- Add, remove, and list habits
- Mark habits done for the day
- Automatic current-streak and longest-streak calculation
- Colored, table-formatted terminal output (via `rich`)
- Installs as a real terminal command (`habit`), not a script you run with `python`

## Install

```bash
pip install -e .
```


This reads `pyproject.toml` and installs the `habit` command onto your system,
along with its dependencies (`click`, `rich`).

python -m venv env
.\env\Scripts\activate

## Usage

```bash
habit add "Read 20 minutes"
habit done "Read 20 minutes"
habit list
habit stats "Read 20 minutes"
habit remove "Read 20 minutes"
```

Data is stored in a local SQLite file at `~/.habit_tracker.db` — no server,
no setup, works the same on any machine with Python installed.

## Running tests

```bash
pip install pytest
python -m pytest tests/
```

## What this project demonstrates
- Working outside a web framework — pure Python, standard library + two small dependencies
- A genuine small algorithm (finding consecutive-day streaks), not just CRUD
- Safe SQL — all queries use parameterized placeholders, never string concatenation
- Proper Python packaging (`pyproject.toml`) so the tool installs and runs like a real CLI utility
- Focused unit testing on the one piece of code with actual logic worth testing

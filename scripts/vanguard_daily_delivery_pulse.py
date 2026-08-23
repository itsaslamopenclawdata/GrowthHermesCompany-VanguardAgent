#!/usr/bin/env python3
"""Daily delivery pulse generator for the VANGUARD repo.

Checks git activity in the VANGUARD repo and the main-build-project repo,
compares it to the morning brief, and writes a mid-day delivery checkpoint.

Deterministic — no LLM provider calls.
"""

from __future__ import annotations

import datetime
import re
import subprocess
from pathlib import Path
from typing import List

VANGUARD_REPO = Path(r"C:\Users\itssh\GrowthHermesCompany-VanguardAgent")
MAIN_BUILD_REPO = Path(r"C:\Users\itssh\HermesProjects\main-build-project")
VAULT_DIR = Path(r"D:\HermesObsidian\Daily-Working-Space-main\memory\hermes-10x")
OUTPUT_DIR = VANGUARD_REPO / "logs" / "delivery-pulses"


def run(cmd: str | List[str], cwd: Path | None = None, check: bool = True) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=isinstance(cmd, str),
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()


def read_text(path: Path, max_lines: int = 100) -> str:
    if not path.exists():
        return "_Not created yet._"
    try:
        text = path.read_text(encoding="utf-8").strip()
        lines = text.splitlines()
        if len(lines) > max_lines:
            text = "\n".join(lines[:max_lines]) + "\n\n..."
        return text
    except Exception as exc:
        return f"_Error reading {path}: {exc}_"


def extract_last_entry(text: str) -> str:
    matches = list(re.finditer(r"###\s*(\d{4}-\d{2}-\d{2}.*?)\n", text))
    if not matches:
        return text
    last = matches[-1]
    start = last.start()
    next_match = next((m for m in matches if m.start() > start), None)
    end = next_match.start() if next_match else len(text)
    return text[start:end].strip()


def extract_unchecked_tasks(entry: str) -> List[str]:
    tasks: List[str] = []
    for line in entry.splitlines():
        m = re.match(r"\s*(?:\d+\.\s*)?-?\s*\[\s*\]\s*(.+)", line)
        if m:
            tasks.append(m.group(1).strip())
    return tasks


def git_commits_today(repo_dir: Path, author: str = "") -> List[str]:
    """Return commit messages from today in the given repo."""
    if not (repo_dir / ".git").exists():
        return [f"_Repo not initialized: {repo_dir}_"]
    today = datetime.date.today().strftime("%Y-%m-%d")
    cmd = f'git log --since="{today} 00:00" --format="%h %s" --no-merges'
    out = run(cmd, cwd=repo_dir, check=False)
    if not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def git_status_summary(repo_dir: Path) -> str:
    if not (repo_dir / ".git").exists():
        return "_No git repo._"
    status = run("git status --short", cwd=repo_dir, check=False)
    return status if status else "_Working tree clean._"


def main() -> None:
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    # Sync VANGUARD repo
    run("git pull origin master", cwd=VANGUARD_REPO, check=False)

    # Read inputs
    daily_goals = read_text(VAULT_DIR / "daily-goals.md", 200)
    last_daily = extract_last_entry(daily_goals)
    unchecked = extract_unchecked_tasks(last_daily)

    morning_brief_path = VANGUARD_REPO / "logs" / "daily-briefings" / f"{date_str}.md"
    morning_brief = read_text(morning_brief_path, 120)

    # Git activity
    vanguard_commits = git_commits_today(VANGUARD_REPO)
    main_build_commits = git_commits_today(MAIN_BUILD_REPO)
    vanguard_status = git_status_summary(VANGUARD_REPO)
    main_build_status = git_status_summary(MAIN_BUILD_REPO)

    total_commits = len(vanguard_commits) + len(main_build_commits)

    # Determine blocker / next action
    blocker = "_No explicit blocker found._"
    for line in last_daily.splitlines():
        if any(k in line.lower() for k in ("block", "stuck", "blocked by", "waiting on")):
            blocker = line.strip().lstrip("-").strip()
            break

    # Smallest next delivery action
    if unchecked:
        next_action = f"Ship the smallest version of: {unchecked[0]}"
    elif not vanguard_commits and not main_build_commits:
        next_action = "Make one commit today — code, docs, or notes — to keep the delivery streak alive."
    else:
        next_action = "Review today's commits and push any uncommitted work."

    report = f"""# ⚡ Daily Delivery Pulse — {date_str}

## Shipped Today

### VANGUARD Repo
"""
    if vanguard_commits:
        for commit in vanguard_commits:
            report += f"- `{commit}`\n"
    else:
        report += "_No commits yet today._\n"

    report += f"""
### Main Build Project
"""
    if main_build_commits:
        for commit in main_build_commits:
            report += f"- `{commit}`\n"
    else:
        report += "_No commits yet today._\n"

    report += f"""
## Working Tree Status
- VANGUARD: `{vanguard_status}`
- Main Build: `{main_build_status}`

## Plan vs. Reality
- Morning tasks defined: {len(unchecked)}
- Commits today: {total_commits}
- Delivery state: {"✅ On track" if total_commits >= 1 else "⚠️ No delivery signal yet"}

## Open Blocker
{blocker}

## Smallest Next Delivery Action
{next_action}

## Suggested Afternoon Focus
"""
    if total_commits == 0:
        report += "Get one meaningful commit in before EOD — code, docs, or a decision logged in the repo.\n"
    elif not main_build_commits:
        report += "Main Build has no commits today. Shift 60 min to the build project if possible.\n"
    elif not vanguard_commits:
        report += "VANGUARD repo has no commits today. Log one strategic update or learning before EOD.\n"
    else:
        report += "Good delivery signal. Use the afternoon to close open loops and prepare tomorrow's priorities.\n"

    report += f"""
## Remaining Morning Tasks
"""
    if unchecked:
        for i, task in enumerate(unchecked[:5], start=1):
            report += f"{i}. {task}\n"
    else:
        report += "_No unchecked tasks found in latest daily-goals entry._\n"

    report += f"""
---

_Generated by the VANGUARD Daily Delivery Pulse cron job._
"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{date_str}.md"
    output_path.write_text(report, encoding="utf-8")

    # Commit and push
    run("git add logs/delivery-pulses/", cwd=VANGUARD_REPO, check=False)
    run(f'git commit -m "daily(delivery): pulse for {date_str}"', cwd=VANGUARD_REPO, check=False)
    run("git push origin master", cwd=VANGUARD_REPO, check=False)

    print(f"Daily delivery pulse written to {output_path} and pushed to GitHub.")


if __name__ == "__main__":
    main()

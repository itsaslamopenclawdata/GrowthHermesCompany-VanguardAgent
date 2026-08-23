#!/usr/bin/env python3
"""Daily learning & priority brief generator for the VANGUARD repo.

Reads the Hermes 10x Obsidian vault and the VANGUARD strategic memory files,
produces a dated markdown brief, commits it to the repo, and pushes to GitHub.

Deterministic — no LLM provider calls, so it runs cheaply and reliably.
"""

from __future__ import annotations

import datetime
import re
import subprocess
from pathlib import Path
from typing import List, Tuple

REPO_DIR = Path(r"C:\Users\itssh\GrowthHermesCompany-VanguardAgent")
VAULT_DIR = Path(r"D:\HermesObsidian\Daily-Working-Space-main\memory\hermes-10x")
OUTPUT_DIR = REPO_DIR / "logs" / "daily-briefings"


def run(cmd: str | List[str], cwd: Path | None = None, check: bool = True) -> str:
    """Run a shell command and return stdout."""
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
    """Return the most recent '### YYYY-MM-DD' entry."""
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


def extract_projects(text: str) -> List[Tuple[str, str, str]]:
    projects: List[Tuple[str, str, str]] = []
    pattern = re.compile(
        r"###\s*Project:\s*(.+?)\n.*?\*\*Goal:\*\*\s*(.+?)\n.*?\*\*Next Action:\*\*\s*(.+?)(?=\n\*\*|$)",
        re.DOTALL | re.IGNORECASE,
    )
    for m in pattern.finditer(text):
        name = m.group(1).strip()
        if name.startswith("<") and name.endswith(">"):
            continue
        goal = " ".join(m.group(2).split())
        next_action = " ".join(m.group(3).split())
        projects.append((name, goal, next_action))
    return projects


def first_matching(tasks: List[str], keywords: Tuple[str, ...]) -> str | None:
    for task in tasks:
        lower = task.lower()
        if any(k in lower for k in keywords):
            return task
    return None


def generate_tasks(projects: List[Tuple[str, str, str]], unchecked: List[str]) -> List[str]:
    main_build = next((p for p in projects if "Main Build" in p[0]), None)
    daily_learning = next((p for p in projects if "Daily Learning" in p[0]), None)

    tasks: List[str] = []

    # 1. Main build / top delivery action
    if main_build:
        tasks.append(f"**Build:** {main_build[2]}")
    elif unchecked:
        tasks.append(f"**Build:** {unchecked[0]}")
    else:
        tasks.append("**Build:** Work on your #1 active project for 90 min of deep focus before opening anything else.")

    # 2. Learning action
    learning = first_matching(unchecked, ("learn", "study", "read", "watch", "mcp", "rag", "langgraph", "qiskit"))
    if learning:
        tasks.append(f"**Learn:** {learning}")
    elif daily_learning and daily_learning[2]:
        tasks.append(f"**Learn:** {daily_learning[2]}")
    else:
        tasks.append("**Learn:** Spend 30 min extracting one reusable pattern from the latest AI/ML source you saved.")

    # 3. Commercial validation
    validate = first_matching(unchecked, ("b2b", "validate", "commercial", "customer", "prospect", "market", "outreach"))
    if validate:
        tasks.append(f"**Validate:** {validate}")
    else:
        tasks.append("**Validate:** Identify one B2B AI opportunity persona + 3 pain points and log it in IDEAS.md.")

    # 4. Unblock / experiment
    unblock = first_matching(unchecked, ("block", "stuck", "unblock", "resolve"))
    if unblock:
        tasks.append(f"**Unblock:** {unblock}")
    elif len(unchecked) > 1:
        tasks.append(f"**Experiment:** {unchecked[1]}")
    else:
        tasks.append("**Unblock:** Pick the oldest open blocker and resolve or escalate it today.")

    # 5. Compound / energy
    energy = first_matching(unchecked, ("health", "energy", "move", "workout", "walk"))
    if energy:
        tasks.append(f"**Energy:** {energy}")
    else:
        tasks.append("**Compound:** Document one reusable pattern, automation, or lesson in Obsidian or the VANGUARD repo.")

    return tasks


def main() -> None:
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    # Sync repo
    run("git pull origin master", cwd=REPO_DIR, check=False)

    # Read inputs
    daily_goals = read_text(VAULT_DIR / "daily-goals.md", 200)
    project_context = read_text(VAULT_DIR / "project-context.md", 100)
    learning_log = read_text(VAULT_DIR / "learning-log.md", 80)
    weekly_sprints = read_text(VAULT_DIR / "weekly-sprints.md", 80)

    goals = read_text(REPO_DIR / "GOALS.md", 80)
    backlog = read_text(REPO_DIR / "BACKLOG.md", 80)
    experiments = read_text(REPO_DIR / "EXPERIMENTS.md", 80)

    last_daily = extract_last_entry(daily_goals)
    unchecked = extract_unchecked_tasks(last_daily)
    projects = extract_projects(project_context)
    tasks = generate_tasks(projects, unchecked)

    main_build = next((p for p in projects if "Main Build" in p[0]), None)

    # Top active experiment
    active_experiment = "_No active experiment summary available._"
    if "## Active Experiments" in experiments:
        parts = experiments.split("## Active Experiments")
        if len(parts) > 1:
            active_experiment = parts[1].split("## Completed Experiments")[0].strip()[:800]

    report = f"""# 🌅 Daily Learning & Priority Brief — {date_str}

## Purpose
Connect today's learning goals with the highest-leverage execution priorities.

## 5 High-Impact Tasks for Today
"""
    for i, task in enumerate(tasks, start=1):
        report += f"{i}. {task}\n"

    report += f"""
## Active Context

### Main Build Goal
{main_build[1] if main_build else "_No Main Build project found._"}

### Main Build Next Action
{main_build[2] if main_build else "_Set the next action in project-context.md._"}

### Latest Learning Goal
{learning_log.splitlines()[0] if learning_log.splitlines() else "_"}

### Weekly Sprint Snapshot
{weekly_sprints.splitlines()[0] if weekly_sprints.splitlines() else "_"}

## Active Experiment Snapshot
{active_experiment}

## 1% Improvement Focus for Today
Identify one manual step in your daily workflow and eliminate or automate it.

## Memory Sources
- Obsidian vault: `D:/HermesObsidian/Daily-Working-Space-main/memory/hermes-10x`
- VANGUARD repo: `C:/Users/itssh/GrowthHermesCompany-VanguardAgent`

---

_Generated by the VANGUARD Daily Learning Brief cron job._
"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{date_str}.md"
    output_path.write_text(report, encoding="utf-8")

    # Commit and push
    run("git add logs/daily-briefings/", cwd=REPO_DIR, check=False)
    run(f'git commit -m "daily(learning): brief for {date_str}"', cwd=REPO_DIR, check=False)
    run("git push origin master", cwd=REPO_DIR, check=False)

    print(f"Daily learning brief written to {output_path} and pushed to GitHub.")


if __name__ == "__main__":
    main()

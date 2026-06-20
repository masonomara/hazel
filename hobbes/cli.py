#!/usr/bin/env python3
"""
hobbes CLI — runs the cycle stages and reads the filesystem state machine.

  cycle      baseline (--fresh) -> findings -> diff   (the deterministic patrol)
  baseline / findings / diff                          (individual steps)
  status     report which stage the newest cycle is at
  plan / execute   print the stage prompt + inputs for an agent (Claude Code)

USAGE: python3 hobbes/cli.py <command> [args passed through to the tool]
"""

import subprocess
import sys
from pathlib import Path

HOBBES = Path(__file__).resolve().parent
TOOLS = HOBBES / "tools"
SCORECARDS = HOBBES / "scorecards"
sys.path.insert(0, str(TOOLS))
import config


def _run(tool, *args):
    subprocess.run([sys.executable, str(TOOLS / tool), *args], check=True)


def _latest_cycle():
    ds = sorted(d for d in SCORECARDS.glob("[0-9]" * 4 + "-[0-9][0-9]-[0-9][0-9]") if d.is_dir())
    return ds[-1] if ds else None


def cmd_cycle(rest):
    rd = str(SCORECARDS / config.today())
    _run("baseline.py", "--fresh", "--run-dir", rd, *rest)
    _run("findings.py", "--run-dir", rd)
    _run("diff.py", "--run-dir", rd)


def cmd_baseline(rest):
    _run("baseline.py", *rest)


def cmd_findings(rest):
    _run("findings.py", *rest)


def cmd_diff(rest):
    _run("diff.py", *rest)


def cmd_status(rest):
    c = _latest_cycle()
    if not c:
        print("no cycle yet — run `hobbes cycle`")
        return
    stages = [("baseline.md", "baseline"), ("findings.md", "findings"),
              ("plan.md", "plan"), ("execution.md", "execute")]
    have = [name for f, name in stages if (c / f).exists()]
    nxt = next((name for f, name in stages if not (c / f).exists()), "publish (human)")
    print(f"cycle {c.name}: {' -> '.join(have) or '(empty)'}  ·  next: {nxt}")


def _agent_stage(template, rest):
    c = _latest_cycle()
    findings = (c / "findings.md") if c else None
    print(f"Stage prompt → hobbes/scorecards/{template}")
    print(f"Cycle        → {c.name if c else '(none)'}")
    print(f"Findings     → {findings if findings and findings.exists() else '(run findings first)'}")
    print("Drive this stage with Claude Code (claude-code-action in CI, or `claude` locally): "
          "follow the template, open a PR, write only to GitHub, never publish.")


def cmd_plan(rest):
    _agent_stage("PLAN-TEMPLATE.md", rest)


def cmd_execute(rest):
    _agent_stage("EXECUTE-TEMPLATE.md", rest)


def cmd_budget(rest):
    print(config.effort_budget())


def cmd_today(rest):
    print(config.today())


COMMANDS = {
    "cycle": cmd_cycle, "baseline": cmd_baseline, "findings": cmd_findings,
    "diff": cmd_diff, "status": cmd_status, "plan": cmd_plan, "execute": cmd_execute,
    "budget": cmd_budget, "today": cmd_today,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        sys.exit("usage: hobbes <cycle|baseline|findings|diff|status|plan|execute|budget|today>")
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()

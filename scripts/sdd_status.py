#!/usr/bin/env python3
"""Validate SDD metadata and generate the repository status dashboard."""

from __future__ import annotations

import argparse
import html
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PHASES = {
    "initialized": 10,
    "requirements-generated": 30,
    "design-generated": 55,
    "tasks-generated": 75,
    "implemented": 100,
}
ARTIFACTS = {
    "requirements": "requirements.md",
    "design": "design.md",
    "tasks": "tasks.md",
}
VALIDATION_STATUSES = {"valid", "review-required", "blocked"}


def load_specs(specs_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Load every feature directory and report fail-closed metadata errors."""
    specs: list[dict[str, Any]] = []
    errors: list[str] = []
    if not specs_dir.is_dir():
        return [], [f"specs directory not found: {specs_dir}"]

    for feature_dir in sorted(path for path in specs_dir.iterdir() if path.is_dir()):
        metadata_path = feature_dir / "spec.json"
        if not metadata_path.is_file():
            errors.append(f"{feature_dir.name}: missing spec.json")
            continue
        try:
            spec = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{feature_dir.name}: invalid spec.json ({exc})")
            continue

        validate_spec(feature_dir, spec, errors)
        spec["_directory"] = feature_dir.name
        specs.append(spec)

    if not specs:
        errors.append("no specs with readable metadata found")
    return specs, errors


def validate_spec(feature_dir: Path, spec: dict[str, Any], errors: list[str]) -> None:
    name = feature_dir.name
    for field in ("created_at", "updated_at", "language"):
        if not isinstance(spec.get(field), str) or not spec[field].strip():
            errors.append(f"{name}: {field} must be a non-empty string")

    if spec.get("feature_name") != name:
        errors.append(
            f"{name}: feature_name must match directory (got {spec.get('feature_name')!r})"
        )

    phase = spec.get("phase")
    if phase not in PHASES:
        errors.append(f"{name}: unsupported phase {phase!r}")

    approvals = spec.get("approvals")
    if not isinstance(approvals, dict):
        errors.append(f"{name}: approvals must be an object")
        approvals = {}

    for key, filename in ARTIFACTS.items():
        state = approvals.get(key)
        if not isinstance(state, dict):
            errors.append(f"{name}: approvals.{key} must be an object")
            continue
        generated = state.get("generated")
        approved = state.get("approved")
        if not isinstance(generated, bool) or not isinstance(approved, bool):
            errors.append(f"{name}: approvals.{key} flags must be booleans")
            continue
        if approved and not generated:
            errors.append(f"{name}: approvals.{key} cannot be approved before generation")
        if generated and not (feature_dir / filename).is_file():
            errors.append(f"{name}: {filename} is declared generated but is missing")

    ready = spec.get("ready_for_implementation")
    if not isinstance(ready, bool):
        errors.append(f"{name}: ready_for_implementation must be a boolean")
    elif ready and not all(
        isinstance(approvals.get(key), dict) and approvals[key].get("approved") is True
        for key in ARTIFACTS
    ):
        errors.append(f"{name}: ready_for_implementation requires all approvals")

    validation = spec.get("validation", {"status": "valid"})
    if not isinstance(validation, dict) or validation.get("status") not in VALIDATION_STATUSES:
        errors.append(
            f"{name}: validation.status must be one of {sorted(VALIDATION_STATUSES)}"
        )
    elif validation.get("status") != "valid" and not validation.get("reason"):
        errors.append(f"{name}: non-valid metadata requires validation.reason")

    required_generated = {
        "requirements-generated": ("requirements",),
        "design-generated": ("requirements", "design"),
        "tasks-generated": ("requirements", "design", "tasks"),
        "implemented": ("requirements", "design", "tasks"),
    }.get(phase, ())
    for key in required_generated:
        if not isinstance(approvals.get(key), dict) or approvals[key].get("generated") is not True:
            errors.append(f"{name}: phase {phase} requires approvals.{key}.generated=true")

    if isinstance(validation, dict) and validation.get("status", "valid") == "valid":
        required_approved = {
            "design-generated": ("requirements",),
            "tasks-generated": ("requirements", "design"),
            "implemented": ("requirements", "design", "tasks"),
        }.get(phase, ())
        for key in required_approved:
            if not isinstance(approvals.get(key), dict) or approvals[key].get("approved") is not True:
                errors.append(f"{name}: valid phase {phase} requires approvals.{key}.approved=true")


def next_action(spec: dict[str, Any]) -> str:
    name = spec["feature_name"]
    validation = spec.get("validation", {})
    if validation.get("status") == "blocked":
        return validation["reason"]
    if validation.get("status") == "review-required":
        return validation["reason"]
    phase = spec["phase"]
    actions = {
        "initialized": f"Gerar requisitos: /sdd:spec-requirements {name}",
        "requirements-generated": f"Revisar requisitos e gerar design: /sdd:spec-design {name}",
        "design-generated": f"Revisar design e gerar tarefas: /sdd:spec-tasks {name}",
        "tasks-generated": f"Revisar tarefas e implementar: /sdd:spec-impl {name}",
        "implemented": "Validar a implementação e manter a spec sincronizada.",
    }
    return actions[phase]


def render_dashboard(specs: list[dict[str, Any]]) -> str:
    ordered = sorted(specs, key=lambda item: item["feature_name"])
    counts = Counter(spec["phase"] for spec in ordered)
    phase_summary = " · ".join(
        f"{phase}: {counts[phase]}" for phase in PHASES if counts[phase]
    )
    rows = []
    for spec in ordered:
        validation = spec.get("validation", {"status": "valid"})
        status = validation.get("status", "valid")
        status_label = status.replace("-", " ")
        progress = PHASES[spec["phase"]]
        rows.append(
            """
          <tr>
            <td><code>{name}</code></td>
            <td>{phase}</td>
            <td><span class="badge {status}">{status_label}</span></td>
            <td><div class="progress"><span style="width:{progress}%"></span></div>{progress}%</td>
            <td>{action}</td>
          </tr>""".format(
                name=html.escape(spec["feature_name"]),
                phase=html.escape(spec["phase"]),
                status=html.escape(status),
                status_label=html.escape(status_label),
                progress=progress,
                action=html.escape(next_action(spec)),
            )
        )

    return """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SDD Status Dashboard</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, system-ui, sans-serif; }}
    body {{ margin: 0; background: #0b1020; color: #e8ecf7; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 48px 24px; }}
    h1 {{ margin-bottom: 8px; }}
    .summary {{ color: #aeb8cf; margin-bottom: 28px; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid #2a3550; border-radius: 14px; }}
    table {{ width: 100%; border-collapse: collapse; background: #11182b; }}
    th, td {{ padding: 16px; border-bottom: 1px solid #26314a; text-align: left; vertical-align: top; }}
    th {{ color: #aeb8cf; font-size: .82rem; text-transform: uppercase; letter-spacing: .05em; }}
    tr:last-child td {{ border-bottom: 0; }}
    code {{ color: #8fd3ff; }}
    .badge {{ display: inline-block; padding: 4px 9px; border-radius: 999px; font-size: .78rem; white-space: nowrap; }}
    .valid {{ background: #153f34; color: #85ebc0; }}
    .review-required {{ background: #4b3b12; color: #ffd979; }}
    .blocked {{ background: #4d2028; color: #ffabb8; }}
    .progress {{ width: 120px; height: 7px; margin-bottom: 5px; border-radius: 99px; background: #2b3650; overflow: hidden; }}
    .progress span {{ display: block; height: 100%; background: #58a6ff; }}
    footer {{ margin-top: 20px; color: #8190ae; font-size: .85rem; }}
  </style>
</head>
<body>
  <main>
    <h1>SDD Status Dashboard</h1>
    <p class="summary">{total} specs · {phase_summary}</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Spec</th><th>Fase canônica</th><th>Validação</th><th>Progresso</th><th>Próxima ação</th></tr></thead>
        <tbody>{rows}
        </tbody>
      </table>
    </div>
    <footer>Gerado de forma determinística a partir de <code>.sdd/specs/*/spec.json</code>. Não edite manualmente.</footer>
  </main>
</body>
</html>
""".format(total=len(ordered), phase_summary=html.escape(phase_summary), rows="".join(rows))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true", help="fail if dashboard is stale")
    args = parser.parse_args()

    root = args.root.resolve()
    specs, errors = load_specs(root / ".sdd" / "specs")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    dashboard = render_dashboard(specs)
    output = root / "sdd-dashboard.html"
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != dashboard:
            print("ERROR: sdd-dashboard.html is stale; run python scripts/sdd_status.py", file=sys.stderr)
            return 1
        print(f"SDD metadata valid: {len(specs)} specs; dashboard is current")
        return 0

    output.write_text(dashboard, encoding="utf-8")
    print(f"Generated {output} from {len(specs)} specs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

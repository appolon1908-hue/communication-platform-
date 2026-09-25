#!/usr/bin/env python3
"""Validate the Codestra master architecture document set."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED = [
    "MASTER-ARCHITECTURE.md",
    "REPOSITORY-OWNERSHIP.md",
    "CANONICAL-API-CATALOGUE.md",
    "EVENT-CATALOGUE.md",
    "STATUS-MODEL.md",
    "DASHBOARD.md",
    "INTEGRATION-MATRIX.md",
    "DEPENDENCY-GRAPH.md",
    "CROSS-REPOSITORY-RELEASE-CHECKLIST.md",
    "SOFTWARE-STACK.md",
]


def fail(msg: str) -> None:
    raise SystemExit(f"ERROR: {msg}")


def main() -> None:
    missing = [name for name in REQUIRED if not (DOCS / name).is_file()]
    if missing:
        fail(f"missing required master architecture document(s): {missing}")

    ownership = (DOCS / "REPOSITORY-OWNERSHIP.md").read_text(encoding="utf-8")
    required_repos = [
        "appolon1908-hue/Caddy",
        "appolon1908-hue/Kong",
        "appolon1908-hue/Keycloak",
        "appolon1908-hue/Middleware-",
        "appolon1908-hue/klyrow.com",
        "appolon1908-hue/telnexa",
        "appolon1908-hue/Vicidialer-Codestra",
        "appolon1908-hue/SDK-repository",
        "appolon1908-hue/N8N",
        "appolon1908-hue/Odoo",
        "appolon1908-hue/Codestra-Grafana-",
        "appolon1908-hue/Codestra-Prometheus",
        "appolon1908-hue/Codestra-Alertmanager",
        "appolon1908-hue/Codestra-Loki",
        "appolon1908-hue/Codestra-Tempo",
        "appolon1908-hue/Codestra-Telemetry",
        "appolon1908-hue/Superset",
        "appolon1908-hue/Codestra-OpenBao",
    ]
    absent = [repo for repo in required_repos if repo not in ownership]
    if absent:
        fail(f"ownership matrix missing principal repo(s): {absent}")

    integration = (DOCS / "INTEGRATION-MATRIX.md").read_text(encoding="utf-8")
    if "Prometheus -> Alertmanager -> Middleware" not in integration:
        fail("integration matrix must preserve Prometheus -> Alertmanager -> Middleware")
    if "Alertmanager -> direct SMS/email/voice provider" not in integration:
        fail("integration matrix must explicitly forbid Alertmanager provider bypass")

    api_catalogue = (DOCS / "CANONICAL-API-CATALOGUE.md").read_text(encoding="utf-8")
    if "/v1/commands" not in api_catalogue or "/v1/operations/{command_id}" not in api_catalogue:
        fail("API catalogue must include the durable Middleware control-plane primitives")
    if "not assigned a public canonical URL" not in api_catalogue:
        fail("Alertmanager ingestion route must remain unclaimed until runtime/source proof exists")

    status = (DOCS / "STATUS-MODEL.md").read_text(encoding="utf-8")
    for state in ["reconciliation_required", "dead_lettered", "acknowledged", "reopened"]:
        if state not in status:
            fail(f"status model missing required state: {state}")

    dashboard = (DOCS / "DASHBOARD.md").read_text(encoding="utf-8")
    if "What is broken, where, since when" not in dashboard:
        fail("dashboard must preserve the primary incident question")
    if "aler.codestra.media" not in dashboard:
        fail("dashboard spec must include canonical Alertmanager host")

    checklist = (DOCS / "CROSS-REPOSITORY-RELEASE-CHECKLIST.md").read_text(encoding="utf-8")
    for gate in ["Exact-head CI", "Staging", "Rollback", "NO-GO"]:
        if gate.lower() not in checklist.lower():
            fail(f"release checklist missing gate: {gate}")

    print("Codestra master architecture validation: PASS")


if __name__ == "__main__":
    main()

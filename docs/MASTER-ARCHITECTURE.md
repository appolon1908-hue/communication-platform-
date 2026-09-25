# Codestra Master Communications Architecture

`communication-platform-` is the master architecture and cross-repository coordination authority for the Codestra communications and observability platform. It does not replace the principal runtime repositories.

## Canonical architecture

```text
Applications / Products
        |
        v
Codestra SDKs
        |
        v
Caddy -> Kong -> Keycloak validation
                |
                v
            Middleware
      +---------+---------+
      |         |         |
      v         v         v
   Klyrow    Telnexa   VICIdial
   Email      SMS       Voice

Runtime telemetry
   |
   +--> Alloy / OpenTelemetry -> Loki / Tempo
   +--> Exporters / metrics ---> Prometheus -> Alertmanager -> Middleware
                                        \------> Grafana

Business analytics read models ----------------------------> Superset
Runtime secrets / dynamic credentials ---------------------> OpenBao
```

## Permanent authority rules

1. Middleware is the only cross-system write/control authority.
2. Caddy owns edge/TLS, Kong owns gateway policy, Keycloak owns identity.
3. Klyrow owns email runtime; Telnexa owns SMS runtime; Vicidialer-Codestra owns voice runtime.
4. n8n orchestrates only through governed Middleware boundaries.
5. Odoo owns CRM/business state, not provider mutation.
6. Grafana/Superset are read-oriented; dashboards never become provider write paths.
7. Alertmanager routes alerts only to Middleware; it is not an independent communications platform.
8. OpenBao owns runtime secrets; real secrets never belong in Git.
9. Each observability component keeps its dedicated repository as its principal source.
10. This repository owns architecture, ownership, cross-repo dependency and release coordination only.

## Master document set

- `docs/REPOSITORY-OWNERSHIP.md` — principal repository and capability authority matrix.
- `docs/CANONICAL-API-CATALOGUE.md` — provider-neutral API targets and implementation authority.
- `docs/EVENT-CATALOGUE.md` — canonical communications/observability event names and ownership.
- `docs/STATUS-MODEL.md` — message, command, provider, alert and incident lifecycle states.
- `docs/DASHBOARD.md` — Grafana/Superset/custom-admin dashboard specification.
- `docs/INTEGRATION-MATRIX.md` — allowed system-to-system paths and security/effect rules.
- `docs/DEPENDENCY-GRAPH.md` — release and runtime dependency graph.
- `docs/CROSS-REPOSITORY-RELEASE-CHECKLIST.md` — required evidence before coordinated release.
- `docs/SOFTWARE-STACK.md` — supporting software roles.
- `docs/OBSERVABILITY-INTEGRATION-WIRING-V1.md` — observability wiring specifics.

## Architecture status language

This repository distinguishes:

- **DEFINED** — architecture contract exists here.
- **SOURCE_PREPARED** — owning repository contains proposed source/config.
- **CI_VALIDATED** — exact source head passed repository CI.
- **STAGING_PROVEN** — behavior was demonstrated in staging.
- **PRODUCTION_APPROVED** — release evidence and human approvals are complete.
- **PRODUCTION_ACTIVE** — runtime activation is independently proven.

Documentation must never use a later status merely because an earlier status is true.

## Current alert-routing direction

The central alert path is:

```text
Prometheus -> Alertmanager -> Middleware -> approved notification/ticket/orchestration path
```

Alertmanager handles grouping, deduplication, inhibition and silence policy. Middleware owns durable incident IDs, acknowledgement/escalation, notification authorization, Odoo incident writes and n8n orchestration.

## Release principle

A cross-repository release is only as ready as its weakest required dependency. The dependency graph and release checklist must be updated whenever a new principal component or required integration is added.

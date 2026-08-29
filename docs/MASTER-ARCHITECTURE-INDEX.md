# Communications Master Architecture Index

Date: 2026-08-29

## Purpose

`communication-platform-` is the master architecture and coordination repository for Codestra communications. It owns the canonical maps, catalogues, dashboard design, dependency graph, and release checklist. It does not own runtime code for Middleware, Klyrow, Telnexa, VICIdial, SDK, Kong, Keycloak, Caddy, observability, analytics, or secrets.

## Canonical Documents

| Area | Document |
| --- | --- |
| Repository ownership | `docs/REPOSITORY-OWNERSHIP.md` |
| Canonical API catalogue | `docs/CANONICAL-API-CATALOGUE.md` |
| Event catalogue | `docs/EVENT-CATALOGUE.md` |
| Status model | `docs/STATUS-MODEL.md` |
| Integration matrix | `docs/INTEGRATION-MATRIX.md` |
| Dependency graph | `docs/DEPENDENCY-GRAPH.md` |
| Dashboard specification | `docs/DASHBOARD.md` |
| Supporting software stack | `docs/SOFTWARE-STACK.md` |
| Observability wiring | `docs/OBSERVABILITY-INTEGRATION-WIRING-V1.md` |
| Cross-repository release checklist | `docs/CROSS-REPOSITORY-RELEASE-CHECKLIST.md` |

## Authority Rule

The SDK repo is the public contract authority. Middleware is the privileged command and event authority. Provider repos remain the runtime authorities. This repository records how those systems fit together and what evidence must exist before release.

## Current Architecture State

| Layer | Current State |
| --- | --- |
| Contracts | Communications API v1 is defined in `SDK-repository`. |
| Email | Step 3 runtime/provider branches exist in Middleware and Klyrow; production delivery remains gated. |
| SMS | Telnexa remains SMS runtime authority; canonical API alignment is next after email. |
| Voice | Vicidialer-Codestra remains voice runtime authority; canonical API alignment follows SMS. |
| Observability | Dedicated repos exist for Grafana, Prometheus, Alertmanager, Loki, Tempo, Telemetry, exporters, Alloy, Superset, and OpenBao. |
| Dashboard | Dashboard architecture is defined here; Grafana owns operational dashboards, Superset owns analytics, and a custom admin UI is still required for controlled workflows. |

## Non-Activation Statement

Merging architecture documentation does not enable live email, SMS, voice, provider writes, Keycloak/Kong production routes, Caddy exposure, n8n effects, Odoo effects, or secrets.

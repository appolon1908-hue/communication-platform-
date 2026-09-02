# Repository Profile — `communication-platform-`

## Identity

- **Repository:** `appolon1908-hue/communication-platform-`
- **Category:** Cross-repository architecture — communications
- **Visibility:** `public`
- **Default branch:** `main`
- **Authority:** Primary unified email, SMS, voice, webhook, dashboard, and communications ownership/coordination authority
- **Status:** Active architecture repository; it intentionally contains coordination and design rather than provider runtime code.

## Purpose

Defines the provider-neutral communications product model, ownership map, API boundaries, message lifecycle, event catalog, dashboards, security, observability, cross-repository tests, and release sequencing.

## Owns

- Unified communications architecture and capability matrix
- Cross-repository ownership, integration, lifecycle, dashboard, security, and release documentation
- Provider-neutral coordination among SDK, Middleware, email, SMS, voice, Odoo, n8n, gateway, identity, and edge systems

## Does not own

- Postal/Mautic, Jasmin, VICIdial/Asterisk, Middleware, Kong, Keycloak, Caddy, or SDK runtime source
- Alternate privileged provider-write paths
- Production activation caused by documentation merge

## Key integrations

- `SDK-repository`
- Middleware
- Klyrow, Telnexa, and VICIdial
- Kong, Keycloak, Caddy, Odoo, n8n, Grafana, and Superset

## Current priorities

1. Finish email implementation evidence, then SMS and voice contract alignment
2. Complete provider-neutral dashboard and read-model design
3. Add cross-repository contract, staging, reconciliation, and failure tests
4. Maintain one authoritative release dependency map and production-readiness checklist

## Governance and safety

- Promotion model: `feature/docs/fix/security/upgrade -> development -> test -> staging -> production -> main`.
- Architecture and contracts must point to exact principal repository authorities and never duplicate their runtime code.
- Never commit provider credentials, customer payloads, private keys, database dumps, or secret-bearing evidence.
- Merge is coordination acceptance only; all live provider effects remain separately approved.
- This document does not send email/SMS, place calls, mutate Odoo, activate n8n, change routes, or deploy services.

## Account-wide catalog

See `appolon1908-hue/documentaions/REPOSITORY_CATALOG.md`.

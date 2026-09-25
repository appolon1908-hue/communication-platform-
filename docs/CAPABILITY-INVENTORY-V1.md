# Communications Capability Inventory v1

## Purpose

This document is the execution authority for **Step 1: inventory the existing communications capabilities before designing or changing the canonical API**.

This is an evidence/audit branch. It must not change runtime behavior in any participating repository.

## Authority

Repository: `appolon1908-hue/communication-platform-`

Branch: `audit/communications-capability-inventory-v1`

The communications-platform repository owns the cross-repository inventory and architecture comparison. It does not own provider runtime code.

## Repositories in scope

1. `appolon1908-hue/SDK-repository`
2. `appolon1908-hue/Middleware-`
3. `appolon1908-hue/klyrow.com`
4. `appolon1908-hue/telnexa`
5. `appolon1908-hue/Vicidialer-Codestra`

Supporting contract/security repositories are referenced when needed:

- `appolon1908-hue/Kong`
- `appolon1908-hue/Keycloak`
- `appolon1908-hue/Caddy`
- `appolon1908-hue/N8N`
- `appolon1908-hue/Odoo`

## Permanent rule

The inventory must describe what actually exists. It must not silently convert a proposed design into a claim that the feature is implemented.

Every capability must be classified as exactly one of:

- `DONE` — implemented and backed by source plus meaningful test evidence.
- `PARTIAL` — meaningful implementation exists but required contract, behavior, testing, read-back, security or operational evidence is incomplete.
- `MISSING` — required capability is not implemented.
- `DUPLICATE` — materially overlapping capability exists in more than one authority and requires an ownership decision.
- `BLOCKED` — implementation exists or is planned but cannot safely proceed because a prerequisite is unresolved.
- `OUT_OF_SCOPE` — intentionally belongs outside the unified communications API.

## Required inventory columns

For every capability record capture:

| Field | Requirement |
|---|---|
| Capability ID | Stable identifier, e.g. `EMAIL-SEND-001` |
| Channel | shared / email / SMS / voice |
| Capability | Human-readable capability |
| Principal repository | Owning source authority |
| Source location | File/module/path |
| Public API | Exact route/method if present |
| Private/provider API | Exact route/method if present |
| SDK support | Package/method or `none` |
| Middleware support | Command/event/adapter or `none` |
| Authentication | OIDC/JWT/mTLS/HMAC/provider auth |
| Tenant isolation | How tenant scope is enforced |
| Idempotency | Key/scope/state-machine behavior |
| Async events | Event names and source |
| Webhooks | Inbound/outbound callback boundaries |
| Status model | Current provider/runtime statuses |
| Read-back | Authoritative status/read-back method |
| Reconciliation | How uncertain outcomes are resolved |
| Suppression/consent | Applicable controls |
| Quota/rate limit | Applicable controls |
| Tests | Unit/integration/contract/live-safe evidence |
| Observability | Metrics/logs/traces currently exposed |
| Runtime activation | disabled / staging / production / unknown |
| Classification | DONE/PARTIAL/MISSING/DUPLICATE/BLOCKED/OUT_OF_SCOPE |
| Gap | Exact missing requirement |
| Proposed canonical mapping | Future provider-neutral concept; not implementation evidence |

## Inventory sections

### A. Shared control-plane capabilities

Inventory:

- authentication and token validation;
- tenant and actor derivation;
- scopes/roles/capabilities;
- idempotency;
- command ledger;
- operation status;
- correlation/causation IDs;
- inbox/outbox;
- retry policy;
- dead letters;
- reconciliation;
- audit records;
- provider health;
- quotas/rate limits;
- webhook verification;
- webhook delivery;
- event catalogue;
- SDK error model;
- pagination/filtering/search;
- usage/analytics read APIs.

### B. Email / Klyrow

Inventory at minimum:

- single send;
- bulk send;
- scheduled send;
- templates;
- personalization;
- sender identities;
- domains;
- SPF state;
- DKIM state/selectors;
- DMARC state;
- PTR/rDNS evidence surfaced by platform;
- TLS/send-path state;
- message lookup;
- delivery timeline;
- bounce classification;
- complaint processing;
- suppressions;
- consent/preferences;
- campaign integration;
- inbound/tracking events where applicable;
- provider queue health;
- quotas;
- deliverability/reputation snapshots;
- signed delivery callbacks;
- reconciliation/read-back.

### C. SMS / Telnexa

Inventory at minimum:

- single send;
- bulk send;
- scheduled send;
- sender identities;
- inbound SMS/MO;
- DLRs;
- failure classification;
- Unicode handling;
- opt-out/consent;
- suppressions;
- throughput/rate limits;
- provider/carrier health;
- wallet/billing/usage where exposed;
- signed callbacks;
- idempotency;
- reconciliation/read-back.

### D. Voice / VICIdial

Inventory at minimum:

- call command/request;
- campaigns;
- campaign isolation;
- agents;
- supervisors;
- lead/list mapping;
- inbound groups/queues;
- scripts;
- dispositions;
- callbacks;
- transfers;
- recording metadata;
- call status/events;
- extension/provisioning capabilities;
- session/webphone support where applicable;
- dialing safety gates;
- read-back;
- reconciliation.

### E. SDK and contracts

Inventory:

- existing public OpenAPI;
- control-plane OpenAPI;
- enterprise/private OpenAPI;
- AsyncAPI catalogue;
- JSON Schemas;
- TypeScript SDK;
- Python SDK;
- PHP SDK;
- webhook SDK;
- connector-kit;
- n8n nodes;
- generated clients;
- contract validation;
- breaking-change detection;
- Pact/compatibility gates;
- package publication readiness.

## Required outputs

Step 1 is not complete until this branch contains:

1. `docs/inventory/SHARED.md`
2. `docs/inventory/EMAIL-KLYROW.md`
3. `docs/inventory/SMS-TELNEXA.md`
4. `docs/inventory/VOICE-VICIDIAL.md`
5. `docs/inventory/SDK-CONTRACTS.md`
6. `docs/inventory/GAP-MATRIX.md`
7. `docs/inventory/DUPLICATE-OWNERSHIP.md`
8. `docs/inventory/BLOCKERS.md`
9. `docs/inventory/PROPOSED-CANONICAL-MAPPING.md`
10. `docs/inventory/STEP1-EXIT-REPORT.md`

## Step 1 exit gate

Step 1 passes only when:

- every required capability has a classification;
- every `DONE` claim points to source and tests;
- duplicates have a proposed principal owner;
- blockers have an explicit prerequisite/owner;
- current provider statuses are mapped without losing provider truth;
- no runtime change occurred as part of the inventory;
- the exact branch SHA is reviewed;
- the Step 1 exit report is accepted before Step 2 contract implementation is treated as authoritative.

## Handoff to Step 2

Accepted findings feed the dedicated SDK branch:

`appolon1908-hue/SDK-repository:feat/communications-api-v1-contracts`

Step 2 may normalize and design the provider-neutral contract, but it must preserve existing source authorities and must not move provider runtime logic into the SDK repository.

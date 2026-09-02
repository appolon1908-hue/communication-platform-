# Communications Gap Matrix

## Executive matrix

| Area | DONE | PARTIAL | MISSING | BLOCKED | Priority |
|---|---|---|---|---|---|
| Shared control plane | command submission, operation status, tenant boundary, idempotency, durable state, dead-letter replay, safety/readiness | provider health aggregation, usage analytics, message search | canonical communications read model | caller-token acceptance proof | P0 |
| Email / Klyrow | `/v1` API, idempotent writes, status/events, consent/preferences, deliverability, domains, templates/campaign foundation, suppressions, signed webhooks, SDKs, safe mode | exact SPF/DKIM/DMARC/PTR API fields, bulk/schedule semantics, authoritative uncertain-outcome reconciliation | canonical Codestra email mapping | production activation remains independently gated | P0/P1 |
| SMS / Telnexa | send, SMPP, MO, DLR, failure callbacks, Unicode, signed callbacks, billing/usage, quotas, health | sender identity lifecycle, opt-out/consent ownership, exact send idempotency/read-back, reconciliation | canonical bulk/scheduled SMS surface | live carrier/provider activation | P1 |
| Voice / VICIdial | restricted adapter, campaign provisioning/isolation, agents/leads/callbacks/transfers/dispositions, recording metadata, provisioning, safety gates, read-back, reconciliation | queue/inbound-group exact API, call event/status mapping, webphone boundary | canonical provider-neutral voice facade | production dialing activation | P1/P2 |
| SDK/contracts | four OpenAPI boundaries, AsyncAPI, schemas, TS/Python/PHP clients, webhook SDK, connector kit, n8n, semantic validation, drift/Pact | provider conformance and protected package publication | Communications API v1 | none for contract authoring; runtime cutover blocked by identity proof | P0 |
| Dashboard | architecture/design defined | provider-specific metrics/read models | canonical communications dashboard read API | depends on normalized read model | P2 |

## P0 gaps before Step 2 is accepted

1. Freeze canonical message identity and lifecycle.
2. Freeze canonical error/failure taxonomy.
3. Define sender/domain/preference/suppression schemas.
4. Define canonical event envelope for email/SMS/voice.
5. Reconcile Middleware command states with public message states.
6. Define exact Keycloak/Kong/Middleware service-token contract and acceptance test.
7. Define provider health and usage read models.
8. Preserve `indeterminate/reconciliation_required` instead of unsafe duplicate submission.

## P1 gaps before channel implementations are production-ready

- Klyrow: exact DNS/deliverability API fields and authoritative uncertain-outcome read-back.
- Telnexa: opt-out/consent enforcement, provider-neutral idempotency and carrier read-back/reconciliation.
- VICIdial: exact operation/event mappings and campaign-isolation conformance tests.

## P2 gaps

- unified message search and timeline;
- central dashboard read model;
- business analytics/usage normalization;
- full observability trace propagation across all channel paths.
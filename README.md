# Codestra Communications Platform

This repository is the **communications-platform architecture and coordination authority** for Codestra. It defines the unified product model, channel contracts, cross-repository ownership map, integration rules, release sequencing, dashboards, and operator/developer experience for email, SMS, voice, webhooks and related communications capabilities.

The repository-only observability alert boundary is defined in [`docs/OBSERVABILITY-ALERT-DELIVERY-BOUNDARY.md`](docs/OBSERVABILITY-ALERT-DELIVERY-BOUNDARY.md). Alertmanager may reach providers only through Middleware's durable governed adapter path; direct SMTP and provider delivery remain disabled.

It is intentionally **not** a second runtime implementation of systems that already have principal repositories.

## Principal runtime authorities

- `appolon1908-hue/klyrow.com` — email runtime: Postal, Mautic, tenant email operations, delivery events, suppressions and deliverability
- `appolon1908-hue/telnexa` — SMS runtime: Jasmin/SMPP/HTTP, outbound/inbound SMS, DLRs and SMS billing/routing
- `appolon1908-hue/Vicidialer-Codestra` — voice/contact-center connector runtime: VICIdial/Asterisk, campaigns, calls, queues, callbacks, dispositions, recordings and transfers
- `appolon1908-hue/Middleware-` — privileged cross-system write/control authority: auth revalidation, tenant isolation, policy, command ledger, idempotency, inbox/outbox, retries, reconciliation and audit
- `appolon1908-hue/Kong` — API gateway/security authority
- `appolon1908-hue/Keycloak` — identity/OIDC authority
- `appolon1908-hue/Caddy` — public TLS/edge authority
- `appolon1908-hue/SDK-repository` — public contracts, generated SDKs, webhook helpers, connector-kit and developer tooling
- `appolon1908-hue/N8N` — orchestration only; privileged mutations go through Middleware
- `appolon1908-hue/Odoo` — CRM/business state and communications-related campaign/business workflows

## Permanent system rule

```text
Application / Product
        |
        v
Codestra SDK
        |
        v
Caddy -> Kong -> Keycloak validation
                |
                v
            Middleware
     +----------+----------+----------+
     |                     |          |
     v                     v          v
Klyrow/Email          Telnexa/SMS   VICIdial/Voice
Postal/Mautic         Jasmin        Asterisk
```

Status, delivery reports and provider events return through governed signed/private boundaries into Middleware, where they are normalized into canonical events for webhooks, SDK consumers, n8n, dashboards and business systems.

Middleware is the only cross-system write authority. The SDK, dashboard, n8n, websites and product applications must not create alternate privileged provider write paths.

## What this repository owns

This repository should contain documentation and coordination artifacts for:

- unified communications architecture;
- provider-neutral API model;
- email/SMS/voice capability matrix;
- canonical message and event lifecycle;
- sender/domain/number/identity model;
- templates and personalization model;
- suppression, consent and preference model;
- delivery/reputation/quality metrics;
- webhook event catalogue;
- dashboard information architecture;
- tenant/RBAC/quota requirements;
- cross-repository contract matrix;
- release dependency map;
- environment and production-readiness checklist;
- operator runbooks and incident ownership matrix.

It must not become the source of Postal, Jasmin, VICIdial/Asterisk, Middleware, Kong, Keycloak or SDK runtime code.

## Unified communications capability model

### Email

Runtime authority: `klyrow.com`

Required platform capabilities include sender domains, domain verification, SPF/DKIM/DMARC status, message submission, templates, scheduled delivery, campaigns, bounces, complaints, suppressions, consent/preferences, delivery events, quotas, reputation/deliverability and safe production gates.

### SMS

Runtime authority: `telnexa`

Required platform capabilities include send, bulk/scheduled send, sender identities, inbound SMS, delivery receipts, failure classification, opt-out/consent enforcement, rate limits, provider health, billing/usage and reconciliation.

### Voice

Runtime authority: `Vicidialer-Codestra`

Required platform capabilities include call commands, campaign isolation, agents, queues, callbacks, dispositions, transfer routing, recording metadata, call events, provisioning, read-back and reconciliation.

### Shared

Shared platform capabilities include:

- tenants and organizations;
- authentication and authorization;
- correlation and causation IDs;
- idempotency;
- quotas and rate policies;
- canonical message identifiers;
- status timelines;
- webhooks/events;
- templates;
- consent and suppression;
- audit trail;
- analytics and dashboards;
- provider health;
- reconciliation and dead-letter handling;
- developer SDKs and test fixtures.

## API ownership

The public/developer contract should be defined in `SDK-repository`. Runtime implementation and privileged command execution belong in `Middleware-` and the appropriate provider repository.

The communications platform should converge on provider-neutral concepts such as:

```text
POST /v1/communications/messages
GET  /v1/communications/messages/{message_id}
GET  /v1/communications/messages/{message_id}/events
POST /v1/communications/messages/{message_id}/cancel
POST /v1/communications/messages/{message_id}/retry   # policy controlled

GET/POST/PATCH /v1/communications/templates
GET              /v1/communications/channels
GET              /v1/communications/providers/health
GET              /v1/communications/usage
GET              /v1/communications/reputation
GET/POST          /v1/communications/suppressions
GET/POST/PATCH    /v1/communications/preferences
```

Channel-specific extensions may exist, but common state, error, idempotency and event rules must remain consistent.

## Canonical message lifecycle

```text
accepted
  -> queued
  -> submitted
  -> provider_accepted
  -> delivered

or

accepted
  -> suppressed / rejected / failed

or

submitted
  -> indeterminate
  -> reconciliation
  -> delivered / failed
```

Do not mark an externally effectful operation successful solely because an HTTP request returned 2xx. Provider acceptance/read-back and durable state rules belong to Middleware/provider contracts.

## Dashboard design

The central communications dashboard should aggregate, not replace provider administration UIs.

Views should include:

- organization/tenant overview;
- channel health;
- email deliverability and domain authentication;
- SMS delivery and opt-out metrics;
- voice queue/call health;
- unified message search and timeline;
- bounces/complaints/suppressions;
- provider status;
- quotas and usage;
- webhook health;
- dead letters and reconciliation;
- security/audit activity;
- infrastructure/operational links.

Grafana should be used for operational metrics where appropriate. Product/operator workflows requiring controlled actions should use a purpose-built admin UI calling governed APIs.

## Required documentation set

- `docs/MASTER-ARCHITECTURE-INDEX.md`
- `docs/ARCHITECTURE.md`
- `docs/REPOSITORY-OWNERSHIP.md`
- `docs/CANONICAL-API-CATALOGUE.md`
- `docs/EVENT-CATALOGUE.md`
- `docs/STATUS-MODEL.md`
- `docs/INTEGRATION-MATRIX.md`
- `docs/DEPENDENCY-GRAPH.md`
- `docs/EMAIL.md`
- `docs/SMS.md`
- `docs/VOICE.md`
- `docs/CONSENT-SUPPRESSION.md`
- `docs/REPUTATION-DELIVERABILITY.md`
- `docs/DASHBOARD.md`
- `docs/SOFTWARE-STACK.md`
- `docs/SECURITY.md`
- `docs/OBSERVABILITY.md`
- `docs/RELEASE-PLAN.md`
- `docs/CROSS-REPOSITORY-RELEASE-CHECKLIST.md`
- `docs/MASTER-ARCHITECTURE-REVIEW.md`
- `docs/CROSS-REPO-TEST-PLAN.md`
- `docs/PRODUCTION-READINESS.md`

## Build sequence

1. Confirm repository authority and boundaries.
2. Inventory existing APIs/capabilities in Klyrow, Telnexa, VICIdial, Middleware and SDK.
3. Define canonical communications OpenAPI/AsyncAPI contracts in `SDK-repository`.
4. Align Middleware command/event contracts.
5. Implement email adapter/contract coverage first against Klyrow.
6. Implement SMS contract coverage against Telnexa.
7. Implement voice contract coverage against VICIdial.
8. Add provider-neutral SDK facades.
9. Build central dashboard against read APIs/events.
10. Add cross-repository Pact/contract-drift/integration gates.
11. Prove Keycloak -> Kong -> Middleware identity path.
12. Run staging delivery/reconciliation tests with live effects constrained.
13. Complete production-readiness evidence and explicit activation approval.

## Branch policy

After bootstrap:

- `main` — accepted architecture/coordination authority
- `development` — active architecture integration
- `staging` — release-candidate documentation/contract coordination
- `docs/*`, `feature/*`, `fix/*` — scoped work

Merging this repository does not activate any email, SMS or voice capability.

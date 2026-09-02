# Step 6 — Communications Dashboard Read Model v1

## Authority

Repository: `appolon1908-hue/communication-platform-`

Branch: `feat/dashboard-read-model-v1`

This branch defines the normalized read model and dashboard information architecture. It does not implement privileged provider actions.

## Sources

The dashboard consumes governed read APIs/events from Middleware and approved provider projections. It must not query Postal, Jasmin, VICIdial, Odoo, Redis, PostgreSQL, or provider admin APIs directly for privileged workflows.

## Core dashboard entities

### Message
- message_id
- tenant_id
- channel: email | sms | voice
- status
- provider
- provider_reference
- correlation_id
- sender identity
- destination summary/redacted destination where appropriate
- created_at
- updated_at
- failure_code/failure_class
- reconciliation_state

### Message event
- event_id
- message_id
- tenant_id
- channel
- canonical status/event
- provider event type
- provider reference
- occurred_at
- failure evidence
- correlation_id

### Provider health
- provider
- channel
- status: healthy | degraded | unavailable | disabled
- reason
- checked_at
- latency/queue/readiness evidence where available

### Reputation/deliverability
- tenant/domain/provider scope
- status: good | watch | limited | suspended
- email SPF/DKIM/DMARC/domain verification state
- bounce rate
- complaint rate
- suppression rate
- provider acceptance/delivery trends
- last evaluated time

### Usage
- tenant
- channel
- provider
- period
- attempted/submitted/delivered/failed counts
- billable units where approved
- SMS segments/usage where exposed
- voice attempts/duration where exposed

### Reconciliation/dead-letter
- message/command ID
- channel/provider
- state
- reason
- first_seen_at
- last_attempt_at
- retry/reconciliation count
- operator-safe next action

## Required views

1. Executive communications overview
2. Unified message search and timeline
3. Email deliverability/domains/reputation
4. SMS delivery/DLR/inbound/opt-out operations
5. Voice queue/call/campaign health
6. Provider health
7. Webhook/event health
8. Reconciliation and dead letters
9. Tenant usage/quotas
10. Security/audit activity
11. Infrastructure links/operational telemetry

## Metrics and observability integration

Grafana is the operational visualization authority and should consume Prometheus/Loki/Tempo/OpenTelemetry-backed telemetry. Superset may consume curated analytics/read models for BI. The purpose-built admin dashboard consumes governed API read models.

Recommended common dimensions: `environment`, `service`, `tenant`, `channel`, `provider`, `status`, `error_class`, `correlation_id` where cardinality is safe.

## Action boundary

Read-only dashboards may aggregate normalized state. Any operator action such as retry, cancellation, suppression change, sender/domain change, reconciliation request or webhook configuration must call governed APIs through Caddy -> Kong -> Middleware with authorization, idempotency and audit.

## Data safety

Do not expose credentials, raw authorization headers, SMTP/SMPP secrets, private keys, webhook secrets, unrestricted message bodies, recordings, or sensitive provider configuration. Use least-privilege tenant-scoped views.

## Build dependency

The read-model specification can proceed while Steps 3–5 are being implemented. Final wiring cannot be certified until email, SMS and voice canonical status/event mappings are proven by cross-repository tests.

## Exit gate

Step 6 passes when all dashboard fields have authoritative sources, no direct privileged provider/database dependency exists, tenant/RBAC filtering is proven, Grafana/Superset/custom-UI boundaries are explicit, and read-model contract tests pass against the implemented channel runtimes.
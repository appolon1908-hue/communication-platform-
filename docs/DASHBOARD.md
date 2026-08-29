# Central Communications Dashboard Specification

## Objective

Provide one corporate-grade view of communications health, delivery, provider status, security and operations across Email, SMS and Voice without replacing the native provider administration systems.

## Dashboard layers

### 1. Executive overview

Widgets:
- total communications volume today / 7d / 30d
- delivery success by channel
- failure rate by channel
- active incidents
- provider health summary
- tenant/customer usage
- SLA status
- top failing domains/providers/routes

### 2. Email dashboard

Source authority: Klyrow / Postal / Mautic via governed read models.

Views:
- accepted, queued, submitted, delivered
- hard/soft bounce rate
- complaint rate
- suppression count
- SPF status
- DKIM selector/status
- DMARC policy/alignment/status
- PTR/rDNS and TLS health evidence where available
- domain-by-domain health
- sending IP health
- queue depth and processing age
- top errors
- webhook/callback health
- campaign/template performance
- sender reputation/deliverability trend

### 3. SMS dashboard

Source authority: Telnexa / Jasmin via Middleware/read models.

Views:
- submitted/delivered/failed/expired
- DLR latency
- inbound SMS volume
- opt-out rate
- provider/carrier health
- route quality
- throughput
- queue depth
- retry/reconciliation state
- usage/cost/margin where authorized

### 4. Voice dashboard

Source authority: Vicidialer-Codestra / VICIdial / Asterisk.

Views:
- calls attempted
- answered
- abandoned
- failed
- average handle time
- queue wait
- agent availability
- campaign health
- transfer success
- callback status
- dispositions
- recording metadata health
- trunk/route health

### 5. Unified message explorer

Search by:
- canonical message/command ID
- tenant
- channel
- recipient/contact reference
- correlation ID
- provider ID
- campaign
- date/time
- status

Timeline should show:
accepted -> policy -> queued -> provider submission -> provider acceptance -> delivery/failure -> callback -> reconciliation

Sensitive payloads must be redacted by default.

### 6. Provider health

Show:
- provider availability
- API latency
- error rate
- circuit-breaker state
- queue backlog
- last successful read-back
- last reconciliation
- degraded/maintenance state

### 7. Webhooks/events

Show:
- subscriptions/endpoints
- active/disabled/pending-verification
- delivery attempts
- success/failure rate
- replay rejection counts
- signature failures
- endpoint latency
- dead letters

Do not reveal signing secrets.

### 8. Security and audit

Show:
- authentication failures
- authorization denials
- tenant-boundary denials
- rate-limit events
- replay/idempotency conflicts
- capability denials
- admin actions
- reconciliation/replay actions

### 9. Infrastructure

Embed/link Grafana views for:
- Caddy
- Kong
- Keycloak
- Middleware
- Klyrow
- Telnexa
- VICIdial connector
- n8n
- Odoo
- PostgreSQL
- Redis
- NATS
- host/container health

## Technology split

### Grafana OSS
Operational and incident dashboards. Fast time-series views, alert context, logs and traces.

### Apache Superset
Business analytics, tenant reporting, campaign/channel analysis, trends, cost/usage and management reporting.

### Custom Admin UI
Controlled workflows requiring actions. The custom UI calls only governed APIs through Kong/Middleware.

## Dashboard software map

| Dashboard Need | Primary Tool | Supporting Repos |
| --- | --- | --- |
| Operational dashboards | Grafana | `Codestra-Grafana-`, `Codestra-Prometheus`, `Codestra-Loki`, `Codestra-Tempo` |
| Metrics collection | Prometheus | `Codestra-Prometheus`, `Codestra-Node-Exporter`, `Codestra-cAdvisor`, `Codestra-Postgres-Exporter`, `Codestra-Redis-Exporter`, `Codestra-Blackbox-Exporter` |
| Alert routing | Alertmanager | `Codestra-Alertmanager` |
| Logs | Loki | `Codestra-Loki`, `Codestra-Alloy`, `Codestra-Telemetry` |
| Traces | Tempo | `Codestra-Tempo`, `Codestra-Telemetry`, `Codestra-Alloy` |
| Analytics/reporting | Superset | `Superset` |
| Secrets and leases | OpenBao | `Codestra-OpenBao` |
| Controlled actions | Custom admin UI | Product/dashboard repo TBD, calling Kong -> Middleware only |

## Required Grafana folders

- Platform Overview
- Communications Overview
- Email and Deliverability
- SMS and DLR
- Voice and Contact Center
- Middleware Commands and Reconciliation
- Provider Health
- Webhooks and Events
- Security and Audit
- Infrastructure
- Staging and Production Gates

## Required Superset subject areas

- tenant communications usage
- campaign performance
- channel/provider quality
- deliverability trends
- cost and margin analytics
- SLA attainment
- opt-out, consent and suppression trends
- product/customer communications volume

## RBAC

Roles should include at minimum:
- platform_admin
- security_operator
- communications_operator
- tenant_admin
- support
- analyst
- read_only

Tenant users must only see their own tenant data. Provider credentials and infrastructure secrets are never displayed.

## Dashboard API requirements

Read endpoints should support efficient pagination, time windows and filters:

- GET /v1/communications/overview
- GET /v1/communications/messages
- GET /v1/communications/messages/{id}
- GET /v1/communications/messages/{id}/events
- GET /v1/communications/channels/health
- GET /v1/communications/providers/health
- GET /v1/communications/reputation
- GET /v1/communications/domains
- GET /v1/communications/suppressions
- GET /v1/communications/usage
- GET /v1/communications/webhooks/health
- GET /v1/communications/reconciliation

Exact public/private ownership must be finalized in SDK and Middleware contracts.

## Non-negotiable rule

Dashboards may observe broadly according to RBAC, but effectful actions must never directly call Postal, Jasmin, Asterisk/VICIdial, databases or provider APIs. All privileged actions go through Kong -> Middleware -> owning adapter/runtime.

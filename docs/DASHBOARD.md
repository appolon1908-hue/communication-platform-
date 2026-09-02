# Central Communications Dashboard Specification

## Objective

Provide one corporate-grade view of communications health, delivery, provider status, security, incidents and operations across Email, SMS and Voice without replacing the native provider administration systems.

Grafana is the operational/SRE dashboard. Superset is the business/management analytics dashboard. Controlled actions belong in governed application/admin UIs that call Kong -> Middleware.

## Primary operational question

The Grafana layer must make it possible to answer:

> What is broken, where, since when, which business/customer is affected, and what changed?

The answer should correlate Prometheus metrics, Alertmanager incidents, Loki logs, Tempo traces and deployment/configuration-change evidence.

## Dashboard layers

### 1. Executive overview

Widgets:
- total communications volume today / 7d / 30d
- delivery success by channel
- failure rate by channel
- active incidents by severity
- provider health summary
- tenant/customer usage
- SLA/SLO status
- top failing domains/providers/routes/services
- current deployment/config-change markers

### 2. Incident command dashboard

Source authorities: Prometheus + Alertmanager + Loki + Tempo + deployment evidence.

Views:
- firing critical/high/warning/informational alerts
- incident ID and acknowledgement/escalation state from Middleware
- business/application and service owner
- environment/server/container
- alert start time and duration
- related deployment SHA/config change
- correlated metrics
- related logs by `trace_id` / `correlation_id`
- distributed trace link
- runbook link
- affected dependency/provider
- silence/maintenance state
- recurrence history

Alertmanager is routing-only. Acknowledge, escalation, ticketing and approved notification actions must be governed through Middleware or a controlled operator UI.

### 3. Email dashboard

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

### 4. SMS dashboard

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

### 5. Voice dashboard

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

### 6. Unified message explorer

Search by:
- canonical message/command ID
- tenant/customer reference where authorized
- channel
- recipient/contact reference
- correlation ID
- provider ID
- campaign
- date/time
- status

Timeline should show:

```text
accepted -> policy -> queued -> provider submission -> provider acceptance
        -> delivery/failure -> callback -> reconciliation
```

Sensitive payloads must be redacted by default.

### 7. Provider health

Show:
- provider availability
- API latency
- error rate
- circuit-breaker state
- queue backlog
- last successful read-back
- last reconciliation
- degraded/maintenance state

### 8. Webhooks/events

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

### 9. Security and audit

Show:
- authentication failures
- authorization denials
- tenant-boundary denials
- rate-limit events
- replay/idempotency conflicts
- capability denials
- admin actions
- reconciliation/replay actions
- OpenBao auth/lease/rotation failures without exposing secrets

### 10. Infrastructure

Grafana operational views should cover:
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
- host/container health via Node Exporter/cAdvisor
- synthetic HTTPS/TLS/DNS checks via Blackbox Exporter
- Alloy/OpenTelemetry collection health
- Prometheus
- Alertmanager
- Loki
- Tempo
- OpenBao

## Alertmanager dashboard behavior

Canonical host: `aler.codestra.media`.

Alertmanager views should expose operational state such as:
- firing/resolved alerts
- alert groups
- grouping key
- receiver
- silence state
- inhibition state
- notification failures/retries
- cluster health when deployed redundantly
- `CodestraWatchdog` heartbeat path

The dashboard must never expose receiver bearer tokens or webhook secret values.

## Technology split

### Grafana OSS
Operational and incident dashboards. Fast time-series views, alert context, logs, traces, deployment correlations and SLOs.

### Apache Superset
Business analytics, tenant reporting, campaign/channel analysis, trends, cost/usage, conversion and management reporting against governed read-only datasets.

### Custom Admin UI
Controlled workflows requiring actions. The custom UI calls only governed APIs through Kong/Middleware.

## RBAC

Roles should include at minimum:
- platform_admin
- security_operator
- communications_operator
- business_owner
- tenant_admin
- support
- analyst
- read_only

Tenant users must only see their own tenant data. Provider credentials, API keys and infrastructure secrets are never displayed.

## Dashboard API/read-model requirements

Read endpoints should support efficient pagination, time windows and filters. The architecture catalogue includes targets such as:
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

These architecture targets are not proof that every endpoint is already implemented. Runtime/public ownership must be proven in SDK/Middleware/provider repositories before release.

## Non-negotiable rule

Dashboards may observe broadly according to RBAC, but effectful actions must never directly call Postal, Jasmin, Asterisk/VICIdial, databases, provider APIs, Alertmanager receivers or external notification providers. All privileged actions go through Kong -> Middleware -> owning adapter/runtime.

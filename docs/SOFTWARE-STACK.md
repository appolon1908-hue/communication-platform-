# Communications Platform Supporting Software Stack

## Purpose

This document defines the recommended supporting software for the Codestra communications platform. It does not replace principal application repositories. Supporting software exists to observe, analyze, secure, operate and troubleshoot the platform.

## Core observability stack

### Grafana OSS — operational dashboard authority

Use Grafana for real-time operational dashboards and incident views across Caddy, Kong, Middleware, Keycloak, Klyrow, Telnexa, VICIdial, n8n, Odoo and infrastructure.

Primary views:
- platform health
- email delivery and reputation
- SMS delivery/DLR health
- voice/call queue health
- API latency/errors
- provider health
- queue/backlog/dead-letter state
- database/Redis/NATS health
- host/container capacity
- alert status

Grafana is a visualization layer only. It must not become a privileged write path into provider systems.

### Prometheus — metrics collection and alert source

Use Prometheus to scrape service, infrastructure and exporter metrics. It remains the canonical time-series metrics source for Grafana operational dashboards.

Required metric families include:
- HTTP request/error/latency
- command state and reconciliation counts
- inbox/outbox lag
- queue depth
- email accepted/delivered/bounced/complained/suppressed
- SMS submitted/delivered/failed/expired/opted-out
- voice call attempts/answered/failed/abandoned/queue depth
- provider latency and health
- database, Redis, NATS, container and host metrics

### Loki — centralized logs

Use Loki for searchable application and infrastructure logs displayed through Grafana.

Rules:
- no credentials, authorization headers, message bodies containing PII, SMTP credentials, provider keys or secrets in logs
- structured logs preferred
- correlation_id, tenant_id, service, environment and operation_id should be standard labels/fields where cardinality remains controlled
- retention and access must be environment/security scoped

### Tempo — distributed tracing

Use Tempo for end-to-end traces across:

Application -> Caddy -> Kong -> Middleware -> provider adapter -> Klyrow/Telnexa/VICIdial

Trace context should preserve correlation across asynchronous processing where practical. Tracing must never record secret-bearing headers or raw sensitive bodies.

### OpenTelemetry — instrumentation and collection standard

OpenTelemetry should be the vendor-neutral instrumentation layer for traces, metrics and logs where supported. Use OpenTelemetry Collector instances to receive, process and export telemetry into the selected backends.

## Business analytics stack

### Apache Superset — communications analytics and reporting

Use Superset for business/operations analytics that are not best represented as real-time infrastructure dashboards.

Recommended datasets/views:
- delivery performance by tenant/channel/provider
- email domain and campaign trends
- SMS usage/cost/margin trends
- call-center productivity and disposition trends
- campaign outcomes
- communication volume by customer/product
- opt-out/consent trends
- SLA attainment
- provider quality comparison
- monthly usage/chargeback reporting

Superset should read curated analytics/read models, not live provider administrative databases directly.

## Product/operator dashboard

A purpose-built communications admin UI is still required for controlled product workflows. It should call governed read/action APIs and cover:
- tenant configuration
- sender/domain/number state
- templates
- message search/timeline
- suppressions/preferences
- webhook configuration
- provider status
- reconciliation/dead-letter workflows
- quotas and usage
- user/RBAC views

Privileged actions must flow through Kong -> Middleware. The dashboard must never hold Postal/Jasmin/VICIdial administrative credentials.

## Optional supporting systems

### Alertmanager
Use for alert routing, grouping, silencing and escalation from Prometheus.

### cAdvisor + Node Exporter
Use for container and host metrics.

### PostgreSQL exporters
Use for database health and performance telemetry. Do not expose business rows through metrics.

### Blackbox Exporter
Use for external and internal synthetic health checks, including HTTPS/TLS and selected private endpoints from approved networks.

## Data ownership rule

Observability and analytics systems are secondary/read-oriented systems. They do not become authoritative stores for:
- CRM state
- message execution state
- billing ledgers
- identities
- provider truth
- campaign membership
- consent/suppression authority

Authoritative state remains in the owning application repositories/services.

## Initial deployment recommendation

Phase 1:
1. Prometheus
2. Alertmanager
3. Grafana OSS
4. Node Exporter
5. cAdvisor
6. PostgreSQL/Redis exporters
7. Blackbox Exporter

Phase 2:
8. OpenTelemetry Collector
9. Loki
10. Tempo

Phase 3:
11. Apache Superset
12. curated analytics/read-model pipeline
13. purpose-built communications admin dashboard

## Repository ownership

Deployment/configuration authority for shared supporting infrastructure belongs in `appolon1908-hue/Infustruction-repo`.

Dashboard architecture, metric definitions and cross-system information design belong in `appolon1908-hue/communication-platform-`.

Service-specific metrics/log/tracing instrumentation belongs in each principal service repository.
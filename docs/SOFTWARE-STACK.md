# Communications Platform Supporting Software Stack

## Purpose

This document defines the supporting software for the Codestra communications platform. Each observability component now has its own principal GitHub repository. `communication-platform-` owns architecture and information design; `Infustruction-repo` coordinates shared topology/deployment relationships; the dedicated component repositories own their own runtime/configuration source.

## Principal observability repositories

| Software | Principal repository | Principal responsibility |
|---|---|---|
| Grafana OSS | `appolon1908-hue/Codestra-Grafana-` | dashboards, folders, provisioning, data-source declarations, Grafana RBAC policy templates and Grafana release evidence |
| Prometheus | `appolon1908-hue/Codestra-Prometheus` | scrape configuration, TSDB/retention policy, recording/alert rules and Prometheus release evidence |
| Alertmanager | `appolon1908-hue/Codestra-Alertmanager` | alert routing, grouping, inhibition, silencing policy and non-secret receiver definitions |
| Loki | `appolon1908-hue/Codestra-Loki` | Loki ingestion, tenancy, storage and retention configuration |
| OpenTelemetry | `appolon1908-hue/Codestra-Telemetry` | OpenTelemetry Collector pipelines, receivers, processors, exporters and propagation conventions |
| Tempo | `appolon1908-hue/Codestra-Tempo` | Tempo trace ingestion, storage, retention and query configuration |

These repositories remain independent release authorities. No central repository may silently replace their accepted configuration.

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

### Alertmanager — alert delivery authority

Alertmanager owns routing, grouping, inhibition, escalation and receiver policy for Prometheus alerts. Secret-bearing receiver credentials are injected externally and never committed.

### Loki — centralized logs

Use Loki for searchable application and infrastructure logs displayed through Grafana.

Rules:
- no credentials, authorization headers, message bodies containing PII, SMTP credentials, provider keys or secrets in logs
- structured logs preferred
- correlation_id, tenant-safe identifier, service, environment and operation_id should be standard fields; labels must remain cardinality-controlled
- retention and access must be environment/security scoped

### Tempo — distributed tracing

Use Tempo for end-to-end traces across:

Application -> Caddy -> Kong -> Middleware -> provider adapter -> Klyrow/Telnexa/VICIdial

Trace context should preserve correlation across asynchronous processing where practical. Tracing must never record secret-bearing headers or raw sensitive bodies.

### OpenTelemetry — instrumentation and collection standard

OpenTelemetry is the vendor-neutral instrumentation and collection standard. The dedicated Telemetry repository owns Collector pipelines and cross-service propagation conventions; each application repository owns its own instrumentation code.

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

Superset should read curated analytics/read models, not live provider administrative databases directly. If Superset receives a dedicated repository later, that repository becomes its principal source automatically under the repository-authority rule.

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

## Additional supporting systems

Node Exporter, cAdvisor, PostgreSQL exporters, Redis exporters and Blackbox Exporter may remain deployment components coordinated through infrastructure unless/until each receives its own principal repository.

## Data ownership rule

Observability and analytics systems are secondary/read-oriented systems. They do not become authoritative stores for CRM state, message execution state, billing ledgers, identities, provider truth, campaign membership or consent/suppression authority.

## Initial deployment sequence

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

Dedicated repositories own their component source/configuration. `Infustruction-repo` owns only cross-component topology, environment conventions, shared network/storage placement, DR coordination and combined deployment evidence. `communication-platform-` owns dashboard architecture, metric definitions and cross-system information design. Service-specific metrics/log/tracing instrumentation remains in each principal service repository.

See `docs/OBSERVABILITY-BRANCH-AND-UPGRADE-POLICY.md` for the permanent branch and future-upgrade model.
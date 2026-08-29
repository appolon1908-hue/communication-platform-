# Communications Platform Supporting Software Stack

## Purpose

This document defines the supporting dashboard, observability, analytics and secrets software for the Codestra communications platform. Each dedicated component repository remains its principal source. `communication-platform-` owns architecture and information design; `Infustruction-repo` coordinates shared topology/deployment relationships.

## Principal repositories

| Software | Principal repository | Principal responsibility |
|---|---|---|
| Grafana OSS | `appolon1908-hue/Codestra-Grafana-` | operational dashboards, folders, provisioning, datasource declarations, RBAC templates and incident views |
| Prometheus | `appolon1908-hue/Codestra-Prometheus` | metrics collection, scrape config, recording rules, alert rules and TSDB policy |
| Alertmanager | `appolon1908-hue/Codestra-Alertmanager` | grouping, deduplication, inhibition, silencing and routing to Middleware only |
| Loki | `appolon1908-hue/Codestra-Loki` | centralized log ingestion/storage/retention/query backend |
| Tempo | `appolon1908-hue/Codestra-Tempo` | distributed trace ingestion/storage/retention/query backend |
| OpenTelemetry Collector | `appolon1908-hue/Codestra-Telemetry` | OTLP receivers/processors/exporters and telemetry normalization |
| Apache Superset | `appolon1908-hue/Superset` | read-only business/management analytics and reporting |
| Node Exporter | `appolon1908-hue/Codestra-Node-Exporter` | host operating-system metrics |
| cAdvisor | `appolon1908-hue/Codestra-cAdvisor` | container resource metrics |
| PostgreSQL Exporter | desired `appolon1908-hue/Codestra-Postgres-Exporter` | read-only PostgreSQL metrics when repository is created/confirmed |
| Redis Exporter | `appolon1908-hue/Codestra-Redis-Exporter` | read-only Redis metrics |
| Blackbox Exporter | `appolon1908-hue/Codestra-Blackbox-Exporter` | synthetic HTTP/TCP/DNS/TLS probes |
| Grafana Alloy | `appolon1908-hue/Codestra-Alloy` | host/container log and telemetry collection agent profiles |
| OpenBao | `appolon1908-hue/Codestra-OpenBao` | runtime secrets, dynamic credentials, PKI/leases/rotation policy |

The connected GitHub inventory still does not show `Codestra-Postgres-Exporter`; architecture reserves the ownership boundary but does not treat the repository/runtime as existing.

## Canonical telemetry path

```text
Applications / hosts / containers
     |
     +--> Alloy / OpenTelemetry -----> Loki
     |                         \-----> Tempo
     |
     +--> metrics / exporters --------> Prometheus
                                           |
                                           v
                                      Alertmanager
                                           |
                                           v
                                       Middleware
                                           |
                              approved notification/ticket path

Prometheus + Loki + Tempo + Alertmanager -> Grafana
Governed analytics/read models ------------> Superset
Workload identities ------------------------> OpenBao
```

## Grafana — operational dashboard authority

Grafana is the main operational/SRE dashboard. It should answer:

> What is broken, where, since when, which business/customer is affected, and what changed?

Primary views include executive health, incidents, infrastructure, Middleware, Kong, Keycloak, Odoo, n8n, VICIdial, PostgreSQL, Redis, Caddy, deployment/version, security events, SLO/error-budget and application-specific dashboards.

Grafana is read-oriented and must never become a privileged provider write path.

## Prometheus — metrics and alert-rule authority

Prometheus scrapes service/infrastructure/exporter metrics and evaluates alert rules. Alert rules must attach stable low-cardinality labels such as `severity`, `environment`, `service`, `codestra_business` and `owner`, plus `summary`, `description` and `runbook_url` annotations.

## Alertmanager — central alert-routing brain

Alertmanager receives Prometheus alerts and owns:

- severity routing;
- grouping;
- deduplication;
- inhibition;
- maintenance silences;
- repeat intervals;
- alert receiver selection.

It does **not** independently send SMS/email/voice or create Odoo/n8n/provider writes. The canonical effect path is:

```text
Prometheus -> Alertmanager -> Middleware -> approved channel / Odoo / n8n
```

Middleware owns durable incident IDs, acknowledgement, escalation, notification authorization and effectful integrations.

## Loki — centralized log authority

Loki stores searchable logs for Linux/systemd, containers, Caddy, Kong, Keycloak, Middleware, Odoo, n8n, PostgreSQL, Redis, VICIdial, application backends, workers, OpenBao and security services.

Preferred structured fields include timestamp, level, service, environment, request/correlation/trace IDs, tenant ID as a field, operation, actor type, result and error code. Customer IDs, phone numbers, emails, request IDs and trace IDs must not be high-cardinality Loki labels.

## Tempo — distributed trace authority

Tempo traces the request path across services such as:

```text
Application -> Caddy -> Kong -> Middleware -> provider adapter/runtime
```

Trace context should correlate with Grafana/Loki/Prometheus without recording secret-bearing headers or raw sensitive bodies.

## OpenTelemetry + Alloy — collection standard

OpenTelemetry defines vendor-neutral telemetry instrumentation/collection. Alloy is the host/container collection agent. Reusable profiles should exist for edge/gateway, Middleware, databases, provider servers, application servers and VICIdial.

## Exporters

- Node Exporter: CPU, memory, disk, filesystem, network, load, uptime and safe textfile operational metrics.
- cAdvisor: container CPU/memory/network/filesystem/throttling/resource usage.
- PostgreSQL Exporter: connections, locks, deadlocks, WAL, checkpoints, replication, cache, transaction age and vacuum health using a read-only account.
- Redis Exporter: memory, clients, commands, keyspace, eviction, replication, persistence and latency.
- Blackbox Exporter: HTTPS/TCP/DNS/TLS reachability and certificate expiry.

Exporter credentials, where required, must be read-only.

## Superset — business analytics

Superset is separate from Grafana. It handles business/management reporting such as tenant/channel/provider delivery trends, campaign performance, cost/margin, call-center productivity and monthly usage. It reads governed analytics/read models or replicas and must not mutate production business state.

## OpenBao — secrets authority

OpenBao owns runtime API keys, provider credentials, database credentials, webhook signing secrets, certificates and dynamic leases. Git repositories store only policies/templates/references, never real secret values.

## Product/operator dashboard

A purpose-built admin UI is still required for effectful workflows such as tenant configuration, templates, suppressions/preferences, webhook management, reconciliation/dead-letter operations and controlled provider/business actions. It calls governed APIs through Kong -> Middleware.

## Deployment sequence

Recommended dependency order:

1. OpenBao/security foundation.
2. Alloy + Node Exporter + cAdvisor.
3. PostgreSQL/Redis exporters.
4. Blackbox Exporter.
5. Prometheus.
6. Alertmanager routing source/config.
7. Loki.
8. Tempo.
9. OpenTelemetry Collector application pipelines.
10. Grafana operational dashboard.
11. Middleware alert ingestion/incident routing proof.
12. Superset business analytics.
13. Purpose-built communications operator dashboard.

Repository/source preparation does not equal runtime deployment or production activation.

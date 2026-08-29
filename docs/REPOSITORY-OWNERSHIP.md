# Communications Repository Ownership Matrix

## Permanent rule

Every component with a dedicated repository keeps that repository as its principal source. `communication-platform-` is the **master architecture, ownership, dependency and release-coordination authority**; it does not become a second runtime source for software already owned elsewhere.

| Capability | Principal repository | Owns | Must not own |
|---|---|---|---|
| Edge/TLS | appolon1908-hue/Caddy | TLS termination, host/path routing, security headers, mTLS edge policy, Caddy->Kong handoff | identity issuance, API authorization, provider writes |
| API gateway | appolon1908-hue/Kong | services/routes/plugins, OIDC/JWT gateway validation, scopes, rate limits, route policy | application business logic, provider runtime |
| Identity | appolon1908-hue/Keycloak | realm/client desired state, PKCE, Client Credentials, scopes/audiences, token issuance policy | API execution, provider credentials |
| Control plane | appolon1908-hue/Middleware- | privileged command/event boundary, tenant/actor auth, idempotency, inbox/outbox, durable ledger, policy, adapters, retries, reconciliation, audit | duplicate provider runtime, SDK distribution |
| Email | appolon1908-hue/klyrow.com | Postal/Mautic email runtime, sender/domain onboarding, delivery, bounces, complaints, suppressions, deliverability/provider truth | cross-system authorization or alternate Middleware path |
| SMS | appolon1908-hue/telnexa | Jasmin/SMPP/HTTP SMS runtime, MO/DLR events, routing/billing/provider truth | voice runtime, direct CRM mutation |
| Voice | appolon1908-hue/Vicidialer-Codestra | VICIdial/Asterisk connector runtime, campaigns, calls, queues, callbacks, dispositions, transfers, read-back | SMS/email runtime, direct Odoo DB writes |
| SDK/contracts | appolon1908-hue/SDK-repository | OpenAPI/AsyncAPI, generated clients, webhook SDK, connector-kit, n8n nodes, developer tooling | privileged provider execution or secrets |
| Orchestration | appolon1908-hue/N8N | approved workflow packs, timing/branching/human workflow coordination | direct provider/Odoo/VICIdial/Jasmin/Postal writes |
| CRM/business state | appolon1908-hue/Odoo | CRM records, leads, campaign business workflows, activities, approved business state | provider delivery engine or cross-system control plane |
| Architecture/master coordination | appolon1908-hue/communication-platform- | ownership matrix, canonical API/event catalogue, status model, dashboard specification, integration matrix, dependency graph, cross-repo release checklist | runtime implementations already owned elsewhere |
| Infrastructure coordination | appolon1908-hue/Infustruction-repo | environment topology, network/storage conventions, shared deployment coordination, backup/restore/DR policy, cross-stack release evidence | duplicating component configuration owned by dedicated repos |
| Grafana | appolon1908-hue/Codestra-Grafana- | Grafana config/provisioning, dashboards, folders, datasource declarations, Grafana RBAC templates, incident/executive views | Prometheus/Loki/Tempo runtime configuration or business/provider writes |
| Prometheus | appolon1908-hue/Codestra-Prometheus | scrape config, recording rules, alert rules, retention/TSDB policy, metric-source integration | Alertmanager routing or Grafana dashboard ownership |
| Alertmanager | appolon1908-hue/Codestra-Alertmanager | grouping, deduplication, inhibition, silence policy, severity routing, Middleware-only alert webhook configuration | metric collection, direct SMS/email/voice/PagerDuty/Slack delivery, Odoo/n8n writes |
| Loki | appolon1908-hue/Codestra-Loki | Loki runtime/config, ingestion/storage/retention policy, log tenancy, log-query authority | application business state, Grafana dashboard ownership |
| OpenTelemetry Collector | appolon1908-hue/Codestra-Telemetry | OTLP receivers/processors/exporters, telemetry normalization, collector pipeline config | authoritative application state or dashboard ownership |
| Tempo | appolon1908-hue/Codestra-Tempo | trace ingestion/storage/retention, trace backend config | application instrumentation or metrics/log storage |
| Grafana Alloy | appolon1908-hue/Codestra-Alloy | host/container log and telemetry collection profiles, agent-side discovery and forwarding | central metric/log/trace storage, business writes |
| Node Exporter | appolon1908-hue/Codestra-Node-Exporter | host OS metric exporter source/config ownership | alert routing or application metrics |
| cAdvisor | appolon1908-hue/Codestra-cAdvisor | container resource metric exporter source/config ownership | application tracing/logging or business state |
| Redis Exporter | appolon1908-hue/Codestra-Redis-Exporter | Redis exporter source/config ownership | Redis application data mutation |
| Blackbox Exporter | appolon1908-hue/Codestra-Blackbox-Exporter | synthetic HTTP/TCP/DNS/TLS probe exporter source/config ownership | provider mutation or application state |
| PostgreSQL Exporter | desired: appolon1908-hue/Codestra-Postgres-Exporter | PostgreSQL read-only exporter source/config when repository exists | database writes or application migrations |
| Superset | appolon1908-hue/Superset | business/management BI dashboards, datasets, read-only analytics connections, row-level security policy | operational alert routing, production business writes |
| OpenBao | appolon1908-hue/Codestra-OpenBao | runtime secret authority, policies, dynamic credentials, PKI/lease/rotation configuration | application business logic or secrets committed to Git |

## Current repository inventory note

The PostgreSQL exporter repository named `Codestra-Postgres-Exporter` was not present in the connected GitHub inventory at the time of this architecture update. The row above reserves the intended ownership boundary but must not be treated as proof that the repository or runtime exists.

Several recently created observability repositories may still be in bootstrap/import work. Repository existence is not production readiness.

## Canonical effect path

```text
Application/Product
  -> SDK
  -> Caddy
  -> Kong
  -> Keycloak-validated identity
  -> Middleware
  -> owning provider adapter/runtime
```

Provider callbacks/events return through signed/private governed ingress to Middleware, which normalizes and persists them before they are exposed to SDK consumers, dashboards, n8n or Odoo workflows.

## Canonical observability path

```text
Applications / servers / containers
      |
      +--> Alloy / OpenTelemetry --------> Loki / Tempo
      +--> Exporters / app metrics ------> Prometheus
                                            |
                                            v
                                      Alertmanager
                                            |
                                            v
                                       Middleware
                                            |
                                approved notification/ticket path

Prometheus + Loki + Tempo + Alertmanager ---> Grafana
Business reporting/read replicas ----------> Superset
Runtime identities ------------------------> OpenBao for secrets
```

Alertmanager is a router, not a separate communication-delivery platform. Any effectful alert notification or ticket/orchestration write crosses Middleware.

## Cross-repository change rule

A public behavior change that crosses repositories must identify all affected owners before implementation. Release evidence must record exact accepted source SHAs for every changed repository and verify contract compatibility.

Examples:

- New email operation: SDK contract + Middleware implementation/adapter + Klyrow runtime/read-back + Kong route/security if externally exposed.
- New SMS event: Telnexa event source + Middleware normalization + SDK AsyncAPI + n8n/Odoo consumer changes only if needed.
- New voice command: SDK contract + Middleware command mapping + Vicidialer-Codestra runtime/read-back + Odoo/n8n workflow changes only where business behavior requires them.
- New platform metric: owning application instrumentation + Prometheus scrape/rule change if required + Grafana dashboard change if visualized.
- New alert: Prometheus rule + required labels/annotations + Alertmanager routing policy + Middleware incident/notification handling + Grafana incident visibility.
- New distributed trace: owning application instrumentation + Telemetry/Alloy pipeline + Tempo policy + Grafana correlation.
- New runtime secret: owning application policy + OpenBao path/policy + deployment identity; never a Git secret.

## No-bypass rules

1. SDKs do not call provider administration APIs directly.
2. n8n does not hold unrestricted provider credentials.
3. Dashboards do not mutate provider systems directly.
4. Caddy does not bypass Kong for shared public API mutations.
5. Kong does not replace Middleware business authorization/reconciliation.
6. Odoo does not directly drive external provider mutations when Middleware governance applies.
7. Provider systems do not write directly into another provider or product database.
8. Observability repositories never become business-state authorities.
9. Alertmanager never becomes a parallel SMS/email/voice notification platform.
10. Superset remains read-only against governed analytics/read models.
11. Exporters use read-only monitoring credentials where credentials are required.
12. OpenBao secrets are never committed into component repositories.
13. `Infustruction-repo` does not duplicate configuration owned by a dedicated component repository.

## Release coordination

This architecture repository owns the dependency map and cross-repository readiness checklist. Runtime approval remains with each owning repository and deployment process. Cross-stack upgrades must pin exact accepted SHA/version for every participating component and prove compatibility in staging before production promotion.

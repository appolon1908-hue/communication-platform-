# Communications Repository Ownership Matrix

## Permanent rule

Every component with a dedicated repository keeps that repository as its principal source. `communication-platform-` coordinates architecture and contracts; it does not become a second runtime source.

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
| Architecture/dashboard | appolon1908-hue/communication-platform- | ownership matrix, dashboard design, capability model, release dependency map, cross-repo architecture | runtime implementations already owned elsewhere |
| Infrastructure coordination | appolon1908-hue/Infustruction-repo | environment topology, network/storage conventions, shared deployment coordination, backup/restore/DR policy, cross-stack release evidence | duplicating component configuration owned by dedicated repos |
| Grafana | appolon1908-hue/Codestra-Grafana- | Grafana configuration, provisioning, dashboards, folders, data-source declarations, RBAC policy templates, Grafana-specific tests and release evidence | Prometheus/Loki/Tempo runtime configuration or provider writes |
| Prometheus | appolon1908-hue/Codestra-Prometheus | Prometheus configuration, scrape policy, recording/alert rules owned by Prometheus, retention/TSDB policy, Prometheus-specific tests and release evidence | Alertmanager routing or Grafana dashboards |
| Alertmanager | appolon1908-hue/Codestra-Alertmanager | alert routing, grouping, inhibition, silencing policy templates, receivers without secrets, Alertmanager-specific tests and release evidence | metric collection or dashboard ownership |
| Loki | appolon1908-hue/Codestra-Loki | Loki runtime/configuration, ingestion/storage/retention policy, log tenancy, Loki-specific tests and release evidence | application log instrumentation or Grafana dashboard ownership |
| OpenTelemetry | appolon1908-hue/Codestra-Telemetry | OpenTelemetry Collector pipelines, receivers/processors/exporters, telemetry propagation conventions, collector tests and release evidence | authoritative application state or backend-specific dashboards |
| Tempo | appolon1908-hue/Codestra-Tempo | Tempo runtime/configuration, trace ingestion/storage/retention, Tempo-specific tests and release evidence | application instrumentation or metrics/log storage |
| Superset | appolon1908-hue/Superset | Analytics dashboards, curated dataset definitions, semantic reporting, management reports and Superset release evidence | privileged provider/admin queries or operational alert ownership |
| Node Exporter | appolon1908-hue/Codestra-Node-Exporter | Host metrics exporter configuration, service definitions and release evidence | application metrics or dashboard ownership |
| cAdvisor | appolon1908-hue/Codestra-cAdvisor | Container metrics exporter configuration and release evidence | application metrics or dashboard ownership |
| PostgreSQL Exporter | appolon1908-hue/Codestra-Postgres-Exporter | PostgreSQL exporter configuration and database metric collection policy | database schema ownership or privileged query dashboards |
| Redis Exporter | appolon1908-hue/Codestra-Redis-Exporter | Redis exporter configuration and metric collection policy | Redis runtime configuration or dashboard ownership |
| Blackbox Exporter | appolon1908-hue/Codestra-Blackbox-Exporter | Synthetic probe configuration and external endpoint checks | application routing, DNS authority or provider writes |
| Grafana Alloy | appolon1908-hue/Codestra-Alloy | Local telemetry collection agent configuration for logs, metrics and traces | canonical metric storage or dashboard ownership |
| OpenBao | appolon1908-hue/Codestra-OpenBao | Secrets, leases, policies, audit telemetry and secret-store release evidence | application business state or committed secret values |

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

## Observability authority path

```text
Applications / infrastructure
        |
        +--> OpenTelemetry instrumentation/collector -> Tempo traces
        |                                         \-> Loki logs where configured
        +--> Prometheus scrape/exporters ------------> Prometheus metrics
                                                          |
                                                          +--> Alertmanager
                                                          +--> Grafana
        +--> Loki ----------------------------------------> Grafana
        +--> Tempo ---------------------------------------> Grafana
```

`Infustruction-repo` coordinates topology and deployment relationships only. It does not duplicate the canonical component configuration from the six dedicated observability repositories.

## Cross-repository change rule

A public behavior change that crosses repositories must identify all affected owners before implementation. The release evidence must record exact accepted source SHAs for every changed repository and verify contract compatibility.

Examples:
- New email operation: SDK contract + Middleware implementation/adapter + Klyrow runtime/read-back + Kong route/security if externally exposed.
- New SMS event: Telnexa event source + Middleware normalization + SDK AsyncAPI + n8n/Odoo consumer changes only if needed.
- New voice command: SDK contract + Middleware command mapping + Vicidialer-Codestra runtime/read-back + Odoo/n8n workflow changes only where business behavior requires them.
- New platform metric: owning application instrumentation + Prometheus scrape/rule change if required + Grafana dashboard change if visualized.
- New distributed trace: owning application instrumentation + Telemetry collector pipeline + Tempo policy + Grafana visualization if required.

## No-bypass rules

1. SDKs do not call provider administration APIs directly.
2. n8n does not hold unrestricted provider credentials.
3. Dashboards do not mutate provider systems directly.
4. Caddy does not bypass Kong for shared public API mutations.
5. Kong does not replace Middleware business authorization/reconciliation.
6. Odoo does not directly drive external provider mutations when Middleware governance applies.
7. Provider systems do not write directly into another provider or product database.
8. Observability repositories never become business-state authorities.
9. `Infustruction-repo` does not duplicate configuration owned by a dedicated observability repository.

## Release coordination

The architecture repo owns the dependency map and readiness checklist. Runtime approval remains with each owning repository and its deployment process. Cross-stack upgrades must pin the exact accepted SHA/version for each participating component.

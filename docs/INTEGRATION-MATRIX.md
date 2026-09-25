# Integration Matrix

This matrix defines allowed cross-system paths. It is the coordination authority; owning repositories remain responsible for implementation and runtime proof.

| Source | Destination | Purpose | Auth/transport expectation | Effect rule |
|---|---|---|---|---|
| Applications/products | Caddy | Public HTTPS ingress | TLS | No business logic at edge |
| Caddy | Kong | Shared API gateway handoff | private/restricted upstream | Caddy must not bypass Kong for shared public mutations |
| Kong | Keycloak/JWKS | Token validation metadata | OIDC/JWKS | Gateway validates, does not issue identity |
| Kong | Middleware | Authenticated API/control-plane request | original bearer where contract requires, tenant/correlation context | Middleware revalidates identity/policy |
| Middleware | Klyrow | Email execution/read-back | private authenticated adapter | Email effects only through Middleware |
| Middleware | Telnexa | SMS execution/read-back | private authenticated adapter | SMS effects only through Middleware |
| Middleware | VICIdial | Voice/call-center execution/read-back | private authenticated adapter | Voice effects only through Middleware |
| Middleware | Odoo | CRM/business updates | governed adapter | No direct provider->Odoo writes |
| Middleware | n8n | Approved orchestration trigger/context | governed webhook/API | n8n must not gain provider bypass credentials |
| n8n | Middleware | Request governed mutation/status | service identity | n8n orchestrates through Middleware only |
| SDK clients | Kong | Public/developer API | OIDC/service JWT | SDK never calls provider admin APIs directly |
| Provider callbacks | Middleware | Delivery/status/inbound events | signed/private/mTLS as appropriate | Normalize/persist before downstream consumers |
| Applications/servers | Alloy/OpenTelemetry | Logs/traces/metrics collection | private agent/OTLP | Telemetry only, no business mutations |
| Alloy/OpenTelemetry | Loki | Log forwarding | private/authenticated | Redact secrets/PII before storage |
| Alloy/OpenTelemetry | Tempo | Trace forwarding | private/authenticated | Trace data only |
| Exporters/apps | Prometheus | Metrics scrape/remote collection | private/read-only | Low-cardinality labels only |
| Prometheus | Alertmanager | Firing/resolved alert groups | private Alertmanager integration | Alert rules stay in Prometheus; routing stays in Alertmanager |
| Alertmanager | Middleware | Alert/incident ingestion | authenticated webhook target loaded from runtime secret | Only approved alert effect path |
| Middleware | notification channels | Incident escalation | policy-controlled adapters | Alertmanager never sends directly |
| Middleware | Odoo | Incident/ticket record | governed adapter | Only when incident policy requires |
| Middleware | n8n | Incident orchestration | governed trigger | No direct Alertmanager->n8n privileged path |
| Prometheus | Grafana | Metrics datasource | read-only | Dashboard only |
| Loki | Grafana | Logs datasource | read-only | Dashboard only |
| Tempo | Grafana | Traces datasource | read-only | Dashboard only |
| Alertmanager | Grafana | Alert state datasource | read-only | Grafana does not mutate notification providers |
| Governed analytics/read replicas | Superset | Business reporting | read-only DB/service credential | Superset must not write production business state |
| Workloads | OpenBao | Runtime secrets/dynamic credentials | workload identity/policy | Secrets never committed to Git |
| Operators | Grafana/Superset | Browser UI | Keycloak SSO/RBAC | Viewer/editor/admin boundaries |

## Business/application onboarding rule

Every business application joining the platform must declare:

- `codestra_business` identifier;
- stable `service` identifiers;
- environment names;
- owning team;
- Keycloak client/scope requirements;
- Kong route requirements if externally exposed;
- Middleware commands/events used;
- provider dependencies;
- telemetry endpoints/pipelines;
- OpenBao secret paths/policies;
- Grafana dashboard folder/ownership;
- Superset datasets if business analytics are required;
- release dependencies and rollback owner.

## Alert integration rule

The required alert chain is:

```text
Prometheus -> Alertmanager -> Middleware -> approved channel / Odoo / n8n
```

Alertmanager owns grouping, deduplication, inhibition and silence policy. Middleware owns durable incident identity, acknowledgement, escalation and all effectful integrations.

## Direct-path prohibitions

The following paths are forbidden unless the master architecture is explicitly revised and security-reviewed:

- Grafana -> provider write API
- Superset -> production business write DB
- Alertmanager -> direct SMS/email/voice provider
- Alertmanager -> direct Odoo write
- Alertmanager -> direct privileged n8n workflow
- n8n -> Postal/Jasmin/VICIdial unrestricted write
- browser/frontend -> provider secret/API administration endpoint
- provider A -> provider B database
- application repo -> embedded production secret

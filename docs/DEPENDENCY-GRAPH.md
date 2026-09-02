# Cross-Repository Dependency Graph

This document defines runtime and release dependencies. It does not grant deployment authority to this repository.

## Runtime graph

```text
                          Keycloak
                             |
Applications -> Caddy -> Kong+------------------+
                             |                  |
                             v                  |
                         Middleware <-----------+
                       /     |      \
                      /      |       \
                 Klyrow   Telnexa   VICIdial
                 Email      SMS      Voice
                    \        |        /
                     \       |       /
                      +---- events ---+
                            |
                            v
                        Middleware
                       /     |      \
                      v      v       v
                    Odoo    n8n   read models

Telemetry:
Applications/hosts -> Alloy/OpenTelemetry -> Loki/Tempo
Applications/exporters -------------------> Prometheus
Prometheus -------------------------------> Alertmanager
Alertmanager -----------------------------> Middleware
Prometheus/Loki/Tempo/Alertmanager --------> Grafana
Governed analytics/read replicas ----------> Superset
Runtime workloads -------------------------> OpenBao
```

## Principal release dependencies

### Public API/control-plane change

```text
SDK contract
   -> Keycloak scope/client if identity changes
   -> Kong route/plugin if exposure changes
   -> Middleware implementation/policy
   -> owning provider adapter/runtime
   -> integration tests
   -> Grafana/observability updates
```

### Email capability

```text
SDK -> Kong/Keycloak as required -> Middleware -> Klyrow -> callback/read-back -> Middleware -> SDK/event consumers
```

### SMS capability

```text
SDK -> Kong/Keycloak as required -> Middleware -> Telnexa -> DLR/MO -> Middleware -> SDK/event consumers
```

### Voice capability

```text
SDK -> Kong/Keycloak as required -> Middleware -> Vicidialer-Codestra -> call/read-back events -> Middleware -> Odoo/n8n as governed
```

### New metric/alert

```text
owning application/exporter
   -> Prometheus scrape/rule
   -> Alertmanager metadata/routing contract
   -> Middleware incident/notification handling
   -> Grafana dashboard/incident view
```

### New logs/traces

```text
owning application instrumentation
   -> Alloy/OpenTelemetry pipeline
   -> Loki and/or Tempo
   -> Grafana datasource/correlation
```

### New business analytics dataset

```text
owning business system
   -> governed read model/replica
   -> Superset dataset/RLS
   -> management dashboard
```

### New secret/provider credential

```text
owning workload identity
   -> OpenBao policy/path
   -> deployment secret injection
   -> application/provider adapter
```

No secret value is a Git dependency.

## Alertmanager dependency position

Alertmanager depends on:

- Prometheus emitting valid alert labels/annotations;
- runtime secret injection for the Middleware webhook URL/token;
- a real authenticated Middleware alert-ingestion implementation before activation;
- Grafana only for visualization, not routing;
- Middleware for incident IDs, acknowledgement, escalation and notification effects.

Middleware must not depend on Alertmanager for ordinary business commands. Alertmanager is an observability/incident input, not the central application API.

## Release ordering rules

1. Contract/identity changes land before consumers depend on them.
2. Backward-compatible provider/runtime support lands before public SDK promotion where possible.
3. Middleware remains compatible with both old and new provider versions during staged rollout when feasible.
4. Observability must be ready before activating a new production effect path.
5. Staging proves the complete dependency chain before production approval.
6. Exact accepted SHAs/versions are recorded for every participating repository.
7. Production activation requires an explicit rollback path for each changed runtime.
8. A documentation merge in `communication-platform-` never activates a runtime dependency.

## Failure-domain rule

A dependency must fail closed for privileged writes and fail visibly for monitoring/read paths. Unknown/stale provider or observability state must not be silently converted to healthy/successful.

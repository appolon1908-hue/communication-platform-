# Observability, Analytics, Telemetry, and Secrets Wiring v1

## Canonical DNS
All records resolve to `37.27.128.39`, TTL `600`.

- `graf.codestra.media` — Grafana
- `prom.codestra.media` — Prometheus
- `aler.codestra.media` — Alertmanager
- `loki.codestra.media` — Loki
- `temp.codestra.media` — Tempo
- `otel.codestra.media` — OpenTelemetry Collector
- `supe.codestra.media` — Superset
- `node.codestra.media` — Node Exporter
- `cadv.codestra.media` — cAdvisor
- `pgex.codestra.media` — PostgreSQL Exporter
- `rdex.codestra.media` — Redis Exporter
- `blac.codestra.media` — Blackbox Exporter
- `allo.codestra.media` — Grafana Alloy
- `bao.codestra.media` — OpenBao

No alternate service hostname is canonical. Repo docs/config examples must use the assigned four-character hostname.

## Wiring

### Metrics
Node Exporter, cAdvisor, PostgreSQL Exporter, Redis Exporter, Blackbox Exporter, service-native metrics, OpenTelemetry/Alloy metrics -> Prometheus -> Grafana. Prometheus evaluates alert rules -> Alertmanager.

### Logs
Applications, containers, Caddy, Kong, Middleware and approved platform services -> Alloy/OpenTelemetry Collector where used -> Loki -> Grafana.

### Traces
Applications and platform services -> OpenTelemetry Collector and/or Alloy -> Tempo -> Grafana. Trace context should propagate Caddy -> Kong -> Middleware -> provider/runtime where supported.

### Analytics
Curated read models/analytics datasets -> Superset. Superset must not query provider administration databases as an uncontrolled write or privileged path.

### Secrets
Approved services -> OpenBao using least-privilege machine identities -> scoped secrets/leases. OpenBao audit/health telemetry -> observability stack. Never export secret values into logs, traces, metrics, dashboards, or Superset.

## Exposure classes
Browser-facing through Caddy: `graf`, `supe`, protected `bao`.
Private service endpoints: `prom`, `aler`, `loki`, `temp`, `otel`, `node`, `cadv`, `pgex`, `rdex`, `blac`, `allo`.

DNS resolution does not authorize public service-port exposure.

## Repository authority
Each component repository owns its own component configuration and release lifecycle. `communication-platform-` owns cross-system information architecture. `Infustruction-repo` owns shared network/topology/DR coordination. Caddy owns browser-facing TLS/reverse-proxy policy.

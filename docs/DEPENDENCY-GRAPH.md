# Communications Dependency Graph

Date: 2026-08-29

## Canonical Runtime Graph

```text
Products
  -> SDK-repository generated clients
  -> Caddy
  -> Kong
  -> Keycloak token validation
  -> Middleware
      -> Klyrow email runtime
      -> Telnexa SMS runtime
      -> Vicidialer-Codestra voice runtime
      -> n8n orchestration events
      -> Odoo governed business updates
```

## Event Return Graph

```text
Klyrow/Telnexa/Vicidialer-Codestra
  -> signed/private provider event ingress
  -> Middleware normalization/read model
  -> canonical events
      -> SDK webhook consumers
      -> n8n workflows
      -> Odoo activities where approved
      -> dashboards and analytics read models
```

## Observability Graph

```text
Applications + infrastructure
  -> OpenTelemetry / Alloy
      -> Tempo traces
      -> Loki logs
      -> Prometheus metrics where applicable
  -> exporters
      -> Prometheus
          -> Alertmanager
          -> Grafana
  -> curated analytics/read models
      -> Superset
```

## Release Dependency Order

1. Architecture inventory accepted in `communication-platform-`.
2. SDK contract updated and frozen.
3. Middleware command/read/event implementation.
4. Provider runtime adapter/read-back implementation.
5. Kong/Keycloak route, scope, and caller identity configuration.
6. Observability instrumentation and dashboard panels.
7. Product backend SDK adoption.
8. Staging canaries and reconciliation evidence.
9. Production activation approval.

## Blocking Dependencies

| Dependency | Blocks |
| --- | --- |
| Keycloak/Kong auth matrix | Product production traffic to Middleware. |
| Durable Middleware communications read model | Production-grade message search/timeline/reconciliation. |
| Provider canaries | Production activation for email/SMS/voice. |
| SDK client generation | Product backend migrations away from raw HTTP. |
| Observability dashboards/alerts | Production readiness sign-off. |
| Secret store wiring | Live provider credentials and production flags. |

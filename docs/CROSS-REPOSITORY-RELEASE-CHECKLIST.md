# Cross-Repository Release Checklist

Use this checklist for any release that changes a behavior spanning more than one principal repository.

## 1. Scope and ownership

- [ ] Change has a clear owner and business/service scope.
- [ ] Every affected principal repository is identified.
- [ ] `REPOSITORY-OWNERSHIP.md` remains accurate.
- [ ] `INTEGRATION-MATRIX.md` includes every new/changed cross-system path.
- [ ] `DEPENDENCY-GRAPH.md` includes any new required dependency.
- [ ] No duplicate runtime authority was introduced into `communication-platform-`.

## 2. Contract authority

- [ ] Public API changes are represented in the SDK/OpenAPI authority where required.
- [ ] Public event changes are represented in the SDK/AsyncAPI authority where required.
- [ ] Canonical API/event/status names match the master catalogues.
- [ ] Backward-compatibility impact is documented.
- [ ] Contract-drift/compatibility gates pass where available.

## 3. Identity and authorization

- [ ] Required Keycloak clients/scopes/audiences are defined.
- [ ] Kong routes/plugins validate the intended identity contract.
- [ ] Middleware revalidates identity/tenant/capability for privileged operations.
- [ ] Browser clients do not receive provider secrets.
- [ ] Service credentials are short-lived or protected according to policy.

## 4. Secrets

- [ ] No real API key/password/token/private key is committed to Git.
- [ ] OpenBao path/policy/workload identity is defined where runtime secrets are needed.
- [ ] Staging and production secrets are separated.
- [ ] Rotation/revocation procedure exists for high-value provider credentials.

## 5. Effect-path safety

- [ ] Effectful requests follow `Caddy -> Kong -> Middleware -> owning runtime` where applicable.
- [ ] n8n does not gain a direct provider/Odoo bypass.
- [ ] Grafana/Superset/Alertmanager do not gain direct provider write capability.
- [ ] Odoo provider effects remain governed through Middleware.
- [ ] Idempotency and durable command/event state are present for externally effectful operations.
- [ ] Reconciliation/read-back requirements are defined.

## 6. Observability

- [ ] Service emits required metrics.
- [ ] Structured logs include stable service/environment/correlation fields without secrets.
- [ ] Trace propagation is present for cross-service paths where applicable.
- [ ] Prometheus scrape/recording/alert rules are updated.
- [ ] Alerts include required `severity`, `environment`, `service`, `codestra_business`, `owner` labels.
- [ ] Alerts include `summary`, `description`, `runbook_url` annotations.
- [ ] Alertmanager routing remains Middleware-only.
- [ ] Grafana dashboard/incident view is updated.
- [ ] Blackbox/endpoint probe is added where external reachability matters.

## 7. Database/cache/exporters

- [ ] Monitoring credentials are read-only.
- [ ] PostgreSQL/Redis exporter queries cannot mutate application state.
- [ ] High-cardinality/customer identifiers are not exported as metric labels.
- [ ] Capacity/connection/replication/latency thresholds are documented.

## 8. CI/source evidence

Record exact accepted heads:

```text
Repository                        SHA/version               CI result
---------------------------------------------------------------------
Caddy                             _______________________   __________
Kong                              _______________________   __________
Keycloak                          _______________________   __________
Middleware                        _______________________   __________
SDK                               _______________________   __________
Owning provider/runtime           _______________________   __________
Prometheus                        _______________________   __________
Alertmanager                      _______________________   __________
Grafana                           _______________________   __________
Loki/Tempo/Telemetry as needed    _______________________   __________
Other affected repositories       _______________________   __________
```

- [ ] Exact-head CI is green for all required repositories.
- [ ] Review threads/blocking annotations are resolved.
- [ ] Required independent approvals are recorded.
- [ ] No branch protection was bypassed.

## 9. Staging

- [ ] Exact approved source versions are deployed to staging.
- [ ] DNS/TLS/private-network rules match architecture.
- [ ] Health/readiness checks pass.
- [ ] Auth/token matrix passes where identity changed.
- [ ] Success, failure, retry and reconciliation paths were exercised.
- [ ] Alert fire/group/dedup/inhibit/resolve behavior was tested when alerts changed.
- [ ] Dashboard shows current deployment/version.
- [ ] Logs/traces/metrics correlate correctly.
- [ ] No unintended provider or business writes occurred.

## 10. Live-effect gates

Before any activation, explicitly record the relevant safety flags/capabilities. For communications/contact-center releases, preserve disabled states until approved, including examples such as:

```text
SEND_EVENTS=false
ENABLE_EXTERNAL_DELIVERY=false
LIVE_WRITE=false
ODOO_WRITE=false
N8N_DELIVERY_ENABLED=false
PRODUCTION_DIALING=DISABLED
CALLS_PLACED=0
```

A source merge must never be interpreted as permission to change these values.

## 11. Production approval

- [ ] Release/change ID exists.
- [ ] Human approver(s) are identified.
- [ ] Deployment window is confirmed.
- [ ] Backup/restore and rollback readiness are current.
- [ ] Alerting/incident ownership is staffed.
- [ ] Canary/smoke plan is defined.
- [ ] Go/no-go decision is explicit.

## 12. Production proof

- [ ] Exact production image/config/source provenance is recorded.
- [ ] Health checks pass.
- [ ] Public/private endpoint behavior matches policy.
- [ ] Metrics/logs/traces are visible.
- [ ] Alertmanager can route through Middleware if part of the release.
- [ ] No secret is exposed in logs/dashboards.
- [ ] Business/provider read-back proves intended effects.
- [ ] Post-deploy observation window completed.

## 13. Rollback

- [ ] Rollback trigger thresholds are defined.
- [ ] Previous known-good versions are pinned.
- [ ] Schema/data compatibility with rollback is proven.
- [ ] Provider side-effects already committed are reconciled, not blindly repeated.
- [ ] Rollback event and final status are recorded.

## Release rule

A cross-repository release is **NO-GO** while any required dependency is unreviewed, CI-failing, staging-unproven, missing runtime secrets/identity, missing rollback evidence, or dependent on a live effect that has not received explicit approval.

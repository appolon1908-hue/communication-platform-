# Observability Repository Branch and Upgrade Policy

## Scope

This policy applies to:

- `appolon1908-hue/Codestra-Grafana-`
- `appolon1908-hue/Codestra-Prometheus`
- `appolon1908-hue/Codestra-Alertmanager`
- `appolon1908-hue/Codestra-Loki`
- `appolon1908-hue/Codestra-Telemetry`
- `appolon1908-hue/Codestra-Tempo`

Another agent may create the actual branches. This document is the architecture authority for the required branch model and future upgrade process.

## Permanent branches required in every repository

| Branch | Purpose | May deploy? |
|---|---|---|
| `main` | accepted canonical source and release history | no automatic production mutation; source authority only |
| `development` | integrated active development after feature PRs | development only |
| `test` | deterministic component and compatibility testing | isolated test only |
| `staging` | release-candidate integration with the wider Codestra stack | staging only after gates |
| `production` | exact production-candidate source awaiting/representing explicit deployment approval | only through protected production workflow |

Promotion flow:

```text
feature/fix/upgrade/security/docs
        -> development
        -> test
        -> staging
        -> production
        -> main
```

`main` remains canonical history. A merge to `production` or `main` does not by itself authorize a server change.

## Short-lived branch families

### `feature/<scope>`
New capability or configuration, for example:
- `feature/grafana-email-deliverability-dashboard`
- `feature/prometheus-middleware-recording-rules`
- `feature/otel-kong-trace-pipeline`

### `fix/<scope>`
Ordinary correctness fixes that are not emergency production hotfixes.

### `docs/<scope>`
Documentation-only changes.

### `upgrade/<component>-<version>`
Every normal upstream software upgrade uses a dedicated upgrade branch. Examples:
- `upgrade/grafana-13.1.0`
- `upgrade/prometheus-3.8.0`
- `upgrade/alertmanager-0.31.0`
- `upgrade/loki-4.0.0`
- `upgrade/opentelemetry-collector-0.150.0`
- `upgrade/tempo-3.0.0`

Never perform an upstream major/minor upgrade directly on `development`, `staging`, `production` or `main`.

### `security/<advisory-or-cve>`
Security remediation with focused scope and required evidence.

### `hotfix/<incident-or-defect>`
Emergency production correction. Start from the exact accepted `production` SHA, validate, promote through the shortest approved emergency path, then back-merge/reconcile the exact fix into `main`, `development`, `test` and `staging` so branches do not drift.

### `rollback/<release-id>`
Only when rollback source/configuration itself must be reviewed. Ordinary rollback should use a previously accepted immutable artifact/configuration rather than creating new code during an incident.

### `release/<version-or-date>`
Optional short-lived release preparation branch when multiple changes must be frozen together. Do not use it as a permanent environment branch.

## Upgrade workflow

Every future upstream upgrade must follow this sequence:

1. Record current accepted source SHA, software version/image digest, configuration checksum and rollback artifact.
2. Read upstream release, migration, deprecation and security notes.
3. Create `upgrade/<component>-<target-version>` from the current accepted development baseline unless a security/hotfix process explicitly requires otherwise.
4. Pin the target version or immutable image digest; never introduce floating `latest` tags.
5. Run syntax/schema/config validation from a clean checkout.
6. Run component-specific unit/config tests.
7. Run backwards/forwards compatibility checks for stored data and APIs.
8. Run security/dependency/image scans.
9. Test migration and rollback with disposable data or a restoreable staging copy.
10. Promote through `development -> test -> staging`.
11. Run cross-stack acceptance with dependent components.
12. Record exact SHAs/digests/config checksums.
13. Promote to protected `production` only after explicit approval.
14. Deploy the exact accepted production artifact/configuration.
15. Run post-deployment health/read-back checks.
16. Promote/record the accepted release on `main` and tag it.

## Repository-specific upgrade gates

### Codestra-Grafana-
Must validate dashboard JSON/provisioning, datasource compatibility, plugin compatibility, authentication/RBAC behavior, folder/dashboard imports, database migrations if applicable, and dashboard smoke tests against staging datasources.

### Codestra-Prometheus
Must validate configuration with `promtool`, rule syntax/tests, scrape-target compatibility, TSDB/storage format and retention impacts, remote-write compatibility if used, query/recording-rule behavior and rollback.

### Codestra-Alertmanager
Must validate configuration, routing tree, inhibition rules, receiver templates, grouping behavior, silence compatibility and test alert delivery without leaking receiver secrets.

### Codestra-Loki
Must validate configuration/schema periods, storage backend compatibility, retention/compactor behavior, ingestion/query compatibility, tenant boundaries, label/cardinality rules and rollback/restore.

### Codestra-Telemetry
Must validate Collector configuration, receiver/processor/exporter compatibility, semantic-convention changes, resource attributes, sampling, memory/batch limits, TLS/auth boundaries and trace/log/metric delivery to staging backends.

### Codestra-Tempo
Must validate configuration, storage schema/backend compatibility, ingestion protocols, query behavior, retention/compaction, tenant boundaries, exemplar/trace-link compatibility and rollback/restore.

## Cross-repository compatibility gates

Changes that alter interfaces must identify dependent repositories. Minimum compatibility relationships:

```text
Codestra-Telemetry -> Codestra-Tempo
Codestra-Telemetry -> Codestra-Loki (when log export is used)
Codestra-Prometheus -> Codestra-Alertmanager
Codestra-Prometheus -> Codestra-Grafana-
Codestra-Loki -> Codestra-Grafana-
Codestra-Tempo -> Codestra-Grafana-
Applications -> Codestra-Prometheus / Codestra-Telemetry contracts
Infustruction-repo -> all six for topology only
```

A component must not silently change ports, protocols, datasource UIDs, metric names, labels, trace attributes or authentication expectations without updating and testing affected owners.

## Release evidence required

Every production upgrade should record:
- repository
- exact commit SHA
- upstream version
- immutable image digest/artifact checksum
- configuration checksum
- CI run IDs/results
- staging acceptance evidence
- migration evidence where applicable
- rollback target and rehearsal result
- deployment approval
- post-deployment health result

## Branch protection requirements

At minimum, protect `main`, `production`, `staging`, `test` and `development` from force-push/deletion. Require PR review and required CI on environment promotion branches. Production deployment credentials must be available only to protected deployment workflows/environments and never to ordinary PR jobs.

## No-secret rule

No branch may contain passwords, tokens, private keys, live datasource credentials, SMTP/chat/webhook receiver secrets, database credentials or secret-bearing runtime exports. Commit only secret references/templates; inject real values through the approved secret-management path.
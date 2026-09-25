# Canonical Status Model

This document defines status vocabularies that must remain distinct. A system must not collapse transport acceptance, provider acceptance, delivery, reconciliation and business/incident completion into one generic `success` value.

## 1. Communications message status

```text
accepted
  -> queued
  -> submitted
  -> provider_accepted
  -> delivered
```

Alternate terminal/exception paths:

```text
accepted -> suppressed
accepted -> rejected
queued/submitted -> failed
submitted/provider_accepted -> indeterminate -> reconciliation_required
reconciliation_required -> delivered | failed | dead_lettered
```

Definitions:

| Status | Meaning |
|---|---|
| accepted | Middleware durably accepted the request after auth/policy validation |
| queued | Awaiting provider dispatch |
| submitted | Submission attempt was made to provider/runtime |
| provider_accepted | Provider/runtime acknowledged request ownership |
| delivered | Provider/read-back evidence proves completion where the channel supports delivery proof |
| suppressed | Consent/suppression/policy intentionally prevented dispatch |
| rejected | Request failed validation/policy before accepted execution |
| failed | Terminal provider/control-plane failure |
| indeterminate | External effect cannot yet be proven |
| reconciliation_required | Durable read-back/reconciliation is required |
| dead_lettered | Retry/reconciliation policy exhausted; operator action required |

## 2. Middleware command/operation status

Canonical durable control-plane states:

```text
queued
-> dispatching
-> accepted
-> readback_pending
-> completed
```

Exception states:

```text
failed
reconciliation_required
dead_lettered
```

`completed` must mean the contract's required success evidence is satisfied; it must not mean merely that an outbound HTTP call returned 2xx.

## 3. Provider health status

```text
healthy
degraded
maintenance
unavailable
unknown
```

- `healthy`: required probes/read-back are inside policy thresholds.
- `degraded`: service is available but one or more SLO/capability thresholds are impaired.
- `maintenance`: planned operator-controlled maintenance state.
- `unavailable`: service/capability cannot satisfy required operations.
- `unknown`: insufficient fresh evidence; must not be rendered as healthy.

## 4. Alertmanager alert status

Alertmanager-native states remain:

```text
firing
resolved
silenced
```

`silenced` is an operational suppression state, not proof that the underlying condition is fixed.

## 5. Durable incident status

Middleware or the governed incident service owns:

```text
detected
-> notified
-> acknowledged
-> escalated
-> mitigating
-> resolved
```

A resolved incident can transition to:

```text
reopened
```

Definitions:

| Status | Meaning |
|---|---|
| detected | Durable incident identity created from alert/event evidence |
| notified | At least one approved notification route was executed/persisted |
| acknowledged | Authorized actor/system acknowledged ownership |
| escalated | Escalation policy increased urgency/ownership level |
| mitigating | Corrective action is actively underway |
| resolved | Resolution evidence accepted by policy |
| reopened | Same/related condition recurred after resolution |

Alertmanager does not own acknowledgement, escalation, Odoo ticket state or n8n workflow state.

## 6. Deployment/release status

```text
planned
source_prepared
ci_validated
staging_deployed
staging_proven
production_approved
production_deployed
production_proven
rolled_back
```

Architecture shorthand used in master docs:

- `DEFINED`
- `SOURCE_PREPARED`
- `CI_VALIDATED`
- `STAGING_PROVEN`
- `PRODUCTION_APPROVED`
- `PRODUCTION_ACTIVE`

Do not infer a later status from an earlier one.

## 7. Observability data freshness

For dashboards/read models:

```text
fresh
stale
unavailable
unknown
```

Dashboards must display stale/unavailable/unknown explicitly rather than silently showing an old value as current truth.

## 8. Safety status

Capabilities that can create external effects should expose an explicit state such as:

```text
disabled
prepared_disabled
approved_not_active
active
```

`prepared_disabled` means source/config is ready but live effects remain off. This status is preferred for staged communications, notification and trading-related capabilities until explicit activation evidence exists.

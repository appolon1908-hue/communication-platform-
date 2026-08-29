# Canonical Communications Status Model

Date: 2026-08-29

## Message Lifecycle

```text
accepted
  -> queued
  -> submitted
  -> provider_accepted
  -> delivered

accepted
  -> rejected

accepted
  -> suppressed

queued/submitted
  -> failed

queued/submitted
  -> cancelled

submitted/provider_accepted
  -> indeterminate
  -> reconciliation
  -> delivered | failed | cancelled
```

## Status Definitions

| Status | Terminal | Meaning |
| --- | --- | --- |
| `accepted` | no | Middleware accepted the intent and created canonical state. |
| `queued` | no | Intent is queued for provider/runtime processing. |
| `submitted` | no | Provider call was attempted. |
| `provider_accepted` | no | Provider accepted the message/call for downstream delivery/execution. |
| `delivered` | yes | Email/SMS delivered or voice objective completed. |
| `received` | yes or no | Inbound SMS/email/call received; terminal depends on workflow. |
| `rejected` | yes | Request failed policy/schema/auth before provider effect. |
| `suppressed` | yes | Consent/preference/suppression policy blocked delivery. |
| `failed` | yes | Known terminal failure. |
| `cancelled` | yes | Cancel accepted before terminal provider effect. |
| `expired` | yes | Provider reports delivery window expired. |
| `indeterminate` | no | Provider effect may have happened but cannot be proven. No blind retry allowed. |
| `reconciliation` | no | Middleware/provider read-back is resolving an indeterminate state. |

## Channel Mapping

| Channel | Delivered Means | Failed Means |
| --- | --- | --- |
| Email | Provider delivery event or approved sandbox capture in test. | Bounce, complaint, provider failure, policy terminal failure. |
| SMS | DLR delivered. | DLR failed/expired/rejected or route failure. |
| Voice | Call answered/completed or approved disposition. | No-answer/failure disposition, trunk error, campaign/lead rejection. |

## Retry Rule

Retry is allowed only after a known-safe failure or explicit operator-approved reconciliation. `indeterminate` must be reconciled before retry.

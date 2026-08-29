# Canonical Event Catalogue

This catalogue defines the normalized event vocabulary shared across communications, observability and incident workflows. Event names are architecture contracts; source repositories must prove implementation before any event is considered runtime-active.

## Common event envelope

Every canonical event should carry, where applicable:

```text
event_id
event_type
event_version
occurred_at
observed_at
tenant_id
codestra_business
service
environment
correlation_id
causation_id
command_id
message_id
provider_id
actor_type
source_system
payload
```

Secrets and unnecessary PII must never be included. High-cardinality identifiers belong in event fields, not Prometheus/Alertmanager labels.

## Communications lifecycle

| Event | Source authority | Meaning |
|---|---|---|
| `communications.message.accepted` | Middleware | Command passed policy and was durably accepted |
| `communications.message.queued` | Middleware/provider adapter | Awaiting provider dispatch |
| `communications.message.submitted` | Provider adapter | Submission attempt made |
| `communications.message.provider_accepted` | Klyrow/Telnexa/VICIdial adapter | Provider accepted request |
| `communications.message.delivered` | Provider truth via Middleware | Delivery/read-back proves completion |
| `communications.message.failed` | Middleware/provider truth | Terminal failure |
| `communications.message.suppressed` | Middleware/policy | Consent/suppression prevented send |
| `communications.message.reconciliation_required` | Middleware | State is indeterminate and requires read-back/reconciliation |
| `communications.message.dead_lettered` | Middleware | Retry/reconciliation policy exhausted |

## Email events

| Event | Source authority |
|---|---|
| `email.delivered` | Klyrow/Postal -> Middleware |
| `email.bounced.soft` | Klyrow/Postal -> Middleware |
| `email.bounced.hard` | Klyrow/Postal -> Middleware |
| `email.complaint` | Klyrow/Postal -> Middleware |
| `email.suppressed` | Middleware/Klyrow normalized state |
| `email.domain.authentication_changed` | Klyrow/domain authority |
| `email.reputation.degraded` | Klyrow/observability read model |

## SMS events

| Event | Source authority |
|---|---|
| `sms.submitted` | Telnexa/Jasmin -> Middleware |
| `sms.delivered` | Telnexa DLR -> Middleware |
| `sms.failed` | Telnexa DLR -> Middleware |
| `sms.expired` | Telnexa DLR -> Middleware |
| `sms.received` | Telnexa MO -> Middleware |
| `sms.opt_out` | Telnexa/Middleware policy normalization |
| `sms.route.degraded` | Telnexa/observability |

## Voice/contact-center events

| Event | Source authority |
|---|---|
| `voice.call.requested` | Middleware |
| `voice.call.started` | VICIdial/Asterisk -> Middleware |
| `voice.call.answered` | VICIdial/Asterisk -> Middleware |
| `voice.call.failed` | VICIdial/Asterisk -> Middleware |
| `voice.call.ended` | VICIdial/Asterisk -> Middleware |
| `voice.call.dispositioned` | VICIdial/Odoo normalized workflow |
| `voice.callback.scheduled` | Middleware/Odoo business workflow |
| `voice.transfer.completed` | VICIdial -> Middleware |

## Webhook/integration events

| Event | Meaning |
|---|---|
| `webhook.delivery.succeeded` | Signed webhook delivered successfully |
| `webhook.delivery.failed` | Delivery failed and retry policy applies |
| `webhook.delivery.dead_lettered` | Delivery exhausted retry policy |
| `webhook.signature.rejected` | Invalid/replayed signature rejected |
| `integration.reconciliation.started` | Read-back/reconciliation initiated |
| `integration.reconciliation.completed` | State reconciled |
| `integration.reconciliation.failed` | Reconciliation failed and operator action required |

## Observability/alert events

| Event | Source authority | Meaning |
|---|---|---|
| `observability.alert.firing` | Alertmanager -> Middleware | Alert group contains firing alert(s) |
| `observability.alert.resolved` | Alertmanager -> Middleware | Alert group resolved |
| `observability.incident.detected` | Middleware | Durable incident created |
| `observability.incident.notified` | Middleware | Approved notification route executed |
| `observability.incident.acknowledged` | Middleware/operator UI | Human/system acknowledgement recorded |
| `observability.incident.escalated` | Middleware | Escalation level changed |
| `observability.incident.mitigating` | Middleware/Odoo governed state | Mitigation underway |
| `observability.incident.resolved` | Middleware | Incident resolved |
| `observability.incident.reopened` | Middleware | Incident recurred after resolution |
| `observability.alert.silenced` | Alertmanager/operator evidence | Alert silence applied |
| `observability.alert.recurrence_detected` | Middleware/analytics | Fingerprint recurrence threshold crossed |

## Deployment/change events

| Event | Source authority |
|---|---|
| `deployment.started` | owning CI/CD/release process |
| `deployment.completed` | owning CI/CD/release process |
| `deployment.failed` | owning CI/CD/release process |
| `configuration.changed` | owning repository/deployment process |
| `release.promoted` | owning release process |
| `release.rolled_back` | owning release process |

Deployment/change events should carry `service`, `environment`, `deployment_sha`, and a change/release reference so Grafana can correlate incidents with what changed.

## SDK/AsyncAPI rule

Publicly consumed canonical events must eventually be represented in the AsyncAPI/event contract owned by `SDK-repository`. This file is the cross-repository architecture catalogue, not a substitute for generated contracts or runtime proof.

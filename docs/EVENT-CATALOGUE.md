# Canonical Communications Event Catalogue

Date: 2026-08-29

## Event Envelope

All external events should carry:

- event id
- event type
- event version
- tenant id
- canonical message or command id
- correlation id
- causation id where available
- channel
- provider
- provider reference where available
- canonical status
- occurred timestamp
- payload metadata with sensitive values redacted

## Message Events

| Event Type | Channel | Source Authority | Status | Meaning |
| --- | --- | --- | --- | --- |
| `codestra.communications.message.accepted.v1` | all | Middleware | Active for email Step 3 | Request accepted and canonical message created. |
| `codestra.communications.message.queued.v1` | all | Middleware/provider | Active for email Step 3 | Message queued for provider submission. |
| `codestra.communications.message.submitted.v1` | all | Provider adapter | Planned | Provider submission attempted. |
| `codestra.communications.message.provider_accepted.v1` | all | Provider adapter | Planned | Provider accepted responsibility for delivery. |
| `codestra.communications.message.delivered.v1` | email/sms/voice | Provider runtime | Email partial | Provider reports delivery or voice completion. |
| `codestra.communications.message.failed.v1` | all | Provider runtime/Middleware | Email partial | Terminal failure. |
| `codestra.communications.message.suppressed.v1` | email/sms | Middleware/provider policy | Email partial | Message blocked by suppression/consent policy. |
| `codestra.communications.message.cancelled.v1` | all | Middleware/provider | Email partial | Message cancelled before terminal provider effect. |
| `codestra.communications.message.indeterminate.v1` | all | Middleware/provider | Planned | Provider effect cannot be proven yet. |
| `codestra.communications.message.reconciled.v1` | all | Middleware | Planned | Indeterminate state resolved. |

## Email Provider Events

| Event Type | Source | Canonical Status |
| --- | --- | --- |
| `klyrow.email.queued` | Klyrow | queued |
| `klyrow.email.delivered` | Klyrow/Postal | delivered |
| `klyrow.email.bounced_soft` | Klyrow/Postal | failed |
| `klyrow.email.bounced_hard` | Klyrow/Postal | failed |
| `klyrow.email.complained` | Klyrow/Postal | failed |
| `klyrow.email.suppressed` | Klyrow | suppressed |
| `klyrow.email.deferred` | Klyrow/Postal | indeterminate |

## SMS Provider Events

| Event Type | Source | Canonical Status |
| --- | --- | --- |
| `telnexa.sms.submitted` | Telnexa/Jasmin | submitted |
| `telnexa.sms.delivered` | Telnexa/Jasmin DLR | delivered |
| `telnexa.sms.failed` | Telnexa/Jasmin DLR | failed |
| `telnexa.sms.expired` | Telnexa/Jasmin DLR | expired |
| `telnexa.sms.received` | Telnexa/Jasmin MO | received |
| `telnexa.sms.opted_out` | Telnexa/policy | suppressed |

## Voice Provider Events

| Event Type | Source | Canonical Status |
| --- | --- | --- |
| `vicidial.call.started` | Vicidialer-Codestra | submitted |
| `vicidial.call.answered` | Vicidialer-Codestra | provider_accepted |
| `vicidial.call.disposition_updated` | Vicidialer-Codestra | delivered or failed by disposition |
| `vicidial.call.completed` | Vicidialer-Codestra | delivered |
| `vicidial.call.failed` | Vicidialer-Codestra | failed |
| `vicidial.call.recording_available` | Vicidialer-Codestra | informational |

## Webhook Delivery Events

| Event Type | Source | Purpose |
| --- | --- | --- |
| `codestra.webhook.delivery.queued.v1` | Middleware | Outbound webhook delivery queued. |
| `codestra.webhook.delivery.succeeded.v1` | Middleware | Subscriber endpoint acknowledged. |
| `codestra.webhook.delivery.failed.v1` | Middleware | Delivery attempt failed. |
| `codestra.webhook.delivery.dead_lettered.v1` | Middleware | Retry policy exhausted. |
| `codestra.webhook.signature.failed.v1` | Middleware | Incoming or outgoing signature verification failed. |

## Rule

Provider-native event names may be retained in metadata, but public consumers should depend on canonical Codestra event names and statuses.

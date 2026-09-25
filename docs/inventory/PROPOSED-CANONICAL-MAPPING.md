# Proposed Canonical Communications Mapping

This file is a Step 1 design handoff, not proof that the routes are implemented.

## Public concepts

### Message

Provider-neutral fields should include:

- `message_id`
- `tenant_id`
- `channel` = `email | sms | voice`
- `sender`
- `recipient`
- `template_id` / content reference
- `scheduled_at`
- `status`
- `provider`
- `provider_operation_id`
- `correlation_id`
- `created_at` / `updated_at`

### Canonical public status

```text
accepted
queued
submitted
provider_accepted
delivered
suppressed
rejected
failed
cancelled
indeterminate
```

Middleware internal states such as `persisted`, `dispatching`, `readback_pending`, `reconciliation_required` and `dead_lettered` remain internal/operational states and map to public status plus event details rather than being erased.

## Proposed API families

```text
POST /v1/communications/messages
GET  /v1/communications/messages/{message_id}
GET  /v1/communications/messages/{message_id}/events
POST /v1/communications/messages/{message_id}/cancel

/v1/communications/templates
/v1/communications/senders
/v1/communications/domains
/v1/communications/suppressions
/v1/communications/preferences

GET /v1/communications/providers/health
GET /v1/communications/usage
GET /v1/communications/reputation
```

## Channel mapping

### Email

Canonical message command -> Middleware -> Klyrow API -> Postal/Mautic. Klyrow delivery/bounce/complaint events -> signed Middleware ingress -> canonical communications events.

### SMS

Canonical message command -> Middleware -> Telnexa restricted SMS operation -> Jasmin/carrier. MO/DLR/failure callbacks -> signed Middleware ingress -> canonical communications events.

### Voice

Canonical voice command -> Middleware -> Vicidialer-Codestra restricted adapter -> VICIdial/Asterisk. Call/disposition/callback/transfer events -> Middleware -> canonical voice events.

## Contract rule

Provider-specific fields may be exposed in a namespaced metadata object where necessary, but the common status/error/idempotency/event contract must remain stable across channels.
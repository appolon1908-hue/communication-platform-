# Canonical Communications API Catalogue

Date: 2026-08-29

## Authority

Public contracts and generated clients belong in `appolon1908-hue/SDK-repository`. Runtime execution belongs in `appolon1908-hue/Middleware-` and the provider runtime repos.

## Message API

| Endpoint | Method | Owner | Status | Purpose |
| --- | --- | --- | --- | --- |
| `/v1/communications/messages` | POST | SDK contract, Middleware runtime | Active for email Step 3 | Submit provider-neutral email/SMS/voice message intent. |
| `/v1/communications/messages` | GET | SDK contract, Middleware read model | Partial | Tenant-scoped message search/list. |
| `/v1/communications/messages/{messageId}` | GET | SDK contract, Middleware read model | Partial | Canonical message read-back. |
| `/v1/communications/messages/{messageId}/events` | GET | SDK contract, Middleware read model | Partial | Canonical timeline. |
| `/v1/communications/messages/{messageId}/cancel` | POST | SDK contract, Middleware runtime | Email partial | Cancel queued/scheduled messages where provider state allows. |
| `/v1/communications/messages/{messageId}/retry` | POST | SDK contract, Middleware runtime | Planned | Policy-controlled retry after known-safe failure. |

## Template API

| Endpoint | Method | Owner | Status | Purpose |
| --- | --- | --- | --- | --- |
| `/v1/communications/templates` | GET/POST | SDK contract, Middleware facade, provider runtime | Planned | List/create templates. |
| `/v1/communications/templates/{templateId}` | GET/PATCH | SDK contract, Middleware facade, provider runtime | Planned | Read/update template metadata and versions. |
| `/v1/communications/templates/{templateId}/render` | POST | SDK contract, Middleware/provider runtime | Planned | Deterministic render preview with redaction rules. |

## Sender, Domain, and Identity API

| Endpoint | Method | Owner | Status | Purpose |
| --- | --- | --- | --- | --- |
| `/v1/communications/senders` | GET/POST | SDK contract, Middleware facade, provider runtime | Planned | Email senders, SMS sender IDs/numbers, voice caller IDs. |
| `/v1/communications/senders/{senderId}` | GET/PATCH | SDK contract, Middleware facade, provider runtime | Planned | Sender read/update. |
| `/v1/communications/domains` | GET/POST | SDK contract, Klyrow provider truth | Email partial | Email domain onboarding/status. |
| `/v1/communications/domains/{domainId}` | GET/PATCH | SDK contract, Klyrow provider truth | Planned | Domain lifecycle. |
| `/v1/communications/domains/{domainId}/dns` | GET | Klyrow provider truth | Partial | SPF/DKIM/DMARC/PTR/TLS evidence. |

## Consent, Suppression, and Preference API

| Endpoint | Method | Owner | Status | Purpose |
| --- | --- | --- | --- | --- |
| `/v1/communications/suppressions` | GET/POST | SDK contract, Middleware policy, provider truth | Planned | Suppression list management. |
| `/v1/communications/suppressions/{suppressionId}` | DELETE | SDK contract, Middleware policy, provider truth | Planned | Governed removal. |
| `/v1/communications/preferences` | GET/POST/PATCH | SDK contract, Middleware policy | Planned | Recipient and tenant communication preferences. |
| `/v1/communications/consent` | GET/POST | SDK contract, Middleware policy | Planned | Consent capture and evidence. |

## Provider, Health, Usage, and Reputation API

| Endpoint | Method | Owner | Status | Purpose |
| --- | --- | --- | --- | --- |
| `/v1/communications/providers/health` | GET | Middleware read model, provider truth | Partial | Cross-provider health. |
| `/v1/communications/reputation` | GET | Middleware read model, Klyrow/provider truth | Email partial | Email/domain/provider reputation. |
| `/v1/communications/usage` | GET | Middleware read model, analytics | Partial | Tenant/channel/provider usage. |
| `/v1/communications/reconciliation` | GET | Middleware read model | Planned | Indeterminate state and repair queue. |
| `/v1/communications/webhooks/health` | GET | Middleware/webhook delivery | Planned | Subscription delivery health. |

## Internal Provider APIs

Internal provider APIs are not public SDK contracts. Middleware may call them using service identity only.

| Provider | Internal Surface | Status |
| --- | --- | --- |
| Klyrow | `/v1/internal/email/communications/*` | Step 3 branch implemented for safe-mode email. |
| Telnexa | SMS command/read-back provider surface | Planned. |
| Vicidialer-Codestra | Voice command/read-back provider surface | Planned. |

## Required Header Model

| Header | Required For | Purpose |
| --- | --- | --- |
| `Authorization: Bearer <token>` | All public calls | Keycloak-issued identity validated by Kong and Middleware. |
| `X-Tenant-ID` | Tenant-scoped calls | Tenant isolation. |
| `X-Correlation-ID` | Effectful calls | Cross-service traceability. |
| `Idempotency-Key` | Effectful calls | Duplicate prevention. |

## Rule

Direct product calls to Klyrow, Telnexa, VICIdial, Postal, Jasmin, Asterisk, Odoo, or n8n are not canonical when the operation is a governed communications write.

# Email / Klyrow Inventory

## Verdict

Klyrow is the strongest channel implementation and should be the first Communications API v1 provider integration.

| Capability | Evidence | Classification | Gap |
|---|---|---|---|
| Authenticated `/v1` API | Bearer-authenticated product API; OpenAPI exposed at `/v1/developer/openapi.json` | DONE | Must be mapped behind canonical Communications API |
| Idempotent email writes | Email/campaign writes require `Idempotency-Key`; content mismatch conflicts | DONE | Canonical request fingerprint must align with Middleware |
| Safe email submission | Safe email submission/status/events are documented | DONE | Exact unified message DTO/status mapping needed |
| Message status/events | Product API includes email status/events | DONE | Normalize into shared message/event lifecycle |
| Consent/preferences | First-class API resource | DONE | Define canonical preference/suppression precedence |
| Deliverability | Deliverability checks/snapshots documented | DONE | Unified reputation read model needed |
| Sender/domain onboarding | Domain onboarding and dedicated domain/DKIM documentation exist | DONE | Canonical sender/domain contract and DNS evidence fields needed |
| SPF/DKIM/DMARC | Deliverability/domain documentation exists; DKIM rotation is documented | PARTIAL | Inventory must prove exact API fields for SPF, DKIM selector state, DMARC and PTR/rDNS |
| Templates/campaigns | Mautic-backed campaign/template foundation exists | DONE | Provider-neutral template CRUD must be mapped |
| Bounces/complaints | Postal delivery event processing and deliverability features exist | DONE | Canonical failure taxonomy needed |
| Suppressions | Klyrow runtime explicitly owns suppressions | DONE | Shared API semantics and source-of-truth precedence needed |
| Signed inbound webhooks | Postal events use timestamp + event_id + exact body HMAC-SHA256; replay IDs persisted | DONE | Map to canonical event envelope |
| Middleware outbound events | Signed canonical JSON plus bearer service auth; fail-fast when Middleware unavailable | DONE | Cross-repo contract tests needed |
| SDKs | Python and TypeScript reference clients exist | DONE | Consolidate behind Codestra SDK rather than expose Klyrow-specific clients to products |
| Safe mode | Accepted IDs without invoking Postal when safe mode is on | DONE | Preserve as staging/sandbox capability |
| Bulk/scheduled send | Campaign/journey foundation exists | PARTIAL | Exact API behavior and cancellation semantics need proof |
| Reconciliation/read-back | Delivery/status surfaces exist | PARTIAL | Must prove authoritative provider read-back for uncertain submission outcomes |

## Step 3 target

Implement the canonical email adapter first: Communications API -> Middleware command -> Klyrow -> Postal/Mautic -> signed delivery event -> Middleware canonical event/read model.
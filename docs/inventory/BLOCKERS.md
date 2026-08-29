# Communications Blockers

## B0 — Caller-token contract

**Owner:** Keycloak + Kong + Middleware

The service identity path must agree on issuer, audience, client identity, scopes, bearer-token preservation and Middleware revalidation. Source configuration alone is insufficient; end-to-end acceptance/rejection tests are required.

**Blocks:** production cutover of Steps 3–5.

## B1 — Canonical Communications API v1 not yet accepted

**Owner:** SDK-repository

The provider-neutral message, sender/domain, template, suppression/preference, health, usage, reputation and event contracts are not yet frozen.

**Blocks:** treating any channel-specific API as the final public Codestra API.

## B2 — Email uncertain-outcome reconciliation proof

**Owner:** Klyrow + Middleware

Klyrow has status/events and delivery processing, but Step 3 must prove authoritative read-back/reconciliation when submission outcome is unknown.

**Blocks:** production-grade exactly-once/at-most-once effect claim for email.

## B3 — SMS consent/idempotency/reconciliation alignment

**Owner:** Telnexa + Middleware

Signed MO/DLR callbacks and runtime are strong, but canonical opt-out enforcement, end-to-end idempotency and unknown-outcome reconciliation must be proven.

**Blocks:** Step 4 production readiness.

## B4 — Voice canonical mapping and campaign isolation conformance

**Owner:** Vicidialer-Codestra + Middleware + SDK

Exact voice command/event schemas must be mapped to the provider-neutral API and cross-campaign access must be denied in tests.

**Blocks:** Step 5 production readiness.

## B5 — Dashboard normalized read model

**Owner:** communication-platform- design; Middleware/provider repos implementation

The dashboard design exists, but a canonical message/search/provider-health/usage read API is not yet accepted.

**Blocks:** Step 6 production action/read integration.

## B6 — Channel activation evidence

Each provider has separate runtime activation gates. API/SDK completion must not be treated as authorization to enable sending or dialing.
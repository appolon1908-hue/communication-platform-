# Phase 1–2 Execution Plan

## Decision

The first two implementation stages are intentionally separated across two repositories and two branches.

| Step | Purpose | Repository | Branch | Change type |
|---|---|---|---|---|
| 1 | Inventory existing communications capabilities and gaps | `appolon1908-hue/communication-platform-` | `audit/communications-capability-inventory-v1` | Evidence/read-only documentation |
| 2 | Define canonical Communications API v1 contracts | `appolon1908-hue/SDK-repository` | `feat/communications-api-v1-contracts` | Contract/SDK implementation |

## Why Step 1 belongs in communication-platform-

`communication-platform-` owns cross-repository architecture, ownership maps, capability comparison, dashboard design and release coordination. A capability inventory spans Klyrow, Telnexa, VICIdial, Middleware and SDK, so placing the audit in any one runtime repository would incorrectly make that repository appear to own the others.

Step 1 therefore records evidence without changing runtime code.

### Step 1 inputs

Principal repositories:

- `SDK-repository`
- `Middleware-`
- `klyrow.com`
- `telnexa`
- `Vicidialer-Codestra`

Supporting repositories:

- `Kong`
- `Keycloak`
- `Caddy`
- `N8N`
- `Odoo`

### Step 1 outputs

The audit must produce channel-by-channel source-backed inventories, a gap matrix, duplicate-ownership report, blockers report and a proposed provider-neutral mapping.

Every capability is classified as `DONE`, `PARTIAL`, `MISSING`, `DUPLICATE`, `BLOCKED` or `OUT_OF_SCOPE`.

No implementation claim is accepted without source/test evidence.

## Why Step 2 belongs in SDK-repository

`SDK-repository` is the developer-facing contract authority. It already owns OpenAPI, AsyncAPI, JSON Schemas, generated clients, TypeScript SDKs, webhook tooling, connector-kit and compatibility gates.

Therefore the canonical provider-neutral Communications API v1 belongs there.

Step 2 must not implement Postal, Jasmin, VICIdial, Middleware execution, Kong or Keycloak runtime behavior.

### Step 2 target

The canonical API should converge on shared concepts including:

```text
POST /v1/communications/messages
GET  /v1/communications/messages/{message_id}
GET  /v1/communications/messages/{message_id}/events
POST /v1/communications/messages/{message_id}/cancel

GET/POST/PATCH/DELETE /v1/communications/templates...
GET/POST           /v1/communications/senders...
GET                /v1/communications/domains...
GET/POST/DELETE    /v1/communications/suppressions...
GET/PATCH          /v1/communications/preferences...
GET                /v1/communications/providers/health
GET                /v1/communications/usage
GET                /v1/communications/reputation
```

Final route shapes remain subject to accepted Step 1 evidence and semantic contract review.

## Handoff rule

The sequence is strict:

```text
Step 1 inventory
    |
    v
Accepted STEP1-EXIT-REPORT
    |
    v
Step 2 canonical API contracts
    |
    v
Email implementation alignment
    |
    v
SMS implementation alignment
    |
    v
Voice implementation alignment
    |
    v
Dashboard/read-model implementation
```

Step 2 may be prepared in parallel as a draft, but it must not be treated as authoritative until the Step 1 inventory resolves contradictory or duplicate provider behavior.

## Branch rules

### communication-platform-

- `main` — accepted master architecture.
- `development` — integrated architecture work.
- `staging` — architecture/release candidate coordination.
- `audit/communications-capability-inventory-v1` — Step 1 only.
- `docs/master-architecture-v1` — master documentation PR.

### SDK-repository

- `main` — accepted SDK/contract baseline.
- `feat/communications-api-v1-contracts` — Step 2 canonical communications contracts.
- `feat/communications-sdk-v1` — broader communications SDK architecture work; do not duplicate canonical contract implementation across branches.
- `docs/communications-platform-authority` — repository ownership/governance documentation.

The `feat/communications-api-v1-contracts` branch is the principal Step 2 implementation branch. Other SDK branches must consume or rebase onto the accepted contract rather than create competing definitions.

## Cross-repository authority after Step 2

| Responsibility | Repository |
|---|---|
| Public communications contracts/SDKs | `SDK-repository` |
| Cross-system execution/control | `Middleware-` |
| Email provider/runtime | `klyrow.com` |
| SMS provider/runtime | `telnexa` |
| Voice provider/runtime | `Vicidialer-Codestra` |
| Gateway/security policy | `Kong` |
| Identity | `Keycloak` |
| TLS/edge | `Caddy` |
| Orchestration | `N8N` |
| CRM/business state | `Odoo` |
| Architecture/dashboard coordination | `communication-platform-` |
| Shared deployment/observability infrastructure | `Infustruction-repo` |

## Production safety

Neither Step 1 nor Step 2 authorizes:

- production email delivery activation;
- production SMS delivery activation;
- dialing activation;
- Keycloak client changes;
- Kong route activation;
- Caddy reload;
- n8n workflow activation;
- Odoo deployment;
- provider credential changes.

Production activation requires later exact-head cross-repository evidence and explicit approval.

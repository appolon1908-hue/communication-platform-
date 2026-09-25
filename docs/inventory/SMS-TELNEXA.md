# SMS / Telnexa Inventory

## Verdict

Telnexa has a substantial SMS runtime around Jasmin and a clear signed callback path. The main gaps are provider-neutral contract mapping, canonical idempotency semantics and end-to-end reconciliation evidence.

| Capability | Evidence | Classification | Gap |
|---|---|---|---|
| SMS send | Jasmin HTTP/SMPP runtime with `/send` path documented | DONE | Canonical Communications API mapping needed |
| SMPP carrier connectivity | Jasmin connector/routing foundation exists | DONE | Live carrier credentials/routes remain separately gated |
| Inbound SMS/MO | Signed inbound callback path exists | DONE | Normalize to canonical event catalogue |
| DLR | Signed DLR callback path exists | DONE | Canonical delivery/failure status mapping needed |
| Failure callbacks | Dedicated signed failure callback path exists | DONE | Shared error taxonomy needed |
| Unicode | `coding=8` documented | DONE | SDK should hide provider-specific encoding detail where possible |
| Callback security | HMAC-SHA256 with timestamp, event ID, body hash and replay controls | DONE | Cross-repo conformance test required |
| Billing/wallet/ledger | Multi-tenant decimal wallet, immutable ledger, reservations and usage/margin foundation documented | DONE | Decide what belongs in Communications usage API versus Telnexa-only billing |
| Quotas/throughput | Jasmin users/groups and throughput quotas exist | DONE | Normalize tenant/channel quota read model |
| Provider health | Health scripts/provider bind checks exist | DONE | Unified provider-health API missing |
| Sender identities | Jasmin sender/from is supported | PARTIAL | Canonical sender registration/verification model missing |
| Bulk/scheduled SMS | Not established as canonical product API in reviewed evidence | MISSING | Design in Communications API if required |
| Consent/opt-out | Communications architecture requires it, but reviewed Telnexa evidence does not prove a complete canonical suppression/consent engine | PARTIAL | Define owner and enforce before dispatch |
| Idempotency | Middleware supplies durable idempotency; Telnexa billing has deterministic state | PARTIAL | Exact Telnexa send idempotency/read-back contract must be aligned |
| Reconciliation | Delivery/result reconciliation is architectural requirement | PARTIAL | Prove provider operation IDs/read-back under timeout/unknown outcome |
| Production delivery | Explicitly gated pending approved provider routes/credentials | BLOCKED | Separate provider activation evidence required |

## Step 4 target

Map canonical SMS commands/events onto Telnexa without moving Jasmin/SMPP logic into Middleware or SDK.
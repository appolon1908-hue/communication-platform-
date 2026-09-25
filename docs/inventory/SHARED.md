# Shared Control-Plane Inventory

## Verdict

The shared control-plane foundation is substantial but not yet a finished provider-neutral Communications API.

| Capability | Evidence | Classification | Gap |
|---|---|---|---|
| Governed command submission | Middleware `POST /v1/commands` with tenant, correlation and idempotency headers | DONE | Communications-specific command types still need canonical mapping |
| Operation status | Middleware `GET /v1/operations/{command_id}` | DONE | Communications message read model is not yet canonical |
| OAuth2 scopes | Integration Fabric API defines Client Credentials scopes | DONE | Keycloak/Kong/Middleware caller-token behavior still requires end-to-end acceptance |
| Tenant boundary | X-Tenant-ID plus Middleware authorization and tenant projection | DONE | Must be preserved by Communications API v1 |
| Idempotency | Required `Idempotency-Key`; durable command model and reconciliation states | DONE | Communications facade must map message identity consistently |
| Durable asynchronous state | Middleware command states include persisted, queued, dispatching, accepted, readback_pending, completed, failed, reconciliation_required, dead_lettered | DONE | Needs provider-neutral message lifecycle mapping |
| Dead-letter replay | Protected dead-letter replay endpoint exists | DONE | Communications dashboard read/action policy still needed |
| Integration catalog/connections | Middleware integration catalog and connection lifecycle exist | DONE | Channel/provider connection schemas need normalization |
| Runtime safety/readiness | `/v1/runtime/safety`, tenant preflight/readiness | DONE | Dashboard aggregation contract missing |
| Inbox/outbox/reconciliation | Middleware repository documents durable inbox/outbox, retries, reconciliation and destination read-back | DONE | Channel-specific acceptance tests remain |
| Provider health | Integration connection testing and provider-side health concepts exist | PARTIAL | Unified `/communications/providers/health` read model not yet defined |
| Usage/analytics | Provider/product-specific metrics exist | PARTIAL | No canonical communications usage API yet |
| Webhook/event normalization | Middleware owns signed/durable event boundary | DONE | Unified event catalogue still incomplete across all communications channels |
| Pagination/search | Exists in individual systems/SDK surfaces | PARTIAL | Unified message search/filter contract missing |

## Primary blocker

The architecture is sound, but the final caller-token contract between Keycloak, Kong and Middleware must be proven against real service identities before production cutover.

## Step 2 implication

Communications API v1 should reuse the durable command/operation machinery instead of building a second execution engine.
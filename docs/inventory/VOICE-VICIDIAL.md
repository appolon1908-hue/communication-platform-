# Voice / VICIdial Inventory

## Verdict

`Vicidialer-Codestra` is the correct principal voice/contact-center runtime. It has a restricted adapter, campaign provisioning, deployment/operations material, tests and reconciliation evidence. The main gap is not ownership; it is proving the exact provider-neutral command/event surface and production-safe read-back behavior.

| Capability | Evidence | Classification | Gap |
|---|---|---|---|
| Restricted VICIdial/Asterisk adapter | Repository authority and adapter/runtime source documented | DONE | Map exact operations to Communications API v1 |
| Campaign provisioning | Dedicated `campaign_provisioning/` source exists | DONE | Preserve campaign isolation in every command/schema |
| Campaign isolation | Permanent architecture rule requires scoped campaigns and disabled-by-default new resources | DONE | Add canonical contract tests for tenant/campaign crossover denial |
| Agents/leads/callbacks/transfers | Repository authority explicitly includes these integration areas | DONE | Inventory exact route/schema names and read models |
| Dispositions | Repository authority explicitly includes dispositions | DONE | Normalize into canonical voice events without losing VICIdial semantics |
| Recording metadata | Repository ownership includes recording metadata | DONE | Define metadata-only API and access controls; recordings themselves remain protected |
| Queues/inbound groups | Voice/contact-center authority covers queues/call control | PARTIAL | Exact API/read-back surface needs proof |
| Extension/provisioning | Repository includes provisioning/runtime operations | DONE | Map to platform provisioning versus communications API boundary |
| Call status/events | Connector architecture supports events and status synchronization | PARTIAL | Canonical event catalogue and exact provider-state mapping needed |
| Webphone/session | Exists in broader Codestra telephony architecture | PARTIAL | Confirm principal source and whether it belongs in communications API or separate telephony API |
| Dialing safety gates | New dialing/campaign resources remain disabled/non-dialing by default; production dialing has separate activation gates | DONE | Keep capability flags explicit in API/readiness |
| Read-back | Repository requires destination read-back before trusting mutation | DONE | Prove exact methods for all effectful commands |
| Reconciliation | Repository explicitly owns voice-system reconciliation | DONE | Add contract tests for indeterminate/unknown outcomes |
| Direct Odoo writes | Explicitly prohibited | OUT_OF_SCOPE | Continue through Middleware only |
| Production dialing | Separate immutable image, preflight, review and activation gates | BLOCKED | No production enablement from API contract work |

## Step 5 target

Expose a provider-neutral voice facade only after exact VICIdial command/event/status contracts are mapped and campaign-isolation tests pass.
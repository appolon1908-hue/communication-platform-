# SDK / Contracts Inventory

## Verdict

The SDK repository already has a strong contract-first foundation. Step 2 is an extension and consolidation job, not a greenfield SDK build.

| Capability | Evidence | Classification | Gap |
|---|---|---|---|
| Public OpenAPI | `contracts/openapi/codestra-public.openapi.yaml` | DONE | Add Communications API v1 surface |
| Control-plane OpenAPI | `codestra-control-plane.openapi.yaml` | DONE | Keep synchronized with principal Middleware runtime |
| Enterprise OpenAPI | `codestra-enterprise.openapi.yaml` | DONE | Clarify what remains enterprise/private after communications facade |
| Restricted gateway OpenAPI | `codestra-restricted-gateway.openapi.yaml` | DONE | Channel adapters must conform without exposing private gateway publicly |
| AsyncAPI | `contracts/asyncapi/` exists and canonical event catalogue is established | DONE | Expand to complete email/SMS/voice communications events |
| JSON Schemas | `contracts/schemas/` | DONE | Add shared message/sender/domain/preference/error schemas |
| TypeScript SDK | Existing public SDK/client packages | DONE | Add provider-neutral communications facade |
| Python SDK | Generated public/control-plane client capability exists | DONE | Generate communications client and smoke-test |
| PHP SDK | Generated client with repaired syntax/smoke tests | DONE | Generate communications client and smoke-test |
| Webhook SDK | Standard Webhooks-style signing/verification helpers | DONE | Add canonical communications event helpers |
| Connector kit | Guarded connector execution/idempotency/reconciliation contracts | DONE | Align communications-specific operation manifests |
| Provider adapters | Klyrow/Telnexa/VICIdial adapter foundations exist | PARTIAL | Conformance against exact principal runtimes needs completion |
| n8n nodes | Existing package/action and internal trigger foundation | DONE | Add communications actions only after canonical API acceptance |
| Semantic contract validation | Added through remediation work | DONE | Communications contracts must enter same gate |
| Contract drift/Pact | Compatibility/drift gates exist | DONE | Extend coverage across all communications operations/events |
| Generated package publication | Generation and smoke tests exist | PARTIAL | Protected publication/provenance/release process still required |
| Canonical Communications API v1 | Dedicated branch created | MISSING | Step 2 deliverable |

## Step 2 rule

Do not create a second runtime API in this repository. Define the public contract and generated clients here; Middleware remains the execution authority.
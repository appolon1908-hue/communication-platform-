# Communications Repository Ownership Matrix

## Permanent rule

Every component with a dedicated repository keeps that repository as its principal source. `communication-platform-` coordinates architecture and contracts; it does not become a second runtime source.

| Capability | Principal repository | Owns | Must not own |
|---|---|---|---|
| Edge/TLS | appolon1908-hue/Caddy | TLS termination, host/path routing, security headers, mTLS edge policy, Caddy->Kong handoff | identity issuance, API authorization, provider writes |
| API gateway | appolon1908-hue/Kong | services/routes/plugins, OIDC/JWT gateway validation, scopes, rate limits, route policy | application business logic, provider runtime |
| Identity | appolon1908-hue/Keycloak | realm/client desired state, PKCE, Client Credentials, scopes/audiences, token issuance policy | API execution, provider credentials |
| Control plane | appolon1908-hue/Middleware- | privileged command/event boundary, tenant/actor auth, idempotency, inbox/outbox, durable ledger, policy, adapters, retries, reconciliation, audit | duplicate provider runtime, SDK distribution |
| Email | appolon1908-hue/klyrow.com | Postal/Mautic email runtime, sender/domain onboarding, delivery, bounces, complaints, suppressions, deliverability/provider truth | cross-system authorization or alternate Middleware path |
| SMS | appolon1908-hue/telnexa | Jasmin/SMPP/HTTP SMS runtime, MO/DLR events, routing/billing/provider truth | voice runtime, direct CRM mutation |
| Voice | appolon1908-hue/Vicidialer-Codestra | VICIdial/Asterisk connector runtime, campaigns, calls, queues, callbacks, dispositions, transfers, read-back | SMS/email runtime, direct Odoo DB writes |
| SDK/contracts | appolon1908-hue/SDK-repository | OpenAPI/AsyncAPI, generated clients, webhook SDK, connector-kit, n8n nodes, developer tooling | privileged provider execution or secrets |
| Orchestration | appolon1908-hue/N8N | approved workflow packs, timing/branching/human workflow coordination | direct provider/Odoo/VICIdial/Jasmin/Postal writes |
| CRM/business state | appolon1908-hue/Odoo | CRM records, leads, campaign business workflows, activities, approved business state | provider delivery engine or cross-system control plane |
| Architecture/dashboard | appolon1908-hue/communication-platform- | ownership matrix, dashboard design, capability model, release dependency map, cross-repo architecture | runtime implementations already owned elsewhere |
| Infrastructure | appolon1908-hue/Infustruction-repo | shared infrastructure definitions, observability deployment, environment topology, backup/restore/DR patterns | product application source |

## Canonical effect path

```text
Application/Product
  -> SDK
  -> Caddy
  -> Kong
  -> Keycloak-validated identity
  -> Middleware
  -> owning provider adapter/runtime
```

Provider callbacks/events return through signed/private governed ingress to Middleware, which normalizes and persists them before they are exposed to SDK consumers, dashboards, n8n or Odoo workflows.

## Cross-repository change rule

A public behavior change that crosses repositories must identify all affected owners before implementation. The release evidence must record exact accepted source SHAs for every changed repository and verify contract compatibility.

Examples:
- New email operation: SDK contract + Middleware implementation/adapter + Klyrow runtime/read-back + Kong route/security if externally exposed.
- New SMS event: Telnexa event source + Middleware normalization + SDK AsyncAPI + n8n/Odoo consumer changes only if needed.
- New voice command: SDK contract + Middleware command mapping + Vicidialer-Codestra runtime/read-back + Odoo/n8n workflow changes only where business behavior requires them.

## No-bypass rules

1. SDKs do not call provider administration APIs directly.
2. n8n does not hold unrestricted provider credentials.
3. Dashboards do not mutate provider systems directly.
4. Caddy does not bypass Kong for shared public API mutations.
5. Kong does not replace Middleware business authorization/reconciliation.
6. Odoo does not directly drive external provider mutations when Middleware governance applies.
7. Provider systems do not write directly into another provider or product database.

## Release coordination

The architecture repo owns the dependency map and readiness checklist. Runtime approval remains with each owning repository and its deployment process.
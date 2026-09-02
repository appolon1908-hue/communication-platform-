# Canonical API Catalogue

This catalogue defines the provider-neutral communications/API architecture. It is an architecture contract, not proof that every endpoint already exists in a deployed runtime.

## Status values

- `EXISTING_SOURCE_CONTRACT` — confirmed in an owning source contract.
- `TARGET_CONTRACT` — canonical endpoint to be implemented/aligned.
- `INTERNAL_ONLY` — not intended as a public developer API.

## Control-plane foundation

| Method | Path | Status | Principal authority | Purpose |
|---|---|---|---|---|
| POST | `/v1/commands` | EXISTING_SOURCE_CONTRACT | Middleware | Durable privileged command submission with tenant/correlation/idempotency context |
| GET | `/v1/operations/{command_id}` | EXISTING_SOURCE_CONTRACT | Middleware | Durable command/operation status and result read-back |

These generic control-plane endpoints remain the underlying safe execution primitive where provider-neutral APIs map into effectful operations.

## Communications message API

| Method | Path | Status | Principal implementation |
|---|---|---|---|
| POST | `/v1/communications/messages` | TARGET_CONTRACT | Middleware + owning provider adapter |
| GET | `/v1/communications/messages` | TARGET_CONTRACT | Middleware/read model |
| GET | `/v1/communications/messages/{message_id}` | TARGET_CONTRACT | Middleware/read model |
| GET | `/v1/communications/messages/{message_id}/events` | TARGET_CONTRACT | Middleware event/read model |
| POST | `/v1/communications/messages/{message_id}/cancel` | TARGET_CONTRACT | Middleware policy + provider capability |
| POST | `/v1/communications/messages/{message_id}/retry` | TARGET_CONTRACT | Middleware policy/reconciliation |

## Templates

| Method | Path | Status | Principal implementation |
|---|---|---|---|
| GET | `/v1/communications/templates` | TARGET_CONTRACT | Middleware/read model + owning channel runtime |
| POST | `/v1/communications/templates` | TARGET_CONTRACT | Middleware + owning channel runtime |
| GET | `/v1/communications/templates/{template_id}` | TARGET_CONTRACT | Middleware/read model |
| PATCH | `/v1/communications/templates/{template_id}` | TARGET_CONTRACT | Middleware + owning channel runtime |

## Channel/provider discovery

| Method | Path | Status | Purpose |
|---|---|---|---|
| GET | `/v1/communications/channels` | TARGET_CONTRACT | Supported channels/capabilities |
| GET | `/v1/communications/channels/health` | TARGET_CONTRACT | Channel health summary |
| GET | `/v1/communications/providers/health` | TARGET_CONTRACT | Provider health, degraded/maintenance state |
| GET | `/v1/communications/usage` | TARGET_CONTRACT | Governed usage/cost view |
| GET | `/v1/communications/reputation` | TARGET_CONTRACT | Email/SMS reputation/deliverability read model |

## Consent/preferences/suppression

| Method | Path | Status |
|---|---|---|
| GET | `/v1/communications/preferences` | TARGET_CONTRACT |
| POST | `/v1/communications/preferences` | TARGET_CONTRACT |
| PATCH | `/v1/communications/preferences/{preference_id}` | TARGET_CONTRACT |
| GET | `/v1/communications/suppressions` | TARGET_CONTRACT |
| POST | `/v1/communications/suppressions` | TARGET_CONTRACT |
| DELETE | `/v1/communications/suppressions/{suppression_id}` | TARGET_CONTRACT |

All effectful changes must enforce tenant, consent, capability, authorization and audit policy in Middleware.

## Dashboard/read-model API

| Method | Path | Status |
|---|---|---|
| GET | `/v1/communications/overview` | TARGET_CONTRACT |
| GET | `/v1/communications/domains` | TARGET_CONTRACT |
| GET | `/v1/communications/webhooks/health` | TARGET_CONTRACT |
| GET | `/v1/communications/reconciliation` | TARGET_CONTRACT |

These endpoints are read-oriented and may be backed by normalized read models rather than direct provider queries.

## Alert/incident integration

The Alertmanager-to-Middleware endpoint is intentionally **not assigned a public canonical URL here yet** because source/runtime proof for a dedicated ingestion route does not currently exist. `Codestra-Alertmanager` loads the webhook target from a runtime secret file and treats the Middleware ingestion contract as `CONTRACT_PREPARED_RUNTIME_ENDPOINT_NOT_PROVEN`.

Target responsibilities for that endpoint are:

- authenticate the Alertmanager workload;
- validate required alert metadata;
- assign/maintain durable incident IDs;
- deduplicate Alertmanager retries;
- route approved notifications;
- persist acknowledgements/escalations;
- create Odoo incident/ticket records only through Middleware;
- trigger n8n orchestration only through Middleware governance.

## Public security rules

Any externally exposed endpoint must follow:

```text
Client -> Caddy -> Kong -> Keycloak-validated identity -> Middleware
```

Required properties include:

- canonical issuer/audience validation;
- short-lived credentials;
- tenant context;
- authorization scopes/capabilities;
- correlation ID;
- idempotency for effectful operations;
- request validation;
- durable audit;
- no browser/provider secrets;
- no direct provider write routes.

## SDK authority

The public OpenAPI/AsyncAPI representations of accepted APIs belong in `appolon1908-hue/SDK-repository`. This architecture catalogue defines cross-repository intent and ownership; it must not become a second generated-SDK source.

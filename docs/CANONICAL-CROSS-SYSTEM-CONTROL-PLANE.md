# Canonical Codestra cross-system control plane

## Status

```text
SOURCE_AUTHORITY=ACCEPTED
RUNTIME_ACTIVATION=BLOCKED
WORKFLOWS_ACTIVE=NO
ODOO_WRITE=false
EXTERNAL_DELIVERY=false
LIVE_SMS_DELIVERY=false
LIVE_EMAIL_DELIVERY=false
LIVE_PSTN_DIALING=false
PRODUCTION_DIALING=DISABLED
```

This document defines how the communications platform participates in the
Codestra integration fabric. It does not enable any communication channel.

## Permanent authorities

| Responsibility | Authority |
|---|---|
| Identity issuance and machine scopes | Keycloak |
| Public API authentication/routing | Kong |
| TLS edge and public reverse proxy | Caddy |
| Cross-system commands, durable state, provider authorization, retries, dead letters and reconciliation | Middleware |
| Workflow timing, branching and coordination | n8n |
| CRM and business history | Odoo 19 |
| Email execution and lifecycle truth | Klyrow / Postal behind Middleware |
| SMS execution and lifecycle truth | Telnexa / Jasmin behind Middleware |
| Voice execution and lifecycle truth | VICIdial / Asterisk behind Middleware |
| Social publication truth | Postly/Postiz adapter behind Middleware |
| Crawler execution and evidence | approved crawler adapter behind Middleware |

No authority in this table may be silently duplicated by another repository.

## Canonical orchestration path

```text
application/provider event
  -> Caddy
  -> Kong
  -> Middleware authenticated inbox
  -> canonical event + durable automation job
  -> private n8n wake
  -> POST /v2/automation/jobs/claim
  -> leased n8n workflow
  -> POST /v2/automation/commands
  -> Middleware policy, capability and approval checks
  -> Temporal destination adapter
  -> Odoo or communications provider
  -> destination read-back
  -> Middleware reconciliation
  -> GET /v2/automation/commands/{command_id}
  -> terminal job result
```

The historical `/v1/integrations/n8n/*` routes are compatibility aliases. New
workflows must use automation v2.

## CRM command boundary

Every communication workflow that creates or updates a lead uses the one
canonical business command:

```text
command_type    = crm.lead.upsert
command_version = "1.0"
```

Middleware calls Odoo's reviewed `codestra_middleware_bridge` through:

```text
POST /codestra/middleware/v1/commands/crm.lead.upsert
GET  /codestra/middleware/v1/commands/{command_id}/status
```

The CRM payload preserves:

- stable source-record identity;
- tenant and business context;
- source and attribution;
- provenance and legal basis;
- consent and channel permissions;
- review requirements;
- contact eligibility;
- campaign code when applicable;
- correlation and idempotency identities.

Odoo does not invent provider delivery truth. Middleware and the destination
adapter provide normalized accepted, submitted, delivered, failed, blocked or
unknown results.

## Communication command families

```text
email.*       -> n8n-messaging-automation -> automation.command.messaging
sms.*         -> n8n-messaging-automation -> automation.command.messaging
telephony.*   -> n8n-telephony-automation -> automation.command.telephony
social.*      -> n8n-social-automation    -> automation.command.social
crm.*         -> n8n-crm-automation       -> automation.command.crm
support.*     -> n8n-crm-automation       -> automation.command.crm
```

A client cannot issue another family’s prefix. There is no generic execute or
command scope.

## Campaign isolation

Campaign isolation remains mandatory across Odoo, Middleware, n8n workflow
selection and provider routing:

1. A normal agent has exactly one active campaign context.
2. The agent cannot view, receive, mutate, transfer into, report on or receive
   communications for another campaign.
3. Each campaign has its own lists, scripts, dispositions, callbacks,
   recording references, inbound groups, transfer routes, inboxes, dashboards
   and approved workflows.
4. Each campaign has one primary supervisor unless a separately reviewed policy
   changes that rule.
5. Supervisors are limited to their campaign.
6. Global administration is separately authorized and fully audited.
7. Tenant, campaign, sender, caller-ID and destination policy are revalidated at
   the Middleware effect boundary.

n8n workflow names or caller-supplied headers never grant campaign authority.

## Consent and suppression

Odoo records business consent and preferences. Middleware enforces the current
cross-channel legal and operational policy before an external effect. Provider
adapters enforce provider-specific sender, caller-ID, routing and destination
requirements.

A communication command is blocked when required consent, jurisdiction,
suppression, calling-hours, approval, sender, caller-ID or capability evidence
is missing. A workflow cannot override a global or legal suppression.

## Unknown outcomes

A timeout is an unknown outcome. The platform must preserve that truth:

```text
n8n automatic retry on timeout = prohibited
Middleware blind effect retry  = prohibited
destination reconciliation     = required
```

For Odoo, Middleware reads the recorded Odoo command status. For a provider,
Middleware uses the destination's idempotency and reconciliation interface.
Only a reviewed policy may authorize a retry after proving the original effect
did not occur or is safely idempotent.

## Odoo HMAC contract

Middleware and Odoo compute HMAC-SHA256 over newline-joined bytes in this exact
order:

```text
X-Codestra-Timestamp
X-Codestra-Event-ID
HTTP method in uppercase
request path
X-Tenant-ID
X-Correlation-ID
Idempotency-Key
raw request body
```

Tenant, correlation and idempotency headers are signed so they cannot be swapped
onto a valid body. The verified machine identity and configured tenant mapping
remain authoritative. HMAC secrets are tenant-scoped and never stored in Git or
n8n workflow JSON.

## Truthful user-facing states

Odoo and product interfaces must not present synchronous success merely because
n8n or Middleware accepted a request. Business-facing state should distinguish:

```text
requested
accepted
blocked
waiting approval
submitted
unknown / reconciliation required
delivered or completed
failed
cancelled
```

The final state comes from normalized destination evidence.

## Release and activation gates

Before any source change becomes live:

1. exact-head and merge-result CI passes in every changed repository;
2. all contracts are byte-compatible at the reviewed SHAs;
3. Keycloak clients, audiences and exact scopes are reviewed;
4. Kong routes, mTLS and header forwarding are verified;
5. tenant, campaign and command-family negative tests pass;
6. exact replay, semantic conflict and concurrent claim tests pass;
7. timeout-after-commit reconciliation proves zero duplicate effects;
8. a write-disabled staging canary proves zero external delivery;
9. database and configuration backup/restore are verified;
10. rollback is rehearsed;
11. immutable artifact, SBOM, provenance and signatures are available;
12. live capability activation receives separate approval.

A source merge does not enable email, SMS, social publishing, callbacks,
VICIdial control, PSTN dialing or Odoo writes.

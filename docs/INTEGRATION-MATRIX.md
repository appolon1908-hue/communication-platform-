# Communications Integration Matrix

Date: 2026-08-29

## Product Integrations

| Product/System | Communication Need | Canonical Path | Current State | Missing Before Production |
| --- | --- | --- | --- | --- |
| Moneybee Backend | Loan notifications, calls, campaign actions | Product -> SDK -> Kong -> Middleware -> Klyrow/Telnexa/VICIdial | Needs SDK switch | Remove hand-written provider calls, add generated SDK, prove auth matrix. |
| Beyvra Backend | Trading/account notifications | Product -> SDK -> Kong -> Middleware -> Klyrow/Telnexa | Needs integration | Add product identity/scopes, SDK calls, canary tests. |
| social.codestra.co | Social notifications, email/SMS alerts | Product -> SDK -> Kong -> Middleware -> Klyrow/Telnexa | Needs integration | Define notification catalogue, product scopes, SDK adoption. |
| kyqra | SMS SaaS workflow | Product/provider classification -> Middleware/Telnexa | Needs classification | Decide if product or provider adapter; add auth and read-back. |
| klyrow.com | Email provider/runtime | Middleware -> Klyrow internal provider API | Email Step 3 branch implemented | Durable staging canary, DNS/evidence, safe-mode proof. |
| Breero.com | Booking confirmations/reminders | Product -> SDK -> Middleware -> Klyrow/Telnexa | Needs integration | Product identity, event catalogue, SDK adoption. |
| LARIM-A Backend | Unknown/product candidate | TBD | Needs classification | Classify, define communication needs, add scopes if active. |
| transportation-backend- | Dispatch/customer notifications | Product -> SDK -> Middleware -> Klyrow/Telnexa | Needs integration | Product identity, event catalogue, SDK adoption. |

## Runtime Integrations

| Source | Target | Protocol | Purpose | Required Evidence |
| --- | --- | --- | --- | --- |
| SDK | Kong | HTTPS/OpenAPI | Public client calls | Generated clients, compatibility gates. |
| Kong | Middleware | HTTPS/JWT/OIDC | Protected canonical API | Valid/no/invalid/wrong-scope auth matrix. |
| Middleware | Klyrow | Internal HTTPS/service identity | Email send/read-back/events | Safe-mode canary and provider read-back. |
| Middleware | Telnexa | Internal HTTPS/service identity | SMS send/read-back/DLR | Safe-mode or test-route DLR evidence. |
| Middleware | Vicidialer-Codestra | Internal HTTPS/service identity | Voice command/read-back | Sandbox campaign/call evidence. |
| Providers | Middleware | Signed webhook/private ingress | Delivery/provider events | Signature, replay, tenant isolation tests. |
| Middleware | n8n | Governed webhook/events | Orchestration | No direct provider mutation evidence. |
| Middleware/Odoo | Odoo/Middleware | Governed APIs | CRM activity/business state | No direct provider write bypass. |

## Observability Integrations

| Source | Destination | Tooling | Purpose |
| --- | --- | --- | --- |
| Services/exporters | Prometheus | Scrape | Metrics and alert rules. |
| Prometheus | Alertmanager | Alert routing | Incident notifications. |
| Prometheus/Loki/Tempo | Grafana | Datasources | Operational dashboard. |
| Services/containers | Loki | Alloy/OpenTelemetry | Logs. |
| Services | Tempo | OpenTelemetry | Traces. |
| Curated read models | Superset | SQL/semantic datasets | Analytics/reporting. |
| Services | OpenBao | Least-privilege identities | Secret retrieval and lease management. |

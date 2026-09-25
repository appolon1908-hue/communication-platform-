# Duplicate Ownership Review

## Decision

No new umbrella runtime should absorb existing provider implementations. Where overlap exists, retain one principal owner and treat other copies as derived adapters/contracts/reference only.

| Capability | Overlap | Principal owner | Decision |
|---|---|---|---|
| Public communications contract | SDK and provider-local APIs | `SDK-repository` | SDK owns canonical public contract; provider APIs remain implementation surfaces |
| Cross-system command execution | Middleware and SDK connector-kit | `Middleware-` | Middleware executes; SDK connector-kit is distributable interface/tooling only |
| Email API/client | Klyrow reference SDKs and Codestra SDK | `SDK-repository` for public Codestra SDK; `klyrow.com` for provider-local API | Product apps should converge on Codestra SDK for unified communications |
| SMS command surface | Telnexa `/send` and Middleware command plane | `Middleware-` for governed cross-system request; `telnexa` for SMS runtime | Do not expose Jasmin provider credentials to products |
| Voice control | VICIdial restricted adapter and broader Middleware telephony workers | `Vicidialer-Codestra` for destination runtime; `Middleware-` for cross-system control | Remove/avoid competing runtime implementations |
| Event normalization | Provider callbacks, Middleware events, SDK AsyncAPI | Provider repo emits truth; Middleware normalizes/durably persists; SDK publishes canonical event contract | Keep all three layers but with explicit roles |
| Dashboard state | Provider dashboards, Grafana, future communications admin UI | Provider UI remains local; communication-platform designs central UI; Middleware/provider read APIs supply governed data | Central dashboard must not become a new system of record |

## Rule

If duplicate runtime code is discovered during Steps 3–5, stop and assign principal ownership before expanding it.
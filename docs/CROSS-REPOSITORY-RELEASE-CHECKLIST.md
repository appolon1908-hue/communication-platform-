# Cross-Repository Release Checklist

Date: 2026-08-29

## Required Release Evidence

Every cross-repository communications release must record:

- exact repository list
- branch name for each repository
- final commit SHA for each repository
- PR URL and review status
- CI run IDs or links
- contract validation result
- compatibility/drift result
- security/auth matrix result
- provider canary result
- rollback plan
- production gates intentionally enabled or left disabled

## Pre-Merge Checklist

| Check | Required |
| --- | --- |
| Architecture impact recorded in `communication-platform-` | yes |
| SDK contract updated before runtime behavior changes | yes, when public API/event surface changes |
| Middleware authorization and idempotency reviewed | yes |
| Provider runtime read-back/reconciliation reviewed | yes |
| Kong routes/scopes/audiences reviewed | yes, when public route changes |
| Keycloak clients/scopes reviewed | yes, when caller identity changes |
| Tests include positive and negative auth paths | yes |
| Safe-mode/write flags unchanged unless explicitly approved | yes |
| Observability impact recorded | yes |
| Rollback path documented | yes |

## Release Order

1. Merge architecture docs.
2. Merge SDK contract branch.
3. Merge Middleware implementation branch.
4. Merge provider implementation branch.
5. Merge Keycloak/Kong route and identity branches.
6. Merge observability dashboard/alert branches.
7. Merge product SDK adoption branches.
8. Promote to staging.
9. Run live auth/provider/reconciliation matrix.
10. Promote to production only after written activation approval.

## Production No-Go Conditions

- Invalid token accepted by Kong or Middleware.
- Wrong tenant/caller can read or mutate another tenant.
- Indeterminate provider state is blindly retried.
- Direct product-to-provider write path remains active.
- Secrets appear in code, logs, traces, metrics, dashboards, or docs.
- Provider live delivery flag enabled without canary and rollback evidence.
- Observability alerts for provider failure/reconciliation backlog are absent.

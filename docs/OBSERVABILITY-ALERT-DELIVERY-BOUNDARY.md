# Observability alert delivery boundary

This repository is the communication-architecture authority for the Codestra observability alert path. It does not ingest alerts, store incidents, own provider credentials, or send messages.

The only approved path is:

```text
Prometheus evaluation
  -> Alertmanager grouping/inhibition
  -> private TLS POST /v1/integrations/alertmanager/events
  -> Middleware durable incident, timeline, audit, and outbox transaction
  -> governed klyrow-alert-email adapter
  -> provider only after a later protected runtime activation
```

Alertmanager cannot use SMTP, call a provider API, select recipients, or execute a business mutation. Middleware owns authentication, validation, idempotency, durable state, retry, provider-ambiguity reconciliation, and audit. The provider authority remains `appolon1908-hue/klyrow.com`; this repository does not duplicate its runtime.

The initial recipient allowlist contains only `appolon@codestra.co`. The address is a policy identity, not a metric label or caller-controlled input. Repository defaults keep delivery disabled. No SMTP connection, provider call, external canary, email, SMS, voice, social, financial, or trading effect is authorized by this contract.

The exact machine authority is [`contracts/observability-alert-delivery.v1.json`](../contracts/observability-alert-delivery.v1.json). Validate it with:

```bash
python3 scripts/validate_observability_alert_boundary.py --check
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Rollback is a protected revert of the contract, documentation, checksum, validator, tests, and workflow. There is no runtime rollback because this source-only change activates nothing.

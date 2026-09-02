#!/usr/bin/env python3
"""Fail-closed validation for the repository-only alert delivery boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "observability-alert-delivery.v1.json"
DOCUMENT_PATH = ROOT / "docs" / "OBSERVABILITY-ALERT-DELIVERY-BOUNDARY.md"
CHECKSUM_PATH = ROOT / "release" / "observability-alert-boundary.sha256"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class BoundaryError(ValueError):
    pass


def load_contract() -> dict[str, Any]:
    try:
        value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BoundaryError(f"cannot load alert boundary: {exc}") from exc
    if not isinstance(value, dict):
        raise BoundaryError("alert boundary must be a JSON object")
    return value


def validate(value: dict[str, Any]) -> None:
    if value.get("schemaVersion") != "1.0" or value.get("contractId") != "codestra-observability-alert-delivery-v1":
        raise BoundaryError("alert boundary identity mismatch")
    if value.get("principalRepository") != "appolon1908-hue/communication-platform-":
        raise BoundaryError("communication-platform repository is not principal")

    source = value.get("source")
    if source != {
        "service": "alertmanager",
        "directProviderDeliveryAllowed": False,
        "directSmtpAllowed": False,
        "providerCredentialsAllowed": False,
    }:
        raise BoundaryError("Alertmanager must remain a provider-credential-free Middleware caller")

    middleware = value.get("middleware")
    if not isinstance(middleware, dict):
        raise BoundaryError("Middleware authority is missing")
    required_middleware = {
        "repository": "appolon1908-hue/Middleware-",
        "ingestionPath": "/v1/integrations/alertmanager/events",
        "privateTlsRequired": True,
        "fileCredentialOrWorkloadIdentityRequired": True,
        "durableIncidentLedgerRequired": True,
        "durableOutboxRequired": True,
        "idempotencyRequired": True,
        "providerAmbiguityRequiresReconciliation": True,
    }
    if any(middleware.get(key) != expected for key, expected in required_middleware.items()):
        raise BoundaryError("Middleware ingestion or durability contract mismatch")
    if not SHA_RE.fullmatch(str(middleware.get("protectedMergeSha", ""))):
        raise BoundaryError("Middleware protected merge SHA must be immutable")

    if value.get("delivery") != {
        "adapter": "klyrow-alert-email",
        "providerAuthorityRepository": "appolon1908-hue/klyrow.com",
        "middlewareOnly": True,
        "synchronousProviderCallDuringIngestionAllowed": False,
    }:
        raise BoundaryError("governed delivery adapter boundary mismatch")

    if value.get("recipientPolicy") != {
        "policyId": "codestra-observability-initial-admin-v1",
        "allowedRecipients": ["appolon@codestra.co"],
        "callerSuppliedRecipientsAllowed": False,
        "tenantSuppliedRecipientsAllowed": False,
        "deliveryEnabledByDefault": False,
    }:
        raise BoundaryError("fixed disabled recipient policy mismatch")

    if value.get("activation") != {
        "repositoryOnly": True,
        "externalDeliveryAuthorized": False,
        "smtpConnectionAuthorized": False,
        "providerApiCallAuthorized": False,
        "productionCanaryAuthorized": False,
    }:
        raise BoundaryError("repository-only activation boundary exceeded")


def checksum() -> str:
    material = b""
    for path in (CONTRACT_PATH, DOCUMENT_PATH):
        material += str(path.relative_to(ROOT)).encode("utf-8") + b"\0"
        material += path.read_bytes()
    return hashlib.sha256(material).hexdigest()


def run(write: bool) -> str:
    validate(load_contract())
    digest = checksum()
    expected = f"{digest}  codestra-observability-alert-boundary-v1\n"
    if write:
        CHECKSUM_PATH.parent.mkdir(parents=True, exist_ok=True)
        CHECKSUM_PATH.write_text(expected, encoding="utf-8")
    elif CHECKSUM_PATH.read_text(encoding="utf-8") != expected:
        raise BoundaryError("alert boundary checksum is missing or stale")
    return digest


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    digest = run(args.write)
    print("OBSERVABILITY_ALERT_COMMUNICATION_BOUNDARY=PASS")
    print("DIRECT_ALERTMANAGER_DELIVERY=DENIED")
    print("EXTERNAL_DELIVERY_AUTHORIZED=NO")
    print(f"OBSERVABILITY_ALERT_BOUNDARY_CHECKSUM={digest}")


if __name__ == "__main__":
    main()

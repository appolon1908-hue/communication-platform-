from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_observability_alert_boundary import (  # noqa: E402
    BoundaryError,
    load_contract,
    run,
    validate,
)


class ObservabilityAlertBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_contract()

    def test_repository_contract_and_checksum_pass(self) -> None:
        run(False)

    def test_direct_smtp_is_rejected(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["source"]["directSmtpAllowed"] = True
        with self.assertRaises(BoundaryError):
            validate(changed)

    def test_second_recipient_is_rejected(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["recipientPolicy"]["allowedRecipients"].append("other@example.invalid")
        with self.assertRaises(BoundaryError):
            validate(changed)

    def test_activation_is_rejected(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["activation"]["externalDeliveryAuthorized"] = True
        with self.assertRaises(BoundaryError):
            validate(changed)

    def test_mutable_middleware_revision_is_rejected(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["middleware"]["protectedMergeSha"] = "main"
        with self.assertRaises(BoundaryError):
            validate(changed)


if __name__ == "__main__":
    unittest.main()

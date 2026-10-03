import csv
import tempfile
import unittest
from pathlib import Path
from lead_ops import FIELDS, enrich, run


class PipelineTests(unittest.TestCase):
    def test_duplicate_and_invalid_source_are_held(self):
        base = dict.fromkeys(FIELDS, "")
        base.update(account_id="1", company="Solar House", category="Spa",
                    market="South Africa", location_count="2",
                    booking_signal="whatsapp", website="https://solar.example",
                    evidence_url="https://solar.example/about",
                    evidence_text="Two sites", observed_on="2026-09-29")
        a, b = enrich([base, {**base, "account_id":"2", "company":"  SOLAR HOUSE  ", "evidence_url":"http://bad.example"}])
        self.assertEqual(a["review_status"], "RESEARCHED_ACCOUNT")
        self.assertEqual(b["review_status"], "REVIEW")
        self.assertIn("duplicate account name", b["review_reason"])
        self.assertIn("invalid source URL", b["review_reason"])
        self.assertEqual(a["sales_ready"], "NO")

    def test_demo_manifest_and_crm_gate(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            result = run(root / "source_accounts.csv", output)
            self.assertEqual((result["rows"], result["unique_researched"], result["exceptions"]), (12, 10, 2))
            self.assertEqual(result["personal_contacts"], 0)
            with (output / "03_crm_account_draft.csv").open(encoding="utf-8-sig", newline="") as fh:
                crm = list(csv.DictReader(fh))
            self.assertEqual(len(crm), 10)
            self.assertTrue(all(r["stage"] == "Research draft - no contact" for r in crm))


if __name__ == "__main__": unittest.main()

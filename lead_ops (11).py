#!/usr/bin/env python3
"""Auditable account-level lead research pipeline. Python standard library only.

Input: a CSV of publicly observed businesses. Output: reviewed candidates,
exceptions, a draft CRM account import, campaign segments and a run manifest.
The program never invents personal contacts, sends outreach, or claims sales.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

FIELDS = [
    "account_id", "company", "category", "market", "location_count",
    "booking_signal", "booking_vendor", "website", "evidence_url",
    "evidence_text", "observed_on",
]
BOOKING = {"website_or_contact", "external_platform", "owned_app", "whatsapp", "unknown"}
OUTPUT_FIELDS = FIELDS + [
    "normalized_company", "domain", "score", "tier", "review_status",
    "review_reason", "next_action", "hypothesis", "contact_verified",
    "sales_ready",
]


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", (value or "").strip())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def domain(url: str) -> str:
    parsed = urlparse((url or "").strip())
    return (parsed.hostname or "").removeprefix("www.").lower()


def valid_url(url: str) -> bool:
    p = urlparse((url or "").strip())
    return p.scheme == "https" and bool(p.netloc) and "." in p.netloc


def score_record(r: dict[str, str]) -> tuple[int, str]:
    """A triage heuristic, never a claim of pain, purchase intent or fit."""
    count = int(r["location_count"]) if r["location_count"].isdigit() else 0
    scale = 30 if count >= 10 else 20 if count >= 3 else 12 if count >= 2 else 5
    category = 20 if r["category"].casefold() in {"barber", "beauty", "spa", "wellness"} else 0
    source = 25 if valid_url(r["evidence_url"]) and r["evidence_text"].strip() else 0
    booking = {
        "whatsapp": 20, "website_or_contact": 15, "unknown": 8,
        "external_platform": 4, "owned_app": 2,
    }.get(r["booking_signal"], 0)
    market = 5 if r["market"].casefold() == "south africa" else 0
    score = scale + category + source + booking + market
    tier = "A / research" if score >= 75 else "B / discovery" if score >= 55 else "C / hold"
    return score, tier


def enrich(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    result = []
    for raw in source_rows:
        r = {k: (raw.get(k) or "").strip() for k in FIELDS}
        key = normalize(r["company"])
        reasons = []
        if not r["company"] or not r["account_id"]: reasons.append("missing identity")
        if key in seen: reasons.append("duplicate account name")
        seen.add(key)
        if not valid_url(r["website"]) or not valid_url(r["evidence_url"]):
            reasons.append("invalid source URL")
        if not r["evidence_text"]: reasons.append("missing evidence")
        if r["booking_signal"] not in BOOKING: reasons.append("invalid booking signal")
        if r["market"].casefold() != "south africa": reasons.append("out of scope market")
        try:
            if r["location_count"] and int(r["location_count"]) < 1:
                reasons.append("invalid location count")
        except ValueError:
            reasons.append("invalid location count")
        try: date.fromisoformat(r["observed_on"])
        except ValueError: reasons.append("invalid observation date")
        points, tier = score_record(r)
        existing = r["booking_signal"] in {"external_platform", "owned_app"}
        r.update(
            normalized_company=key, domain=domain(r["website"]),
            score=str(points), tier=tier,
            review_status="REVIEW" if reasons else "RESEARCHED_ACCOUNT",
            review_reason="; ".join(reasons),
            next_action="Resolve quality exception" if reasons else (
                "Research integration opportunity" if existing else
                "Confirm workflow and decision maker"),
            hypothesis=("Existing booking stack: assess integration and switching cost" if existing
                        else "Booking workflow unknown: validate current process"),
            contact_verified="NO", sales_ready="NO",
        )
        result.append(r)
    return result


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            # Prevent spreadsheet applications from executing untrusted input as a formula.
            safe = {k: ("'" + str(row.get(k, "")) if str(row.get(k, "")).lstrip().startswith(("=", "+", "-", "@"))
                        else row.get(k, "")) for k in fields}
            writer.writerow(safe)


def run(input_path: Path, output_dir: Path) -> dict:
    with input_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        missing = set(FIELDS) - set(reader.fieldnames or [])
        if missing: raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
        source_rows = list(reader)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = enrich(source_rows)
    clean = [r for r in rows if r["review_status"] == "RESEARCHED_ACCOUNT"]
    exceptions = [r for r in rows if r["review_status"] == "REVIEW"]
    write_csv(output_dir / "01_account_research.csv", rows, OUTPUT_FIELDS)
    write_csv(output_dir / "02_review_queue.csv", exceptions, OUTPUT_FIELDS)
    crm_fields = ["external_id", "account_name", "website", "category", "country", "priority", "source_url", "stage"]
    crm = [
        dict(external_id=r["account_id"], account_name=r["company"], website=r["website"],
             category=r["category"], country=r["market"], priority=r["tier"],
             source_url=r["evidence_url"], stage="Research draft - no contact")
        for r in clean
    ]
    write_csv(output_dir / "03_crm_account_draft.csv", crm, crm_fields)
    segments = Counter(r["category"] for r in clean)
    campaign_fields = ["segment", "accounts", "channel", "message_hypothesis", "metric", "status"]
    campaign = [
        dict(segment=segment, accounts=count, channel="Manual account research",
             message_hypothesis="Test operational relevance after buyer discovery",
             metric="Verified buyer conversations (actuals only)", status="Concept only - not launched")
        for segment, count in sorted(segments.items())
    ]
    write_csv(output_dir / "04_campaign_hypotheses.csv", campaign, campaign_fields)
    sha = hashlib.sha256(input_path.read_bytes()).hexdigest()
    manifest = dict(input=input_path.name, input_sha256=sha, rows=len(rows), unique_researched=len(clean),
                    exceptions=len(exceptions), source_scope="Public company pages only",
                    personal_contacts=0, outreach_sent=0, sales_results=0,
                    score_definition="scale 30 + category 20 + source 25 + booking 20 + market 5")
    (output_dir / "05_run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (output_dir / "06_records.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path, help="Public-account research CSV")
    p.add_argument("output", type=Path, help="Directory for review and CRM draft CSV files")
    a = p.parse_args()
    print(json.dumps(run(a.input, a.output), indent=2))


if __name__ == "__main__": main()

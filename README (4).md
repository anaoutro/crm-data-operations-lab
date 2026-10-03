# Public B2B Lead Intelligence — real company data

This is an independent portfolio demonstration, prepared on 30 September 2026. It uses seven real businesses and observations from their public official websites. The records are **researched company accounts**, not verified buyers or sales-qualified leads.

## Deliverables

- `Public_B2B_Lead_Intelligence_2026.xlsx`: editable public inputs, calculated duplicate checks, research scores and next actions; a linked B2B segment plan; method and refresh rules.
- `source_accounts.csv`: source data for the Python pipeline.
- `lead_ops.py`: Python standard-library automation for normalization, source validation, duplicate exceptions, CRM account draft and campaign hypotheses.
- `generated/`: outputs of the run with seven unique accounts and zero quality exceptions.

## Run

```bash
python lead_ops.py source_accounts.csv generated
```

The workbook recalculates in Excel when public inputs change. The Python program regenerates CSV/JSON exports when its CSV input changes. These are complementary, and the heuristic scores have different scales; compare statuses and source facts, not their numeric scores.

## Provenance and limits

Every record includes an official evidence URL, observation date and a short observation. The named businesses, public booking routes and reported scale are factual observations from those URLs; location figures are source claims and not independently audited. For Sorbet and Legends, the numeric cell uses the public minimum (200 and 80 respectively), while the evidence text preserves “over.” Camelot's 16 branches and Life Day Spa's 11 include locations outside South Africa.

No personal contact, email address, buyer identity, willingness to buy, outreach, booked meeting, sale or conversion is claimed. The B2B campaign plan is a set of discovery hypotheses. Recheck websites before any real commercial use.

## Verified official pages

- Barber Club: https://www.barberclub.co.za/branches
- Sorbet: https://www.sorbet.co.za/salon
- Camelot Spa Group: https://www.camelotspa.co.za/
- Life Day Spa Group: https://lifedayspa.co.za/book-a-treatment/
- Legends Barbershop: https://www.legends-barber.com/
- Sirina Thai Spa: https://sirinathaispa.co.za/
- Perfect 10: https://www.perfect10.co.za/

## Quality check

The delivered Excel contains seven accounts, seven unique names, zero verified buyers and zero outbound contacts. A temporary duplicate of Sorbet was inserted during verification: the formula marked `REVIEW DUPLICATE`, reduced the unique count to six and changed the next action to `Resolve duplicate`. The original Perfect 10 row was restored before export.

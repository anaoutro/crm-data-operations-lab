# CRM & Data Operations Lab

Practical CRM engineering and auditable account research by **Ana Maria do Céu Gomes**. Companion to the larger **signaldesk-salesforce-apex** project.

| Project | Source and deliverable | Actual scope |
|---|---|---|
| [Salesforce Aster](salesforce-aster) | Apex, Visualforce and isolated scenario seed | Developer Edition implementation verified 29 Sep 2026; three tests and 100% coverage of the two production classes in the documented run. Fictional opportunities. |
| [Fieldwork](fieldwork) | Python, public CSV, Excel, tests and outputs | Ten real company accounts from 12 raw rows; two duplicates held; no personal contacts or outreach. |
| [Public B2B Seven](public-b2b-seven) | Separate workbook and Python variant | Seven public accounts. Preserved as a distinct version; heuristic score scales differ from Fieldwork. |
| [Excel scenarios](excel-scenarios) | HelioBook and Lumen workbooks/cases | 36 fictional HelioBook accounts; 32 synthetic Lumen rows. Planning simulations, not real leads. |
| [CRM implementations](docs/crm-implementations) | HubSpot and Zoho evidence PDFs | Prior live/developer-test setup evidence. Not an SDK or a recreated API integration. |
| [Offline CRM examples](examples/offline-crm) | Four standalone Python demos | Synthetic rule prototypes for HubSpot, Zoho, Salesforce and GHL; no real CRM calls. |
| [GoHighLevel blueprint](blueprints) | Documented workflow design | Specification only; no live sub-account. |

## Run the public research pipelines

Python 3.11+; standard library only:

```bash
cd fieldwork
python lead_ops.py source_accounts.csv generated
python -m unittest -v
cd ../public-b2b-seven
python lead_ops.py source_accounts.csv generated
```

Inspect the raw source, duplicates, generated account draft and each evidence link. Review priority is not buying intent. Workbook formulas and Python scores are documented separately rather than claimed to be identical.

## Run the offline examples

```bash
cd examples/offline-crm
python hubspot_demo.py
python zoho_demo.py
python salesforce_demo.py
python ghl_demo.py
```

No messages or campaigns are sent. Run from that directory because the examples read nearby input files.

## Deploy the Salesforce Aster source

```bash
cd salesforce-aster
sf org login web --alias aster-lab
sf project deploy start --target-org aster-lab --test-level RunLocalTests --wait 20
```

Review the seed before running it: it creates fictional account/opportunity records and must not be repeated against existing scenario records. The read-only dashboard is `AsterPipelineConsole`. The historical 100% coverage result belongs to Aster, **not** the new SignalDesk app.

## Verification and reuse

See [VALIDATION.md](VALIDATION.md). Tests and outputs can be rerun; GitHub-hosted CI and Salesforce org execution have not been run during package preparation. No React HubSpot App Cards/Marketplace app source was found in the supplied packages. The live HubSpot case and Python example are accurately separated.

Code is shared for portfolio evaluation; no open-source redistribution license has been declared. Public business sources remain attributed in each project. No customer credentials are included.

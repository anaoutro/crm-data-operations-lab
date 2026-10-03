# Aster Opportunity Command Center

Implemented in Ana Gomes's Salesforce Developer Edition on 29 September 2026. This is an independent portfolio lab with fictional account and opportunity records, not a client engagement or production outcome.

## What runs in the org

- `AsterPipelineController`: read-only, user-mode SOQL scoped to the fictional Aster Portfolio Lab account. It classifies up to 500 open opportunities using three deterministic checks: blank Next Step, overdue Close Date, and missing or nonpositive Amount. Two or more issues are Critical, one is Attention, none is Healthy.
- `AsterPipelinePageController`: small Visualforce adapter that memoizes the summary for the page request.
- `AsterPipelineConsole`: responsive Visualforce dashboard showing the live summary and review table.
- `AsterPipelineControllerTest`: two passing tests for all three severity levels, totals, immutability, and an empty pipeline.
- `AsterPipelinePageControllerTest`: an integration test that creates included and excluded accounts, verifies the scoped query, values, and memoized page summary. The Developer Console showed all three tests passing with 0 failures across the two runs and 100% coverage of both production Apex classes (47/47 and 3/3 lines) at the observed run.
- `scripts/AsterPortfolioSeed.apex`: the anonymous Apex used once to create one fictional account and three fictional opportunities. Do not rerun without checking for existing records.

Observed dashboard values on 29 September 2026: 3 open opportunities, USD 50,000 in positive amounts, 1 Critical, 1 Attention, 1 Healthy. These are synthetic scenarios and will change if the records are edited or the date changes.

The dashboard reads data only. It does not write opportunity updates, create tasks, forecast revenue, or send messages. The dedicated scenario filter keeps preinstalled Developer Edition sample records out of the displayed figures. The source package is provided so a reviewer can examine the rules and page. An earlier LWC prototype exists separately but was not deployed to the org or included in this verified package.

To inspect in the signed-in org, open the Visualforce page named `AsterPipelineConsole`. Access is subject to Salesforce authentication and permissions.

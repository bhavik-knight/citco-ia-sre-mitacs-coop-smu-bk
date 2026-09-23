# CAIS Deadline Process — Context

## What is CAIS?

CAIS stands for **Citco Alternative Investment Services**. It is an alternative
investment platform that serves as a marketplace connecting financial advisors and
wealth management firms with alternative investment products. It streamlines access,
execution, and administration of alternative investments.

## CAIS Deadline Project

The **CAIS Deadline Project** is an RPA automation that handles two key processes:

### Part I — Upload Deadline

The bot picks up a **Standard Allocation Sheet** (containing Client Number, Deadline
DateTime, and NAV Date) from a shared drive and uploads the deadline into the
**PDS database**. Once successfully uploaded, the deadline goes directly to
**Approved** status.

### Part II — Download Report & Backups

The bot:

1. Identifies clients with deadlines due in the next 2 days (and again 1 day before
   deadline expiry).
2. Checks if the client belongs to a **Consolidated Group** or is an individual client.
3. Downloads the **Deadline Report**, applies pricing rules/checks:
   - Price Type, Price Source, Price Status hierarchies
   - Stale price highlighting
   - % change thresholds: >5% and >20%
4. Downloads trade documents.
5. Merges all documents into a single PDF.
6. Zips the folder.
7. Sends a **Success Completion Email**.

### Exception Handling

If any of the following occur, the bot sends **exception notification emails** to the
CAIS team:
- Connection to PDS fails
- Allocation sheet is missing or non-standard
- Documents are unavailable

## Repositories

- `core-ia-bpo-cais-dl` — main CAIS Deadline Lambda codebase (CodeCommit)

## Incident Context (IISS-706 / June 2026)

The CAIS Deadline Lambda failed with `SMBAuthenticationError: SpnegoError` during
UCM upload. Root cause: `constants.py` cached credentials at module import time;
a Secrets Manager rotation left empty values, causing silent authentication failures.

Hotfix applied:
1. Fail-fast UCM credential validation at startup and before each SMB connection
2. Guard against empty `deadline_ids` generating invalid SQL `IN()` clause
3. Zip file existence check before attempting UCM upload

The CAIS filing completed before the regulatory deadline.

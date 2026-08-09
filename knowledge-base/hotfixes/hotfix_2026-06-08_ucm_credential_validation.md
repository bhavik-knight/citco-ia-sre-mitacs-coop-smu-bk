# Hotfix: UCM Credential Validation

**Date:** 2026-06-08  
**Branch:** `hotfix/ucm-credential-validation`  
**Severity:** High — Production service failure with misleading error  
**Affected Service:** CAIS Deadline (ECS Fargate, eu-west-1)

---

## Problem Summary

On June 8, 2026, the CAIS Deadline process failed with a cryptic `SMBAuthenticationError` / `SpnegoError` when uploading to UCM (`ucm.int.sharedprod01.citcosvc.com`). The actual root cause is **empty or missing UCM credentials** loaded from AWS Secrets Manager, but the error message provides no indication of this.

**Error seen in logs:**
```
SMBAuthenticationError: Failed to authenticate with server: SpnegoError (1): 
SpnegoError (16): Operation not supported or available, Context: No username 
or password was specified and the credential cache did not exist or contained 
no credentials, Context: Unable to negotiate common mechanism
```

**What should have been logged:**
```
RuntimeError: UCM credentials are empty or missing. Secret: IA-BPO/UCM/PRD/credentials, 
username present: False, password present: False
```

---

## Root Cause

The credential loading in `constants.py` (lines 38-43) does not validate that the fetched secret contains non-empty values. When the secret returns empty strings or missing keys, the code proceeds silently. The failure only surfaces much later during SMB upload — deep inside the `smbprotocol` library — producing a confusing SPNEGO negotiation error.

Possible triggers:
1. Secret rotation invalidated the `ucm_username` / `ucm_password` fields
2. Secret fetch returned stale/empty data
3. Secret JSON structure changed (key names differ)

---

## Architecture

```
core-ia-bpo-cais-dl/
├── deadline-api/
│   └── src/
│       └── backend/
│           ├── constants.py        ← CHANGE 1: Add credential validation
│           ├── pysmb_helper.py     ← CHANGE 2: Add pre-connection check
│           ├── smb_client.py
│           ├── main.py
│           └── fnp_functions.py
└── templates/
    └── ecs-deadline-fargate-api.yaml  (UCM_SECRET env var defined here)
```

---

## Current Error Flow (BEFORE fix)

```
 ┌──────────────┐       ┌──────────────────┐       ┌─────────────────┐
 │  ECS Startup │       │ Secrets Manager   │       │   UCM Server    │
 └──────┬───────┘       └────────┬─────────┘       └────────┬────────┘
        │                        │                           │
        │  1. import constants.py│                           │
        │  ──────────────────────>                           │
        │  get_secret(UCM_SECRET)│                           │
        │                        │                           │
        │  2. Returns:           │                           │
        │  <──────────────────────                           │
        │  {"ucm_username": "",  │                           │
        │   "ucm_password": ""}  │                           │
        │                        │                           │
        │  ⚠️  NO VALIDATION     │                           │
        │  UCM_USER_NAME = ""    │                           │
        │  UCM_USER_PASSWORD = ""│                           │
        │  Module loads OK       │                           │
        │                        │                           │
        │  ~~~~~~~~ minutes pass, fund processing ~~~~~~~~   │
        │                        │                           │
        │  3. upload_to_share(user="", passw="", host=ucm)   │
        │  ─────────────────────────────────────────────────>│
        │                        │                           │
        │  4. register_session(host, user="", pass="")       │
        │                        │                           │
        │  5. ❌ SpnegoError:     │                           │
        │  <─────────────────────────────────────────────────│
        │  "No username or password was specified"           │
        │                        │                           │
        │  🔴 RESULT: Cryptic error deep in smbprotocol     │
        │     User has no idea credentials were empty        │
 ───────┴────────────────────────┴───────────────────────────┴──────────
```

---

## Proposed Fix Flow (AFTER fix)

**Scenario A: Empty credentials at startup (fail-fast)**

```
 ┌──────────────┐       ┌──────────────────┐
 │  ECS Startup │       │ Secrets Manager   │
 └──────┬───────┘       └────────┬─────────┘
        │                        │
        │  1. import constants.py│
        │  ──────────────────────>
        │  get_secret(UCM_SECRET)│
        │                        │
        │  2. Returns:           │
        │  <──────────────────────
        │  {"ucm_username": "",  │
        │   "ucm_password": ""}  │
        │                        │
        │  ✅ NEW: VALIDATION    │
        │  username present? NO  │
        │  password present? NO  │
        │                        │
        │  ❌ RAISE RuntimeError:│
        │  "UCM credentials are  │
        │   empty or missing.    │
        │   Secret: IA-BPO/UCM/  │
        │   PRD/credentials,     │
        │   username present:    │
        │   False"               │
        │                        │
        │  🟢 RESULT:            │
        │  • Container fails immediately at startup
        │  • Clear error in CloudWatch logs
        │  • Operator knows exactly which secret to fix
        │  • No confusing SPNEGO trace
 ───────┴────────────────────────┴──────────────────────────────────────
```

**Scenario B: Credentials invalid at call-time (defense in depth)**

```
 ┌──────────────┐       ┌──────────────────┐
 │   main.py    │       │ pysmb_helper.py   │
 └──────┬───────┘       └────────┬─────────┘
        │                        │
        │  upload_to_share(      │
        │    user=None,          │
        │    passw=None,         │
        │    host=ucm...)        │
        │  ──────────────────────>
        │                        │
        │  ✅ NEW: PRE-CHECK     │
        │  user set? NO          │
        │                        │
        │  ❌ RAISE ValueError:  │
        │  <──────────────────────
        │  "SMB credentials not  │
        │   provided for host=   │
        │   ucm.int.sharedprod01.│
        │   Check UCM secret in  │
        │   AWS Secrets Manager."│
        │                        │
        │  🟢 RESULT:            │
        │  • Clear error before any network IO
        │  • No timeout waiting for SMB connection
        │  • Actionable message points to Secrets Manager
 ───────┴────────────────────────┴──────────────────────────────────────
```

---

## Files Changed

| # | File | Change |
|---|------|--------|
| 1 | `deadline-api/src/backend/constants.py` | Validate UCM credentials immediately after loading from Secrets Manager |
| 2 | `deadline-api/src/backend/pysmb_helper.py` | Add credential pre-check in `upload_to_share` and `download_from_share` |

---

## Detailed Changes

### File 1: `constants.py`

**Before (lines 38-43):**
```python
# Set up SMB UCM
UCM_SECRET = os.environ['UCM_SECRET']
ucm_login = json.loads(get_secret(UCM_SECRET))
UCM_USER_NAME = ucm_login['ucm_username']
UCM_USER_PASSWORD = ucm_login['ucm_password']
```

**After:**
```python
# Set up SMB UCM
UCM_SECRET = os.environ['UCM_SECRET']
ucm_login = json.loads(get_secret(UCM_SECRET))
UCM_USER_NAME = ucm_login.get('ucm_username', '')
UCM_USER_PASSWORD = ucm_login.get('ucm_password', '')

if not UCM_USER_NAME or not UCM_USER_PASSWORD:
    raise RuntimeError(
        f"UCM credentials are empty or missing. "
        f"Secret: {UCM_SECRET}, "
        f"Keys in secret: {list(ucm_login.keys())}, "
        f"username present: {bool(UCM_USER_NAME)}, "
        f"password present: {bool(UCM_USER_PASSWORD)}"
    )
```

### File 2: `pysmb_helper.py`

**Add at the start of `upload_to_share` (before `smb = None`):**
```python
if not user or not passw:
    raise ValueError(
        f"SMB credentials not provided. "
        f"host={host}, user={'set' if user else 'EMPTY'}, "
        f"password={'set' if passw else 'EMPTY'}. "
        f"Check UCM secret in AWS Secrets Manager."
    )
```

**Same check added at the start of `download_from_share`.**

---

## Impact Assessment

- **No functional change** when credentials are valid
- **Fail-fast at startup** if the secret is empty/malformed
- **Clear actionable error message** in CloudWatch logs
- **Defense in depth** — validation at both load-time and call-time

---

## Testing

1. Set `UCM_SECRET` to a secret with empty `ucm_username` → verify `RuntimeError` raised at import
2. Call `upload_to_share` with `user=""` → verify `ValueError` raised before connection attempt
3. Normal operation with valid credentials → verify no behavioral change

---

## Remediation Steps (for the immediate production issue)

1. Verify secret contents: `aws secretsmanager get-secret-value --secret-id "IA-BPO/UCM/PRD/credentials" --region us-east-1`
2. Confirm `ucm_username` and `ucm_password` fields are non-empty
3. If expired, update the secret with valid credentials
4. Restart the ECS task to pick up fresh credentials

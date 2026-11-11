# NextGenERP Security Test Report

Date: 2026-11-11
Branch: `main` (working tree, uncommitted)
Catalog: `tests/security_spec.py` — 1,000 cases
Executable suite: `backend/tests/test_security_suite.py`

## 1. Final result

| Metric | Result |
| --- | ---: |
| Catalogued cases | 1,000 |
| Automated cases executed | **906** |
| Automated cases passed | **906** |
| Automated cases failed | **0** |
| Automated cases skipped | **0** |
| Manual cases not executed | 13 |
| Blocked cases not executed | 43 |
| Not-implemented / documented gaps | 38 |
| Final security-suite duration | 325.15 s |
| Full backend suite | **972 passed**, 0 failed, 0 skipped, 424.68 s |
| Frontend production build | **Passed** |

The 906 automated cases are the only cases counted as passing. Manual, blocked and not-implemented cases are listed in Section 4 and are **not** reported as successful tests.

### Evidence

- Security JUnit: `C:\Users\noma1\AppData\Local\Temp\opencode\security-results-run2.xml`
  - `<testsuite tests="906" failures="0" errors="0" skipped="0" time="325.145">`
- Security log: `C:\Users\noma1\AppData\Local\Temp\opencode\security-run2.txt`
- Full backend JUnit: `C:\Users\noma1\AppData\Local\Temp\opencode\backend-full.xml`
  - `<testsuite tests="972" failures="0" errors="0" skipped="0" time="424.684">`
- Full backend log: `C:\Users\noma1\AppData\Local\Temp\opencode\backend-full.txt`
- Frontend build log: `C:\Users\noma1\AppData\Local\Temp\opencode\frontend-build.txt`

### Reproduction

```powershell
Set-Location C:\Users\noma1\OneDrive\Desktop\NextGenERP\backend
.\venv\Scripts\python.exe -m pytest tests\test_security_suite.py -q `
  --junitxml=C:\Users\noma1\AppData\Local\Temp\opencode\security-results-run2.xml

# Full backend regression suite
.\venv\Scripts\python.exe -m pytest -q `
  --junitxml=C:\Users\noma1\AppData\Local\Temp\opencode\backend-full.xml

Set-Location ..\frontend
npm run build
```

## 2. Environment

- Windows 10/11 host (`LAPTOP-64M01JB1`), Python virtual environment at `backend/venv`.
- Isolated temporary SQLite database created per test session; dropped and recreated per test.
- Rate limiting disabled globally in the test environment and enabled explicitly only inside rate-limit cases, with the limiter store reset around each case.
- No production data, live provider key or real secret used.
- `ASSISTANT_LLM_API_KEY` and `OPENAI_API_KEY` forced empty; provider tests monkeypatch `requests.post`.
- CORS test origins: `http://localhost:5173`, `http://localhost:8080`, `http://127.0.0.1:8080`, `https://erp.example.com`.

## 3. Coverage by category

| Category | Cases | Automated | Automated passed | Manual | Blocked | Not implemented |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Authentication & Login Security | 100 | 100 | 100 | 0 | 0 | 0 |
| Password Hashing & Credential Protection | 60 | 54 | 54 | 0 | 0 | 6 |
| RBAC & Authorization | 100 | 100 | 100 | 0 | 0 | 0 |
| Admin Panel & Privilege Escalation | 100 | 93 | 93 | 1 | 0 | 6 |
| JWT & Session Security | 80 | 76 | 76 | 2 | 0 | 2 |
| API Security & Input Validation | 100 | 94 | 94 | 0 | 6 | 0 |
| SQL Injection & Database Security | 80 | 80 | 80 | 0 | 0 | 0 |
| AI Assistant Security & Prompt Injection | 80 | 80 | 80 | 0 | 0 | 0 |
| Voice Assistant Security | 40 | 10 | 10 | 10 | 20 | 0 |
| Rate Limiting & Abuse Protection | 60 | 60 | 60 | 0 | 0 | 0 |
| CORS, CSP & Security Headers | 40 | 40 | 40 | 0 | 0 | 0 |
| Secrets & Environment Configuration | 40 | 40 | 40 | 0 | 0 | 0 |
| File Upload & Data Exposure | 30 | 30 | 30 | 0 | 0 | 0 |
| Audit Logging & Sensitive Operations | 30 | 6 | 6 | 0 | 0 | 24 |
| PostgreSQL & Production Deployment Security | 40 | 27 | 27 | 0 | 13 | 0 |
| Supply Chain & Dependency Security | 20 | 16 | 16 | 0 | 4 | 0 |
| **Total** | **1,000** | **906** | **906** | **13** | **43** | **38** |

All 906 executed cases passed in the final run. The full catalog, including expected results and handler names, is in `SECURITY_TEST_CATALOG.md`.

## 4. Cases not executed

### Manual (13)

| Area | Cases | Why not automated / current evidence |
| --- | ---: | --- |
| Admin UI shell separation | 1 (`SEC-0325`) | Existing admin browser E2E evidence (50/50 checks); no committed E2E framework |
| JWT lifetime and replay | 2 (`SEC-0436`, `SEC-0438`) | 30-minute lifetime and stateless replay are design properties; verification is documentation/manual |
| Voice mock flows | 10 (`SEC-0701`–`SEC-0710`) | Prior mocked browser E2E evidence (41/41 checks); not rerun in this environment |

Manual cases were not counted as passed.

### Blocked (43)

| Area | Cases | Reason |
| --- | ---: | --- |
| Concurrent inventory/order operations | 6 (`SEC-0535`–`SEC-0540`) | SQLite makes `with_for_update()` a no-op; no PostgreSQL service |
| PostgreSQL production checks | 13 (`SEC-0941`–`SEC-0953`, and related) | No PostgreSQL service or Docker in this environment |
| Real microphone / speech device checks | 20 (`SEC-0721`–`SEC-0740`) | Headless Edge cannot grant microphone permission or supply audio; only English voices installed |
| Dependency advisory scans | 4 (`SEC-0985`–`SEC-0988`) | `pip-audit` unavailable; npm audit constrained by network/offline access |

### Not implemented / documented gaps (38)

| Area | Cases | Gap |
| --- | ---: | --- |
| Admin audit, password policy, session timeout, role management | 6 | Features absent by design/documented gap |
| Audit logging model/middleware/events | 24 | No structured audit-log implementation |
| JWT refresh rotation and server-side revocation | 2 | Not implemented; stateless JWT by design |
| Password reset/change endpoints | 6 | Not implemented |
| **Total** | **38** | |

These gaps are tracked as accepted or open risks in `SECURITY_VULNERABILITY_REPORT.md` and `BUG_TRACKER.md`.

## 5. First run and remediation

The first full execution produced **118 failed / 788 passed** out of 906. Every failure was triaged; the final run is clean.

| Disposition | Count | Examples |
| --- | ---: | --- |
| Test-harness/fixture ordering or expectation defects | 112 | Lazy `regression-user` creation before `db_snapshot()`; admin fixture ordering; wrong fixture password in token-log cases; 252-character “256-character” email; registered user expected absent; generated SKU where JSON `null` was intended; wrong analytics key; `detail` assertion applied to successful search responses |
| Token-test construction issues | 4 | Unicode header transport; empty HMAC key blocked by PyJWT; RS256/ES256 generation requiring optional `cryptography`; modeled with safe assertions or manually constructed attacker tokens |
| Application defects | 2 | Oversized JWT subject caused a 500 (`SEC-0401`); inventory-history DELETE returned 404 instead of the specified 405 (`SEC-0235`) |

Application fixes:

- `auth/security.py`: reject non-ASCII and out-of-range `sub` values before database lookup.
- `routes/inventory_transactions.py`: explicit DELETE handler returning 405 for immutable audit history.

No failure was converted into a skip or silently ignored.

## 6. Regression tests added

- `backend/tests/test_security_suite.py` — 906 parametrized cases covering the full automated catalog.
- `backend/tests/conftest.py` — isolated test environment, rate-limit/provider isolation, and a cached `frontend_dist` fixture that builds the real frontend when absent.
- `backend/tests/test_auth.py` — invalid-email rejection and normalization.
- `backend/tests/test_catalog_routes.py` — supplier email/phone rejection and normalization.
- `backend/tests/test_order_routes.py` — sales-order customer email validation and stock preservation.
- Existing backend suite extended to **972 passing tests** in total.

## 7. Frontend build and chart verification

### Build

`npm run build` succeeded with Vite 8.3.4:

- `dist/index.html` 0.47 kB
- `dist/assets/index-B48XRtJI.css` 52.98 kB
- `dist/assets/index-BWhq-6zO.js` 552.03 kB
- `dist/assets/three.module-1-iL3Gi1.js` 694.91 kB

Vite emits a chunk-size warning for the Three.js bundle (tracked as BUG-017); the build itself passes.

### “Orders by status” chart

Verified by source inspection and built-bundle inspection:

- `AdminOverview.jsx` defines `STATUS_COLORS` for Pending, Confirmed, Shipped, Delivered and Cancelled and passes `colorMap={STATUS_COLORS} colorKey="label"`.
- `Charts.jsx` resolves each bar with `colorMap?.[item[colorKey]] ?? color`, so color follows the actual status value, never the array index.
- The legend maps the same `STATUS_COLORS` object, so graph and legend cannot diverge.
- `statusSeries` always contains all five statuses; zero-count bars render at zero height (opacity 0.2) and the legend entry remains.
- The chart uses a responsive `viewBox` with `h-auto w-full`; no animation behavior was removed.
- All five color values are present in the built JavaScript bundle.
- No fake orders or demo historical sales were added. The chart reads live counts from `/admin/overview` only.

## 8. Limitations

- SQLite is not PostgreSQL: concurrency, type parity, migration behavior and UTC timestamp round-trip remain unverified on the production database.
- Rate limiting is process-local; multi-worker enforcement is unverified and requires a shared store.
- Real microphone capture and Bengali/Hindi speech output were not exercised on hardware.
- Dependency advisory databases were not reachable; lockfile hygiene was checked, but vulnerability advisories were not scanned.
- No frontend unit/E2E framework is committed; browser checks rely on existing ad-hoc evidence.
- The 24 audit-logging gaps and 6 password-reset/change gaps are documented feature absences, not passing security tests.

## 9. Conclusion

Within the automated scope, the NextGenERP security catalog is fully green: **906/906 executed cases passed** and the complete backend suite is **972/972 green**. The remaining 94 cases are explicitly manual, blocked or documented gaps. Deployment readiness still depends on the PostgreSQL, multi-worker rate-limit, dependency-scan and real-device voice checks listed in `PRE_DEPLOYMENT_CHECKLIST.md`.

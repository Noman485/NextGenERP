"""Generate the NextGenERP test-case catalog.

The catalog is a planning and traceability artifact. It deliberately marks a
scenario as passed only when it was actually executed and the evidence is
recorded. Everything else is `not_run` or `blocked`.

Run from the repository root:
    python tests/generate_test_cases.py
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"

SCENARIOS: list[dict] = []
_SEEN_TITLES: set[str] = set()


def add(
    module: str,
    area: str,
    title: str,
    *,
    scenario_type: str = "API",
    priority: str = "P2",
    steps: list[str],
    expected: str,
    status: str = "not_run",
    blocked_reason: str | None = None,
    evidence: str | None = None,
    tags: list[str] | None = None,
) -> None:
    full_title = f"{area}: {title}"
    if full_title in _SEEN_TITLES:
        raise ValueError(f"Duplicate scenario title: {full_title}")
    _SEEN_TITLES.add(full_title)

    record = {
        "id": f"TC-{len(SCENARIOS) + 1:04d}",
        "module": module,
        "area": area,
        "title": full_title,
        "type": scenario_type,
        "priority": priority,
        "steps": steps,
        "expected": expected,
        "status": status,
        "tags": tags or [],
    }
    if blocked_reason:
        record["blocked_reason"] = blocked_reason
    if evidence:
        record["evidence"] = evidence
    SCENARIOS.append(record)


def render(template: str, values: dict) -> str:
    """Replace only the placeholders present in ``values``.

    Plain ``str.format`` would treat literal braces in endpoint text such as
    ``/products/{id}`` as placeholders. This keeps those intact.
    """
    for key, value in values.items():
        template = template.replace("{" + key + "}", str(value))
    return template


def family(
    module: str,
    area: str,
    variants: list,
    title: str,
    action: str,
    expected: str,
    *,
    scenario_type: str = "API",
    priority: str = "P2",
    status: str = "not_run",
    blocked_reason: str | None = None,
    evidence: str | None = None,
    tags: list[str] | None = None,
) -> None:
    for variant in variants:
        values = {"value": variant} if not isinstance(variant, dict) else variant
        variant_blocked_reason = values.get("blocked_reason", blocked_reason)
        variant_status = values.get(
            "status", "blocked" if variant_blocked_reason else status
        )
        variant_evidence = values.get("evidence", evidence)
        if scenario_type == "UI":
            steps = [
                "Sign in with a valid account and open the relevant screen.",
                f"Perform: {render(action, values)}",
                "Verify the visible result, keyboard/focus behavior, and the browser console.",
            ]
        else:
            steps = [
                "Prepare the stated data and authenticate unless the scenario tests authentication.",
                f"Execute: {render(action, values)}",
                "Inspect the status code, response body, and persisted database state.",
            ]
        add(
            module,
            area,
            render(title, values),
            scenario_type=scenario_type,
            priority=priority,
            steps=steps,
            expected=render(expected, values),
            status=variant_status,
            blocked_reason=variant_blocked_reason,
            evidence=variant_evidence,
            tags=tags,
        )


# ---------------------------------------------------------------------------
# Authentication (80)
# ---------------------------------------------------------------------------
AUTH = "Authentication"
family(
    AUTH,
    "Registration",
    [
        "abc", "user1", "user.name", "user_name", "user-name", "User.Mixed",
        "a1b2c3", "z9y8x7", "demo.user", "ops_team", "sales-team", "TestUser99",
    ],
    "register username '{value}'",
    "POST /auth/register with username '{value}' and a 12-character password",
    "201 Created, username stored in lowercase, and a bearer token returned.",
)
family(
    AUTH,
    "Registration",
    [
        "ab", "a" * 81, "user name", "user@name", "user/name", "user+name",
        "üser", "user!", "user#1", "", "   ", "user\tname",
    ],
    "reject invalid username '{value}'",
    "POST /auth/register with username '{value}'",
    "422 Unprocessable Entity with a validation message; no account is created.",
)
family(
    AUTH,
    "Registration",
    [
        {"label": "11-character password", "password": "x" * 11, "code": "422"},
        {"label": "12-character password", "password": "x" * 12, "code": "201"},
        {"label": "128-character password", "password": "x" * 128, "code": "201"},
        {"label": "129-character password", "password": "x" * 129, "code": "422"},
        {"label": "12 digits", "password": "123456789012", "code": "201"},
        {"label": "12 spaces", "password": " " * 12, "code": "201"},
        {"label": "12 unicode characters", "password": "पासवर्ड12345", "code": "201"},
        {"label": "empty password", "password": "", "code": "422"},
    ],
    "password boundary: {label}",
    "POST /auth/register with username 'boundary-user' and password '{password}'",
    "Response is {code}; the password is never returned or logged.",
)
family(
    AUTH,
    "Login",
    [
        "correct password", "wrong password", "unknown username", "uppercase username",
        "leading whitespace in username", "empty username", "empty password",
        "129-character password", "81-character username", "SQL injection string",
        "unicode username", "repeated failed login",
    ],
    "login scenario: {value}",
    "POST /auth/login using the described credential variant",
    "A valid credential pair returns 200 with a token; every invalid variant returns 401 or 422 without leaking which field failed.",
)
family(
    AUTH,
    "Tokens",
    [
        "missing Authorization header", "malformed Bearer prefix", "expired token",
        "invalid signature", "wrong algorithm", "tampered payload", "lowercase bearer",
        "extra spaces after Bearer", "empty token", "valid token", "token signed with another secret",
        "token for a deleted user",
    ],
    "token handling: {value}",
    "Call GET /auth/me with the described token variant",
    "Only a valid, unexpired token for an existing user returns 200; all other variants return 401 with WWW-Authenticate.",
)
family(
    AUTH,
    "Registration",
    [
        "duplicate username with identical case", "duplicate username with different case",
        "duplicate username containing a dot", "database commit failure during registration",
        "database query failure during login", "two concurrent registrations for the same username",
    ],
    "account conflict: {value}",
    "Perform the described registration or login action",
    "Conflicts return 409, database failures return 503, and no partial account is committed.",
)
family(
    AUTH,
    "Registration UI",
    [
        "valid form submission", "username shorter than 3 characters", "invalid username character",
        "password shorter than 12 characters", "duplicate username", "submit while request is in flight",
        "successful redirect into the app shell", "server error message is shown",
    ],
    "registration form: {value}",
    "Complete and submit the registration form with the described input",
    "The form prevents invalid submission or shows the API error, preserves entered values on failure, and redirects only on success.",
    scenario_type="UI",
)
family(
    AUTH,
    "Login UI",
    [
        {"label": "valid credentials sign in", "status": "passed"},
        {"label": "signed-in identity shows the username", "status": "passed"},
        {"label": "invalid credentials", "status": "not_run"},
        {"label": "empty fields", "status": "not_run"},
        {"label": "show and hide password", "status": "not_run"},
        {"label": "session expiry returns to login", "status": "not_run"},
        {"label": "sign out clears the session", "status": "not_run"},
        {"label": "back button after sign out", "status": "not_run"},
        {"label": "401 response clears the token", "status": "not_run"},
        {"label": "mobile login layout", "status": "not_run"},
    ],
    "{label}",
    "Use the login screen with the described state",
    "The screen renders the correct state, gives clear feedback, and never displays a hardcoded user identity.",
    scenario_type="UI",
)
# Apply the two executed login checks.
for scenario in SCENARIOS:
    if scenario["title"] == "Login UI: valid credentials sign in":
        scenario["status"] = "passed"
        scenario["evidence"] = "Puppeteer assistant-test.cjs, 2026-11-11: login and authenticated shell rendered."
    if scenario["title"] == "Login UI: signed-in identity shows the username":
        scenario["status"] = "passed"
        scenario["evidence"] = "Puppeteer assistant-test.cjs, 2026-11-11: identity showed demo438765052 and no hardcoded Ops Admin."


# ---------------------------------------------------------------------------
# Dashboard (60)
# ---------------------------------------------------------------------------
DASH = "Dashboard"
family(
    DASH,
    "KPI calculations",
    [
        "zero products", "one product", "many products", "zero stock", "low-stock boundary",
        "out-of-stock product", "units sum", "category count", "pending sales orders",
        "confirmed sales orders", "delivered sales orders", "pending purchase orders",
        "received purchase orders", "supplier count", "mixed statuses",
    ],
    "KPI calculation with {value}",
    "Load the dashboard and compare each KPI with the source collections",
    "Every KPI equals the value derived from the source collection; loading placeholders appear before data arrives.",
    scenario_type="UI",
)
family(
    DASH,
    "Low-stock boundaries",
    [
        "stock 0, reorder 0", "stock 1, reorder 0", "stock 1, reorder 1", "stock 1, reorder 2",
        "stock 5, reorder 5", "stock 6, reorder 5", "missing reorder level", "missing stock quantity",
        "very large stock value", "negative stock value",
    ],
    "low-stock boundary: {value}",
    "Render a product with the described stock and reorder values",
    "The product is classified exactly once as in stock, low stock, or out of stock according to the documented rules.",
    scenario_type="UI",
)
family(
    DASH,
    "Partial loading",
    [
        {"value": "products endpoint unavailable", "status": "not_run"},
        {"value": "categories endpoint unavailable", "status": "not_run"},
        {"value": "suppliers endpoint unavailable", "status": "not_run"},
        {"value": "sales orders endpoint unavailable", "status": "passed"},
        {"value": "purchase orders endpoint unavailable", "status": "not_run"},
    ],
    "{value}",
    "Abort the described endpoint and load the dashboard",
    "A banner names the failed section, successful sections keep live values, and the failed section shows an unavailable state instead of zero.",
    scenario_type="UI",
)
for scenario in SCENARIOS:
    if scenario["title"] == "Partial loading: sales orders endpoint unavailable":
        scenario["evidence"] = (
            "Puppeteer stabilization-check.cjs, 2026-11-11: orders aborted; products, categories, "
            "low-stock table and counts still rendered; sales cards showed Unavailable right now."
        )
family(
    DASH,
    "Empty states",
    [
        "no products", "no categories", "no suppliers", "no sales orders",
        "no purchase orders", "completely empty workspace",
    ],
    "empty dashboard: {value}",
    "Load the dashboard with the described empty collection",
    "The affected section shows a clear empty-state message and does not display misleading zeros.",
    scenario_type="UI",
)
family(
    DASH,
    "Refresh and retry",
    [
        "refresh success", "refresh failure retains existing data", "retry after a failed load",
        "double-click refresh", "initial load", "slow endpoint response",
    ],
    "dashboard refresh: {value}",
    "Trigger the described refresh or retry action",
    "The refresh control shows progress, duplicate requests are avoided, and previous data is not discarded on failure.",
    scenario_type="UI",
)
family(
    DASH,
    "Recent activity",
    [
        "no orders", "one order", "three orders", "more than three orders",
        "two records with equal IDs", "mixed sales and purchase statuses",
    ],
    "recent activity: {value}",
    "Render the recent activity lists with the described data",
    "The latest three records are shown per list in descending ID order with the correct status labels.",
    scenario_type="UI",
)
family(
    DASH,
    "3D snapshot",
    [
        "WebGL unavailable", "empty item list", "one item", "twelve items",
    ],
    "3D snapshot fallback: {value}",
    "Load the dashboard with the described 3D condition",
    "The dashboard remains usable, shows a fallback message when WebGL fails, and does not throw an uncaught error.",
    scenario_type="UI",
)
family(
    DASH,
    "Responsive and accessibility",
    [
        "desktop 1440px", "tablet 768px", "mobile 390px", "skip link focus",
        "heading order", "table header semantics", "status announcements", "reduced motion",
    ],
    "dashboard accessibility: {value}",
    "Inspect the dashboard under the described viewport or assistive condition",
    "Layout has no horizontal overflow, landmarks and headings are meaningful, and status changes are announced.",
    scenario_type="Accessibility",
)


# ---------------------------------------------------------------------------
# Products (100)
# ---------------------------------------------------------------------------
PRODUCTS = "Products"
family(
    PRODUCTS,
    "Create",
    [
        "minimal payload", "full payload", "zero opening stock", "reorder level zero",
        "large price", "decimal price", "unicode name", "100-character name",
        "50-character SKU", "stock equal to reorder level", "stock above reorder level",
        "category assigned", "no category", "price with two decimals", "maximum safe stock",
    ],
    "create product: {value}",
    "POST /products/ with the described valid payload",
    "200 OK, the product is persisted with normalized values, and opening stock creates one history row when non-zero.",
)
family(
    PRODUCTS,
    "Create validation",
    [
        "empty name", "whitespace-only name", "empty SKU", "duplicate SKU",
        "negative stock", "fractional stock", "negative reorder level", "fractional reorder level",
        "negative price", "zero price", "NaN price", "missing category",
        "very large stock", "missing name", "missing SKU",
    ],
    "reject product payload: {value}",
    "POST /products/ with the described invalid payload",
    "The request returns 400/404/422 as appropriate, no product is created, and stock history is unchanged.",
)
family(
    PRODUCTS,
    "Update",
    [
        "name", "SKU", "price", "stock increase", "stock decrease", "reorder level",
        "assign category", "clear category", "duplicate SKU", "missing product",
        "invalid stock value", "unchanged values",
    ],
    "update product: {value}",
    "PUT /products/{id} with the described change",
    "Valid changes persist, stock changes create an adjustment row, invalid changes are rejected, and missing IDs return 404.",
)
family(
    PRODUCTS,
    "Delete and relationships",
    [
        "no references", "referenced by a sales order", "referenced by a purchase order",
        "referenced by both order types", "nonexistent product", "double delete",
        "order cancelled but still referenced", "order delivered and still referenced",
        "product with stock", "product with category only",
    ],
    "delete product: {value}",
    "DELETE /products/{id} under the described relationship",
    "Unreferenced products are deleted; referenced products return 409; history remains intact.",
)
family(
    PRODUCTS,
    "Search, filter, sort",
    [
        "name search", "SKU search", "case-insensitive search", "no-match search",
        "clear search", "sort name ascending", "sort name descending", "sort stock ascending",
        "sort stock descending", "filter low stock", "filter out of stock", "combined filter",
    ],
    "product list interaction: {value}",
    "Use the described search, filter, or sort control",
    "The table updates to the correct subset and order, shows a no-match message, and clears back to the full list.",
    scenario_type="UI",
)
family(
    PRODUCTS,
    "Large data",
    [
        "0 products", "1 product", "10 products", "50 products", "100 products",
        "500 products", "last page boundary", "long list scrolling",
    ],
    "product list volume: {value}",
    "Load the product list with the described volume",
    "The page remains responsive, renders all expected rows or a documented page, and does not overflow horizontally.",
    scenario_type="UI",
)
family(
    PRODUCTS,
    "Stock adjustment",
    [
        "opening stock on create", "stock increase via update", "stock decrease via update",
        "same stock value", "stock set to zero", "fractional stock rejected",
        "negative stock rejected", "adjustment history row",
    ],
    "product stock adjustment: {value}",
    "Perform the described stock change through product create or update",
    "Stock is updated atomically and every change is recorded with previous and new values.",
)
family(
    PRODUCTS,
    "UI dialogs",
    [
        "add dialog opens", "add dialog closes", "edit dialog prefill", "delete confirm accepted",
        "delete confirm cancelled", "required field validation", "duplicate SKU error",
        "server error message", "saving state", "success feedback", "Escape closes dialog",
        "mobile dialog layout",
    ],
    "product dialog: {value}",
    "Open and operate the described product dialog",
    "Focus moves into the dialog, validation is announced, destructive actions require confirmation, and closing restores focus.",
    scenario_type="UI",
)
family(
    PRODUCTS,
    "API security",
    [
        "unauthenticated list", "unauthenticated create", "unauthenticated update",
        "unauthenticated delete", "invalid product ID", "malformed JSON",
        "database failure", "CORS preflight",
    ],
    "product API security: {value}",
    "Call the products API with the described condition",
    "Protected calls return 401, invalid input returns 4xx without a stack trace, and database failures return a safe error.",
)


# ---------------------------------------------------------------------------
# Categories (60)
# ---------------------------------------------------------------------------
CATEGORIES = "Categories"
family(
    CATEGORIES,
    "Create",
    [
        "simple name", "with description", "unicode name", "long name",
        "long description", "hyphenated name", "dot in name", "mixed case",
        "numeric name", "leading and trailing spaces",
    ],
    "create category: {value}",
    "POST /categories/ with the described valid name and description",
    "200 OK, the category is persisted, whitespace is trimmed, and the list reflects the new record.",
)
family(
    CATEGORIES,
    "Validation",
    [
        "empty name", "whitespace-only name", "duplicate exact name", "duplicate different case",
        "one-character name", "very long name", "special characters", "missing name",
        "malformed JSON", "database failure",
    ],
    "reject category: {value}",
    "POST /categories/ with the described invalid input",
    "Duplicates return 409, validation failures return 422, database failures return 503, and no category is created.",
)
family(
    CATEGORIES,
    "Update",
    [
        "name", "description", "clear description", "duplicate name",
        "missing category", "invalid name", "unchanged values", "case-only change",
    ],
    "update category: {value}",
    "PUT /categories/{id} with the described change",
    "Valid changes persist; duplicate names and invalid values are rejected; missing IDs return 404.",
)
family(
    CATEGORIES,
    "Delete and relationships",
    [
        "no products", "one product", "many products", "nonexistent category",
        "double delete", "after product moved to another category", "after product deleted",
        "database failure during delete",
    ],
    "delete category: {value}",
    "DELETE /categories/{id} under the described relationship",
    "Unreferenced categories are deleted; referenced categories return 409; failures are rolled back.",
)
family(
    CATEGORIES,
    "UI",
    [
        "list rendering", "empty state", "add dialog", "edit dialog", "delete confirmation",
        "cancel delete", "error message", "loading state", "search", "sort",
        "mobile layout", "keyboard navigation",
    ],
    "category UI: {value}",
    "Use the described category screen interaction",
    "The screen renders the correct state, actions are discoverable, and errors are announced without losing input.",
    scenario_type="UI",
)
family(
    CATEGORIES,
    "API security",
    [
        "unauthenticated list", "unauthenticated create", "unauthenticated update",
        "unauthenticated delete", "404 response", "409 response", "422 response",
        "500 response", "CORS preflight", "method not allowed", "trailing slash redirect",
        "malformed JSON",
    ],
    "category API security: {value}",
    "Call the categories API with the described condition",
    "The API returns the documented status and never exposes internals.",
)


# ---------------------------------------------------------------------------
# Suppliers (90)
# ---------------------------------------------------------------------------
SUPPLIERS = "Suppliers"
family(
    SUPPLIERS,
    "Create",
    [
        "minimal name", "full contact details", "zero lead time", "365-day lead time",
        "rating 0", "rating 5", "rating 4.5", "unicode name", "long name",
        "no email", "no phone", "no address", "hyphenated name", "numeric name",
        "leading and trailing spaces",
    ],
    "create supplier: {value}",
    "POST /suppliers/ with the described valid payload",
    "200 OK, the supplier is persisted, name whitespace is trimmed, and the list reflects the new record.",
)
family(
    SUPPLIERS,
    "Validation",
    [
        "empty name", "whitespace-only name", "negative lead time", "fractional lead time",
        "rating -0.1", "rating 5.1", "rating NaN", "rating infinity", "missing name",
        "very long name", "wrong type for lead time", "wrong type for rating",
        "malformed JSON", "null body", "extra unknown fields",
    ],
    "reject supplier: {value}",
    "POST /suppliers/ with the described invalid payload",
    "The request returns 422/400 without creating a supplier and without exposing a stack trace.",
)
family(
    SUPPLIERS,
    "Update",
    [
        "name", "email", "phone", "address", "lead time", "rating",
        "clear optional fields", "missing supplier", "invalid rating", "unchanged values",
    ],
    "update supplier: {value}",
    "PUT /suppliers/{id} with the described change",
    "Valid changes persist; invalid values are rejected; missing IDs return 404.",
)
family(
    SUPPLIERS,
    "Delete and relationships",
    [
        "no purchase orders", "one purchase order", "many purchase orders",
        "nonexistent supplier", "double delete", "after purchase order cancelled",
        "after purchase order received", "database failure", "delete with product only",
        "delete after purchase order deleted",
    ],
    "delete supplier: {value}",
    "DELETE /suppliers/{id} under the described relationship",
    "Unreferenced suppliers are deleted; referenced suppliers return 409; database failures return 503.",
)
family(
    SUPPLIERS,
    "Boundaries",
    [
        "lead time 0", "lead time 1", "lead time 30", "lead time 365", "lead time 366",
        "rating 0", "rating 0.1", "rating 4.999", "rating 5", "rating 5.0001",
    ],
    "supplier boundary: {value}",
    "Create or update a supplier with the described boundary value",
    "Values inside the accepted range persist; values outside it are rejected with 422.",
)
family(
    SUPPLIERS,
    "UI dialogs",
    [
        "add dialog opens", "edit dialog prefill", "delete confirmation", "cancel delete",
        "required name validation", "rating input", "lead-time input", "server error message",
        "saving state", "mobile layout",
    ],
    "supplier dialog: {value}",
    "Operate the described supplier dialog",
    "The dialog is accessible, preserves input on failure, and reports success or failure clearly.",
    scenario_type="UI",
)
family(
    SUPPLIERS,
    "API security",
    [
        "unauthenticated list", "unauthenticated create", "unauthenticated update",
        "unauthenticated delete", "404 response", "422 response", "409 response",
        "503 response", "CORS preflight", "malformed JSON",
    ],
    "supplier API security: {value}",
    "Call the suppliers API with the described condition",
    "The API returns the documented status and never exposes internals.",
)
family(
    SUPPLIERS,
    "Large list",
    [
        "0 suppliers", "1 supplier", "10 suppliers", "50 suppliers", "100 suppliers",
        "search by name", "search by email", "sort by name", "no-match search",
        "pagination boundary",
    ],
    "supplier list volume: {value}",
    "Load or search the supplier list with the described volume",
    "The list remains responsive, search is case-insensitive, and no-match states are clear.",
    scenario_type="UI",
)


# ---------------------------------------------------------------------------
# Inventory operations (110)
# ---------------------------------------------------------------------------
INVENTORY = "Inventory Operations"
family(
    INVENTORY,
    "Stock In",
    [
        "quantity 1", "quantity 5", "quantity 100", "quantity 1000", "maximum safe quantity",
        "short reason", "long reason", "unicode reason", "product with zero stock",
        "product with low stock", "product with high stock", "repeated stock in",
        "stock in after order deduction", "stock in after purchase receipt", "stock in with category",
    ],
    "stock in: {value}",
    "POST /inventory-transactions/ with transaction_type 'Stock In' and the described values",
    "Stock increases by the quantity, one history row is created, and previous/new values are correct.",
)
family(
    INVENTORY,
    "Stock Out",
    [
        "quantity 1", "exact available stock", "available stock minus one", "available stock plus one",
        "zero stock product", "negative quantity", "fractional quantity", "zero quantity",
        "very large quantity", "short reason", "missing product", "repeated stock out",
        "stock out after order deduction", "stock out after purchase receipt", "stock out with unicode reason",
    ],
    "stock out: {value}",
    "POST /inventory-transactions/ with transaction_type 'Stock Out' and the described values",
    "Valid stock-out decreases stock and records history; overdraw and invalid quantities are rejected without changing stock.",
)
family(
    INVENTORY,
    "Validation",
    [
        "missing product_id", "invalid transaction type", "lowercase transaction type",
        "empty reason", "whitespace-only reason", "missing quantity", "string quantity",
        "float quantity", "negative quantity", "zero quantity", "nonexistent product",
        "unauthenticated request", "malformed JSON", "extra unknown fields", "null body",
    ],
    "reject inventory transaction: {value}",
    "POST /inventory-transactions/ with the described invalid input",
    "The request returns 400/401/404/422 as appropriate and no stock or history row changes.",
)
family(
    INVENTORY,
    "History",
    [
        "empty history", "one row", "many rows", "descending order", "all response fields",
        "product name resolution", "date formatting", "mixed stock in and out",
        "unicode reason", "large history", "history after failed transaction",
        "history after product update",
    ],
    "inventory history: {value}",
    "Load GET /inventory-transactions/ under the described condition",
    "Rows are returned newest first with product names and accurate previous/new stock values.",
)
family(
    INVENTORY,
    "Concurrency",
    [
        "two stock-out requests for the same product",
        "two stock-in requests for the same product",
        "stock-out racing a sales order",
        "stock-out racing a cancellation restore",
        "purchase receipt racing a stock-out",
        "SQLite foreign-key and locking behavior",
        "PostgreSQL row lock behavior",
        "deadlock retry behavior",
    ],
    "concurrency: {value}",
    "Run the described concurrent operations against PostgreSQL",
    "Stock never goes negative, exactly one conflicting operation succeeds, and the transaction history is consistent.",
    blocked_reason="PostgreSQL runtime is not available in the current test environment; SQLite treats with_for_update() as a no-op.",
    tags=["postgres", "concurrency"],
)
family(
    INVENTORY,
    "UI",
    [
        {"value": "page renders inside the app shell without nested main", "status": "passed"},
        {"value": "stock history table renders rows", "status": "passed"},
        {"value": "no products available", "status": "not_run"},
        {"value": "one product available", "status": "not_run"},
        {"value": "many products available", "status": "not_run"},
        {"value": "product selector shows stock", "status": "not_run"},
        {"value": "low-stock indicator", "status": "not_run"},
        {"value": "type toggle", "status": "not_run"},
        {"value": "quantity input", "status": "not_run"},
        {"value": "reason input", "status": "not_run"},
        {"value": "submit disabled while saving", "status": "not_run"},
        {"value": "success message", "status": "not_run"},
        {"value": "error message", "status": "not_run"},
        {"value": "selected product summary", "status": "not_run"},
        {"value": "mobile layout and keyboard", "status": "not_run"},
    ],
    "{value}",
    "Use the Inventory Operations screen in the described state",
    "The form, snapshot, and history remain usable; validation is announced; the page does not nest a second main landmark.",
    scenario_type="UI",
)
for scenario in SCENARIOS:
    if scenario["title"] == "UI: page renders inside the app shell without nested main":
        scenario["evidence"] = "Puppeteer stabilization-check.cjs, 2026-11-11: exactly one main landmark; form, snapshot and history rendered."
    if scenario["title"] == "UI: stock history table renders rows":
        scenario["evidence"] = "Puppeteer stabilization-check.cjs, 2026-11-11: Stock History showed three seeded movements with product, type, quantity and stock values."
family(
    INVENTORY,
    "Refresh and errors",
    [
        "products endpoint fails", "transactions endpoint fails", "both endpoints fail",
        "retry after failure", "refresh success", "slow response", "unauthorized response",
        "server error", "network failure", "partial data",
    ],
    "inventory load failure: {value}",
    "Load the Inventory Operations screen under the described condition",
    "A retryable error is shown, the form remains visible, and successful data is not silently replaced with zeros.",
    scenario_type="UI",
)
family(
    INVENTORY,
    "Large history",
    [
        "10 rows", "50 rows", "100 rows", "500 rows", "1000 rows",
        "scrolling", "performance", "date formatting", "long reason", "many products",
    ],
    "inventory history volume: {value}",
    "Load the stock history with the described volume",
    "The table remains usable, dates are readable, and the page does not freeze or overflow.",
    scenario_type="UI",
)
family(
    INVENTORY,
    "Snapshot metrics",
    [
        "zero products", "one product", "many products", "units sum", "low-stock count boundary",
        "out-of-stock count", "loading state", "error state", "refresh updates metrics",
        "selected product summary",
    ],
    "inventory snapshot: {value}",
    "Inspect the stock snapshot under the described condition",
    "Products, units on hand, and low-stock counts match the catalog and update after a refresh.",
    scenario_type="UI",
)


# ---------------------------------------------------------------------------
# Sales orders (120)
# ---------------------------------------------------------------------------
SALES = "Sales Orders"
family(
    SALES,
    "Create",
    [
        "quantity 1", "quantity equal to stock", "quantity one below stock", "multiple products",
        "unicode customer name", "long customer name", "email present", "email absent",
        "zero-price product", "large total", "decimal total", "pending status",
        "stock deduction", "inventory history row", "order list refresh",
    ],
    "create sales order: {value}",
    "POST /orders/ with the described valid order",
    "200 OK, stock is reduced by the quantity, the order is Pending, and one stock-out history row is created.",
)
family(
    SALES,
    "Create validation",
    [
        "quantity 0", "quantity -1", "quantity 1.5", "quantity as string", "missing product",
        "nonexistent product", "insufficient stock", "empty customer name",
        "whitespace-only customer name", "missing customer name", "malformed email",
        "malformed JSON", "unauthenticated request", "null body", "extra unknown fields",
    ],
    "reject sales order: {value}",
    "POST /orders/ with the described invalid input",
    "The request returns 400/401/404/422 as appropriate and stock is unchanged.",
)
family(
    SALES,
    "Stock deduction",
    [
        "exact stock", "partial stock", "stock becomes zero", "concurrent last unit",
        "failed order leaves stock unchanged", "database error rollback", "two sequential orders",
        "cancel restores stock", "delivered order does not restore stock", "stock-out after order",
        "order for out-of-stock product", "order for low-stock product",
    ],
    "sales stock deduction: {value}",
    "Create or process the described sales order",
    "Stock changes exactly once per successful action and failed operations leave stock untouched.",
)
family(
    SALES,
    "Status transitions",
    [
        "Pending to Confirmed", "Confirmed to Shipped", "Shipped to Delivered",
        "Pending to Shipped", "Pending to Delivered", "Confirmed to Delivered",
        "Delivered to Cancelled", "Cancelled to Confirmed", "unknown status", "same status",
        "Pending to Cancelled", "Confirmed to Cancelled", "Shipped to Cancelled",
        "Delivered to Delivered", "lowercase status value",
    ],
    "sales status transition: {value}",
    "PUT /orders/{id}/status with the described transition",
    "Only the documented forward transitions and cancellations succeed; all others return 400.",
)
family(
    SALES,
    "Cancellation",
    [
        "cancel pending", "cancel confirmed", "cancel shipped", "cancel delivered",
        "cancel already cancelled", "stock restored once", "history row created",
        "cancellation reason", "concurrent cancellation", "cancel after stock-out",
        "cancel after product delete attempt", "cancel then delete",
    ],
    "sales cancellation: {value}",
    "PUT /orders/{id}/status with status Cancelled under the described condition",
    "Cancellable orders restore reserved stock exactly once; final states remain final.",
)
family(
    SALES,
    "Update customer",
    [
        "name", "email", "trim whitespace", "blank name", "clear email",
        "missing order", "invalid payload", "unicode name", "long name", "unchanged values",
    ],
    "update sales order: {value}",
    "PUT /orders/{id} with the described customer change",
    "Valid changes persist with trimmed values; blank names are rejected; missing IDs return 404.",
)
family(
    SALES,
    "Delete restrictions",
    [
        "delete pending order", "delete confirmed order", "delete shipped order",
        "delete delivered order", "delete cancelled order", "nonexistent order",
        "double delete", "database error during delete",
    ],
    "delete sales order: {value}",
    "DELETE /orders/{id} in the described state",
    "Sales order history cannot be deleted; the API returns 409 for existing orders and 404 for missing ones.",
)
family(
    SALES,
    "UI",
    [
        "empty list", "list rendering", "status filter", "search customer", "search product",
        "sort order", "pagination", "create dialog", "edit dialog", "status control",
        "cancel confirmation", "error message", "loading state", "mobile layout",
        "keyboard navigation",
    ],
    "sales order UI: {value}",
    "Use the described Sales Orders screen interaction",
    "The list and controls reflect live data, destructive actions are confirmed, and errors are announced.",
    scenario_type="UI",
)
family(
    SALES,
    "API security",
    [
        "unauthenticated list", "unauthenticated create", "unauthenticated update",
        "unauthenticated status change", "unauthenticated delete", "404 response",
        "422 response", "400 response", "409 response", "500 response",
    ],
    "sales API security: {value}",
    "Call the sales orders API with the described condition",
    "Protected calls return 401, invalid input returns 4xx, and internals are never exposed.",
)
family(
    SALES,
    "Concurrency",
    [
        "two orders for the last unit",
        "cancel racing ship",
        "two status updates for the same order",
        "delete racing create",
        "stock-out racing order creation",
        "two simultaneous cancellations",
        "two simultaneous customer updates",
        "database lock contention",
    ],
    "sales concurrency: {value}",
    "Run the described concurrent sales operations against PostgreSQL",
    "Stock never goes negative, only one conflicting transition wins, and history remains consistent.",
    blocked_reason="PostgreSQL runtime is not available in the current test environment; SQLite serializes writes differently.",
    tags=["postgres", "concurrency"],
)


# ---------------------------------------------------------------------------
# Purchase orders (120)
# ---------------------------------------------------------------------------
PURCHASE = "Purchase Orders"
family(
    PURCHASE,
    "Create",
    [
        "quantity 1", "quantity 10", "quantity 1000", "unit price 0", "decimal unit price",
        "large total", "supplier and product pair", "pending status", "total amount calculation",
        "unicode supplier name", "long supplier name", "product with zero stock",
        "product with high stock", "no category", "list refresh",
    ],
    "create purchase order: {value}",
    "POST /purchase-orders/ with the described valid order",
    "200 OK, the order is Pending, the total equals quantity times unit price, and stock is unchanged.",
)
family(
    PURCHASE,
    "Create validation",
    [
        "quantity 0", "quantity -1", "quantity 1.5", "quantity as string", "missing supplier",
        "nonexistent supplier", "missing product", "nonexistent product", "negative unit price",
        "NaN unit price", "missing quantity", "malformed JSON", "unauthenticated request",
        "null body", "extra unknown fields",
    ],
    "reject purchase order: {value}",
    "POST /purchase-orders/ with the described invalid input",
    "The request returns 400/401/404/422 as appropriate and no order is created.",
)
family(
    PURCHASE,
    "Status transitions",
    [
        "Pending to Approved", "Approved to Ordered", "Ordered to Received",
        "Approved to Received", "Pending to Received", "Pending to Ordered",
        "Ordered to Approved", "Received to Cancelled", "Cancelled to Approved",
        "unknown status", "same status", "Pending to Cancelled", "Approved to Cancelled",
        "Ordered to Cancelled", "lowercase status value",
    ],
    "purchase status transition: {value}",
    "PUT /purchase-orders/{id}/status with the described transition",
    "Only documented transitions succeed; invalid jumps and final-state changes return 400.",
)
family(
    PURCHASE,
    "Receiving",
    [
        "receive once adds stock", "receive twice does not double-add", "Approved to Received",
        "Ordered to Received", "Pending to Received", "history row created",
        "receiving reason", "stock levels after receive", "missing product",
        "missing supplier", "database error", "concurrent receive",
    ],
    "purchase receiving: {value}",
    "Mark the described purchase order as Received",
    "Stock increases by the ordered quantity exactly once and a stock-in history row is recorded.",
)
family(
    PURCHASE,
    "Cancellation and delete",
    [
        "cancel pending", "cancel approved", "cancel ordered", "cancel received",
        "cancel already cancelled", "delete pending", "delete approved", "delete ordered",
        "delete received", "delete cancelled", "nonexistent order", "database error",
    ],
    "purchase cancellation or delete: {value}",
    "Perform the described cancellation or deletion",
    "Unreceived orders can be cancelled or deleted; received orders are protected; missing IDs return 404.",
)
family(
    PURCHASE,
    "UI",
    [
        "empty list", "list rendering", "status filter", "search supplier", "search product",
        "sort order", "pagination", "create dialog", "status control", "receive confirmation",
        "cancel confirmation", "error message", "loading state", "mobile layout",
        "keyboard navigation",
    ],
    "purchase order UI: {value}",
    "Use the described Purchase Orders screen interaction",
    "The list and controls reflect live data, receiving is confirmed, and errors are announced.",
    scenario_type="UI",
)
family(
    PURCHASE,
    "API security",
    [
        "unauthenticated list", "unauthenticated create", "unauthenticated status change",
        "unauthenticated delete", "404 response", "422 response", "400 response",
        "409 response", "500 response", "CORS preflight", "malformed JSON",
        "method not allowed",
    ],
    "purchase API security: {value}",
    "Call the purchase orders API with the described condition",
    "Protected calls return 401, invalid input returns 4xx, and internals are never exposed.",
)
family(
    PURCHASE,
    "Relationships",
    [
        "delete supplier with purchase order", "delete product with purchase order",
        "supplier missing", "product missing", "multiple orders for one supplier",
        "multiple products for one supplier", "supplier lead time used in planning",
        "unit price differs from product price", "delete supplier after receive",
        "delete supplier after cancellation", "delete product after cancellation",
        "delete product after receive",
    ],
    "purchase relationship: {value}",
    "Perform the described relationship action",
    "Referenced suppliers and products cannot be deleted; historical orders remain readable.",
)
family(
    PURCHASE,
    "Concurrency",
    [
        "two receive requests for the same order",
        "receive racing cancel",
        "approve racing receive",
        "delete racing receive",
        "stock-out racing receive",
        "two purchase orders for the same product",
        "database lock contention",
        "deadlock retry",
        "receive racing product update",
        "cancel racing status update",
        "two simultaneous deletes",
        "two simultaneous creates",
    ],
    "purchase concurrency: {value}",
    "Run the described concurrent purchase operations against PostgreSQL",
    "Stock is added at most once, conflicting transitions fail cleanly, and no partial order state remains.",
    blocked_reason="PostgreSQL runtime is not available in the current test environment; SQLite serializes writes differently.",
    tags=["postgres", "concurrency"],
)


# ---------------------------------------------------------------------------
# Forecasting (80)
# ---------------------------------------------------------------------------
FORECAST = "Demand Forecast"
family(
    FORECAST,
    "Data display",
    [
        "7-day outlook", "product list", "forecast values", "reorder suggestions",
        "urgent items", "empty forecast", "one product", "many products",
        "loading state", "error state", "refresh", "stale data",
    ],
    "forecast display: {value}",
    "Open the Demand Forecast page under the described condition",
    "The page shows the expected forecast and reorder data with clear loading, empty, and error states.",
    scenario_type="UI",
)
family(
    FORECAST,
    "Reorder logic",
    [
        "stock 0", "stock below reorder level", "stock at reorder level", "stock above reorder level",
        "lead time 0", "lead time 1", "lead time 7", "lead time 30", "safety stock",
        "high demand", "low demand", "supplier missing", "reorder quantity 0",
        "negative available stock", "very large demand",
    ],
    "reorder calculation: {value}",
    "Inspect the suggested reorder quantity for the described inputs",
    "The suggestion follows the documented demand, lead-time, safety-stock, and current-stock formula.",
)
family(
    FORECAST,
    "Filters",
    [
        "All filter", "Needs reorder filter", "no matching rows", "clear filter",
        "count badge", "mobile filter layout", "keyboard filter use", "filter after refresh",
    ],
    "forecast filter: {value}",
    "Use the described forecast filter",
    "The table shows the correct subset and the count badge matches the visible rows.",
    scenario_type="UI",
)
family(
    FORECAST,
    "Refresh and errors",
    [
        "refresh success", "refresh failure retains data", "retry after failure", "slow response",
        "500 response", "network failure", "unauthorized response", "empty response",
    ],
    "forecast refresh: {value}",
    "Trigger the described forecast load or refresh",
    "The page remains usable, previous data is retained on failure, and retry is available.",
    scenario_type="UI",
)
family(
    FORECAST,
    "Model integrity",
    [
        "model file unchanged", "dataset unchanged", "reported metrics unchanged",
        "no retraining during request", "single forecast generation per request",
        "deterministic output for identical input", "no database writes during forecast",
        "model load failure", "missing model file", "model version recorded",
    ],
    "frozen model check: {value}",
    "Inspect or exercise the forecast under the described model condition",
    "The frozen XGBoost model, dataset, and metrics are unchanged; a request does not retrain or mutate the model.",
    tags=["ml", "regression"],
)
family(
    FORECAST,
    "ERP overlay",
    [
        "exact product-name match", "case-insensitive match", "leading/trailing whitespace",
        "SKU-only match", "duplicate ERP product names", "no ERP match fallback",
        "ERP stock 0", "ERP reorder level applied", "category assigned", "product deleted after forecast",
    ],
    "ERP overlay: {value}",
    "Compare forecast recommendations with the ERP catalog for the described match",
    "Matching is case-insensitive, live ERP stock overrides fallback stock, and unmatched products use the bundled snapshot.",
)
family(
    FORECAST,
    "3D chart",
    [
        "WebGL unavailable", "empty data", "one data point", "many data points",
        "window resize", "mobile viewport", "reduced motion",
    ],
    "forecast 3D fallback: {value}",
    "Load the forecast chart under the described condition",
    "The page remains usable and shows a fallback or correctly sized chart without uncaught errors.",
    scenario_type="UI",
)
family(
    FORECAST,
    "Accessibility and responsive",
    [
        "desktop 1440px", "tablet 768px", "mobile 390px", "table semantics",
        "heading order", "status announcements", "keyboard navigation", "color contrast",
        "chart alternative text", "reduced motion",
    ],
    "forecast accessibility: {value}",
    "Inspect the forecast page under the described viewport or assistive condition",
    "The page has no horizontal overflow, meaningful headings, accessible table/chart alternatives, and announced loading states.",
    scenario_type="Accessibility",
)


# ---------------------------------------------------------------------------
# Assistant (80)
# ---------------------------------------------------------------------------
ASSISTANT = "NextGenERP Assistant"
family(
    ASSISTANT,
    "Allowed scope",
    [
        "low stock", "pending sales orders", "pending purchase orders", "product stock",
        "supplier details", "reorder needs", "navigation help",
        "add product help", "forecast help", "login help",
    ],
    "answer allowed topic: {value}",
    "POST /assistant/chat with the described NextGenERP question",
    "200 OK with a project-specific answer, suggestions, and mode 'local' when no provider is configured.",
)
family(
    ASSISTANT,
    "Refused scope",
    [
        "cricket result", "weather forecast", "world news", "coding question",
        "medical question", "legal question", "personal advice", "math problem",
        "general knowledge", "prompt injection",
    ],
    "refuse off-topic topic: {value}",
    "POST /assistant/chat with the described off-topic request",
    "The reply refuses the topic before any LLM call and redirects to NextGenERP examples.",
)
family(
    ASSISTANT,
    "Live data answers",
    [
        "low-stock boundary", "out-of-stock list", "no low-stock items", "product by name",
        "product by SKU", "supplier details", "sales order lookup", "purchase order lookup",
        "catalog counts", "empty database", "many products", "unicode product name",
    ],
    "live-data answer: {value}",
    "Ask the described question against the current workspace snapshot",
    "The answer uses live data, respects list caps, and never invents records.",
)
family(
    ASSISTANT,
    "Help topics",
    [
        "add product", "edit or delete product", "record stock movement", "create sales order",
        "create purchase order", "read demand forecast", "delete rules", "common errors",
    ],
    "help topic: {value}",
    "Ask the described how-to question",
    "The answer names the correct page and steps, stays concise, and does not claim to perform the action.",
)
family(
    ASSISTANT,
    "LLM external provider",
    [
        "provider success", "provider timeout", "provider 401", "provider 429",
        "custom base URL",
    ],
    "external provider: {value}",
    "Configure an OpenAI-compatible provider and trigger the described condition",
    "Successful calls return mode 'llm'; failures fall back to the local answer without exposing the key.",
    blocked_reason="No external provider key is configured in this environment; the local fallback path is tested instead.",
    tags=["llm", "external"],
)
family(
    ASSISTANT,
    "LLM local fallback",
    [
        "no key configured", "provider request failure",
        "key never returned in response", "strict scope prompt sent",
    ],
    "local LLM behavior: {value}",
    "Exercise the assistant with the described provider configuration",
    "The assistant uses local mode, includes the strict scope prompt when a provider is called, and never leaks secrets.",
)
family(
    ASSISTANT,
    "UI",
    [
        {
            "value": "launcher is visible",
            "status": "passed",
            "evidence": "Puppeteer assistant-test.cjs, 2026-11-11: launcher visible on desktop and mobile.",
        },
        {
            "value": "panel opens",
            "status": "passed",
            "evidence": "Puppeteer assistant-test.cjs, 2026-11-11: panel opened from the launcher.",
        },
        {
            "value": "panel closes",
            "status": "passed",
            "evidence": "Puppeteer assistant-test.cjs, 2026-11-11: close button removed the panel.",
        },
        {
            "value": "low-stock suggestion returns live answer",
            "status": "passed",
            "evidence": "Puppeteer assistant-test.cjs, 2026-11-11: low-stock reply contained live DEMO- products.",
        },
        {
            "value": "help suggestion returns steps",
            "status": "passed",
            "evidence": "Puppeteer assistant-test.cjs, 2026-11-11: add-product help returned step-by-step instructions.",
        },
        {
            "value": "off-topic question is refused",
            "status": "passed",
            "evidence": "Puppeteer assistant-test.cjs, 2026-11-11: off-topic request returned the scope refusal.",
        },
        {
            "value": "mobile panel fits viewport",
            "status": "passed",
            "evidence": "Puppeteer assistant-test.cjs, 2026-11-11: 390 px viewport, panel inside the viewport, zero horizontal overflow.",
        },
        {
            "value": "Escape closes panel",
            "status": "passed",
            "evidence": "Puppeteer assistant-test.cjs, 2026-11-11: Escape removed the panel.",
        },
    ],
    "{value}",
    "Use the assistant panel in the described state",
    "The panel is accessible, keeps the conversation, handles errors, and fits desktop and mobile layouts.",
    scenario_type="UI",
)
family(
    ASSISTANT,
    "Localization",
    [
        {
            "value": "Hindi greeting returns a localized intro and suggestions",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: test_assistant_localizes_greeting_and_suggestions returned language=hi with a Devanagari intro and suggestions.",
        },
        {
            "value": "Bengali greeting returns a localized intro and suggestions",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: same test returned language=bn with a Bengali intro and suggestions.",
        },
        {
            "value": "Devanagari combining-mark greeting is recognized",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: 'नमस्ते' returned the intro after _is_greeting preserved U+0900-U+097F combining marks.",
        },
        {
            "value": "Hindi live low-stock answer is localized",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: test_assistant_localizes_live_low_stock_answers returned a Devanagari reply containing the live Hindi Widget record.",
        },
        {
            "value": "Bengali live low-stock answer is localized",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: same test returned a Bengali reply containing the live Hindi Widget record.",
        },
        {
            "value": "localized help topic answer",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: test_assistant_localizes_help_and_scope_refusal returned Hindi and Bengali add-product steps with SKU guidance.",
        },
        {
            "value": "localized scope refusal in Hindi and Bengali",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: Hindi refusal contained 'केवल NextGenERP'; Bengali refusal contained 'শুধু NextGenERP'.",
        },
        {
            "value": "unsupported language code is rejected",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: test_assistant_rejects_unsupported_language returned 422 for language=fr.",
        },
        {
            "value": "LLM receives an explicit language instruction",
            "status": "passed",
            "evidence": "pytest backend/tests/test_assistant.py, 2026-11-11: mocked provider payload contained 'Hindi using Devanagari script'; response mode=llm, language=hi.",
        },
    ],
    "{value}",
    "Send the described message to /assistant/chat with the stated language code",
    "The reply, suggestions and status labels use the selected language; the response echoes the language.",
)
family(
    ASSISTANT,
    "Voice UI",
    [
        {
            "value": "language selector lists English, Hindi and Bengali",
            "status": "passed",
            "evidence": "Puppeteer assistant-voice-test.cjs, 2026-11-11: options were en/English, hi/हिन्दी and bn/বাংলা.",
        },
        {
            "value": "language switch updates welcome and suggestions",
            "status": "passed",
            "evidence": "Puppeteer assistant-voice-test.cjs, 2026-11-11: Hindi and Bengali welcome text and suggestion chips appeared after switching; the launcher kept the Bengali label after close.",
        },
        {
            "value": "microphone control is enabled when supported",
            "status": "passed",
            "evidence": "Puppeteer assistant-voice-test.cjs, 2026-11-11: headless Edge reported recognition=true and the mic button was enabled; actual audio capture was not exercised.",
        },
        {
            "value": "speaker play/stop and auto-speak toggle",
            "status": "passed",
            "evidence": "Puppeteer assistant-voice-test.cjs, 2026-11-11: auto-speak toggled on/off and the speaker button changed to the stop state; no console errors.",
        },
        {
            "value": "actual microphone capture and permission grant",
            "status": "blocked",
            "blocked_reason": "Headless Edge cannot grant a real microphone permission or provide audio input; only the controls and error paths were verified.",
        },
        {
            "value": "cross-browser voice support",
            "status": "blocked",
            "blocked_reason": "Only headless Microsoft Edge is available; Firefox and Safari Web Speech behavior is not tested.",
        },
    ],
    "{value}",
    "Use the assistant panel with the described voice or language control",
    "The panel exposes voice controls only when the browser supports them and keeps the selected language across the conversation.",
    scenario_type="UI",
)
family(
    ASSISTANT,
    "Security and privacy",
    [
        "authentication required", "blank message rejected", "oversized message rejected",
        "over-long history rejected", "no secrets in response",
        "off-topic refusal before provider call", "read-only claims", "XSS in user message",
    ],
    "assistant security: {value}",
    "Send the described request to /assistant/chat",
    "The endpoint enforces authentication and limits, refuses out-of-scope requests, and never leaks secrets.",
)


# ---------------------------------------------------------------------------
# Navigation and UI shell (50)
# ---------------------------------------------------------------------------
NAV = "Navigation and UI"
family(
    NAV,
    "Routes",
    [
        "/", "/forecasting", "/products", "/categories", "/suppliers",
        "/sales-orders", "/purchase-orders", "/inventory-operations", "/auth", "unknown route",
    ],
    "route: {value}",
    "Navigate directly to the described route",
    "The correct page renders inside the shell; protected routes require a session; unknown routes show the 404 page.",
    scenario_type="UI",
)
family(
    NAV,
    "Sidebar and mobile",
    [
        "desktop sidebar", "mobile menu opens", "mobile menu closes", "overlay click closes",
        "active route state", "sign out", "identity display", "logo link",
    ],
    "shell navigation: {value}",
    "Use the described navigation control",
    "Navigation is keyboard-accessible, active state is clear, and the mobile drawer closes without trapping focus.",
    scenario_type="UI",
)
family(
    NAV,
    "Search jump",
    [
        "exact page name", "keyword 'stock'", "keyword 'vendors'", "case-insensitive match",
        "no-match feedback", "clear feedback", "Enter submits", "mobile hides search",
    ],
    "module search: {value}",
    "Use the header Jump to module search with the described input",
    "The matching page opens, no-match feedback is visible, and the search field remains accessible.",
    scenario_type="UI",
)
family(
    NAV,
    "404 and error boundary",
    [
        {"value": "unknown route shows Page not found", "status": "passed"},
        {"value": "nested unknown route", "status": "not_run"},
        {"value": "ErrorBoundary fallback", "status": "not_run"},
        {"value": "ErrorBoundary resets on navigation", "status": "not_run"},
        {"value": "browser back button", "status": "not_run"},
        {"value": "direct load of unknown route", "status": "not_run"},
    ],
    "{value}",
    "Navigate to the described route or trigger the described boundary",
    "A clear not-found or error screen appears with a way back, and the shell does not crash.",
    scenario_type="UI",
)
for scenario in SCENARIOS:
    if scenario["title"] == "404 and error boundary: unknown route shows Page not found":
        scenario["evidence"] = "Puppeteer assistant-test.cjs, 2026-11-11: /does-not-exist rendered Page not found."
family(
    NAV,
    "Accessibility",
    [
        "skip link", "focus visible", "heading order", "landmarks", "form labels",
        "table headers", "aria-live announcements", "color contrast", "keyboard dialogs",
        "reduced motion",
    ],
    "shell accessibility: {value}",
    "Inspect the described accessibility behavior across the app shell",
    "The app is keyboard-operable, has one main landmark, visible focus, meaningful labels, and announced status changes.",
    scenario_type="Accessibility",
)
family(
    NAV,
    "Responsive",
    [
        "320px width", "390px width", "768px width", "1024px width",
        "1440px width", "1920px width", "landscape phone", "200% zoom",
    ],
    "responsive layout: {value}",
    "Inspect the app shell at the described viewport or zoom",
    "No horizontal overflow occurs, navigation remains reachable, and content is readable.",
    scenario_type="Accessibility",
)


# ---------------------------------------------------------------------------
# Security and API (50)
# ---------------------------------------------------------------------------
SECURITY = "Security and API"
family(
    SECURITY,
    "Authentication required",
    [
        "GET /products/", "POST /products/", "GET /categories/", "POST /categories/",
        "GET /suppliers/", "POST /suppliers/", "GET /orders/", "POST /orders/",
        "GET /purchase-orders/", "GET /inventory-transactions/", "GET /ml/insights",
        "POST /assistant/chat",
    ],
    "unauthenticated access: {value}",
    "Call the described protected endpoint without a token",
    "401 Unauthorized with WWW-Authenticate and no business data in the body.",
)
family(
    SECURITY,
    "Input validation",
    [
        "SQL injection in username", "SQL injection in product name", "SQL injection in search",
        "SQL injection in customer name", "SQL injection in supplier name",
        "SQL injection in category name", "SQL injection in inventory reason",
        "script tag in assistant message", "deeply nested JSON", "oversized query parameter",
    ],
    "input attack: {value}",
    "Send the described malicious or malformed input",
    "Input is validated or safely parameterized; no SQL executes, no script runs, and no stack trace is returned.",
)
family(
    SECURITY,
    "CORS",
    [
        "allowed origin", "disallowed origin", "wildcard configuration rejected",
        "preflight request", "credentials disabled", "allowed headers",
    ],
    "CORS behavior: {value}",
    "Send the described cross-origin request",
    "Only explicit configured origins are allowed; wildcard configuration prevents startup.",
)
family(
    SECURITY,
    "Secrets and logging",
    [
        "JWT secret absent from responses", "password absent from logs",
        "assistant key absent from logs", "database URL absent from responses",
        "stack trace absent from 500 responses", "token absent from URLs",
        ".env ignored by git", "sensitive docs skipped by retrieval",
    ],
    "secret handling: {value}",
    "Inspect responses, logs, repository status, and assistant context",
    "No secret, token, password, or connection string is exposed to the browser or logs.",
)
family(
    SECURITY,
    "XSS and injection",
    [
        "script tag in product name", "script tag in category name", "script tag in supplier name",
        "script tag in customer name", "script tag in assistant reply", "script tag in reason",
        "stored XSS rendering", "missing Content-Security-Policy",
    ],
    "XSS defense: {value}",
    "Store or render the described payload and inspect the DOM",
    "React escapes rendered text; no script executes; the missing CSP is recorded as a hardening gap.",
)
family(
    SECURITY,
    "Rate limiting",
    [
        "login brute force", "assistant abuse", "registration spam",
        "API burst", "LLM cost abuse", "429 response behavior",
    ],
    "rate limiting: {value}",
    "Send the described repeated requests",
    "The endpoint returns 429 after a documented threshold and does not allow unlimited credential or LLM abuse.",
    blocked_reason="Rate limiting is not implemented in this build; the scenario is blocked until the control exists.",
    tags=["security", "not-implemented"],
)


# ---------------------------------------------------------------------------
# Validation and output
# ---------------------------------------------------------------------------
EXPECTED_COUNTS = {
    "Authentication": 80,
    "Dashboard": 60,
    "Products": 100,
    "Categories": 60,
    "Suppliers": 90,
    "Inventory Operations": 110,
    "Sales Orders": 120,
    "Purchase Orders": 120,
    "Demand Forecast": 80,
    "NextGenERP Assistant": 80,
    "Navigation and UI": 50,
    "Security and API": 50,
}

actual_counts = Counter(scenario["module"] for scenario in SCENARIOS)
if actual_counts != Counter(EXPECTED_COUNTS):
    raise SystemExit(f"Module counts do not match: {dict(actual_counts)}")
if len(SCENARIOS) != 1000:
    raise SystemExit(f"Expected 1000 scenarios, got {len(SCENARIOS)}")

status_counts = Counter(scenario["status"] for scenario in SCENARIOS)
for scenario in SCENARIOS:
    if scenario["status"] == "blocked" and "blocked_reason" not in scenario:
        raise SystemExit(f"Blocked scenario without reason: {scenario['id']}")
    if scenario["status"] == "passed" and "evidence" not in scenario:
        raise SystemExit(f"Passed scenario without evidence: {scenario['id']}")

TESTS_DIR.mkdir(exist_ok=True)
(TESTS_DIR / "test_cases.json").write_text(
    json.dumps(
        {
            "generated": date.today().isoformat(),
            "project": "NextGenERP",
            "total": len(SCENARIOS),
            "status_counts": dict(status_counts),
            "scenarios": SCENARIOS,
        },
        indent=2,
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)

# Catalog grouped by module and area.
lines = [
    "# NextGenERP Test Case Catalog",
    "",
    f"Generated: {date.today().isoformat()}",
    "",
    f"Total scenarios: **{len(SCENARIOS)}**",
    "",
    "Status values:",
    "",
    "- `passed` — executed and verified; evidence is recorded in `test_cases.json`.",
    "- `not_run` — defined but not yet executed.",
    "- `blocked` — cannot be executed in the current environment; the reason is recorded.",
    "",
    "> This catalog is a planning artifact. A scenario is not marked passed unless it was actually executed.",
    "",
    "## Summary",
    "",
    "| Module | Scenarios | Passed | Not run | Blocked |",
    "| --- | ---: | ---: | ---: | ---: |",
]
for module, count in EXPECTED_COUNTS.items():
    module_scenarios = [s for s in SCENARIOS if s["module"] == module]
    module_status = Counter(s["status"] for s in module_scenarios)
    lines.append(
        f"| {module} | {count} | {module_status['passed']} | "
        f"{module_status['not_run']} | {module_status['blocked']} |"
    )
lines.extend(
    [
        f"| **Total** | **{len(SCENARIOS)}** | **{status_counts['passed']}** | "
        f"**{status_counts['not_run']}** | **{status_counts['blocked']}** |",
        "",
    ]
)

for module in EXPECTED_COUNTS:
    module_scenarios = [s for s in SCENARIOS if s["module"] == module]
    lines.extend([f"## {module}", ""])
    areas = defaultdict(list)
    for scenario in module_scenarios:
        areas[scenario["area"]].append(scenario)
    for area, area_scenarios in areas.items():
        lines.extend([f"### {area}", "", "| ID | Scenario | Type | Priority | Status |", "| --- | --- | --- | --- | --- |"])
        for scenario in area_scenarios:
            lines.append(
                f"| {scenario['id']} | {scenario['title']} | {scenario['type']} | "
                f"{scenario['priority']} | {scenario['status']} |"
            )
        lines.append("")

(TESTS_DIR / "TEST_CASE_CATALOG.md").write_text("\n".join(lines), encoding="utf-8")

report_lines = [
    "# NextGenERP Test Execution Report",
    "",
    f"Date: {date.today().isoformat()}",
    "",
    "## Executive summary",
    "",
    f"- Catalog scenarios: **{len(SCENARIOS)}**",
    f"- Executed and passed: **{status_counts['passed']}**",
    f"- Not yet executed: **{status_counts['not_run']}**",
    f"- Blocked: **{status_counts['blocked']}**",
    "- Automated backend suite: **48 passed** (1 third-party deprecation warning).",
    "- Frontend production build: **passed**; one chunk-size warning for the lazy Three.js bundle.",
    "- Assistant browser flow: **passed** on desktop and mobile with no console errors.",
    "- Assistant voice/language flow: **passed** in headless Edge for the three language options, mic control, auto-speak, localized Hindi/Bengali answers, Bengali refusal, speaker state and mobile layout; real microphone capture remains blocked.",
    "- Dashboard partial-failure check: **passed**; an aborted sales-orders request did not blank the other sections.",
    "- Inventory Operations browser check: **passed**; one main landmark, form, snapshot, and history rendered.",
    "",
    "## Commands actually run",
    "",
    "```powershell",
    "cd backend",
    ".\\venv\\Scripts\\python.exe -m pytest -q",
    "# 48 passed, 1 warning",
    "",
    "cd ..\\frontend",
    "npm run build",
    "# built successfully; three.module chunk is 694.91 kB",
    "```",
    "",
    "Browser checks used Puppeteer with Microsoft Edge against `http://localhost:5173` and the live backend on `http://127.0.0.1:8000`.",
    "The assistant voice/language script also checked the three language options, mic control state, auto-speak, localized live answers, refusal, speaker state and mobile layout.",
    "",
    "## Executed scenarios",
    "",
    "| ID | Scenario | Evidence |",
    "| --- | --- | --- |",
]
for scenario in SCENARIOS:
    if scenario["status"] == "passed":
        report_lines.append(
            f"| {scenario['id']} | {scenario['title']} | {scenario['evidence']} |"
        )
report_lines.extend(
    [
        "",
        "## Blocked scenarios",
        "",
        "| Count | Area | Reason |",
        "| ---: | --- | --- |",
    ]
)
blocked_by_reason = Counter(
    (s["module"], s["area"], s["blocked_reason"])
    for s in SCENARIOS
    if s["status"] == "blocked"
)
for (module, area, reason), count in blocked_by_reason.items():
    report_lines.append(f"| {count} | {module} / {area} | {reason} |")
report_lines.extend(
    [
        "",
        "## Honest status notes",
        "",
        "- The 1000 scenarios are distinct test intents, not 1000 automated tests. Only the rows marked `passed` were executed.",
        "- The backend suite covers 48 tests; it is not mapped one-to-one to catalog IDs, so no bulk pass status was inferred.",
        "- `blocked` means the capability or environment is missing, not that the test failed.",
        "- No result in this report was fabricated or copied from an earlier run.",
        "",
        "## Known gaps",
        "",
        "- PostgreSQL-specific concurrency and locking paths are blocked in this SQLite-based test environment.",
        "- External LLM provider success, timeout, 401, 429, and custom-base-URL paths are blocked without a provider key.",
        "- Rate limiting is not implemented, so those security scenarios are blocked.",
        "- Real microphone capture and permission prompts cannot be exercised in headless Edge; only the controls and language payloads were verified.",
        "- Cross-browser Web Speech behavior is not tested; only Microsoft Edge is available.",
        "- Frontend unit tests and a permanent cross-browser E2E suite are not configured.",
        "- The Three.js chunk remains above Vite's 500 kB warning threshold.",
        "",
    ]
)

(TESTS_DIR / "TEST_EXECUTION_REPORT.md").write_text("\n".join(report_lines), encoding="utf-8")

print(f"Generated {len(SCENARIOS)} scenarios")
print(f"Status counts: {dict(status_counts)}")
print(f"Module counts: {dict(actual_counts)}")

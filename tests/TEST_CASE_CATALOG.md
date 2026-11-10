# NextGenERP Test Case Catalog

Generated: 2026-11-11

Total scenarios: **1000**

Status values:

- `passed` — executed and verified; evidence is recorded in `test_cases.json`.
- `not_run` — defined but not yet executed.
- `blocked` — cannot be executed in the current environment; the reason is recorded.

> This catalog is a planning artifact. A scenario is not marked passed unless it was actually executed.

## Summary

| Module | Scenarios | Passed | Not run | Blocked |
| --- | ---: | ---: | ---: | ---: |
| Authentication | 80 | 2 | 78 | 0 |
| Dashboard | 60 | 1 | 59 | 0 |
| Products | 100 | 0 | 100 | 0 |
| Categories | 60 | 0 | 60 | 0 |
| Suppliers | 90 | 0 | 90 | 0 |
| Inventory Operations | 110 | 2 | 100 | 8 |
| Sales Orders | 120 | 0 | 112 | 8 |
| Purchase Orders | 120 | 0 | 108 | 12 |
| Demand Forecast | 80 | 0 | 80 | 0 |
| NextGenERP Assistant | 80 | 8 | 67 | 5 |
| Navigation and UI | 50 | 1 | 49 | 0 |
| Security and API | 50 | 0 | 44 | 6 |
| **Total** | **1000** | **14** | **947** | **39** |

## Authentication

### Registration

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0001 | Registration: register username 'abc' | API | P2 | not_run |
| TC-0002 | Registration: register username 'user1' | API | P2 | not_run |
| TC-0003 | Registration: register username 'user.name' | API | P2 | not_run |
| TC-0004 | Registration: register username 'user_name' | API | P2 | not_run |
| TC-0005 | Registration: register username 'user-name' | API | P2 | not_run |
| TC-0006 | Registration: register username 'User.Mixed' | API | P2 | not_run |
| TC-0007 | Registration: register username 'a1b2c3' | API | P2 | not_run |
| TC-0008 | Registration: register username 'z9y8x7' | API | P2 | not_run |
| TC-0009 | Registration: register username 'demo.user' | API | P2 | not_run |
| TC-0010 | Registration: register username 'ops_team' | API | P2 | not_run |
| TC-0011 | Registration: register username 'sales-team' | API | P2 | not_run |
| TC-0012 | Registration: register username 'TestUser99' | API | P2 | not_run |
| TC-0013 | Registration: reject invalid username 'ab' | API | P2 | not_run |
| TC-0014 | Registration: reject invalid username 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' | API | P2 | not_run |
| TC-0015 | Registration: reject invalid username 'user name' | API | P2 | not_run |
| TC-0016 | Registration: reject invalid username 'user@name' | API | P2 | not_run |
| TC-0017 | Registration: reject invalid username 'user/name' | API | P2 | not_run |
| TC-0018 | Registration: reject invalid username 'user+name' | API | P2 | not_run |
| TC-0019 | Registration: reject invalid username 'üser' | API | P2 | not_run |
| TC-0020 | Registration: reject invalid username 'user!' | API | P2 | not_run |
| TC-0021 | Registration: reject invalid username 'user#1' | API | P2 | not_run |
| TC-0022 | Registration: reject invalid username '' | API | P2 | not_run |
| TC-0023 | Registration: reject invalid username '   ' | API | P2 | not_run |
| TC-0024 | Registration: reject invalid username 'user	name' | API | P2 | not_run |
| TC-0025 | Registration: password boundary: 11-character password | API | P2 | not_run |
| TC-0026 | Registration: password boundary: 12-character password | API | P2 | not_run |
| TC-0027 | Registration: password boundary: 128-character password | API | P2 | not_run |
| TC-0028 | Registration: password boundary: 129-character password | API | P2 | not_run |
| TC-0029 | Registration: password boundary: 12 digits | API | P2 | not_run |
| TC-0030 | Registration: password boundary: 12 spaces | API | P2 | not_run |
| TC-0031 | Registration: password boundary: 12 unicode characters | API | P2 | not_run |
| TC-0032 | Registration: password boundary: empty password | API | P2 | not_run |
| TC-0057 | Registration: account conflict: duplicate username with identical case | API | P2 | not_run |
| TC-0058 | Registration: account conflict: duplicate username with different case | API | P2 | not_run |
| TC-0059 | Registration: account conflict: duplicate username containing a dot | API | P2 | not_run |
| TC-0060 | Registration: account conflict: database commit failure during registration | API | P2 | not_run |
| TC-0061 | Registration: account conflict: database query failure during login | API | P2 | not_run |
| TC-0062 | Registration: account conflict: two concurrent registrations for the same username | API | P2 | not_run |

### Login

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0033 | Login: login scenario: correct password | API | P2 | not_run |
| TC-0034 | Login: login scenario: wrong password | API | P2 | not_run |
| TC-0035 | Login: login scenario: unknown username | API | P2 | not_run |
| TC-0036 | Login: login scenario: uppercase username | API | P2 | not_run |
| TC-0037 | Login: login scenario: leading whitespace in username | API | P2 | not_run |
| TC-0038 | Login: login scenario: empty username | API | P2 | not_run |
| TC-0039 | Login: login scenario: empty password | API | P2 | not_run |
| TC-0040 | Login: login scenario: 129-character password | API | P2 | not_run |
| TC-0041 | Login: login scenario: 81-character username | API | P2 | not_run |
| TC-0042 | Login: login scenario: SQL injection string | API | P2 | not_run |
| TC-0043 | Login: login scenario: unicode username | API | P2 | not_run |
| TC-0044 | Login: login scenario: repeated failed login | API | P2 | not_run |

### Tokens

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0045 | Tokens: token handling: missing Authorization header | API | P2 | not_run |
| TC-0046 | Tokens: token handling: malformed Bearer prefix | API | P2 | not_run |
| TC-0047 | Tokens: token handling: expired token | API | P2 | not_run |
| TC-0048 | Tokens: token handling: invalid signature | API | P2 | not_run |
| TC-0049 | Tokens: token handling: wrong algorithm | API | P2 | not_run |
| TC-0050 | Tokens: token handling: tampered payload | API | P2 | not_run |
| TC-0051 | Tokens: token handling: lowercase bearer | API | P2 | not_run |
| TC-0052 | Tokens: token handling: extra spaces after Bearer | API | P2 | not_run |
| TC-0053 | Tokens: token handling: empty token | API | P2 | not_run |
| TC-0054 | Tokens: token handling: valid token | API | P2 | not_run |
| TC-0055 | Tokens: token handling: token signed with another secret | API | P2 | not_run |
| TC-0056 | Tokens: token handling: token for a deleted user | API | P2 | not_run |

### Registration UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0063 | Registration UI: registration form: valid form submission | UI | P2 | not_run |
| TC-0064 | Registration UI: registration form: username shorter than 3 characters | UI | P2 | not_run |
| TC-0065 | Registration UI: registration form: invalid username character | UI | P2 | not_run |
| TC-0066 | Registration UI: registration form: password shorter than 12 characters | UI | P2 | not_run |
| TC-0067 | Registration UI: registration form: duplicate username | UI | P2 | not_run |
| TC-0068 | Registration UI: registration form: submit while request is in flight | UI | P2 | not_run |
| TC-0069 | Registration UI: registration form: successful redirect into the app shell | UI | P2 | not_run |
| TC-0070 | Registration UI: registration form: server error message is shown | UI | P2 | not_run |

### Login UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0071 | Login UI: valid credentials sign in | UI | P2 | passed |
| TC-0072 | Login UI: signed-in identity shows the username | UI | P2 | passed |
| TC-0073 | Login UI: invalid credentials | UI | P2 | not_run |
| TC-0074 | Login UI: empty fields | UI | P2 | not_run |
| TC-0075 | Login UI: show and hide password | UI | P2 | not_run |
| TC-0076 | Login UI: session expiry returns to login | UI | P2 | not_run |
| TC-0077 | Login UI: sign out clears the session | UI | P2 | not_run |
| TC-0078 | Login UI: back button after sign out | UI | P2 | not_run |
| TC-0079 | Login UI: 401 response clears the token | UI | P2 | not_run |
| TC-0080 | Login UI: mobile login layout | UI | P2 | not_run |

## Dashboard

### KPI calculations

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0081 | KPI calculations: KPI calculation with zero products | UI | P2 | not_run |
| TC-0082 | KPI calculations: KPI calculation with one product | UI | P2 | not_run |
| TC-0083 | KPI calculations: KPI calculation with many products | UI | P2 | not_run |
| TC-0084 | KPI calculations: KPI calculation with zero stock | UI | P2 | not_run |
| TC-0085 | KPI calculations: KPI calculation with low-stock boundary | UI | P2 | not_run |
| TC-0086 | KPI calculations: KPI calculation with out-of-stock product | UI | P2 | not_run |
| TC-0087 | KPI calculations: KPI calculation with units sum | UI | P2 | not_run |
| TC-0088 | KPI calculations: KPI calculation with category count | UI | P2 | not_run |
| TC-0089 | KPI calculations: KPI calculation with pending sales orders | UI | P2 | not_run |
| TC-0090 | KPI calculations: KPI calculation with confirmed sales orders | UI | P2 | not_run |
| TC-0091 | KPI calculations: KPI calculation with delivered sales orders | UI | P2 | not_run |
| TC-0092 | KPI calculations: KPI calculation with pending purchase orders | UI | P2 | not_run |
| TC-0093 | KPI calculations: KPI calculation with received purchase orders | UI | P2 | not_run |
| TC-0094 | KPI calculations: KPI calculation with supplier count | UI | P2 | not_run |
| TC-0095 | KPI calculations: KPI calculation with mixed statuses | UI | P2 | not_run |

### Low-stock boundaries

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0096 | Low-stock boundaries: low-stock boundary: stock 0, reorder 0 | UI | P2 | not_run |
| TC-0097 | Low-stock boundaries: low-stock boundary: stock 1, reorder 0 | UI | P2 | not_run |
| TC-0098 | Low-stock boundaries: low-stock boundary: stock 1, reorder 1 | UI | P2 | not_run |
| TC-0099 | Low-stock boundaries: low-stock boundary: stock 1, reorder 2 | UI | P2 | not_run |
| TC-0100 | Low-stock boundaries: low-stock boundary: stock 5, reorder 5 | UI | P2 | not_run |
| TC-0101 | Low-stock boundaries: low-stock boundary: stock 6, reorder 5 | UI | P2 | not_run |
| TC-0102 | Low-stock boundaries: low-stock boundary: missing reorder level | UI | P2 | not_run |
| TC-0103 | Low-stock boundaries: low-stock boundary: missing stock quantity | UI | P2 | not_run |
| TC-0104 | Low-stock boundaries: low-stock boundary: very large stock value | UI | P2 | not_run |
| TC-0105 | Low-stock boundaries: low-stock boundary: negative stock value | UI | P2 | not_run |

### Partial loading

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0106 | Partial loading: products endpoint unavailable | UI | P2 | not_run |
| TC-0107 | Partial loading: categories endpoint unavailable | UI | P2 | not_run |
| TC-0108 | Partial loading: suppliers endpoint unavailable | UI | P2 | not_run |
| TC-0109 | Partial loading: sales orders endpoint unavailable | UI | P2 | passed |
| TC-0110 | Partial loading: purchase orders endpoint unavailable | UI | P2 | not_run |

### Empty states

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0111 | Empty states: empty dashboard: no products | UI | P2 | not_run |
| TC-0112 | Empty states: empty dashboard: no categories | UI | P2 | not_run |
| TC-0113 | Empty states: empty dashboard: no suppliers | UI | P2 | not_run |
| TC-0114 | Empty states: empty dashboard: no sales orders | UI | P2 | not_run |
| TC-0115 | Empty states: empty dashboard: no purchase orders | UI | P2 | not_run |
| TC-0116 | Empty states: empty dashboard: completely empty workspace | UI | P2 | not_run |

### Refresh and retry

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0117 | Refresh and retry: dashboard refresh: refresh success | UI | P2 | not_run |
| TC-0118 | Refresh and retry: dashboard refresh: refresh failure retains existing data | UI | P2 | not_run |
| TC-0119 | Refresh and retry: dashboard refresh: retry after a failed load | UI | P2 | not_run |
| TC-0120 | Refresh and retry: dashboard refresh: double-click refresh | UI | P2 | not_run |
| TC-0121 | Refresh and retry: dashboard refresh: initial load | UI | P2 | not_run |
| TC-0122 | Refresh and retry: dashboard refresh: slow endpoint response | UI | P2 | not_run |

### Recent activity

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0123 | Recent activity: recent activity: no orders | UI | P2 | not_run |
| TC-0124 | Recent activity: recent activity: one order | UI | P2 | not_run |
| TC-0125 | Recent activity: recent activity: three orders | UI | P2 | not_run |
| TC-0126 | Recent activity: recent activity: more than three orders | UI | P2 | not_run |
| TC-0127 | Recent activity: recent activity: two records with equal IDs | UI | P2 | not_run |
| TC-0128 | Recent activity: recent activity: mixed sales and purchase statuses | UI | P2 | not_run |

### 3D snapshot

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0129 | 3D snapshot: 3D snapshot fallback: WebGL unavailable | UI | P2 | not_run |
| TC-0130 | 3D snapshot: 3D snapshot fallback: empty item list | UI | P2 | not_run |
| TC-0131 | 3D snapshot: 3D snapshot fallback: one item | UI | P2 | not_run |
| TC-0132 | 3D snapshot: 3D snapshot fallback: twelve items | UI | P2 | not_run |

### Responsive and accessibility

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0133 | Responsive and accessibility: dashboard accessibility: desktop 1440px | Accessibility | P2 | not_run |
| TC-0134 | Responsive and accessibility: dashboard accessibility: tablet 768px | Accessibility | P2 | not_run |
| TC-0135 | Responsive and accessibility: dashboard accessibility: mobile 390px | Accessibility | P2 | not_run |
| TC-0136 | Responsive and accessibility: dashboard accessibility: skip link focus | Accessibility | P2 | not_run |
| TC-0137 | Responsive and accessibility: dashboard accessibility: heading order | Accessibility | P2 | not_run |
| TC-0138 | Responsive and accessibility: dashboard accessibility: table header semantics | Accessibility | P2 | not_run |
| TC-0139 | Responsive and accessibility: dashboard accessibility: status announcements | Accessibility | P2 | not_run |
| TC-0140 | Responsive and accessibility: dashboard accessibility: reduced motion | Accessibility | P2 | not_run |

## Products

### Create

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0141 | Create: create product: minimal payload | API | P2 | not_run |
| TC-0142 | Create: create product: full payload | API | P2 | not_run |
| TC-0143 | Create: create product: zero opening stock | API | P2 | not_run |
| TC-0144 | Create: create product: reorder level zero | API | P2 | not_run |
| TC-0145 | Create: create product: large price | API | P2 | not_run |
| TC-0146 | Create: create product: decimal price | API | P2 | not_run |
| TC-0147 | Create: create product: unicode name | API | P2 | not_run |
| TC-0148 | Create: create product: 100-character name | API | P2 | not_run |
| TC-0149 | Create: create product: 50-character SKU | API | P2 | not_run |
| TC-0150 | Create: create product: stock equal to reorder level | API | P2 | not_run |
| TC-0151 | Create: create product: stock above reorder level | API | P2 | not_run |
| TC-0152 | Create: create product: category assigned | API | P2 | not_run |
| TC-0153 | Create: create product: no category | API | P2 | not_run |
| TC-0154 | Create: create product: price with two decimals | API | P2 | not_run |
| TC-0155 | Create: create product: maximum safe stock | API | P2 | not_run |

### Create validation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0156 | Create validation: reject product payload: empty name | API | P2 | not_run |
| TC-0157 | Create validation: reject product payload: whitespace-only name | API | P2 | not_run |
| TC-0158 | Create validation: reject product payload: empty SKU | API | P2 | not_run |
| TC-0159 | Create validation: reject product payload: duplicate SKU | API | P2 | not_run |
| TC-0160 | Create validation: reject product payload: negative stock | API | P2 | not_run |
| TC-0161 | Create validation: reject product payload: fractional stock | API | P2 | not_run |
| TC-0162 | Create validation: reject product payload: negative reorder level | API | P2 | not_run |
| TC-0163 | Create validation: reject product payload: fractional reorder level | API | P2 | not_run |
| TC-0164 | Create validation: reject product payload: negative price | API | P2 | not_run |
| TC-0165 | Create validation: reject product payload: zero price | API | P2 | not_run |
| TC-0166 | Create validation: reject product payload: NaN price | API | P2 | not_run |
| TC-0167 | Create validation: reject product payload: missing category | API | P2 | not_run |
| TC-0168 | Create validation: reject product payload: very large stock | API | P2 | not_run |
| TC-0169 | Create validation: reject product payload: missing name | API | P2 | not_run |
| TC-0170 | Create validation: reject product payload: missing SKU | API | P2 | not_run |

### Update

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0171 | Update: update product: name | API | P2 | not_run |
| TC-0172 | Update: update product: SKU | API | P2 | not_run |
| TC-0173 | Update: update product: price | API | P2 | not_run |
| TC-0174 | Update: update product: stock increase | API | P2 | not_run |
| TC-0175 | Update: update product: stock decrease | API | P2 | not_run |
| TC-0176 | Update: update product: reorder level | API | P2 | not_run |
| TC-0177 | Update: update product: assign category | API | P2 | not_run |
| TC-0178 | Update: update product: clear category | API | P2 | not_run |
| TC-0179 | Update: update product: duplicate SKU | API | P2 | not_run |
| TC-0180 | Update: update product: missing product | API | P2 | not_run |
| TC-0181 | Update: update product: invalid stock value | API | P2 | not_run |
| TC-0182 | Update: update product: unchanged values | API | P2 | not_run |

### Delete and relationships

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0183 | Delete and relationships: delete product: no references | API | P2 | not_run |
| TC-0184 | Delete and relationships: delete product: referenced by a sales order | API | P2 | not_run |
| TC-0185 | Delete and relationships: delete product: referenced by a purchase order | API | P2 | not_run |
| TC-0186 | Delete and relationships: delete product: referenced by both order types | API | P2 | not_run |
| TC-0187 | Delete and relationships: delete product: nonexistent product | API | P2 | not_run |
| TC-0188 | Delete and relationships: delete product: double delete | API | P2 | not_run |
| TC-0189 | Delete and relationships: delete product: order cancelled but still referenced | API | P2 | not_run |
| TC-0190 | Delete and relationships: delete product: order delivered and still referenced | API | P2 | not_run |
| TC-0191 | Delete and relationships: delete product: product with stock | API | P2 | not_run |
| TC-0192 | Delete and relationships: delete product: product with category only | API | P2 | not_run |

### Search, filter, sort

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0193 | Search, filter, sort: product list interaction: name search | UI | P2 | not_run |
| TC-0194 | Search, filter, sort: product list interaction: SKU search | UI | P2 | not_run |
| TC-0195 | Search, filter, sort: product list interaction: case-insensitive search | UI | P2 | not_run |
| TC-0196 | Search, filter, sort: product list interaction: no-match search | UI | P2 | not_run |
| TC-0197 | Search, filter, sort: product list interaction: clear search | UI | P2 | not_run |
| TC-0198 | Search, filter, sort: product list interaction: sort name ascending | UI | P2 | not_run |
| TC-0199 | Search, filter, sort: product list interaction: sort name descending | UI | P2 | not_run |
| TC-0200 | Search, filter, sort: product list interaction: sort stock ascending | UI | P2 | not_run |
| TC-0201 | Search, filter, sort: product list interaction: sort stock descending | UI | P2 | not_run |
| TC-0202 | Search, filter, sort: product list interaction: filter low stock | UI | P2 | not_run |
| TC-0203 | Search, filter, sort: product list interaction: filter out of stock | UI | P2 | not_run |
| TC-0204 | Search, filter, sort: product list interaction: combined filter | UI | P2 | not_run |

### Large data

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0205 | Large data: product list volume: 0 products | UI | P2 | not_run |
| TC-0206 | Large data: product list volume: 1 product | UI | P2 | not_run |
| TC-0207 | Large data: product list volume: 10 products | UI | P2 | not_run |
| TC-0208 | Large data: product list volume: 50 products | UI | P2 | not_run |
| TC-0209 | Large data: product list volume: 100 products | UI | P2 | not_run |
| TC-0210 | Large data: product list volume: 500 products | UI | P2 | not_run |
| TC-0211 | Large data: product list volume: last page boundary | UI | P2 | not_run |
| TC-0212 | Large data: product list volume: long list scrolling | UI | P2 | not_run |

### Stock adjustment

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0213 | Stock adjustment: product stock adjustment: opening stock on create | API | P2 | not_run |
| TC-0214 | Stock adjustment: product stock adjustment: stock increase via update | API | P2 | not_run |
| TC-0215 | Stock adjustment: product stock adjustment: stock decrease via update | API | P2 | not_run |
| TC-0216 | Stock adjustment: product stock adjustment: same stock value | API | P2 | not_run |
| TC-0217 | Stock adjustment: product stock adjustment: stock set to zero | API | P2 | not_run |
| TC-0218 | Stock adjustment: product stock adjustment: fractional stock rejected | API | P2 | not_run |
| TC-0219 | Stock adjustment: product stock adjustment: negative stock rejected | API | P2 | not_run |
| TC-0220 | Stock adjustment: product stock adjustment: adjustment history row | API | P2 | not_run |

### UI dialogs

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0221 | UI dialogs: product dialog: add dialog opens | UI | P2 | not_run |
| TC-0222 | UI dialogs: product dialog: add dialog closes | UI | P2 | not_run |
| TC-0223 | UI dialogs: product dialog: edit dialog prefill | UI | P2 | not_run |
| TC-0224 | UI dialogs: product dialog: delete confirm accepted | UI | P2 | not_run |
| TC-0225 | UI dialogs: product dialog: delete confirm cancelled | UI | P2 | not_run |
| TC-0226 | UI dialogs: product dialog: required field validation | UI | P2 | not_run |
| TC-0227 | UI dialogs: product dialog: duplicate SKU error | UI | P2 | not_run |
| TC-0228 | UI dialogs: product dialog: server error message | UI | P2 | not_run |
| TC-0229 | UI dialogs: product dialog: saving state | UI | P2 | not_run |
| TC-0230 | UI dialogs: product dialog: success feedback | UI | P2 | not_run |
| TC-0231 | UI dialogs: product dialog: Escape closes dialog | UI | P2 | not_run |
| TC-0232 | UI dialogs: product dialog: mobile dialog layout | UI | P2 | not_run |

### API security

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0233 | API security: product API security: unauthenticated list | API | P2 | not_run |
| TC-0234 | API security: product API security: unauthenticated create | API | P2 | not_run |
| TC-0235 | API security: product API security: unauthenticated update | API | P2 | not_run |
| TC-0236 | API security: product API security: unauthenticated delete | API | P2 | not_run |
| TC-0237 | API security: product API security: invalid product ID | API | P2 | not_run |
| TC-0238 | API security: product API security: malformed JSON | API | P2 | not_run |
| TC-0239 | API security: product API security: database failure | API | P2 | not_run |
| TC-0240 | API security: product API security: CORS preflight | API | P2 | not_run |

## Categories

### Create

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0241 | Create: create category: simple name | API | P2 | not_run |
| TC-0242 | Create: create category: with description | API | P2 | not_run |
| TC-0243 | Create: create category: unicode name | API | P2 | not_run |
| TC-0244 | Create: create category: long name | API | P2 | not_run |
| TC-0245 | Create: create category: long description | API | P2 | not_run |
| TC-0246 | Create: create category: hyphenated name | API | P2 | not_run |
| TC-0247 | Create: create category: dot in name | API | P2 | not_run |
| TC-0248 | Create: create category: mixed case | API | P2 | not_run |
| TC-0249 | Create: create category: numeric name | API | P2 | not_run |
| TC-0250 | Create: create category: leading and trailing spaces | API | P2 | not_run |

### Validation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0251 | Validation: reject category: empty name | API | P2 | not_run |
| TC-0252 | Validation: reject category: whitespace-only name | API | P2 | not_run |
| TC-0253 | Validation: reject category: duplicate exact name | API | P2 | not_run |
| TC-0254 | Validation: reject category: duplicate different case | API | P2 | not_run |
| TC-0255 | Validation: reject category: one-character name | API | P2 | not_run |
| TC-0256 | Validation: reject category: very long name | API | P2 | not_run |
| TC-0257 | Validation: reject category: special characters | API | P2 | not_run |
| TC-0258 | Validation: reject category: missing name | API | P2 | not_run |
| TC-0259 | Validation: reject category: malformed JSON | API | P2 | not_run |
| TC-0260 | Validation: reject category: database failure | API | P2 | not_run |

### Update

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0261 | Update: update category: name | API | P2 | not_run |
| TC-0262 | Update: update category: description | API | P2 | not_run |
| TC-0263 | Update: update category: clear description | API | P2 | not_run |
| TC-0264 | Update: update category: duplicate name | API | P2 | not_run |
| TC-0265 | Update: update category: missing category | API | P2 | not_run |
| TC-0266 | Update: update category: invalid name | API | P2 | not_run |
| TC-0267 | Update: update category: unchanged values | API | P2 | not_run |
| TC-0268 | Update: update category: case-only change | API | P2 | not_run |

### Delete and relationships

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0269 | Delete and relationships: delete category: no products | API | P2 | not_run |
| TC-0270 | Delete and relationships: delete category: one product | API | P2 | not_run |
| TC-0271 | Delete and relationships: delete category: many products | API | P2 | not_run |
| TC-0272 | Delete and relationships: delete category: nonexistent category | API | P2 | not_run |
| TC-0273 | Delete and relationships: delete category: double delete | API | P2 | not_run |
| TC-0274 | Delete and relationships: delete category: after product moved to another category | API | P2 | not_run |
| TC-0275 | Delete and relationships: delete category: after product deleted | API | P2 | not_run |
| TC-0276 | Delete and relationships: delete category: database failure during delete | API | P2 | not_run |

### UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0277 | UI: category UI: list rendering | UI | P2 | not_run |
| TC-0278 | UI: category UI: empty state | UI | P2 | not_run |
| TC-0279 | UI: category UI: add dialog | UI | P2 | not_run |
| TC-0280 | UI: category UI: edit dialog | UI | P2 | not_run |
| TC-0281 | UI: category UI: delete confirmation | UI | P2 | not_run |
| TC-0282 | UI: category UI: cancel delete | UI | P2 | not_run |
| TC-0283 | UI: category UI: error message | UI | P2 | not_run |
| TC-0284 | UI: category UI: loading state | UI | P2 | not_run |
| TC-0285 | UI: category UI: search | UI | P2 | not_run |
| TC-0286 | UI: category UI: sort | UI | P2 | not_run |
| TC-0287 | UI: category UI: mobile layout | UI | P2 | not_run |
| TC-0288 | UI: category UI: keyboard navigation | UI | P2 | not_run |

### API security

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0289 | API security: category API security: unauthenticated list | API | P2 | not_run |
| TC-0290 | API security: category API security: unauthenticated create | API | P2 | not_run |
| TC-0291 | API security: category API security: unauthenticated update | API | P2 | not_run |
| TC-0292 | API security: category API security: unauthenticated delete | API | P2 | not_run |
| TC-0293 | API security: category API security: 404 response | API | P2 | not_run |
| TC-0294 | API security: category API security: 409 response | API | P2 | not_run |
| TC-0295 | API security: category API security: 422 response | API | P2 | not_run |
| TC-0296 | API security: category API security: 500 response | API | P2 | not_run |
| TC-0297 | API security: category API security: CORS preflight | API | P2 | not_run |
| TC-0298 | API security: category API security: method not allowed | API | P2 | not_run |
| TC-0299 | API security: category API security: trailing slash redirect | API | P2 | not_run |
| TC-0300 | API security: category API security: malformed JSON | API | P2 | not_run |

## Suppliers

### Create

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0301 | Create: create supplier: minimal name | API | P2 | not_run |
| TC-0302 | Create: create supplier: full contact details | API | P2 | not_run |
| TC-0303 | Create: create supplier: zero lead time | API | P2 | not_run |
| TC-0304 | Create: create supplier: 365-day lead time | API | P2 | not_run |
| TC-0305 | Create: create supplier: rating 0 | API | P2 | not_run |
| TC-0306 | Create: create supplier: rating 5 | API | P2 | not_run |
| TC-0307 | Create: create supplier: rating 4.5 | API | P2 | not_run |
| TC-0308 | Create: create supplier: unicode name | API | P2 | not_run |
| TC-0309 | Create: create supplier: long name | API | P2 | not_run |
| TC-0310 | Create: create supplier: no email | API | P2 | not_run |
| TC-0311 | Create: create supplier: no phone | API | P2 | not_run |
| TC-0312 | Create: create supplier: no address | API | P2 | not_run |
| TC-0313 | Create: create supplier: hyphenated name | API | P2 | not_run |
| TC-0314 | Create: create supplier: numeric name | API | P2 | not_run |
| TC-0315 | Create: create supplier: leading and trailing spaces | API | P2 | not_run |

### Validation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0316 | Validation: reject supplier: empty name | API | P2 | not_run |
| TC-0317 | Validation: reject supplier: whitespace-only name | API | P2 | not_run |
| TC-0318 | Validation: reject supplier: negative lead time | API | P2 | not_run |
| TC-0319 | Validation: reject supplier: fractional lead time | API | P2 | not_run |
| TC-0320 | Validation: reject supplier: rating -0.1 | API | P2 | not_run |
| TC-0321 | Validation: reject supplier: rating 5.1 | API | P2 | not_run |
| TC-0322 | Validation: reject supplier: rating NaN | API | P2 | not_run |
| TC-0323 | Validation: reject supplier: rating infinity | API | P2 | not_run |
| TC-0324 | Validation: reject supplier: missing name | API | P2 | not_run |
| TC-0325 | Validation: reject supplier: very long name | API | P2 | not_run |
| TC-0326 | Validation: reject supplier: wrong type for lead time | API | P2 | not_run |
| TC-0327 | Validation: reject supplier: wrong type for rating | API | P2 | not_run |
| TC-0328 | Validation: reject supplier: malformed JSON | API | P2 | not_run |
| TC-0329 | Validation: reject supplier: null body | API | P2 | not_run |
| TC-0330 | Validation: reject supplier: extra unknown fields | API | P2 | not_run |

### Update

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0331 | Update: update supplier: name | API | P2 | not_run |
| TC-0332 | Update: update supplier: email | API | P2 | not_run |
| TC-0333 | Update: update supplier: phone | API | P2 | not_run |
| TC-0334 | Update: update supplier: address | API | P2 | not_run |
| TC-0335 | Update: update supplier: lead time | API | P2 | not_run |
| TC-0336 | Update: update supplier: rating | API | P2 | not_run |
| TC-0337 | Update: update supplier: clear optional fields | API | P2 | not_run |
| TC-0338 | Update: update supplier: missing supplier | API | P2 | not_run |
| TC-0339 | Update: update supplier: invalid rating | API | P2 | not_run |
| TC-0340 | Update: update supplier: unchanged values | API | P2 | not_run |

### Delete and relationships

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0341 | Delete and relationships: delete supplier: no purchase orders | API | P2 | not_run |
| TC-0342 | Delete and relationships: delete supplier: one purchase order | API | P2 | not_run |
| TC-0343 | Delete and relationships: delete supplier: many purchase orders | API | P2 | not_run |
| TC-0344 | Delete and relationships: delete supplier: nonexistent supplier | API | P2 | not_run |
| TC-0345 | Delete and relationships: delete supplier: double delete | API | P2 | not_run |
| TC-0346 | Delete and relationships: delete supplier: after purchase order cancelled | API | P2 | not_run |
| TC-0347 | Delete and relationships: delete supplier: after purchase order received | API | P2 | not_run |
| TC-0348 | Delete and relationships: delete supplier: database failure | API | P2 | not_run |
| TC-0349 | Delete and relationships: delete supplier: delete with product only | API | P2 | not_run |
| TC-0350 | Delete and relationships: delete supplier: delete after purchase order deleted | API | P2 | not_run |

### Boundaries

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0351 | Boundaries: supplier boundary: lead time 0 | API | P2 | not_run |
| TC-0352 | Boundaries: supplier boundary: lead time 1 | API | P2 | not_run |
| TC-0353 | Boundaries: supplier boundary: lead time 30 | API | P2 | not_run |
| TC-0354 | Boundaries: supplier boundary: lead time 365 | API | P2 | not_run |
| TC-0355 | Boundaries: supplier boundary: lead time 366 | API | P2 | not_run |
| TC-0356 | Boundaries: supplier boundary: rating 0 | API | P2 | not_run |
| TC-0357 | Boundaries: supplier boundary: rating 0.1 | API | P2 | not_run |
| TC-0358 | Boundaries: supplier boundary: rating 4.999 | API | P2 | not_run |
| TC-0359 | Boundaries: supplier boundary: rating 5 | API | P2 | not_run |
| TC-0360 | Boundaries: supplier boundary: rating 5.0001 | API | P2 | not_run |

### UI dialogs

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0361 | UI dialogs: supplier dialog: add dialog opens | UI | P2 | not_run |
| TC-0362 | UI dialogs: supplier dialog: edit dialog prefill | UI | P2 | not_run |
| TC-0363 | UI dialogs: supplier dialog: delete confirmation | UI | P2 | not_run |
| TC-0364 | UI dialogs: supplier dialog: cancel delete | UI | P2 | not_run |
| TC-0365 | UI dialogs: supplier dialog: required name validation | UI | P2 | not_run |
| TC-0366 | UI dialogs: supplier dialog: rating input | UI | P2 | not_run |
| TC-0367 | UI dialogs: supplier dialog: lead-time input | UI | P2 | not_run |
| TC-0368 | UI dialogs: supplier dialog: server error message | UI | P2 | not_run |
| TC-0369 | UI dialogs: supplier dialog: saving state | UI | P2 | not_run |
| TC-0370 | UI dialogs: supplier dialog: mobile layout | UI | P2 | not_run |

### API security

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0371 | API security: supplier API security: unauthenticated list | API | P2 | not_run |
| TC-0372 | API security: supplier API security: unauthenticated create | API | P2 | not_run |
| TC-0373 | API security: supplier API security: unauthenticated update | API | P2 | not_run |
| TC-0374 | API security: supplier API security: unauthenticated delete | API | P2 | not_run |
| TC-0375 | API security: supplier API security: 404 response | API | P2 | not_run |
| TC-0376 | API security: supplier API security: 422 response | API | P2 | not_run |
| TC-0377 | API security: supplier API security: 409 response | API | P2 | not_run |
| TC-0378 | API security: supplier API security: 503 response | API | P2 | not_run |
| TC-0379 | API security: supplier API security: CORS preflight | API | P2 | not_run |
| TC-0380 | API security: supplier API security: malformed JSON | API | P2 | not_run |

### Large list

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0381 | Large list: supplier list volume: 0 suppliers | UI | P2 | not_run |
| TC-0382 | Large list: supplier list volume: 1 supplier | UI | P2 | not_run |
| TC-0383 | Large list: supplier list volume: 10 suppliers | UI | P2 | not_run |
| TC-0384 | Large list: supplier list volume: 50 suppliers | UI | P2 | not_run |
| TC-0385 | Large list: supplier list volume: 100 suppliers | UI | P2 | not_run |
| TC-0386 | Large list: supplier list volume: search by name | UI | P2 | not_run |
| TC-0387 | Large list: supplier list volume: search by email | UI | P2 | not_run |
| TC-0388 | Large list: supplier list volume: sort by name | UI | P2 | not_run |
| TC-0389 | Large list: supplier list volume: no-match search | UI | P2 | not_run |
| TC-0390 | Large list: supplier list volume: pagination boundary | UI | P2 | not_run |

## Inventory Operations

### Stock In

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0391 | Stock In: stock in: quantity 1 | API | P2 | not_run |
| TC-0392 | Stock In: stock in: quantity 5 | API | P2 | not_run |
| TC-0393 | Stock In: stock in: quantity 100 | API | P2 | not_run |
| TC-0394 | Stock In: stock in: quantity 1000 | API | P2 | not_run |
| TC-0395 | Stock In: stock in: maximum safe quantity | API | P2 | not_run |
| TC-0396 | Stock In: stock in: short reason | API | P2 | not_run |
| TC-0397 | Stock In: stock in: long reason | API | P2 | not_run |
| TC-0398 | Stock In: stock in: unicode reason | API | P2 | not_run |
| TC-0399 | Stock In: stock in: product with zero stock | API | P2 | not_run |
| TC-0400 | Stock In: stock in: product with low stock | API | P2 | not_run |
| TC-0401 | Stock In: stock in: product with high stock | API | P2 | not_run |
| TC-0402 | Stock In: stock in: repeated stock in | API | P2 | not_run |
| TC-0403 | Stock In: stock in: stock in after order deduction | API | P2 | not_run |
| TC-0404 | Stock In: stock in: stock in after purchase receipt | API | P2 | not_run |
| TC-0405 | Stock In: stock in: stock in with category | API | P2 | not_run |

### Stock Out

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0406 | Stock Out: stock out: quantity 1 | API | P2 | not_run |
| TC-0407 | Stock Out: stock out: exact available stock | API | P2 | not_run |
| TC-0408 | Stock Out: stock out: available stock minus one | API | P2 | not_run |
| TC-0409 | Stock Out: stock out: available stock plus one | API | P2 | not_run |
| TC-0410 | Stock Out: stock out: zero stock product | API | P2 | not_run |
| TC-0411 | Stock Out: stock out: negative quantity | API | P2 | not_run |
| TC-0412 | Stock Out: stock out: fractional quantity | API | P2 | not_run |
| TC-0413 | Stock Out: stock out: zero quantity | API | P2 | not_run |
| TC-0414 | Stock Out: stock out: very large quantity | API | P2 | not_run |
| TC-0415 | Stock Out: stock out: short reason | API | P2 | not_run |
| TC-0416 | Stock Out: stock out: missing product | API | P2 | not_run |
| TC-0417 | Stock Out: stock out: repeated stock out | API | P2 | not_run |
| TC-0418 | Stock Out: stock out: stock out after order deduction | API | P2 | not_run |
| TC-0419 | Stock Out: stock out: stock out after purchase receipt | API | P2 | not_run |
| TC-0420 | Stock Out: stock out: stock out with unicode reason | API | P2 | not_run |

### Validation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0421 | Validation: reject inventory transaction: missing product_id | API | P2 | not_run |
| TC-0422 | Validation: reject inventory transaction: invalid transaction type | API | P2 | not_run |
| TC-0423 | Validation: reject inventory transaction: lowercase transaction type | API | P2 | not_run |
| TC-0424 | Validation: reject inventory transaction: empty reason | API | P2 | not_run |
| TC-0425 | Validation: reject inventory transaction: whitespace-only reason | API | P2 | not_run |
| TC-0426 | Validation: reject inventory transaction: missing quantity | API | P2 | not_run |
| TC-0427 | Validation: reject inventory transaction: string quantity | API | P2 | not_run |
| TC-0428 | Validation: reject inventory transaction: float quantity | API | P2 | not_run |
| TC-0429 | Validation: reject inventory transaction: negative quantity | API | P2 | not_run |
| TC-0430 | Validation: reject inventory transaction: zero quantity | API | P2 | not_run |
| TC-0431 | Validation: reject inventory transaction: nonexistent product | API | P2 | not_run |
| TC-0432 | Validation: reject inventory transaction: unauthenticated request | API | P2 | not_run |
| TC-0433 | Validation: reject inventory transaction: malformed JSON | API | P2 | not_run |
| TC-0434 | Validation: reject inventory transaction: extra unknown fields | API | P2 | not_run |
| TC-0435 | Validation: reject inventory transaction: null body | API | P2 | not_run |

### History

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0436 | History: inventory history: empty history | API | P2 | not_run |
| TC-0437 | History: inventory history: one row | API | P2 | not_run |
| TC-0438 | History: inventory history: many rows | API | P2 | not_run |
| TC-0439 | History: inventory history: descending order | API | P2 | not_run |
| TC-0440 | History: inventory history: all response fields | API | P2 | not_run |
| TC-0441 | History: inventory history: product name resolution | API | P2 | not_run |
| TC-0442 | History: inventory history: date formatting | API | P2 | not_run |
| TC-0443 | History: inventory history: mixed stock in and out | API | P2 | not_run |
| TC-0444 | History: inventory history: unicode reason | API | P2 | not_run |
| TC-0445 | History: inventory history: large history | API | P2 | not_run |
| TC-0446 | History: inventory history: history after failed transaction | API | P2 | not_run |
| TC-0447 | History: inventory history: history after product update | API | P2 | not_run |

### Concurrency

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0448 | Concurrency: concurrency: two stock-out requests for the same product | API | P2 | blocked |
| TC-0449 | Concurrency: concurrency: two stock-in requests for the same product | API | P2 | blocked |
| TC-0450 | Concurrency: concurrency: stock-out racing a sales order | API | P2 | blocked |
| TC-0451 | Concurrency: concurrency: stock-out racing a cancellation restore | API | P2 | blocked |
| TC-0452 | Concurrency: concurrency: purchase receipt racing a stock-out | API | P2 | blocked |
| TC-0453 | Concurrency: concurrency: SQLite foreign-key and locking behavior | API | P2 | blocked |
| TC-0454 | Concurrency: concurrency: PostgreSQL row lock behavior | API | P2 | blocked |
| TC-0455 | Concurrency: concurrency: deadlock retry behavior | API | P2 | blocked |

### UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0456 | UI: page renders inside the app shell without nested main | UI | P2 | passed |
| TC-0457 | UI: stock history table renders rows | UI | P2 | passed |
| TC-0458 | UI: no products available | UI | P2 | not_run |
| TC-0459 | UI: one product available | UI | P2 | not_run |
| TC-0460 | UI: many products available | UI | P2 | not_run |
| TC-0461 | UI: product selector shows stock | UI | P2 | not_run |
| TC-0462 | UI: low-stock indicator | UI | P2 | not_run |
| TC-0463 | UI: type toggle | UI | P2 | not_run |
| TC-0464 | UI: quantity input | UI | P2 | not_run |
| TC-0465 | UI: reason input | UI | P2 | not_run |
| TC-0466 | UI: submit disabled while saving | UI | P2 | not_run |
| TC-0467 | UI: success message | UI | P2 | not_run |
| TC-0468 | UI: error message | UI | P2 | not_run |
| TC-0469 | UI: selected product summary | UI | P2 | not_run |
| TC-0470 | UI: mobile layout and keyboard | UI | P2 | not_run |

### Refresh and errors

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0471 | Refresh and errors: inventory load failure: products endpoint fails | UI | P2 | not_run |
| TC-0472 | Refresh and errors: inventory load failure: transactions endpoint fails | UI | P2 | not_run |
| TC-0473 | Refresh and errors: inventory load failure: both endpoints fail | UI | P2 | not_run |
| TC-0474 | Refresh and errors: inventory load failure: retry after failure | UI | P2 | not_run |
| TC-0475 | Refresh and errors: inventory load failure: refresh success | UI | P2 | not_run |
| TC-0476 | Refresh and errors: inventory load failure: slow response | UI | P2 | not_run |
| TC-0477 | Refresh and errors: inventory load failure: unauthorized response | UI | P2 | not_run |
| TC-0478 | Refresh and errors: inventory load failure: server error | UI | P2 | not_run |
| TC-0479 | Refresh and errors: inventory load failure: network failure | UI | P2 | not_run |
| TC-0480 | Refresh and errors: inventory load failure: partial data | UI | P2 | not_run |

### Large history

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0481 | Large history: inventory history volume: 10 rows | UI | P2 | not_run |
| TC-0482 | Large history: inventory history volume: 50 rows | UI | P2 | not_run |
| TC-0483 | Large history: inventory history volume: 100 rows | UI | P2 | not_run |
| TC-0484 | Large history: inventory history volume: 500 rows | UI | P2 | not_run |
| TC-0485 | Large history: inventory history volume: 1000 rows | UI | P2 | not_run |
| TC-0486 | Large history: inventory history volume: scrolling | UI | P2 | not_run |
| TC-0487 | Large history: inventory history volume: performance | UI | P2 | not_run |
| TC-0488 | Large history: inventory history volume: date formatting | UI | P2 | not_run |
| TC-0489 | Large history: inventory history volume: long reason | UI | P2 | not_run |
| TC-0490 | Large history: inventory history volume: many products | UI | P2 | not_run |

### Snapshot metrics

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0491 | Snapshot metrics: inventory snapshot: zero products | UI | P2 | not_run |
| TC-0492 | Snapshot metrics: inventory snapshot: one product | UI | P2 | not_run |
| TC-0493 | Snapshot metrics: inventory snapshot: many products | UI | P2 | not_run |
| TC-0494 | Snapshot metrics: inventory snapshot: units sum | UI | P2 | not_run |
| TC-0495 | Snapshot metrics: inventory snapshot: low-stock count boundary | UI | P2 | not_run |
| TC-0496 | Snapshot metrics: inventory snapshot: out-of-stock count | UI | P2 | not_run |
| TC-0497 | Snapshot metrics: inventory snapshot: loading state | UI | P2 | not_run |
| TC-0498 | Snapshot metrics: inventory snapshot: error state | UI | P2 | not_run |
| TC-0499 | Snapshot metrics: inventory snapshot: refresh updates metrics | UI | P2 | not_run |
| TC-0500 | Snapshot metrics: inventory snapshot: selected product summary | UI | P2 | not_run |

## Sales Orders

### Create

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0501 | Create: create sales order: quantity 1 | API | P2 | not_run |
| TC-0502 | Create: create sales order: quantity equal to stock | API | P2 | not_run |
| TC-0503 | Create: create sales order: quantity one below stock | API | P2 | not_run |
| TC-0504 | Create: create sales order: multiple products | API | P2 | not_run |
| TC-0505 | Create: create sales order: unicode customer name | API | P2 | not_run |
| TC-0506 | Create: create sales order: long customer name | API | P2 | not_run |
| TC-0507 | Create: create sales order: email present | API | P2 | not_run |
| TC-0508 | Create: create sales order: email absent | API | P2 | not_run |
| TC-0509 | Create: create sales order: zero-price product | API | P2 | not_run |
| TC-0510 | Create: create sales order: large total | API | P2 | not_run |
| TC-0511 | Create: create sales order: decimal total | API | P2 | not_run |
| TC-0512 | Create: create sales order: pending status | API | P2 | not_run |
| TC-0513 | Create: create sales order: stock deduction | API | P2 | not_run |
| TC-0514 | Create: create sales order: inventory history row | API | P2 | not_run |
| TC-0515 | Create: create sales order: order list refresh | API | P2 | not_run |

### Create validation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0516 | Create validation: reject sales order: quantity 0 | API | P2 | not_run |
| TC-0517 | Create validation: reject sales order: quantity -1 | API | P2 | not_run |
| TC-0518 | Create validation: reject sales order: quantity 1.5 | API | P2 | not_run |
| TC-0519 | Create validation: reject sales order: quantity as string | API | P2 | not_run |
| TC-0520 | Create validation: reject sales order: missing product | API | P2 | not_run |
| TC-0521 | Create validation: reject sales order: nonexistent product | API | P2 | not_run |
| TC-0522 | Create validation: reject sales order: insufficient stock | API | P2 | not_run |
| TC-0523 | Create validation: reject sales order: empty customer name | API | P2 | not_run |
| TC-0524 | Create validation: reject sales order: whitespace-only customer name | API | P2 | not_run |
| TC-0525 | Create validation: reject sales order: missing customer name | API | P2 | not_run |
| TC-0526 | Create validation: reject sales order: malformed email | API | P2 | not_run |
| TC-0527 | Create validation: reject sales order: malformed JSON | API | P2 | not_run |
| TC-0528 | Create validation: reject sales order: unauthenticated request | API | P2 | not_run |
| TC-0529 | Create validation: reject sales order: null body | API | P2 | not_run |
| TC-0530 | Create validation: reject sales order: extra unknown fields | API | P2 | not_run |

### Stock deduction

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0531 | Stock deduction: sales stock deduction: exact stock | API | P2 | not_run |
| TC-0532 | Stock deduction: sales stock deduction: partial stock | API | P2 | not_run |
| TC-0533 | Stock deduction: sales stock deduction: stock becomes zero | API | P2 | not_run |
| TC-0534 | Stock deduction: sales stock deduction: concurrent last unit | API | P2 | not_run |
| TC-0535 | Stock deduction: sales stock deduction: failed order leaves stock unchanged | API | P2 | not_run |
| TC-0536 | Stock deduction: sales stock deduction: database error rollback | API | P2 | not_run |
| TC-0537 | Stock deduction: sales stock deduction: two sequential orders | API | P2 | not_run |
| TC-0538 | Stock deduction: sales stock deduction: cancel restores stock | API | P2 | not_run |
| TC-0539 | Stock deduction: sales stock deduction: delivered order does not restore stock | API | P2 | not_run |
| TC-0540 | Stock deduction: sales stock deduction: stock-out after order | API | P2 | not_run |
| TC-0541 | Stock deduction: sales stock deduction: order for out-of-stock product | API | P2 | not_run |
| TC-0542 | Stock deduction: sales stock deduction: order for low-stock product | API | P2 | not_run |

### Status transitions

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0543 | Status transitions: sales status transition: Pending to Confirmed | API | P2 | not_run |
| TC-0544 | Status transitions: sales status transition: Confirmed to Shipped | API | P2 | not_run |
| TC-0545 | Status transitions: sales status transition: Shipped to Delivered | API | P2 | not_run |
| TC-0546 | Status transitions: sales status transition: Pending to Shipped | API | P2 | not_run |
| TC-0547 | Status transitions: sales status transition: Pending to Delivered | API | P2 | not_run |
| TC-0548 | Status transitions: sales status transition: Confirmed to Delivered | API | P2 | not_run |
| TC-0549 | Status transitions: sales status transition: Delivered to Cancelled | API | P2 | not_run |
| TC-0550 | Status transitions: sales status transition: Cancelled to Confirmed | API | P2 | not_run |
| TC-0551 | Status transitions: sales status transition: unknown status | API | P2 | not_run |
| TC-0552 | Status transitions: sales status transition: same status | API | P2 | not_run |
| TC-0553 | Status transitions: sales status transition: Pending to Cancelled | API | P2 | not_run |
| TC-0554 | Status transitions: sales status transition: Confirmed to Cancelled | API | P2 | not_run |
| TC-0555 | Status transitions: sales status transition: Shipped to Cancelled | API | P2 | not_run |
| TC-0556 | Status transitions: sales status transition: Delivered to Delivered | API | P2 | not_run |
| TC-0557 | Status transitions: sales status transition: lowercase status value | API | P2 | not_run |

### Cancellation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0558 | Cancellation: sales cancellation: cancel pending | API | P2 | not_run |
| TC-0559 | Cancellation: sales cancellation: cancel confirmed | API | P2 | not_run |
| TC-0560 | Cancellation: sales cancellation: cancel shipped | API | P2 | not_run |
| TC-0561 | Cancellation: sales cancellation: cancel delivered | API | P2 | not_run |
| TC-0562 | Cancellation: sales cancellation: cancel already cancelled | API | P2 | not_run |
| TC-0563 | Cancellation: sales cancellation: stock restored once | API | P2 | not_run |
| TC-0564 | Cancellation: sales cancellation: history row created | API | P2 | not_run |
| TC-0565 | Cancellation: sales cancellation: cancellation reason | API | P2 | not_run |
| TC-0566 | Cancellation: sales cancellation: concurrent cancellation | API | P2 | not_run |
| TC-0567 | Cancellation: sales cancellation: cancel after stock-out | API | P2 | not_run |
| TC-0568 | Cancellation: sales cancellation: cancel after product delete attempt | API | P2 | not_run |
| TC-0569 | Cancellation: sales cancellation: cancel then delete | API | P2 | not_run |

### Update customer

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0570 | Update customer: update sales order: name | API | P2 | not_run |
| TC-0571 | Update customer: update sales order: email | API | P2 | not_run |
| TC-0572 | Update customer: update sales order: trim whitespace | API | P2 | not_run |
| TC-0573 | Update customer: update sales order: blank name | API | P2 | not_run |
| TC-0574 | Update customer: update sales order: clear email | API | P2 | not_run |
| TC-0575 | Update customer: update sales order: missing order | API | P2 | not_run |
| TC-0576 | Update customer: update sales order: invalid payload | API | P2 | not_run |
| TC-0577 | Update customer: update sales order: unicode name | API | P2 | not_run |
| TC-0578 | Update customer: update sales order: long name | API | P2 | not_run |
| TC-0579 | Update customer: update sales order: unchanged values | API | P2 | not_run |

### Delete restrictions

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0580 | Delete restrictions: delete sales order: delete pending order | API | P2 | not_run |
| TC-0581 | Delete restrictions: delete sales order: delete confirmed order | API | P2 | not_run |
| TC-0582 | Delete restrictions: delete sales order: delete shipped order | API | P2 | not_run |
| TC-0583 | Delete restrictions: delete sales order: delete delivered order | API | P2 | not_run |
| TC-0584 | Delete restrictions: delete sales order: delete cancelled order | API | P2 | not_run |
| TC-0585 | Delete restrictions: delete sales order: nonexistent order | API | P2 | not_run |
| TC-0586 | Delete restrictions: delete sales order: double delete | API | P2 | not_run |
| TC-0587 | Delete restrictions: delete sales order: database error during delete | API | P2 | not_run |

### UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0588 | UI: sales order UI: empty list | UI | P2 | not_run |
| TC-0589 | UI: sales order UI: list rendering | UI | P2 | not_run |
| TC-0590 | UI: sales order UI: status filter | UI | P2 | not_run |
| TC-0591 | UI: sales order UI: search customer | UI | P2 | not_run |
| TC-0592 | UI: sales order UI: search product | UI | P2 | not_run |
| TC-0593 | UI: sales order UI: sort order | UI | P2 | not_run |
| TC-0594 | UI: sales order UI: pagination | UI | P2 | not_run |
| TC-0595 | UI: sales order UI: create dialog | UI | P2 | not_run |
| TC-0596 | UI: sales order UI: edit dialog | UI | P2 | not_run |
| TC-0597 | UI: sales order UI: status control | UI | P2 | not_run |
| TC-0598 | UI: sales order UI: cancel confirmation | UI | P2 | not_run |
| TC-0599 | UI: sales order UI: error message | UI | P2 | not_run |
| TC-0600 | UI: sales order UI: loading state | UI | P2 | not_run |
| TC-0601 | UI: sales order UI: mobile layout | UI | P2 | not_run |
| TC-0602 | UI: sales order UI: keyboard navigation | UI | P2 | not_run |

### API security

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0603 | API security: sales API security: unauthenticated list | API | P2 | not_run |
| TC-0604 | API security: sales API security: unauthenticated create | API | P2 | not_run |
| TC-0605 | API security: sales API security: unauthenticated update | API | P2 | not_run |
| TC-0606 | API security: sales API security: unauthenticated status change | API | P2 | not_run |
| TC-0607 | API security: sales API security: unauthenticated delete | API | P2 | not_run |
| TC-0608 | API security: sales API security: 404 response | API | P2 | not_run |
| TC-0609 | API security: sales API security: 422 response | API | P2 | not_run |
| TC-0610 | API security: sales API security: 400 response | API | P2 | not_run |
| TC-0611 | API security: sales API security: 409 response | API | P2 | not_run |
| TC-0612 | API security: sales API security: 500 response | API | P2 | not_run |

### Concurrency

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0613 | Concurrency: sales concurrency: two orders for the last unit | API | P2 | blocked |
| TC-0614 | Concurrency: sales concurrency: cancel racing ship | API | P2 | blocked |
| TC-0615 | Concurrency: sales concurrency: two status updates for the same order | API | P2 | blocked |
| TC-0616 | Concurrency: sales concurrency: delete racing create | API | P2 | blocked |
| TC-0617 | Concurrency: sales concurrency: stock-out racing order creation | API | P2 | blocked |
| TC-0618 | Concurrency: sales concurrency: two simultaneous cancellations | API | P2 | blocked |
| TC-0619 | Concurrency: sales concurrency: two simultaneous customer updates | API | P2 | blocked |
| TC-0620 | Concurrency: sales concurrency: database lock contention | API | P2 | blocked |

## Purchase Orders

### Create

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0621 | Create: create purchase order: quantity 1 | API | P2 | not_run |
| TC-0622 | Create: create purchase order: quantity 10 | API | P2 | not_run |
| TC-0623 | Create: create purchase order: quantity 1000 | API | P2 | not_run |
| TC-0624 | Create: create purchase order: unit price 0 | API | P2 | not_run |
| TC-0625 | Create: create purchase order: decimal unit price | API | P2 | not_run |
| TC-0626 | Create: create purchase order: large total | API | P2 | not_run |
| TC-0627 | Create: create purchase order: supplier and product pair | API | P2 | not_run |
| TC-0628 | Create: create purchase order: pending status | API | P2 | not_run |
| TC-0629 | Create: create purchase order: total amount calculation | API | P2 | not_run |
| TC-0630 | Create: create purchase order: unicode supplier name | API | P2 | not_run |
| TC-0631 | Create: create purchase order: long supplier name | API | P2 | not_run |
| TC-0632 | Create: create purchase order: product with zero stock | API | P2 | not_run |
| TC-0633 | Create: create purchase order: product with high stock | API | P2 | not_run |
| TC-0634 | Create: create purchase order: no category | API | P2 | not_run |
| TC-0635 | Create: create purchase order: list refresh | API | P2 | not_run |

### Create validation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0636 | Create validation: reject purchase order: quantity 0 | API | P2 | not_run |
| TC-0637 | Create validation: reject purchase order: quantity -1 | API | P2 | not_run |
| TC-0638 | Create validation: reject purchase order: quantity 1.5 | API | P2 | not_run |
| TC-0639 | Create validation: reject purchase order: quantity as string | API | P2 | not_run |
| TC-0640 | Create validation: reject purchase order: missing supplier | API | P2 | not_run |
| TC-0641 | Create validation: reject purchase order: nonexistent supplier | API | P2 | not_run |
| TC-0642 | Create validation: reject purchase order: missing product | API | P2 | not_run |
| TC-0643 | Create validation: reject purchase order: nonexistent product | API | P2 | not_run |
| TC-0644 | Create validation: reject purchase order: negative unit price | API | P2 | not_run |
| TC-0645 | Create validation: reject purchase order: NaN unit price | API | P2 | not_run |
| TC-0646 | Create validation: reject purchase order: missing quantity | API | P2 | not_run |
| TC-0647 | Create validation: reject purchase order: malformed JSON | API | P2 | not_run |
| TC-0648 | Create validation: reject purchase order: unauthenticated request | API | P2 | not_run |
| TC-0649 | Create validation: reject purchase order: null body | API | P2 | not_run |
| TC-0650 | Create validation: reject purchase order: extra unknown fields | API | P2 | not_run |

### Status transitions

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0651 | Status transitions: purchase status transition: Pending to Approved | API | P2 | not_run |
| TC-0652 | Status transitions: purchase status transition: Approved to Ordered | API | P2 | not_run |
| TC-0653 | Status transitions: purchase status transition: Ordered to Received | API | P2 | not_run |
| TC-0654 | Status transitions: purchase status transition: Approved to Received | API | P2 | not_run |
| TC-0655 | Status transitions: purchase status transition: Pending to Received | API | P2 | not_run |
| TC-0656 | Status transitions: purchase status transition: Pending to Ordered | API | P2 | not_run |
| TC-0657 | Status transitions: purchase status transition: Ordered to Approved | API | P2 | not_run |
| TC-0658 | Status transitions: purchase status transition: Received to Cancelled | API | P2 | not_run |
| TC-0659 | Status transitions: purchase status transition: Cancelled to Approved | API | P2 | not_run |
| TC-0660 | Status transitions: purchase status transition: unknown status | API | P2 | not_run |
| TC-0661 | Status transitions: purchase status transition: same status | API | P2 | not_run |
| TC-0662 | Status transitions: purchase status transition: Pending to Cancelled | API | P2 | not_run |
| TC-0663 | Status transitions: purchase status transition: Approved to Cancelled | API | P2 | not_run |
| TC-0664 | Status transitions: purchase status transition: Ordered to Cancelled | API | P2 | not_run |
| TC-0665 | Status transitions: purchase status transition: lowercase status value | API | P2 | not_run |

### Receiving

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0666 | Receiving: purchase receiving: receive once adds stock | API | P2 | not_run |
| TC-0667 | Receiving: purchase receiving: receive twice does not double-add | API | P2 | not_run |
| TC-0668 | Receiving: purchase receiving: Approved to Received | API | P2 | not_run |
| TC-0669 | Receiving: purchase receiving: Ordered to Received | API | P2 | not_run |
| TC-0670 | Receiving: purchase receiving: Pending to Received | API | P2 | not_run |
| TC-0671 | Receiving: purchase receiving: history row created | API | P2 | not_run |
| TC-0672 | Receiving: purchase receiving: receiving reason | API | P2 | not_run |
| TC-0673 | Receiving: purchase receiving: stock levels after receive | API | P2 | not_run |
| TC-0674 | Receiving: purchase receiving: missing product | API | P2 | not_run |
| TC-0675 | Receiving: purchase receiving: missing supplier | API | P2 | not_run |
| TC-0676 | Receiving: purchase receiving: database error | API | P2 | not_run |
| TC-0677 | Receiving: purchase receiving: concurrent receive | API | P2 | not_run |

### Cancellation and delete

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0678 | Cancellation and delete: purchase cancellation or delete: cancel pending | API | P2 | not_run |
| TC-0679 | Cancellation and delete: purchase cancellation or delete: cancel approved | API | P2 | not_run |
| TC-0680 | Cancellation and delete: purchase cancellation or delete: cancel ordered | API | P2 | not_run |
| TC-0681 | Cancellation and delete: purchase cancellation or delete: cancel received | API | P2 | not_run |
| TC-0682 | Cancellation and delete: purchase cancellation or delete: cancel already cancelled | API | P2 | not_run |
| TC-0683 | Cancellation and delete: purchase cancellation or delete: delete pending | API | P2 | not_run |
| TC-0684 | Cancellation and delete: purchase cancellation or delete: delete approved | API | P2 | not_run |
| TC-0685 | Cancellation and delete: purchase cancellation or delete: delete ordered | API | P2 | not_run |
| TC-0686 | Cancellation and delete: purchase cancellation or delete: delete received | API | P2 | not_run |
| TC-0687 | Cancellation and delete: purchase cancellation or delete: delete cancelled | API | P2 | not_run |
| TC-0688 | Cancellation and delete: purchase cancellation or delete: nonexistent order | API | P2 | not_run |
| TC-0689 | Cancellation and delete: purchase cancellation or delete: database error | API | P2 | not_run |

### UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0690 | UI: purchase order UI: empty list | UI | P2 | not_run |
| TC-0691 | UI: purchase order UI: list rendering | UI | P2 | not_run |
| TC-0692 | UI: purchase order UI: status filter | UI | P2 | not_run |
| TC-0693 | UI: purchase order UI: search supplier | UI | P2 | not_run |
| TC-0694 | UI: purchase order UI: search product | UI | P2 | not_run |
| TC-0695 | UI: purchase order UI: sort order | UI | P2 | not_run |
| TC-0696 | UI: purchase order UI: pagination | UI | P2 | not_run |
| TC-0697 | UI: purchase order UI: create dialog | UI | P2 | not_run |
| TC-0698 | UI: purchase order UI: status control | UI | P2 | not_run |
| TC-0699 | UI: purchase order UI: receive confirmation | UI | P2 | not_run |
| TC-0700 | UI: purchase order UI: cancel confirmation | UI | P2 | not_run |
| TC-0701 | UI: purchase order UI: error message | UI | P2 | not_run |
| TC-0702 | UI: purchase order UI: loading state | UI | P2 | not_run |
| TC-0703 | UI: purchase order UI: mobile layout | UI | P2 | not_run |
| TC-0704 | UI: purchase order UI: keyboard navigation | UI | P2 | not_run |

### API security

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0705 | API security: purchase API security: unauthenticated list | API | P2 | not_run |
| TC-0706 | API security: purchase API security: unauthenticated create | API | P2 | not_run |
| TC-0707 | API security: purchase API security: unauthenticated status change | API | P2 | not_run |
| TC-0708 | API security: purchase API security: unauthenticated delete | API | P2 | not_run |
| TC-0709 | API security: purchase API security: 404 response | API | P2 | not_run |
| TC-0710 | API security: purchase API security: 422 response | API | P2 | not_run |
| TC-0711 | API security: purchase API security: 400 response | API | P2 | not_run |
| TC-0712 | API security: purchase API security: 409 response | API | P2 | not_run |
| TC-0713 | API security: purchase API security: 500 response | API | P2 | not_run |
| TC-0714 | API security: purchase API security: CORS preflight | API | P2 | not_run |
| TC-0715 | API security: purchase API security: malformed JSON | API | P2 | not_run |
| TC-0716 | API security: purchase API security: method not allowed | API | P2 | not_run |

### Relationships

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0717 | Relationships: purchase relationship: delete supplier with purchase order | API | P2 | not_run |
| TC-0718 | Relationships: purchase relationship: delete product with purchase order | API | P2 | not_run |
| TC-0719 | Relationships: purchase relationship: supplier missing | API | P2 | not_run |
| TC-0720 | Relationships: purchase relationship: product missing | API | P2 | not_run |
| TC-0721 | Relationships: purchase relationship: multiple orders for one supplier | API | P2 | not_run |
| TC-0722 | Relationships: purchase relationship: multiple products for one supplier | API | P2 | not_run |
| TC-0723 | Relationships: purchase relationship: supplier lead time used in planning | API | P2 | not_run |
| TC-0724 | Relationships: purchase relationship: unit price differs from product price | API | P2 | not_run |
| TC-0725 | Relationships: purchase relationship: delete supplier after receive | API | P2 | not_run |
| TC-0726 | Relationships: purchase relationship: delete supplier after cancellation | API | P2 | not_run |
| TC-0727 | Relationships: purchase relationship: delete product after cancellation | API | P2 | not_run |
| TC-0728 | Relationships: purchase relationship: delete product after receive | API | P2 | not_run |

### Concurrency

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0729 | Concurrency: purchase concurrency: two receive requests for the same order | API | P2 | blocked |
| TC-0730 | Concurrency: purchase concurrency: receive racing cancel | API | P2 | blocked |
| TC-0731 | Concurrency: purchase concurrency: approve racing receive | API | P2 | blocked |
| TC-0732 | Concurrency: purchase concurrency: delete racing receive | API | P2 | blocked |
| TC-0733 | Concurrency: purchase concurrency: stock-out racing receive | API | P2 | blocked |
| TC-0734 | Concurrency: purchase concurrency: two purchase orders for the same product | API | P2 | blocked |
| TC-0735 | Concurrency: purchase concurrency: database lock contention | API | P2 | blocked |
| TC-0736 | Concurrency: purchase concurrency: deadlock retry | API | P2 | blocked |
| TC-0737 | Concurrency: purchase concurrency: receive racing product update | API | P2 | blocked |
| TC-0738 | Concurrency: purchase concurrency: cancel racing status update | API | P2 | blocked |
| TC-0739 | Concurrency: purchase concurrency: two simultaneous deletes | API | P2 | blocked |
| TC-0740 | Concurrency: purchase concurrency: two simultaneous creates | API | P2 | blocked |

## Demand Forecast

### Data display

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0741 | Data display: forecast display: 7-day outlook | UI | P2 | not_run |
| TC-0742 | Data display: forecast display: product list | UI | P2 | not_run |
| TC-0743 | Data display: forecast display: forecast values | UI | P2 | not_run |
| TC-0744 | Data display: forecast display: reorder suggestions | UI | P2 | not_run |
| TC-0745 | Data display: forecast display: urgent items | UI | P2 | not_run |
| TC-0746 | Data display: forecast display: empty forecast | UI | P2 | not_run |
| TC-0747 | Data display: forecast display: one product | UI | P2 | not_run |
| TC-0748 | Data display: forecast display: many products | UI | P2 | not_run |
| TC-0749 | Data display: forecast display: loading state | UI | P2 | not_run |
| TC-0750 | Data display: forecast display: error state | UI | P2 | not_run |
| TC-0751 | Data display: forecast display: refresh | UI | P2 | not_run |
| TC-0752 | Data display: forecast display: stale data | UI | P2 | not_run |

### Reorder logic

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0753 | Reorder logic: reorder calculation: stock 0 | API | P2 | not_run |
| TC-0754 | Reorder logic: reorder calculation: stock below reorder level | API | P2 | not_run |
| TC-0755 | Reorder logic: reorder calculation: stock at reorder level | API | P2 | not_run |
| TC-0756 | Reorder logic: reorder calculation: stock above reorder level | API | P2 | not_run |
| TC-0757 | Reorder logic: reorder calculation: lead time 0 | API | P2 | not_run |
| TC-0758 | Reorder logic: reorder calculation: lead time 1 | API | P2 | not_run |
| TC-0759 | Reorder logic: reorder calculation: lead time 7 | API | P2 | not_run |
| TC-0760 | Reorder logic: reorder calculation: lead time 30 | API | P2 | not_run |
| TC-0761 | Reorder logic: reorder calculation: safety stock | API | P2 | not_run |
| TC-0762 | Reorder logic: reorder calculation: high demand | API | P2 | not_run |
| TC-0763 | Reorder logic: reorder calculation: low demand | API | P2 | not_run |
| TC-0764 | Reorder logic: reorder calculation: supplier missing | API | P2 | not_run |
| TC-0765 | Reorder logic: reorder calculation: reorder quantity 0 | API | P2 | not_run |
| TC-0766 | Reorder logic: reorder calculation: negative available stock | API | P2 | not_run |
| TC-0767 | Reorder logic: reorder calculation: very large demand | API | P2 | not_run |

### Filters

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0768 | Filters: forecast filter: All filter | UI | P2 | not_run |
| TC-0769 | Filters: forecast filter: Needs reorder filter | UI | P2 | not_run |
| TC-0770 | Filters: forecast filter: no matching rows | UI | P2 | not_run |
| TC-0771 | Filters: forecast filter: clear filter | UI | P2 | not_run |
| TC-0772 | Filters: forecast filter: count badge | UI | P2 | not_run |
| TC-0773 | Filters: forecast filter: mobile filter layout | UI | P2 | not_run |
| TC-0774 | Filters: forecast filter: keyboard filter use | UI | P2 | not_run |
| TC-0775 | Filters: forecast filter: filter after refresh | UI | P2 | not_run |

### Refresh and errors

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0776 | Refresh and errors: forecast refresh: refresh success | UI | P2 | not_run |
| TC-0777 | Refresh and errors: forecast refresh: refresh failure retains data | UI | P2 | not_run |
| TC-0778 | Refresh and errors: forecast refresh: retry after failure | UI | P2 | not_run |
| TC-0779 | Refresh and errors: forecast refresh: slow response | UI | P2 | not_run |
| TC-0780 | Refresh and errors: forecast refresh: 500 response | UI | P2 | not_run |
| TC-0781 | Refresh and errors: forecast refresh: network failure | UI | P2 | not_run |
| TC-0782 | Refresh and errors: forecast refresh: unauthorized response | UI | P2 | not_run |
| TC-0783 | Refresh and errors: forecast refresh: empty response | UI | P2 | not_run |

### Model integrity

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0784 | Model integrity: frozen model check: model file unchanged | API | P2 | not_run |
| TC-0785 | Model integrity: frozen model check: dataset unchanged | API | P2 | not_run |
| TC-0786 | Model integrity: frozen model check: reported metrics unchanged | API | P2 | not_run |
| TC-0787 | Model integrity: frozen model check: no retraining during request | API | P2 | not_run |
| TC-0788 | Model integrity: frozen model check: single forecast generation per request | API | P2 | not_run |
| TC-0789 | Model integrity: frozen model check: deterministic output for identical input | API | P2 | not_run |
| TC-0790 | Model integrity: frozen model check: no database writes during forecast | API | P2 | not_run |
| TC-0791 | Model integrity: frozen model check: model load failure | API | P2 | not_run |
| TC-0792 | Model integrity: frozen model check: missing model file | API | P2 | not_run |
| TC-0793 | Model integrity: frozen model check: model version recorded | API | P2 | not_run |

### ERP overlay

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0794 | ERP overlay: ERP overlay: exact product-name match | API | P2 | not_run |
| TC-0795 | ERP overlay: ERP overlay: case-insensitive match | API | P2 | not_run |
| TC-0796 | ERP overlay: ERP overlay: leading/trailing whitespace | API | P2 | not_run |
| TC-0797 | ERP overlay: ERP overlay: SKU-only match | API | P2 | not_run |
| TC-0798 | ERP overlay: ERP overlay: duplicate ERP product names | API | P2 | not_run |
| TC-0799 | ERP overlay: ERP overlay: no ERP match fallback | API | P2 | not_run |
| TC-0800 | ERP overlay: ERP overlay: ERP stock 0 | API | P2 | not_run |
| TC-0801 | ERP overlay: ERP overlay: ERP reorder level applied | API | P2 | not_run |
| TC-0802 | ERP overlay: ERP overlay: category assigned | API | P2 | not_run |
| TC-0803 | ERP overlay: ERP overlay: product deleted after forecast | API | P2 | not_run |

### 3D chart

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0804 | 3D chart: forecast 3D fallback: WebGL unavailable | UI | P2 | not_run |
| TC-0805 | 3D chart: forecast 3D fallback: empty data | UI | P2 | not_run |
| TC-0806 | 3D chart: forecast 3D fallback: one data point | UI | P2 | not_run |
| TC-0807 | 3D chart: forecast 3D fallback: many data points | UI | P2 | not_run |
| TC-0808 | 3D chart: forecast 3D fallback: window resize | UI | P2 | not_run |
| TC-0809 | 3D chart: forecast 3D fallback: mobile viewport | UI | P2 | not_run |
| TC-0810 | 3D chart: forecast 3D fallback: reduced motion | UI | P2 | not_run |

### Accessibility and responsive

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0811 | Accessibility and responsive: forecast accessibility: desktop 1440px | Accessibility | P2 | not_run |
| TC-0812 | Accessibility and responsive: forecast accessibility: tablet 768px | Accessibility | P2 | not_run |
| TC-0813 | Accessibility and responsive: forecast accessibility: mobile 390px | Accessibility | P2 | not_run |
| TC-0814 | Accessibility and responsive: forecast accessibility: table semantics | Accessibility | P2 | not_run |
| TC-0815 | Accessibility and responsive: forecast accessibility: heading order | Accessibility | P2 | not_run |
| TC-0816 | Accessibility and responsive: forecast accessibility: status announcements | Accessibility | P2 | not_run |
| TC-0817 | Accessibility and responsive: forecast accessibility: keyboard navigation | Accessibility | P2 | not_run |
| TC-0818 | Accessibility and responsive: forecast accessibility: color contrast | Accessibility | P2 | not_run |
| TC-0819 | Accessibility and responsive: forecast accessibility: chart alternative text | Accessibility | P2 | not_run |
| TC-0820 | Accessibility and responsive: forecast accessibility: reduced motion | Accessibility | P2 | not_run |

## NextGenERP Assistant

### Allowed scope

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0821 | Allowed scope: answer allowed topic: low stock | API | P2 | not_run |
| TC-0822 | Allowed scope: answer allowed topic: pending sales orders | API | P2 | not_run |
| TC-0823 | Allowed scope: answer allowed topic: pending purchase orders | API | P2 | not_run |
| TC-0824 | Allowed scope: answer allowed topic: product stock | API | P2 | not_run |
| TC-0825 | Allowed scope: answer allowed topic: supplier details | API | P2 | not_run |
| TC-0826 | Allowed scope: answer allowed topic: catalog counts | API | P2 | not_run |
| TC-0827 | Allowed scope: answer allowed topic: reorder needs | API | P2 | not_run |
| TC-0828 | Allowed scope: answer allowed topic: navigation help | API | P2 | not_run |
| TC-0829 | Allowed scope: answer allowed topic: add product help | API | P2 | not_run |
| TC-0830 | Allowed scope: answer allowed topic: forecast help | API | P2 | not_run |
| TC-0831 | Allowed scope: answer allowed topic: login help | API | P2 | not_run |
| TC-0832 | Allowed scope: answer allowed topic: dashboard help | API | P2 | not_run |

### Refused scope

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0833 | Refused scope: refuse off-topic topic: cricket result | API | P2 | not_run |
| TC-0834 | Refused scope: refuse off-topic topic: weather forecast | API | P2 | not_run |
| TC-0835 | Refused scope: refuse off-topic topic: world news | API | P2 | not_run |
| TC-0836 | Refused scope: refuse off-topic topic: coding question | API | P2 | not_run |
| TC-0837 | Refused scope: refuse off-topic topic: medical question | API | P2 | not_run |
| TC-0838 | Refused scope: refuse off-topic topic: legal question | API | P2 | not_run |
| TC-0839 | Refused scope: refuse off-topic topic: personal advice | API | P2 | not_run |
| TC-0840 | Refused scope: refuse off-topic topic: math problem | API | P2 | not_run |
| TC-0841 | Refused scope: refuse off-topic topic: translation request | API | P2 | not_run |
| TC-0842 | Refused scope: refuse off-topic topic: politics | API | P2 | not_run |
| TC-0843 | Refused scope: refuse off-topic topic: general knowledge | API | P2 | not_run |
| TC-0844 | Refused scope: refuse off-topic topic: prompt injection | API | P2 | not_run |

### Live data answers

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0845 | Live data answers: live-data answer: low-stock boundary | API | P2 | not_run |
| TC-0846 | Live data answers: live-data answer: out-of-stock list | API | P2 | not_run |
| TC-0847 | Live data answers: live-data answer: no low-stock items | API | P2 | not_run |
| TC-0848 | Live data answers: live-data answer: product by name | API | P2 | not_run |
| TC-0849 | Live data answers: live-data answer: product by SKU | API | P2 | not_run |
| TC-0850 | Live data answers: live-data answer: supplier details | API | P2 | not_run |
| TC-0851 | Live data answers: live-data answer: sales order lookup | API | P2 | not_run |
| TC-0852 | Live data answers: live-data answer: purchase order lookup | API | P2 | not_run |
| TC-0853 | Live data answers: live-data answer: catalog counts | API | P2 | not_run |
| TC-0854 | Live data answers: live-data answer: empty database | API | P2 | not_run |
| TC-0855 | Live data answers: live-data answer: many products | API | P2 | not_run |
| TC-0856 | Live data answers: live-data answer: unicode product name | API | P2 | not_run |
| TC-0857 | Live data answers: live-data answer: case-insensitive product name | API | P2 | not_run |
| TC-0858 | Live data answers: live-data answer: missing product | API | P2 | not_run |
| TC-0859 | Live data answers: live-data answer: deleted product | API | P2 | not_run |

### Help topics

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0860 | Help topics: help topic: add product | API | P2 | not_run |
| TC-0861 | Help topics: help topic: edit or delete product | API | P2 | not_run |
| TC-0862 | Help topics: help topic: record stock movement | API | P2 | not_run |
| TC-0863 | Help topics: help topic: create sales order | API | P2 | not_run |
| TC-0864 | Help topics: help topic: create purchase order | API | P2 | not_run |
| TC-0865 | Help topics: help topic: read demand forecast | API | P2 | not_run |
| TC-0866 | Help topics: help topic: sign in | API | P2 | not_run |
| TC-0867 | Help topics: help topic: roles and permissions | API | P2 | not_run |
| TC-0868 | Help topics: help topic: delete rules | API | P2 | not_run |
| TC-0869 | Help topics: help topic: common errors | API | P2 | not_run |

### LLM external provider

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0870 | LLM external provider: external provider: provider success | API | P2 | blocked |
| TC-0871 | LLM external provider: external provider: provider timeout | API | P2 | blocked |
| TC-0872 | LLM external provider: external provider: provider 401 | API | P2 | blocked |
| TC-0873 | LLM external provider: external provider: provider 429 | API | P2 | blocked |
| TC-0874 | LLM external provider: external provider: custom base URL | API | P2 | blocked |

### LLM local fallback

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0875 | LLM local fallback: local LLM behavior: no key configured | API | P2 | not_run |
| TC-0876 | LLM local fallback: local LLM behavior: provider request failure | API | P2 | not_run |
| TC-0877 | LLM local fallback: local LLM behavior: invalid provider JSON | API | P2 | not_run |
| TC-0878 | LLM local fallback: local LLM behavior: key never returned in response | API | P2 | not_run |
| TC-0879 | LLM local fallback: local LLM behavior: strict scope prompt sent | API | P2 | not_run |

### UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0880 | UI: launcher is visible | UI | P2 | passed |
| TC-0881 | UI: panel opens | UI | P2 | passed |
| TC-0882 | UI: panel closes | UI | P2 | passed |
| TC-0883 | UI: low-stock suggestion returns live answer | UI | P2 | passed |
| TC-0884 | UI: help suggestion returns steps | UI | P2 | passed |
| TC-0885 | UI: off-topic question is refused | UI | P2 | passed |
| TC-0886 | UI: mobile panel fits viewport | UI | P2 | passed |
| TC-0887 | UI: Escape closes panel | UI | P2 | passed |
| TC-0888 | UI: clear conversation | UI | P2 | not_run |
| TC-0889 | UI: suggestion chips | UI | P2 | not_run |
| TC-0890 | UI: retry after error | UI | P2 | not_run |
| TC-0891 | UI: focus and scroll behavior | UI | P2 | not_run |

### Security and privacy

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0892 | Security and privacy: assistant security: authentication required | API | P2 | not_run |
| TC-0893 | Security and privacy: assistant security: blank message rejected | API | P2 | not_run |
| TC-0894 | Security and privacy: assistant security: oversized message rejected | API | P2 | not_run |
| TC-0895 | Security and privacy: assistant security: over-long history rejected | API | P2 | not_run |
| TC-0896 | Security and privacy: assistant security: invalid role rejected | API | P2 | not_run |
| TC-0897 | Security and privacy: assistant security: no secrets in response | API | P2 | not_run |
| TC-0898 | Security and privacy: assistant security: off-topic refusal before provider call | API | P2 | not_run |
| TC-0899 | Security and privacy: assistant security: read-only claims | API | P2 | not_run |
| TC-0900 | Security and privacy: assistant security: XSS in user message | API | P2 | not_run |

## Navigation and UI

### Routes

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0901 | Routes: route: / | UI | P2 | not_run |
| TC-0902 | Routes: route: /forecasting | UI | P2 | not_run |
| TC-0903 | Routes: route: /products | UI | P2 | not_run |
| TC-0904 | Routes: route: /categories | UI | P2 | not_run |
| TC-0905 | Routes: route: /suppliers | UI | P2 | not_run |
| TC-0906 | Routes: route: /sales-orders | UI | P2 | not_run |
| TC-0907 | Routes: route: /purchase-orders | UI | P2 | not_run |
| TC-0908 | Routes: route: /inventory-operations | UI | P2 | not_run |
| TC-0909 | Routes: route: /auth | UI | P2 | not_run |
| TC-0910 | Routes: route: unknown route | UI | P2 | not_run |

### Sidebar and mobile

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0911 | Sidebar and mobile: shell navigation: desktop sidebar | UI | P2 | not_run |
| TC-0912 | Sidebar and mobile: shell navigation: mobile menu opens | UI | P2 | not_run |
| TC-0913 | Sidebar and mobile: shell navigation: mobile menu closes | UI | P2 | not_run |
| TC-0914 | Sidebar and mobile: shell navigation: overlay click closes | UI | P2 | not_run |
| TC-0915 | Sidebar and mobile: shell navigation: active route state | UI | P2 | not_run |
| TC-0916 | Sidebar and mobile: shell navigation: sign out | UI | P2 | not_run |
| TC-0917 | Sidebar and mobile: shell navigation: identity display | UI | P2 | not_run |
| TC-0918 | Sidebar and mobile: shell navigation: logo link | UI | P2 | not_run |

### Search jump

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0919 | Search jump: module search: exact page name | UI | P2 | not_run |
| TC-0920 | Search jump: module search: keyword 'stock' | UI | P2 | not_run |
| TC-0921 | Search jump: module search: keyword 'vendors' | UI | P2 | not_run |
| TC-0922 | Search jump: module search: case-insensitive match | UI | P2 | not_run |
| TC-0923 | Search jump: module search: no-match feedback | UI | P2 | not_run |
| TC-0924 | Search jump: module search: clear feedback | UI | P2 | not_run |
| TC-0925 | Search jump: module search: Enter submits | UI | P2 | not_run |
| TC-0926 | Search jump: module search: mobile hides search | UI | P2 | not_run |

### 404 and error boundary

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0927 | 404 and error boundary: unknown route shows Page not found | UI | P2 | passed |
| TC-0928 | 404 and error boundary: nested unknown route | UI | P2 | not_run |
| TC-0929 | 404 and error boundary: ErrorBoundary fallback | UI | P2 | not_run |
| TC-0930 | 404 and error boundary: ErrorBoundary resets on navigation | UI | P2 | not_run |
| TC-0931 | 404 and error boundary: browser back button | UI | P2 | not_run |
| TC-0932 | 404 and error boundary: direct load of unknown route | UI | P2 | not_run |

### Accessibility

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0933 | Accessibility: shell accessibility: skip link | Accessibility | P2 | not_run |
| TC-0934 | Accessibility: shell accessibility: focus visible | Accessibility | P2 | not_run |
| TC-0935 | Accessibility: shell accessibility: heading order | Accessibility | P2 | not_run |
| TC-0936 | Accessibility: shell accessibility: landmarks | Accessibility | P2 | not_run |
| TC-0937 | Accessibility: shell accessibility: form labels | Accessibility | P2 | not_run |
| TC-0938 | Accessibility: shell accessibility: table headers | Accessibility | P2 | not_run |
| TC-0939 | Accessibility: shell accessibility: aria-live announcements | Accessibility | P2 | not_run |
| TC-0940 | Accessibility: shell accessibility: color contrast | Accessibility | P2 | not_run |
| TC-0941 | Accessibility: shell accessibility: keyboard dialogs | Accessibility | P2 | not_run |
| TC-0942 | Accessibility: shell accessibility: reduced motion | Accessibility | P2 | not_run |

### Responsive

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0943 | Responsive: responsive layout: 320px width | Accessibility | P2 | not_run |
| TC-0944 | Responsive: responsive layout: 390px width | Accessibility | P2 | not_run |
| TC-0945 | Responsive: responsive layout: 768px width | Accessibility | P2 | not_run |
| TC-0946 | Responsive: responsive layout: 1024px width | Accessibility | P2 | not_run |
| TC-0947 | Responsive: responsive layout: 1440px width | Accessibility | P2 | not_run |
| TC-0948 | Responsive: responsive layout: 1920px width | Accessibility | P2 | not_run |
| TC-0949 | Responsive: responsive layout: landscape phone | Accessibility | P2 | not_run |
| TC-0950 | Responsive: responsive layout: 200% zoom | Accessibility | P2 | not_run |

## Security and API

### Authentication required

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0951 | Authentication required: unauthenticated access: GET /products/ | API | P2 | not_run |
| TC-0952 | Authentication required: unauthenticated access: POST /products/ | API | P2 | not_run |
| TC-0953 | Authentication required: unauthenticated access: GET /categories/ | API | P2 | not_run |
| TC-0954 | Authentication required: unauthenticated access: POST /categories/ | API | P2 | not_run |
| TC-0955 | Authentication required: unauthenticated access: GET /suppliers/ | API | P2 | not_run |
| TC-0956 | Authentication required: unauthenticated access: POST /suppliers/ | API | P2 | not_run |
| TC-0957 | Authentication required: unauthenticated access: GET /orders/ | API | P2 | not_run |
| TC-0958 | Authentication required: unauthenticated access: POST /orders/ | API | P2 | not_run |
| TC-0959 | Authentication required: unauthenticated access: GET /purchase-orders/ | API | P2 | not_run |
| TC-0960 | Authentication required: unauthenticated access: GET /inventory-transactions/ | API | P2 | not_run |
| TC-0961 | Authentication required: unauthenticated access: GET /ml/insights | API | P2 | not_run |
| TC-0962 | Authentication required: unauthenticated access: POST /assistant/chat | API | P2 | not_run |

### Input validation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0963 | Input validation: input attack: SQL injection in username | API | P2 | not_run |
| TC-0964 | Input validation: input attack: SQL injection in product name | API | P2 | not_run |
| TC-0965 | Input validation: input attack: SQL injection in search | API | P2 | not_run |
| TC-0966 | Input validation: input attack: SQL injection in customer name | API | P2 | not_run |
| TC-0967 | Input validation: input attack: SQL injection in supplier name | API | P2 | not_run |
| TC-0968 | Input validation: input attack: SQL injection in category name | API | P2 | not_run |
| TC-0969 | Input validation: input attack: SQL injection in inventory reason | API | P2 | not_run |
| TC-0970 | Input validation: input attack: script tag in assistant message | API | P2 | not_run |
| TC-0971 | Input validation: input attack: deeply nested JSON | API | P2 | not_run |
| TC-0972 | Input validation: input attack: oversized query parameter | API | P2 | not_run |

### CORS

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0973 | CORS: CORS behavior: allowed origin | API | P2 | not_run |
| TC-0974 | CORS: CORS behavior: disallowed origin | API | P2 | not_run |
| TC-0975 | CORS: CORS behavior: wildcard configuration rejected | API | P2 | not_run |
| TC-0976 | CORS: CORS behavior: preflight request | API | P2 | not_run |
| TC-0977 | CORS: CORS behavior: credentials disabled | API | P2 | not_run |
| TC-0978 | CORS: CORS behavior: allowed headers | API | P2 | not_run |

### Secrets and logging

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0979 | Secrets and logging: secret handling: JWT secret absent from responses | API | P2 | not_run |
| TC-0980 | Secrets and logging: secret handling: password absent from logs | API | P2 | not_run |
| TC-0981 | Secrets and logging: secret handling: assistant key absent from logs | API | P2 | not_run |
| TC-0982 | Secrets and logging: secret handling: database URL absent from responses | API | P2 | not_run |
| TC-0983 | Secrets and logging: secret handling: stack trace absent from 500 responses | API | P2 | not_run |
| TC-0984 | Secrets and logging: secret handling: token absent from URLs | API | P2 | not_run |
| TC-0985 | Secrets and logging: secret handling: .env ignored by git | API | P2 | not_run |
| TC-0986 | Secrets and logging: secret handling: sensitive docs skipped by retrieval | API | P2 | not_run |

### XSS and injection

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0987 | XSS and injection: XSS defense: script tag in product name | API | P2 | not_run |
| TC-0988 | XSS and injection: XSS defense: script tag in category name | API | P2 | not_run |
| TC-0989 | XSS and injection: XSS defense: script tag in supplier name | API | P2 | not_run |
| TC-0990 | XSS and injection: XSS defense: script tag in customer name | API | P2 | not_run |
| TC-0991 | XSS and injection: XSS defense: script tag in assistant reply | API | P2 | not_run |
| TC-0992 | XSS and injection: XSS defense: script tag in reason | API | P2 | not_run |
| TC-0993 | XSS and injection: XSS defense: stored XSS rendering | API | P2 | not_run |
| TC-0994 | XSS and injection: XSS defense: missing Content-Security-Policy | API | P2 | not_run |

### Rate limiting

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0995 | Rate limiting: rate limiting: login brute force | API | P2 | blocked |
| TC-0996 | Rate limiting: rate limiting: assistant abuse | API | P2 | blocked |
| TC-0997 | Rate limiting: rate limiting: registration spam | API | P2 | blocked |
| TC-0998 | Rate limiting: rate limiting: API burst | API | P2 | blocked |
| TC-0999 | Rate limiting: rate limiting: LLM cost abuse | API | P2 | blocked |
| TC-1000 | Rate limiting: rate limiting: 429 response behavior | API | P2 | blocked |

# NextGenERP Test Case Catalog

Generated: 2026-11-11

Total scenarios: **2000**

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
| NextGenERP Assistant | 80 | 21 | 52 | 7 |
| Voice Assistant | 1000 | 53 | 947 | 0 |
| Navigation and UI | 50 | 1 | 49 | 0 |
| Security and API | 50 | 0 | 44 | 6 |
| **Total** | **2000** | **80** | **1879** | **41** |

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
| TC-0826 | Allowed scope: answer allowed topic: reorder needs | API | P2 | not_run |
| TC-0827 | Allowed scope: answer allowed topic: navigation help | API | P2 | not_run |
| TC-0828 | Allowed scope: answer allowed topic: add product help | API | P2 | not_run |
| TC-0829 | Allowed scope: answer allowed topic: forecast help | API | P2 | not_run |
| TC-0830 | Allowed scope: answer allowed topic: login help | API | P2 | not_run |

### Refused scope

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0831 | Refused scope: refuse off-topic topic: cricket result | API | P2 | not_run |
| TC-0832 | Refused scope: refuse off-topic topic: weather forecast | API | P2 | not_run |
| TC-0833 | Refused scope: refuse off-topic topic: world news | API | P2 | not_run |
| TC-0834 | Refused scope: refuse off-topic topic: coding question | API | P2 | not_run |
| TC-0835 | Refused scope: refuse off-topic topic: medical question | API | P2 | not_run |
| TC-0836 | Refused scope: refuse off-topic topic: legal question | API | P2 | not_run |
| TC-0837 | Refused scope: refuse off-topic topic: personal advice | API | P2 | not_run |
| TC-0838 | Refused scope: refuse off-topic topic: math problem | API | P2 | not_run |
| TC-0839 | Refused scope: refuse off-topic topic: general knowledge | API | P2 | not_run |
| TC-0840 | Refused scope: refuse off-topic topic: prompt injection | API | P2 | not_run |

### Live data answers

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0841 | Live data answers: live-data answer: low-stock boundary | API | P2 | not_run |
| TC-0842 | Live data answers: live-data answer: out-of-stock list | API | P2 | not_run |
| TC-0843 | Live data answers: live-data answer: no low-stock items | API | P2 | not_run |
| TC-0844 | Live data answers: live-data answer: product by name | API | P2 | not_run |
| TC-0845 | Live data answers: live-data answer: product by SKU | API | P2 | not_run |
| TC-0846 | Live data answers: live-data answer: supplier details | API | P2 | not_run |
| TC-0847 | Live data answers: live-data answer: sales order lookup | API | P2 | not_run |
| TC-0848 | Live data answers: live-data answer: purchase order lookup | API | P2 | not_run |
| TC-0849 | Live data answers: live-data answer: catalog counts | API | P2 | not_run |
| TC-0850 | Live data answers: live-data answer: empty database | API | P2 | not_run |
| TC-0851 | Live data answers: live-data answer: many products | API | P2 | not_run |
| TC-0852 | Live data answers: live-data answer: unicode product name | API | P2 | not_run |

### Help topics

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0853 | Help topics: help topic: add product | API | P2 | not_run |
| TC-0854 | Help topics: help topic: edit or delete product | API | P2 | not_run |
| TC-0855 | Help topics: help topic: record stock movement | API | P2 | not_run |
| TC-0856 | Help topics: help topic: create sales order | API | P2 | not_run |
| TC-0857 | Help topics: help topic: create purchase order | API | P2 | not_run |
| TC-0858 | Help topics: help topic: read demand forecast | API | P2 | not_run |
| TC-0859 | Help topics: help topic: delete rules | API | P2 | not_run |
| TC-0860 | Help topics: help topic: common errors | API | P2 | not_run |

### LLM external provider

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0861 | LLM external provider: external provider: provider success | API | P2 | blocked |
| TC-0862 | LLM external provider: external provider: provider timeout | API | P2 | blocked |
| TC-0863 | LLM external provider: external provider: provider 401 | API | P2 | blocked |
| TC-0864 | LLM external provider: external provider: provider 429 | API | P2 | blocked |
| TC-0865 | LLM external provider: external provider: custom base URL | API | P2 | blocked |

### LLM local fallback

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0866 | LLM local fallback: local LLM behavior: no key configured | API | P2 | not_run |
| TC-0867 | LLM local fallback: local LLM behavior: provider request failure | API | P2 | not_run |
| TC-0868 | LLM local fallback: local LLM behavior: key never returned in response | API | P2 | not_run |
| TC-0869 | LLM local fallback: local LLM behavior: strict scope prompt sent | API | P2 | not_run |

### UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0870 | UI: launcher is visible | UI | P2 | passed |
| TC-0871 | UI: panel opens | UI | P2 | passed |
| TC-0872 | UI: panel closes | UI | P2 | passed |
| TC-0873 | UI: low-stock suggestion returns live answer | UI | P2 | passed |
| TC-0874 | UI: help suggestion returns steps | UI | P2 | passed |
| TC-0875 | UI: off-topic question is refused | UI | P2 | passed |
| TC-0876 | UI: mobile panel fits viewport | UI | P2 | passed |
| TC-0877 | UI: Escape closes panel | UI | P2 | passed |

### Localization

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0878 | Localization: Hindi greeting returns a localized intro and suggestions | API | P2 | passed |
| TC-0879 | Localization: Bengali greeting returns a localized intro and suggestions | API | P2 | passed |
| TC-0880 | Localization: Devanagari combining-mark greeting is recognized | API | P2 | passed |
| TC-0881 | Localization: Hindi live low-stock answer is localized | API | P2 | passed |
| TC-0882 | Localization: Bengali live low-stock answer is localized | API | P2 | passed |
| TC-0883 | Localization: localized help topic answer | API | P2 | passed |
| TC-0884 | Localization: localized scope refusal in Hindi and Bengali | API | P2 | passed |
| TC-0885 | Localization: unsupported language code is rejected | API | P2 | passed |
| TC-0886 | Localization: LLM receives an explicit language instruction | API | P2 | passed |

### Voice UI

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0887 | Voice UI: language selector lists English, Hindi and Bengali | UI | P2 | passed |
| TC-0888 | Voice UI: language switch updates welcome and suggestions | UI | P2 | passed |
| TC-0889 | Voice UI: microphone control is enabled when supported | UI | P2 | passed |
| TC-0890 | Voice UI: speaker play/stop and auto-speak toggle | UI | P2 | passed |
| TC-0891 | Voice UI: actual microphone capture and permission grant | UI | P2 | blocked |
| TC-0892 | Voice UI: cross-browser voice support | UI | P2 | blocked |

### Security and privacy

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0893 | Security and privacy: assistant security: authentication required | API | P2 | not_run |
| TC-0894 | Security and privacy: assistant security: blank message rejected | API | P2 | not_run |
| TC-0895 | Security and privacy: assistant security: oversized message rejected | API | P2 | not_run |
| TC-0896 | Security and privacy: assistant security: over-long history rejected | API | P2 | not_run |
| TC-0897 | Security and privacy: assistant security: no secrets in response | API | P2 | not_run |
| TC-0898 | Security and privacy: assistant security: off-topic refusal before provider call | API | P2 | not_run |
| TC-0899 | Security and privacy: assistant security: read-only claims | API | P2 | not_run |
| TC-0900 | Security and privacy: assistant security: XSS in user message | API | P2 | not_run |

## Voice Assistant

### Support detection

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0901 | Support detection: Microsoft Edge with standard SpeechRecognition present | UI | P1 | passed |
| TC-0902 | Support detection: Microsoft Edge with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0903 | Support detection: Microsoft Edge with SpeechRecognition absent | UI | P1 | passed |
| TC-0904 | Support detection: Microsoft Edge with insecure HTTP origin | UI | P1 | passed |
| TC-0905 | Support detection: Microsoft Edge with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0906 | Support detection: Google Chrome with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0907 | Support detection: Google Chrome with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0908 | Support detection: Google Chrome with SpeechRecognition absent | UI | P1 | not_run |
| TC-0909 | Support detection: Google Chrome with insecure HTTP origin | UI | P1 | not_run |
| TC-0910 | Support detection: Google Chrome with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0911 | Support detection: Mozilla Firefox with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0912 | Support detection: Mozilla Firefox with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0913 | Support detection: Mozilla Firefox with SpeechRecognition absent | UI | P1 | not_run |
| TC-0914 | Support detection: Mozilla Firefox with insecure HTTP origin | UI | P1 | not_run |
| TC-0915 | Support detection: Mozilla Firefox with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0916 | Support detection: Apple Safari with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0917 | Support detection: Apple Safari with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0918 | Support detection: Apple Safari with SpeechRecognition absent | UI | P1 | not_run |
| TC-0919 | Support detection: Apple Safari with insecure HTTP origin | UI | P1 | not_run |
| TC-0920 | Support detection: Apple Safari with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0921 | Support detection: Opera with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0922 | Support detection: Opera with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0923 | Support detection: Opera with SpeechRecognition absent | UI | P1 | not_run |
| TC-0924 | Support detection: Opera with insecure HTTP origin | UI | P1 | not_run |
| TC-0925 | Support detection: Opera with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0926 | Support detection: Brave with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0927 | Support detection: Brave with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0928 | Support detection: Brave with SpeechRecognition absent | UI | P1 | not_run |
| TC-0929 | Support detection: Brave with insecure HTTP origin | UI | P1 | not_run |
| TC-0930 | Support detection: Brave with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0931 | Support detection: Samsung Internet with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0932 | Support detection: Samsung Internet with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0933 | Support detection: Samsung Internet with SpeechRecognition absent | UI | P1 | not_run |
| TC-0934 | Support detection: Samsung Internet with insecure HTTP origin | UI | P1 | not_run |
| TC-0935 | Support detection: Samsung Internet with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0936 | Support detection: Chrome on Android with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0937 | Support detection: Chrome on Android with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0938 | Support detection: Chrome on Android with SpeechRecognition absent | UI | P1 | not_run |
| TC-0939 | Support detection: Chrome on Android with insecure HTTP origin | UI | P1 | not_run |
| TC-0940 | Support detection: Chrome on Android with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0941 | Support detection: Safari on iOS with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0942 | Support detection: Safari on iOS with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0943 | Support detection: Safari on iOS with SpeechRecognition absent | UI | P1 | not_run |
| TC-0944 | Support detection: Safari on iOS with insecure HTTP origin | UI | P1 | not_run |
| TC-0945 | Support detection: Safari on iOS with speechSynthesis present but no voices installed | UI | P1 | not_run |
| TC-0946 | Support detection: Firefox on Android with standard SpeechRecognition present | UI | P1 | not_run |
| TC-0947 | Support detection: Firefox on Android with only webkitSpeechRecognition present | UI | P1 | not_run |
| TC-0948 | Support detection: Firefox on Android with SpeechRecognition absent | UI | P1 | not_run |
| TC-0949 | Support detection: Firefox on Android with insecure HTTP origin | UI | P1 | not_run |
| TC-0950 | Support detection: Firefox on Android with speechSynthesis present but no voices installed | UI | P1 | not_run |

### Permission and errors

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-0951 | Permission and errors: recognition error: not-allowed on the first attempt | UI | P1 | not_run |
| TC-0952 | Permission and errors: recognition error: not-allowed after the user denied permission | UI | P1 | not_run |
| TC-0953 | Permission and errors: recognition error: not-allowed after permission is granted | UI | P1 | not_run |
| TC-0954 | Permission and errors: recognition error: not-allowed after a page reload | UI | P1 | not_run |
| TC-0955 | Permission and errors: recognition error: not-allowed while an answer is sending | UI | P1 | not_run |
| TC-0956 | Permission and errors: recognition error: not-allowed after switching to Hindi | UI | P1 | passed |
| TC-0957 | Permission and errors: recognition error: not-allowed after switching to Bengali | UI | P1 | not_run |
| TC-0958 | Permission and errors: recognition error: not-allowed after closing the panel | UI | P1 | not_run |
| TC-0959 | Permission and errors: recognition error: not-allowed on a repeated start click | UI | P1 | not_run |
| TC-0960 | Permission and errors: recognition error: not-allowed after a 15-second silence | UI | P1 | not_run |
| TC-0961 | Permission and errors: recognition error: service-not-allowed on the first attempt | UI | P1 | not_run |
| TC-0962 | Permission and errors: recognition error: service-not-allowed after the user denied permission | UI | P1 | not_run |
| TC-0963 | Permission and errors: recognition error: service-not-allowed after permission is granted | UI | P1 | not_run |
| TC-0964 | Permission and errors: recognition error: service-not-allowed after a page reload | UI | P1 | not_run |
| TC-0965 | Permission and errors: recognition error: service-not-allowed while an answer is sending | UI | P1 | not_run |
| TC-0966 | Permission and errors: recognition error: service-not-allowed after switching to Hindi | UI | P1 | not_run |
| TC-0967 | Permission and errors: recognition error: service-not-allowed after switching to Bengali | UI | P1 | not_run |
| TC-0968 | Permission and errors: recognition error: service-not-allowed after closing the panel | UI | P1 | not_run |
| TC-0969 | Permission and errors: recognition error: service-not-allowed on a repeated start click | UI | P1 | not_run |
| TC-0970 | Permission and errors: recognition error: service-not-allowed after a 15-second silence | UI | P1 | not_run |
| TC-0971 | Permission and errors: recognition error: no-speech on the first attempt | UI | P1 | not_run |
| TC-0972 | Permission and errors: recognition error: no-speech after the user denied permission | UI | P1 | not_run |
| TC-0973 | Permission and errors: recognition error: no-speech after permission is granted | UI | P1 | not_run |
| TC-0974 | Permission and errors: recognition error: no-speech after a page reload | UI | P1 | not_run |
| TC-0975 | Permission and errors: recognition error: no-speech while an answer is sending | UI | P1 | not_run |
| TC-0976 | Permission and errors: recognition error: no-speech after switching to Hindi | UI | P1 | not_run |
| TC-0977 | Permission and errors: recognition error: no-speech after switching to Bengali | UI | P1 | not_run |
| TC-0978 | Permission and errors: recognition error: no-speech after closing the panel | UI | P1 | not_run |
| TC-0979 | Permission and errors: recognition error: no-speech on a repeated start click | UI | P1 | not_run |
| TC-0980 | Permission and errors: recognition error: no-speech after a 15-second silence | UI | P1 | not_run |
| TC-0981 | Permission and errors: recognition error: audio-capture on the first attempt | UI | P1 | not_run |
| TC-0982 | Permission and errors: recognition error: audio-capture after the user denied permission | UI | P1 | not_run |
| TC-0983 | Permission and errors: recognition error: audio-capture after permission is granted | UI | P1 | not_run |
| TC-0984 | Permission and errors: recognition error: audio-capture after a page reload | UI | P1 | not_run |
| TC-0985 | Permission and errors: recognition error: audio-capture while an answer is sending | UI | P1 | not_run |
| TC-0986 | Permission and errors: recognition error: audio-capture after switching to Hindi | UI | P1 | not_run |
| TC-0987 | Permission and errors: recognition error: audio-capture after switching to Bengali | UI | P1 | not_run |
| TC-0988 | Permission and errors: recognition error: audio-capture after closing the panel | UI | P1 | not_run |
| TC-0989 | Permission and errors: recognition error: audio-capture on a repeated start click | UI | P1 | not_run |
| TC-0990 | Permission and errors: recognition error: audio-capture after a 15-second silence | UI | P1 | not_run |
| TC-0991 | Permission and errors: recognition error: network on the first attempt | UI | P1 | not_run |
| TC-0992 | Permission and errors: recognition error: network after the user denied permission | UI | P1 | not_run |
| TC-0993 | Permission and errors: recognition error: network after permission is granted | UI | P1 | not_run |
| TC-0994 | Permission and errors: recognition error: network after a page reload | UI | P1 | not_run |
| TC-0995 | Permission and errors: recognition error: network while an answer is sending | UI | P1 | not_run |
| TC-0996 | Permission and errors: recognition error: network after switching to Hindi | UI | P1 | not_run |
| TC-0997 | Permission and errors: recognition error: network after switching to Bengali | UI | P1 | passed |
| TC-0998 | Permission and errors: recognition error: network after closing the panel | UI | P1 | not_run |
| TC-0999 | Permission and errors: recognition error: network on a repeated start click | UI | P1 | not_run |
| TC-1000 | Permission and errors: recognition error: network after a 15-second silence | UI | P1 | not_run |
| TC-1001 | Permission and errors: recognition error: language-not-supported on the first attempt | UI | P1 | not_run |
| TC-1002 | Permission and errors: recognition error: language-not-supported after the user denied permission | UI | P1 | not_run |
| TC-1003 | Permission and errors: recognition error: language-not-supported after permission is granted | UI | P1 | not_run |
| TC-1004 | Permission and errors: recognition error: language-not-supported after a page reload | UI | P1 | not_run |
| TC-1005 | Permission and errors: recognition error: language-not-supported while an answer is sending | UI | P1 | not_run |
| TC-1006 | Permission and errors: recognition error: language-not-supported after switching to Hindi | UI | P1 | not_run |
| TC-1007 | Permission and errors: recognition error: language-not-supported after switching to Bengali | UI | P1 | not_run |
| TC-1008 | Permission and errors: recognition error: language-not-supported after closing the panel | UI | P1 | not_run |
| TC-1009 | Permission and errors: recognition error: language-not-supported on a repeated start click | UI | P1 | not_run |
| TC-1010 | Permission and errors: recognition error: language-not-supported after a 15-second silence | UI | P1 | not_run |
| TC-1011 | Permission and errors: recognition error: aborted on the first attempt | UI | P1 | not_run |
| TC-1012 | Permission and errors: recognition error: aborted after the user denied permission | UI | P1 | not_run |
| TC-1013 | Permission and errors: recognition error: aborted after permission is granted | UI | P1 | not_run |
| TC-1014 | Permission and errors: recognition error: aborted after a page reload | UI | P1 | not_run |
| TC-1015 | Permission and errors: recognition error: aborted while an answer is sending | UI | P1 | not_run |
| TC-1016 | Permission and errors: recognition error: aborted after switching to Hindi | UI | P1 | not_run |
| TC-1017 | Permission and errors: recognition error: aborted after switching to Bengali | UI | P1 | not_run |
| TC-1018 | Permission and errors: recognition error: aborted after closing the panel | UI | P1 | not_run |
| TC-1019 | Permission and errors: recognition error: aborted on a repeated start click | UI | P1 | not_run |
| TC-1020 | Permission and errors: recognition error: aborted after a 15-second silence | UI | P1 | not_run |
| TC-1021 | Permission and errors: recognition error: busy on the first attempt | UI | P1 | not_run |
| TC-1022 | Permission and errors: recognition error: busy after the user denied permission | UI | P1 | not_run |
| TC-1023 | Permission and errors: recognition error: busy after permission is granted | UI | P1 | not_run |
| TC-1024 | Permission and errors: recognition error: busy after a page reload | UI | P1 | not_run |
| TC-1025 | Permission and errors: recognition error: busy while an answer is sending | UI | P1 | not_run |
| TC-1026 | Permission and errors: recognition error: busy after switching to Hindi | UI | P1 | not_run |
| TC-1027 | Permission and errors: recognition error: busy after switching to Bengali | UI | P1 | not_run |
| TC-1028 | Permission and errors: recognition error: busy after closing the panel | UI | P1 | not_run |
| TC-1029 | Permission and errors: recognition error: busy on a repeated start click | UI | P1 | not_run |
| TC-1030 | Permission and errors: recognition error: busy after a 15-second silence | UI | P1 | not_run |

### Locale coverage

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1031 | Locale coverage: locale: en-IN recognition language assignment | UI | P2 | passed |
| TC-1032 | Locale coverage: locale: en-IN speech synthesis language assignment | UI | P2 | passed |
| TC-1033 | Locale coverage: locale: en-IN exact voice match | UI | P2 | passed |
| TC-1034 | Locale coverage: locale: en-IN same-language voice fallback | UI | P2 | not_run |
| TC-1035 | Locale coverage: locale: en-IN default voice fallback | UI | P2 | not_run |
| TC-1036 | Locale coverage: locale: en-IN localized welcome text | UI | P2 | passed |
| TC-1037 | Locale coverage: locale: en-IN localized suggestion chips | UI | P2 | passed |
| TC-1038 | Locale coverage: locale: en-IN localized scope refusal | UI | P2 | not_run |
| TC-1039 | Locale coverage: locale: hi-IN recognition language assignment | UI | P2 | passed |
| TC-1040 | Locale coverage: locale: hi-IN speech synthesis language assignment | UI | P2 | passed |
| TC-1041 | Locale coverage: locale: hi-IN exact voice match | UI | P2 | passed |
| TC-1042 | Locale coverage: locale: hi-IN same-language voice fallback | UI | P2 | not_run |
| TC-1043 | Locale coverage: locale: hi-IN default voice fallback | UI | P2 | not_run |
| TC-1044 | Locale coverage: locale: hi-IN localized welcome text | UI | P2 | passed |
| TC-1045 | Locale coverage: locale: hi-IN localized suggestion chips | UI | P2 | passed |
| TC-1046 | Locale coverage: locale: hi-IN localized scope refusal | UI | P2 | not_run |
| TC-1047 | Locale coverage: locale: bn-IN recognition language assignment | UI | P2 | not_run |
| TC-1048 | Locale coverage: locale: bn-IN speech synthesis language assignment | UI | P2 | passed |
| TC-1049 | Locale coverage: locale: bn-IN exact voice match | UI | P2 | passed |
| TC-1050 | Locale coverage: locale: bn-IN same-language voice fallback | UI | P2 | not_run |
| TC-1051 | Locale coverage: locale: bn-IN default voice fallback | UI | P2 | not_run |
| TC-1052 | Locale coverage: locale: bn-IN localized welcome text | UI | P2 | passed |
| TC-1053 | Locale coverage: locale: bn-IN localized suggestion chips | UI | P2 | passed |
| TC-1054 | Locale coverage: locale: bn-IN localized scope refusal | UI | P2 | passed |
| TC-1055 | Locale coverage: locale: en-US recognition language assignment | UI | P2 | not_run |
| TC-1056 | Locale coverage: locale: en-US speech synthesis language assignment | UI | P2 | not_run |
| TC-1057 | Locale coverage: locale: en-US exact voice match | UI | P2 | not_run |
| TC-1058 | Locale coverage: locale: en-US same-language voice fallback | UI | P2 | not_run |
| TC-1059 | Locale coverage: locale: en-US default voice fallback | UI | P2 | not_run |
| TC-1060 | Locale coverage: locale: en-US localized welcome text | UI | P2 | not_run |
| TC-1061 | Locale coverage: locale: en-US localized suggestion chips | UI | P2 | not_run |
| TC-1062 | Locale coverage: locale: en-US localized scope refusal | UI | P2 | not_run |
| TC-1063 | Locale coverage: locale: en-GB recognition language assignment | UI | P2 | not_run |
| TC-1064 | Locale coverage: locale: en-GB speech synthesis language assignment | UI | P2 | not_run |
| TC-1065 | Locale coverage: locale: en-GB exact voice match | UI | P2 | not_run |
| TC-1066 | Locale coverage: locale: en-GB same-language voice fallback | UI | P2 | not_run |
| TC-1067 | Locale coverage: locale: en-GB default voice fallback | UI | P2 | not_run |
| TC-1068 | Locale coverage: locale: en-GB localized welcome text | UI | P2 | not_run |
| TC-1069 | Locale coverage: locale: en-GB localized suggestion chips | UI | P2 | not_run |
| TC-1070 | Locale coverage: locale: en-GB localized scope refusal | UI | P2 | not_run |
| TC-1071 | Locale coverage: locale: hi-Latn recognition language assignment | UI | P2 | not_run |
| TC-1072 | Locale coverage: locale: hi-Latn speech synthesis language assignment | UI | P2 | not_run |
| TC-1073 | Locale coverage: locale: hi-Latn exact voice match | UI | P2 | not_run |
| TC-1074 | Locale coverage: locale: hi-Latn same-language voice fallback | UI | P2 | not_run |
| TC-1075 | Locale coverage: locale: hi-Latn default voice fallback | UI | P2 | not_run |
| TC-1076 | Locale coverage: locale: hi-Latn localized welcome text | UI | P2 | not_run |
| TC-1077 | Locale coverage: locale: hi-Latn localized suggestion chips | UI | P2 | not_run |
| TC-1078 | Locale coverage: locale: hi-Latn localized scope refusal | UI | P2 | not_run |
| TC-1079 | Locale coverage: locale: bn-BD recognition language assignment | UI | P2 | not_run |
| TC-1080 | Locale coverage: locale: bn-BD speech synthesis language assignment | UI | P2 | not_run |
| TC-1081 | Locale coverage: locale: bn-BD exact voice match | UI | P2 | not_run |
| TC-1082 | Locale coverage: locale: bn-BD same-language voice fallback | UI | P2 | not_run |
| TC-1083 | Locale coverage: locale: bn-BD default voice fallback | UI | P2 | not_run |
| TC-1084 | Locale coverage: locale: bn-BD localized welcome text | UI | P2 | not_run |
| TC-1085 | Locale coverage: locale: bn-BD localized suggestion chips | UI | P2 | not_run |
| TC-1086 | Locale coverage: locale: bn-BD localized scope refusal | UI | P2 | not_run |
| TC-1087 | Locale coverage: locale: en-AU recognition language assignment | UI | P2 | not_run |
| TC-1088 | Locale coverage: locale: en-AU speech synthesis language assignment | UI | P2 | not_run |
| TC-1089 | Locale coverage: locale: en-AU exact voice match | UI | P2 | not_run |
| TC-1090 | Locale coverage: locale: en-AU same-language voice fallback | UI | P2 | not_run |
| TC-1091 | Locale coverage: locale: en-AU default voice fallback | UI | P2 | not_run |
| TC-1092 | Locale coverage: locale: en-AU localized welcome text | UI | P2 | not_run |
| TC-1093 | Locale coverage: locale: en-AU localized suggestion chips | UI | P2 | not_run |
| TC-1094 | Locale coverage: locale: en-AU localized scope refusal | UI | P2 | not_run |
| TC-1095 | Locale coverage: locale: hi-IN Devanagari recognition language assignment | UI | P2 | not_run |
| TC-1096 | Locale coverage: locale: hi-IN Devanagari speech synthesis language assignment | UI | P2 | not_run |
| TC-1097 | Locale coverage: locale: hi-IN Devanagari exact voice match | UI | P2 | not_run |
| TC-1098 | Locale coverage: locale: hi-IN Devanagari same-language voice fallback | UI | P2 | not_run |
| TC-1099 | Locale coverage: locale: hi-IN Devanagari default voice fallback | UI | P2 | not_run |
| TC-1100 | Locale coverage: locale: hi-IN Devanagari localized welcome text | UI | P2 | not_run |
| TC-1101 | Locale coverage: locale: hi-IN Devanagari localized suggestion chips | UI | P2 | not_run |
| TC-1102 | Locale coverage: locale: hi-IN Devanagari localized scope refusal | UI | P2 | not_run |
| TC-1103 | Locale coverage: locale: bn-IN Bengali script recognition language assignment | UI | P2 | not_run |
| TC-1104 | Locale coverage: locale: bn-IN Bengali script speech synthesis language assignment | UI | P2 | not_run |
| TC-1105 | Locale coverage: locale: bn-IN Bengali script exact voice match | UI | P2 | not_run |
| TC-1106 | Locale coverage: locale: bn-IN Bengali script same-language voice fallback | UI | P2 | not_run |
| TC-1107 | Locale coverage: locale: bn-IN Bengali script default voice fallback | UI | P2 | not_run |
| TC-1108 | Locale coverage: locale: bn-IN Bengali script localized welcome text | UI | P2 | not_run |
| TC-1109 | Locale coverage: locale: bn-IN Bengali script localized suggestion chips | UI | P2 | not_run |
| TC-1110 | Locale coverage: locale: bn-IN Bengali script localized scope refusal | UI | P2 | not_run |

### Recognition lifecycle

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1111 | Recognition lifecycle: click the microphone while idle | UI | P1 | not_run |
| TC-1112 | Recognition lifecycle: click the microphone while starting | UI | P1 | not_run |
| TC-1113 | Recognition lifecycle: click the microphone while actively listening | UI | P1 | passed |
| TC-1114 | Recognition lifecycle: click the microphone while showing an interim transcript | UI | P1 | not_run |
| TC-1115 | Recognition lifecycle: click the microphone while showing a final transcript | UI | P1 | not_run |
| TC-1116 | Recognition lifecycle: click the microphone while sending a request | UI | P1 | not_run |
| TC-1117 | Recognition lifecycle: click the microphone while showing an error | UI | P1 | not_run |
| TC-1118 | Recognition lifecycle: click the microphone while the panel is closed | UI | P1 | not_run |
| TC-1119 | Recognition lifecycle: click the microphone while Hindi is selected | UI | P1 | not_run |
| TC-1120 | Recognition lifecycle: click the microphone while Bengali is selected | UI | P1 | not_run |
| TC-1121 | Recognition lifecycle: click stop listening while idle | UI | P1 | not_run |
| TC-1122 | Recognition lifecycle: click stop listening while starting | UI | P1 | not_run |
| TC-1123 | Recognition lifecycle: click stop listening while actively listening | UI | P1 | passed |
| TC-1124 | Recognition lifecycle: click stop listening while showing an interim transcript | UI | P1 | not_run |
| TC-1125 | Recognition lifecycle: click stop listening while showing a final transcript | UI | P1 | not_run |
| TC-1126 | Recognition lifecycle: click stop listening while sending a request | UI | P1 | not_run |
| TC-1127 | Recognition lifecycle: click stop listening while showing an error | UI | P1 | not_run |
| TC-1128 | Recognition lifecycle: click stop listening while the panel is closed | UI | P1 | not_run |
| TC-1129 | Recognition lifecycle: click stop listening while Hindi is selected | UI | P1 | not_run |
| TC-1130 | Recognition lifecycle: click stop listening while Bengali is selected | UI | P1 | not_run |
| TC-1131 | Recognition lifecycle: press Escape while idle | UI | P1 | not_run |
| TC-1132 | Recognition lifecycle: press Escape while starting | UI | P1 | not_run |
| TC-1133 | Recognition lifecycle: press Escape while actively listening | UI | P1 | passed |
| TC-1134 | Recognition lifecycle: press Escape while showing an interim transcript | UI | P1 | not_run |
| TC-1135 | Recognition lifecycle: press Escape while showing a final transcript | UI | P1 | not_run |
| TC-1136 | Recognition lifecycle: press Escape while sending a request | UI | P1 | not_run |
| TC-1137 | Recognition lifecycle: press Escape while showing an error | UI | P1 | not_run |
| TC-1138 | Recognition lifecycle: press Escape while the panel is closed | UI | P1 | not_run |
| TC-1139 | Recognition lifecycle: press Escape while Hindi is selected | UI | P1 | not_run |
| TC-1140 | Recognition lifecycle: press Escape while Bengali is selected | UI | P1 | not_run |
| TC-1141 | Recognition lifecycle: close the panel while idle | UI | P1 | not_run |
| TC-1142 | Recognition lifecycle: close the panel while starting | UI | P1 | not_run |
| TC-1143 | Recognition lifecycle: close the panel while actively listening | UI | P1 | not_run |
| TC-1144 | Recognition lifecycle: close the panel while showing an interim transcript | UI | P1 | not_run |
| TC-1145 | Recognition lifecycle: close the panel while showing a final transcript | UI | P1 | not_run |
| TC-1146 | Recognition lifecycle: close the panel while sending a request | UI | P1 | not_run |
| TC-1147 | Recognition lifecycle: close the panel while showing an error | UI | P1 | not_run |
| TC-1148 | Recognition lifecycle: close the panel while the panel is closed | UI | P1 | not_run |
| TC-1149 | Recognition lifecycle: close the panel while Hindi is selected | UI | P1 | not_run |
| TC-1150 | Recognition lifecycle: close the panel while Bengali is selected | UI | P1 | not_run |
| TC-1151 | Recognition lifecycle: switch language while idle | UI | P1 | not_run |
| TC-1152 | Recognition lifecycle: switch language while starting | UI | P1 | not_run |
| TC-1153 | Recognition lifecycle: switch language while actively listening | UI | P1 | passed |
| TC-1154 | Recognition lifecycle: switch language while showing an interim transcript | UI | P1 | not_run |
| TC-1155 | Recognition lifecycle: switch language while showing a final transcript | UI | P1 | not_run |
| TC-1156 | Recognition lifecycle: switch language while sending a request | UI | P1 | not_run |
| TC-1157 | Recognition lifecycle: switch language while showing an error | UI | P1 | not_run |
| TC-1158 | Recognition lifecycle: switch language while the panel is closed | UI | P1 | not_run |
| TC-1159 | Recognition lifecycle: switch language while Hindi is selected | UI | P1 | not_run |
| TC-1160 | Recognition lifecycle: switch language while Bengali is selected | UI | P1 | not_run |
| TC-1161 | Recognition lifecycle: clear the chat while idle | UI | P1 | not_run |
| TC-1162 | Recognition lifecycle: clear the chat while starting | UI | P1 | not_run |
| TC-1163 | Recognition lifecycle: clear the chat while actively listening | UI | P1 | not_run |
| TC-1164 | Recognition lifecycle: clear the chat while showing an interim transcript | UI | P1 | not_run |
| TC-1165 | Recognition lifecycle: clear the chat while showing a final transcript | UI | P1 | not_run |
| TC-1166 | Recognition lifecycle: clear the chat while sending a request | UI | P1 | not_run |
| TC-1167 | Recognition lifecycle: clear the chat while showing an error | UI | P1 | not_run |
| TC-1168 | Recognition lifecycle: clear the chat while the panel is closed | UI | P1 | not_run |
| TC-1169 | Recognition lifecycle: clear the chat while Hindi is selected | UI | P1 | not_run |
| TC-1170 | Recognition lifecycle: clear the chat while Bengali is selected | UI | P1 | not_run |
| TC-1171 | Recognition lifecycle: submit a typed message while idle | UI | P1 | passed |
| TC-1172 | Recognition lifecycle: submit a typed message while starting | UI | P1 | not_run |
| TC-1173 | Recognition lifecycle: submit a typed message while actively listening | UI | P1 | not_run |
| TC-1174 | Recognition lifecycle: submit a typed message while showing an interim transcript | UI | P1 | not_run |
| TC-1175 | Recognition lifecycle: submit a typed message while showing a final transcript | UI | P1 | not_run |
| TC-1176 | Recognition lifecycle: submit a typed message while sending a request | UI | P1 | not_run |
| TC-1177 | Recognition lifecycle: submit a typed message while showing an error | UI | P1 | not_run |
| TC-1178 | Recognition lifecycle: submit a typed message while the panel is closed | UI | P1 | not_run |
| TC-1179 | Recognition lifecycle: submit a typed message while Hindi is selected | UI | P1 | not_run |
| TC-1180 | Recognition lifecycle: submit a typed message while Bengali is selected | UI | P1 | not_run |
| TC-1181 | Recognition lifecycle: toggle auto-speak while idle | UI | P1 | passed |
| TC-1182 | Recognition lifecycle: toggle auto-speak while starting | UI | P1 | not_run |
| TC-1183 | Recognition lifecycle: toggle auto-speak while actively listening | UI | P1 | not_run |
| TC-1184 | Recognition lifecycle: toggle auto-speak while showing an interim transcript | UI | P1 | not_run |
| TC-1185 | Recognition lifecycle: toggle auto-speak while showing a final transcript | UI | P1 | not_run |
| TC-1186 | Recognition lifecycle: toggle auto-speak while sending a request | UI | P1 | not_run |
| TC-1187 | Recognition lifecycle: toggle auto-speak while showing an error | UI | P1 | not_run |
| TC-1188 | Recognition lifecycle: toggle auto-speak while the panel is closed | UI | P1 | not_run |
| TC-1189 | Recognition lifecycle: toggle auto-speak while Hindi is selected | UI | P1 | not_run |
| TC-1190 | Recognition lifecycle: toggle auto-speak while Bengali is selected | UI | P1 | not_run |
| TC-1191 | Recognition lifecycle: unmount the assistant while idle | UI | P1 | not_run |
| TC-1192 | Recognition lifecycle: unmount the assistant while starting | UI | P1 | not_run |
| TC-1193 | Recognition lifecycle: unmount the assistant while actively listening | UI | P1 | not_run |
| TC-1194 | Recognition lifecycle: unmount the assistant while showing an interim transcript | UI | P1 | not_run |
| TC-1195 | Recognition lifecycle: unmount the assistant while showing a final transcript | UI | P1 | not_run |
| TC-1196 | Recognition lifecycle: unmount the assistant while sending a request | UI | P1 | not_run |
| TC-1197 | Recognition lifecycle: unmount the assistant while showing an error | UI | P1 | not_run |
| TC-1198 | Recognition lifecycle: unmount the assistant while the panel is closed | UI | P1 | not_run |
| TC-1199 | Recognition lifecycle: unmount the assistant while Hindi is selected | UI | P1 | not_run |
| TC-1200 | Recognition lifecycle: unmount the assistant while Bengali is selected | UI | P1 | not_run |
| TC-1201 | Recognition lifecycle: navigate to another page while idle | UI | P1 | not_run |
| TC-1202 | Recognition lifecycle: navigate to another page while starting | UI | P1 | not_run |
| TC-1203 | Recognition lifecycle: navigate to another page while actively listening | UI | P1 | not_run |
| TC-1204 | Recognition lifecycle: navigate to another page while showing an interim transcript | UI | P1 | not_run |
| TC-1205 | Recognition lifecycle: navigate to another page while showing a final transcript | UI | P1 | not_run |
| TC-1206 | Recognition lifecycle: navigate to another page while sending a request | UI | P1 | not_run |
| TC-1207 | Recognition lifecycle: navigate to another page while showing an error | UI | P1 | not_run |
| TC-1208 | Recognition lifecycle: navigate to another page while the panel is closed | UI | P1 | not_run |
| TC-1209 | Recognition lifecycle: navigate to another page while Hindi is selected | UI | P1 | not_run |
| TC-1210 | Recognition lifecycle: navigate to another page while Bengali is selected | UI | P1 | not_run |

### Transcript handling

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1211 | Transcript handling: a single final result with leading and trailing spaces | UI | P1 | not_run |
| TC-1212 | Transcript handling: a single final result with repeated internal spaces | UI | P1 | not_run |
| TC-1213 | Transcript handling: a single final result with exactly 1000 characters | UI | P1 | not_run |
| TC-1214 | Transcript handling: a single final result with 1001 characters | UI | P1 | not_run |
| TC-1215 | Transcript handling: a single final result with emoji characters | UI | P1 | not_run |
| TC-1216 | Transcript handling: a single final result with quotation marks | UI | P1 | not_run |
| TC-1217 | Transcript handling: a single final result with a newline | UI | P1 | not_run |
| TC-1218 | Transcript handling: a single final result with an HTML tag | UI | P1 | passed |
| TC-1219 | Transcript handling: a single final result with SQL-like text | UI | P1 | not_run |
| TC-1220 | Transcript handling: a single final result with trailing punctuation | UI | P1 | not_run |
| TC-1221 | Transcript handling: multiple final results with leading and trailing spaces | UI | P1 | not_run |
| TC-1222 | Transcript handling: multiple final results with repeated internal spaces | UI | P1 | not_run |
| TC-1223 | Transcript handling: multiple final results with exactly 1000 characters | UI | P1 | not_run |
| TC-1224 | Transcript handling: multiple final results with 1001 characters | UI | P1 | not_run |
| TC-1225 | Transcript handling: multiple final results with emoji characters | UI | P1 | not_run |
| TC-1226 | Transcript handling: multiple final results with quotation marks | UI | P1 | not_run |
| TC-1227 | Transcript handling: multiple final results with a newline | UI | P1 | not_run |
| TC-1228 | Transcript handling: multiple final results with an HTML tag | UI | P1 | not_run |
| TC-1229 | Transcript handling: multiple final results with SQL-like text | UI | P1 | not_run |
| TC-1230 | Transcript handling: multiple final results with trailing punctuation | UI | P1 | not_run |
| TC-1231 | Transcript handling: an interim result only with leading and trailing spaces | UI | P1 | not_run |
| TC-1232 | Transcript handling: an interim result only with repeated internal spaces | UI | P1 | not_run |
| TC-1233 | Transcript handling: an interim result only with exactly 1000 characters | UI | P1 | not_run |
| TC-1234 | Transcript handling: an interim result only with 1001 characters | UI | P1 | not_run |
| TC-1235 | Transcript handling: an interim result only with emoji characters | UI | P1 | not_run |
| TC-1236 | Transcript handling: an interim result only with quotation marks | UI | P1 | not_run |
| TC-1237 | Transcript handling: an interim result only with a newline | UI | P1 | not_run |
| TC-1238 | Transcript handling: an interim result only with an HTML tag | UI | P1 | not_run |
| TC-1239 | Transcript handling: an interim result only with SQL-like text | UI | P1 | not_run |
| TC-1240 | Transcript handling: an interim result only with trailing punctuation | UI | P1 | not_run |
| TC-1241 | Transcript handling: an interim followed by a final with leading and trailing spaces | UI | P1 | not_run |
| TC-1242 | Transcript handling: an interim followed by a final with repeated internal spaces | UI | P1 | not_run |
| TC-1243 | Transcript handling: an interim followed by a final with exactly 1000 characters | UI | P1 | not_run |
| TC-1244 | Transcript handling: an interim followed by a final with 1001 characters | UI | P1 | not_run |
| TC-1245 | Transcript handling: an interim followed by a final with emoji characters | UI | P1 | not_run |
| TC-1246 | Transcript handling: an interim followed by a final with quotation marks | UI | P1 | not_run |
| TC-1247 | Transcript handling: an interim followed by a final with a newline | UI | P1 | not_run |
| TC-1248 | Transcript handling: an interim followed by a final with an HTML tag | UI | P1 | not_run |
| TC-1249 | Transcript handling: an interim followed by a final with SQL-like text | UI | P1 | not_run |
| TC-1250 | Transcript handling: an interim followed by a final with trailing punctuation | UI | P1 | not_run |
| TC-1251 | Transcript handling: an empty final result with leading and trailing spaces | UI | P1 | not_run |
| TC-1252 | Transcript handling: an empty final result with repeated internal spaces | UI | P1 | not_run |
| TC-1253 | Transcript handling: an empty final result with exactly 1000 characters | UI | P1 | not_run |
| TC-1254 | Transcript handling: an empty final result with 1001 characters | UI | P1 | not_run |
| TC-1255 | Transcript handling: an empty final result with emoji characters | UI | P1 | not_run |
| TC-1256 | Transcript handling: an empty final result with quotation marks | UI | P1 | not_run |
| TC-1257 | Transcript handling: an empty final result with a newline | UI | P1 | not_run |
| TC-1258 | Transcript handling: an empty final result with an HTML tag | UI | P1 | not_run |
| TC-1259 | Transcript handling: an empty final result with SQL-like text | UI | P1 | not_run |
| TC-1260 | Transcript handling: an empty final result with trailing punctuation | UI | P1 | not_run |
| TC-1261 | Transcript handling: a whitespace-only final with leading and trailing spaces | UI | P1 | not_run |
| TC-1262 | Transcript handling: a whitespace-only final with repeated internal spaces | UI | P1 | not_run |
| TC-1263 | Transcript handling: a whitespace-only final with exactly 1000 characters | UI | P1 | not_run |
| TC-1264 | Transcript handling: a whitespace-only final with 1001 characters | UI | P1 | not_run |
| TC-1265 | Transcript handling: a whitespace-only final with emoji characters | UI | P1 | not_run |
| TC-1266 | Transcript handling: a whitespace-only final with quotation marks | UI | P1 | not_run |
| TC-1267 | Transcript handling: a whitespace-only final with a newline | UI | P1 | not_run |
| TC-1268 | Transcript handling: a whitespace-only final with an HTML tag | UI | P1 | not_run |
| TC-1269 | Transcript handling: a whitespace-only final with SQL-like text | UI | P1 | not_run |
| TC-1270 | Transcript handling: a whitespace-only final with trailing punctuation | UI | P1 | not_run |
| TC-1271 | Transcript handling: punctuated speech with leading and trailing spaces | UI | P1 | not_run |
| TC-1272 | Transcript handling: punctuated speech with repeated internal spaces | UI | P1 | not_run |
| TC-1273 | Transcript handling: punctuated speech with exactly 1000 characters | UI | P1 | not_run |
| TC-1274 | Transcript handling: punctuated speech with 1001 characters | UI | P1 | not_run |
| TC-1275 | Transcript handling: punctuated speech with emoji characters | UI | P1 | not_run |
| TC-1276 | Transcript handling: punctuated speech with quotation marks | UI | P1 | not_run |
| TC-1277 | Transcript handling: punctuated speech with a newline | UI | P1 | not_run |
| TC-1278 | Transcript handling: punctuated speech with an HTML tag | UI | P1 | not_run |
| TC-1279 | Transcript handling: punctuated speech with SQL-like text | UI | P1 | not_run |
| TC-1280 | Transcript handling: punctuated speech with trailing punctuation | UI | P1 | not_run |
| TC-1281 | Transcript handling: Devanagari speech with leading and trailing spaces | UI | P1 | not_run |
| TC-1282 | Transcript handling: Devanagari speech with repeated internal spaces | UI | P1 | not_run |
| TC-1283 | Transcript handling: Devanagari speech with exactly 1000 characters | UI | P1 | not_run |
| TC-1284 | Transcript handling: Devanagari speech with 1001 characters | UI | P1 | not_run |
| TC-1285 | Transcript handling: Devanagari speech with emoji characters | UI | P1 | not_run |
| TC-1286 | Transcript handling: Devanagari speech with quotation marks | UI | P1 | not_run |
| TC-1287 | Transcript handling: Devanagari speech with a newline | UI | P1 | not_run |
| TC-1288 | Transcript handling: Devanagari speech with an HTML tag | UI | P1 | not_run |
| TC-1289 | Transcript handling: Devanagari speech with SQL-like text | UI | P1 | not_run |
| TC-1290 | Transcript handling: Devanagari speech with trailing punctuation | UI | P1 | not_run |
| TC-1291 | Transcript handling: Bengali speech with leading and trailing spaces | UI | P1 | not_run |
| TC-1292 | Transcript handling: Bengali speech with repeated internal spaces | UI | P1 | not_run |
| TC-1293 | Transcript handling: Bengali speech with exactly 1000 characters | UI | P1 | not_run |
| TC-1294 | Transcript handling: Bengali speech with 1001 characters | UI | P1 | not_run |
| TC-1295 | Transcript handling: Bengali speech with emoji characters | UI | P1 | not_run |
| TC-1296 | Transcript handling: Bengali speech with quotation marks | UI | P1 | not_run |
| TC-1297 | Transcript handling: Bengali speech with a newline | UI | P1 | not_run |
| TC-1298 | Transcript handling: Bengali speech with an HTML tag | UI | P1 | not_run |
| TC-1299 | Transcript handling: Bengali speech with SQL-like text | UI | P1 | not_run |
| TC-1300 | Transcript handling: Bengali speech with trailing punctuation | UI | P1 | not_run |
| TC-1301 | Transcript handling: mixed Latin and Devanagari speech with leading and trailing spaces | UI | P1 | not_run |
| TC-1302 | Transcript handling: mixed Latin and Devanagari speech with repeated internal spaces | UI | P1 | not_run |
| TC-1303 | Transcript handling: mixed Latin and Devanagari speech with exactly 1000 characters | UI | P1 | not_run |
| TC-1304 | Transcript handling: mixed Latin and Devanagari speech with 1001 characters | UI | P1 | not_run |
| TC-1305 | Transcript handling: mixed Latin and Devanagari speech with emoji characters | UI | P1 | not_run |
| TC-1306 | Transcript handling: mixed Latin and Devanagari speech with quotation marks | UI | P1 | not_run |
| TC-1307 | Transcript handling: mixed Latin and Devanagari speech with a newline | UI | P1 | not_run |
| TC-1308 | Transcript handling: mixed Latin and Devanagari speech with an HTML tag | UI | P1 | not_run |
| TC-1309 | Transcript handling: mixed Latin and Devanagari speech with SQL-like text | UI | P1 | not_run |
| TC-1310 | Transcript handling: mixed Latin and Devanagari speech with trailing punctuation | UI | P1 | not_run |

### Voice request payload

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1311 | Voice request payload: message field — a typed question | API | P2 | not_run |
| TC-1312 | Voice request payload: message field — a voice question | API | P2 | passed |
| TC-1313 | Voice request payload: message field — a suggestion click | API | P2 | not_run |
| TC-1314 | Voice request payload: message field — a retry | API | P2 | not_run |
| TC-1315 | Voice request payload: message field — after a language switch | API | P2 | not_run |
| TC-1316 | Voice request payload: message field — a long transcript | API | P2 | not_run |
| TC-1317 | Voice request payload: message field — a unicode transcript | API | P2 | not_run |
| TC-1318 | Voice request payload: message field — an empty history | API | P2 | not_run |
| TC-1319 | Voice request payload: message field — a full history | API | P2 | not_run |
| TC-1320 | Voice request payload: message field — auto-speak enabled | API | P2 | not_run |
| TC-1321 | Voice request payload: history roles — a typed question | API | P2 | not_run |
| TC-1322 | Voice request payload: history roles — a voice question | API | P2 | not_run |
| TC-1323 | Voice request payload: history roles — a suggestion click | API | P2 | not_run |
| TC-1324 | Voice request payload: history roles — a retry | API | P2 | not_run |
| TC-1325 | Voice request payload: history roles — after a language switch | API | P2 | not_run |
| TC-1326 | Voice request payload: history roles — a long transcript | API | P2 | not_run |
| TC-1327 | Voice request payload: history roles — a unicode transcript | API | P2 | not_run |
| TC-1328 | Voice request payload: history roles — an empty history | API | P2 | not_run |
| TC-1329 | Voice request payload: history roles — a full history | API | P2 | not_run |
| TC-1330 | Voice request payload: history roles — auto-speak enabled | API | P2 | not_run |
| TC-1331 | Voice request payload: history cap of eight turns — a typed question | API | P2 | not_run |
| TC-1332 | Voice request payload: history cap of eight turns — a voice question | API | P2 | not_run |
| TC-1333 | Voice request payload: history cap of eight turns — a suggestion click | API | P2 | not_run |
| TC-1334 | Voice request payload: history cap of eight turns — a retry | API | P2 | not_run |
| TC-1335 | Voice request payload: history cap of eight turns — after a language switch | API | P2 | not_run |
| TC-1336 | Voice request payload: history cap of eight turns — a long transcript | API | P2 | not_run |
| TC-1337 | Voice request payload: history cap of eight turns — a unicode transcript | API | P2 | not_run |
| TC-1338 | Voice request payload: history cap of eight turns — an empty history | API | P2 | not_run |
| TC-1339 | Voice request payload: history cap of eight turns — a full history | API | P2 | not_run |
| TC-1340 | Voice request payload: history cap of eight turns — auto-speak enabled | API | P2 | not_run |
| TC-1341 | Voice request payload: language en — a typed question | API | P2 | not_run |
| TC-1342 | Voice request payload: language en — a voice question | API | P2 | passed |
| TC-1343 | Voice request payload: language en — a suggestion click | API | P2 | not_run |
| TC-1344 | Voice request payload: language en — a retry | API | P2 | not_run |
| TC-1345 | Voice request payload: language en — after a language switch | API | P2 | not_run |
| TC-1346 | Voice request payload: language en — a long transcript | API | P2 | not_run |
| TC-1347 | Voice request payload: language en — a unicode transcript | API | P2 | not_run |
| TC-1348 | Voice request payload: language en — an empty history | API | P2 | not_run |
| TC-1349 | Voice request payload: language en — a full history | API | P2 | not_run |
| TC-1350 | Voice request payload: language en — auto-speak enabled | API | P2 | not_run |
| TC-1351 | Voice request payload: language hi — a typed question | API | P2 | not_run |
| TC-1352 | Voice request payload: language hi — a voice question | API | P2 | not_run |
| TC-1353 | Voice request payload: language hi — a suggestion click | API | P2 | not_run |
| TC-1354 | Voice request payload: language hi — a retry | API | P2 | not_run |
| TC-1355 | Voice request payload: language hi — after a language switch | API | P2 | not_run |
| TC-1356 | Voice request payload: language hi — a long transcript | API | P2 | not_run |
| TC-1357 | Voice request payload: language hi — a unicode transcript | API | P2 | not_run |
| TC-1358 | Voice request payload: language hi — an empty history | API | P2 | not_run |
| TC-1359 | Voice request payload: language hi — a full history | API | P2 | not_run |
| TC-1360 | Voice request payload: language hi — auto-speak enabled | API | P2 | not_run |
| TC-1361 | Voice request payload: language bn — a typed question | API | P2 | not_run |
| TC-1362 | Voice request payload: language bn — a voice question | API | P2 | not_run |
| TC-1363 | Voice request payload: language bn — a suggestion click | API | P2 | not_run |
| TC-1364 | Voice request payload: language bn — a retry | API | P2 | not_run |
| TC-1365 | Voice request payload: language bn — after a language switch | API | P2 | not_run |
| TC-1366 | Voice request payload: language bn — a long transcript | API | P2 | not_run |
| TC-1367 | Voice request payload: language bn — a unicode transcript | API | P2 | not_run |
| TC-1368 | Voice request payload: language bn — an empty history | API | P2 | not_run |
| TC-1369 | Voice request payload: language bn — a full history | API | P2 | not_run |
| TC-1370 | Voice request payload: language bn — auto-speak enabled | API | P2 | not_run |
| TC-1371 | Voice request payload: Authorization header — a typed question | API | P2 | not_run |
| TC-1372 | Voice request payload: Authorization header — a voice question | API | P2 | not_run |
| TC-1373 | Voice request payload: Authorization header — a suggestion click | API | P2 | not_run |
| TC-1374 | Voice request payload: Authorization header — a retry | API | P2 | not_run |
| TC-1375 | Voice request payload: Authorization header — after a language switch | API | P2 | not_run |
| TC-1376 | Voice request payload: Authorization header — a long transcript | API | P2 | not_run |
| TC-1377 | Voice request payload: Authorization header — a unicode transcript | API | P2 | not_run |
| TC-1378 | Voice request payload: Authorization header — an empty history | API | P2 | not_run |
| TC-1379 | Voice request payload: Authorization header — a full history | API | P2 | not_run |
| TC-1380 | Voice request payload: Authorization header — auto-speak enabled | API | P2 | not_run |
| TC-1381 | Voice request payload: 401 response — a typed question | API | P2 | not_run |
| TC-1382 | Voice request payload: 401 response — a voice question | API | P2 | not_run |
| TC-1383 | Voice request payload: 401 response — a suggestion click | API | P2 | not_run |
| TC-1384 | Voice request payload: 401 response — a retry | API | P2 | not_run |
| TC-1385 | Voice request payload: 401 response — after a language switch | API | P2 | not_run |
| TC-1386 | Voice request payload: 401 response — a long transcript | API | P2 | not_run |
| TC-1387 | Voice request payload: 401 response — a unicode transcript | API | P2 | not_run |
| TC-1388 | Voice request payload: 401 response — an empty history | API | P2 | not_run |
| TC-1389 | Voice request payload: 401 response — a full history | API | P2 | not_run |
| TC-1390 | Voice request payload: 401 response — auto-speak enabled | API | P2 | not_run |
| TC-1391 | Voice request payload: 422 response — a typed question | API | P2 | not_run |
| TC-1392 | Voice request payload: 422 response — a voice question | API | P2 | not_run |
| TC-1393 | Voice request payload: 422 response — a suggestion click | API | P2 | not_run |
| TC-1394 | Voice request payload: 422 response — a retry | API | P2 | not_run |
| TC-1395 | Voice request payload: 422 response — after a language switch | API | P2 | not_run |
| TC-1396 | Voice request payload: 422 response — a long transcript | API | P2 | not_run |
| TC-1397 | Voice request payload: 422 response — a unicode transcript | API | P2 | not_run |
| TC-1398 | Voice request payload: 422 response — an empty history | API | P2 | not_run |
| TC-1399 | Voice request payload: 422 response — a full history | API | P2 | not_run |
| TC-1400 | Voice request payload: 422 response — auto-speak enabled | API | P2 | not_run |
| TC-1401 | Voice request payload: network failure — a typed question | API | P2 | not_run |
| TC-1402 | Voice request payload: network failure — a voice question | API | P2 | not_run |
| TC-1403 | Voice request payload: network failure — a suggestion click | API | P2 | not_run |
| TC-1404 | Voice request payload: network failure — a retry | API | P2 | not_run |
| TC-1405 | Voice request payload: network failure — after a language switch | API | P2 | not_run |
| TC-1406 | Voice request payload: network failure — a long transcript | API | P2 | not_run |
| TC-1407 | Voice request payload: network failure — a unicode transcript | API | P2 | not_run |
| TC-1408 | Voice request payload: network failure — an empty history | API | P2 | not_run |
| TC-1409 | Voice request payload: network failure — a full history | API | P2 | not_run |
| TC-1410 | Voice request payload: network failure — auto-speak enabled | API | P2 | not_run |

### Speech synthesis

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1411 | Speech synthesis: play a reply: voices already loaded | UI | P2 | passed |
| TC-1412 | Speech synthesis: play a reply: an empty voice list | UI | P2 | not_run |
| TC-1413 | Speech synthesis: play a reply: a late voiceschanged event | UI | P2 | not_run |
| TC-1414 | Speech synthesis: play a reply: English selected | UI | P2 | passed |
| TC-1415 | Speech synthesis: play a reply: Hindi selected | UI | P2 | passed |
| TC-1416 | Speech synthesis: play a reply: Bengali selected | UI | P2 | passed |
| TC-1417 | Speech synthesis: play a reply: a long reply | UI | P2 | not_run |
| TC-1418 | Speech synthesis: play a reply: a short reply | UI | P2 | not_run |
| TC-1419 | Speech synthesis: play a reply: the panel closed | UI | P2 | not_run |
| TC-1420 | Speech synthesis: play a reply: a language change mid-playback | UI | P2 | passed |
| TC-1421 | Speech synthesis: stop playback: voices already loaded | UI | P2 | passed |
| TC-1422 | Speech synthesis: stop playback: an empty voice list | UI | P2 | not_run |
| TC-1423 | Speech synthesis: stop playback: a late voiceschanged event | UI | P2 | not_run |
| TC-1424 | Speech synthesis: stop playback: English selected | UI | P2 | not_run |
| TC-1425 | Speech synthesis: stop playback: Hindi selected | UI | P2 | not_run |
| TC-1426 | Speech synthesis: stop playback: Bengali selected | UI | P2 | not_run |
| TC-1427 | Speech synthesis: stop playback: a long reply | UI | P2 | not_run |
| TC-1428 | Speech synthesis: stop playback: a short reply | UI | P2 | not_run |
| TC-1429 | Speech synthesis: stop playback: the panel closed | UI | P2 | not_run |
| TC-1430 | Speech synthesis: stop playback: a language change mid-playback | UI | P2 | not_run |
| TC-1431 | Speech synthesis: toggle the same reply: voices already loaded | UI | P2 | not_run |
| TC-1432 | Speech synthesis: toggle the same reply: an empty voice list | UI | P2 | not_run |
| TC-1433 | Speech synthesis: toggle the same reply: a late voiceschanged event | UI | P2 | not_run |
| TC-1434 | Speech synthesis: toggle the same reply: English selected | UI | P2 | not_run |
| TC-1435 | Speech synthesis: toggle the same reply: Hindi selected | UI | P2 | not_run |
| TC-1436 | Speech synthesis: toggle the same reply: Bengali selected | UI | P2 | not_run |
| TC-1437 | Speech synthesis: toggle the same reply: a long reply | UI | P2 | not_run |
| TC-1438 | Speech synthesis: toggle the same reply: a short reply | UI | P2 | not_run |
| TC-1439 | Speech synthesis: toggle the same reply: the panel closed | UI | P2 | not_run |
| TC-1440 | Speech synthesis: toggle the same reply: a language change mid-playback | UI | P2 | not_run |
| TC-1441 | Speech synthesis: switch to another reply: voices already loaded | UI | P2 | not_run |
| TC-1442 | Speech synthesis: switch to another reply: an empty voice list | UI | P2 | not_run |
| TC-1443 | Speech synthesis: switch to another reply: a late voiceschanged event | UI | P2 | not_run |
| TC-1444 | Speech synthesis: switch to another reply: English selected | UI | P2 | not_run |
| TC-1445 | Speech synthesis: switch to another reply: Hindi selected | UI | P2 | not_run |
| TC-1446 | Speech synthesis: switch to another reply: Bengali selected | UI | P2 | not_run |
| TC-1447 | Speech synthesis: switch to another reply: a long reply | UI | P2 | not_run |
| TC-1448 | Speech synthesis: switch to another reply: a short reply | UI | P2 | not_run |
| TC-1449 | Speech synthesis: switch to another reply: the panel closed | UI | P2 | not_run |
| TC-1450 | Speech synthesis: switch to another reply: a language change mid-playback | UI | P2 | not_run |
| TC-1451 | Speech synthesis: auto-speak on: voices already loaded | UI | P2 | not_run |
| TC-1452 | Speech synthesis: auto-speak on: an empty voice list | UI | P2 | not_run |
| TC-1453 | Speech synthesis: auto-speak on: a late voiceschanged event | UI | P2 | not_run |
| TC-1454 | Speech synthesis: auto-speak on: English selected | UI | P2 | not_run |
| TC-1455 | Speech synthesis: auto-speak on: Hindi selected | UI | P2 | not_run |
| TC-1456 | Speech synthesis: auto-speak on: Bengali selected | UI | P2 | not_run |
| TC-1457 | Speech synthesis: auto-speak on: a long reply | UI | P2 | not_run |
| TC-1458 | Speech synthesis: auto-speak on: a short reply | UI | P2 | not_run |
| TC-1459 | Speech synthesis: auto-speak on: the panel closed | UI | P2 | not_run |
| TC-1460 | Speech synthesis: auto-speak on: a language change mid-playback | UI | P2 | not_run |
| TC-1461 | Speech synthesis: auto-speak off: voices already loaded | UI | P2 | not_run |
| TC-1462 | Speech synthesis: auto-speak off: an empty voice list | UI | P2 | not_run |
| TC-1463 | Speech synthesis: auto-speak off: a late voiceschanged event | UI | P2 | not_run |
| TC-1464 | Speech synthesis: auto-speak off: English selected | UI | P2 | not_run |
| TC-1465 | Speech synthesis: auto-speak off: Hindi selected | UI | P2 | not_run |
| TC-1466 | Speech synthesis: auto-speak off: Bengali selected | UI | P2 | not_run |
| TC-1467 | Speech synthesis: auto-speak off: a long reply | UI | P2 | not_run |
| TC-1468 | Speech synthesis: auto-speak off: a short reply | UI | P2 | not_run |
| TC-1469 | Speech synthesis: auto-speak off: the panel closed | UI | P2 | not_run |
| TC-1470 | Speech synthesis: auto-speak off: a language change mid-playback | UI | P2 | not_run |
| TC-1471 | Speech synthesis: exact voice match: voices already loaded | UI | P2 | passed |
| TC-1472 | Speech synthesis: exact voice match: an empty voice list | UI | P2 | not_run |
| TC-1473 | Speech synthesis: exact voice match: a late voiceschanged event | UI | P2 | not_run |
| TC-1474 | Speech synthesis: exact voice match: English selected | UI | P2 | passed |
| TC-1475 | Speech synthesis: exact voice match: Hindi selected | UI | P2 | passed |
| TC-1476 | Speech synthesis: exact voice match: Bengali selected | UI | P2 | passed |
| TC-1477 | Speech synthesis: exact voice match: a long reply | UI | P2 | not_run |
| TC-1478 | Speech synthesis: exact voice match: a short reply | UI | P2 | not_run |
| TC-1479 | Speech synthesis: exact voice match: the panel closed | UI | P2 | not_run |
| TC-1480 | Speech synthesis: exact voice match: a language change mid-playback | UI | P2 | not_run |
| TC-1481 | Speech synthesis: same-language voice fallback: voices already loaded | UI | P2 | not_run |
| TC-1482 | Speech synthesis: same-language voice fallback: an empty voice list | UI | P2 | not_run |
| TC-1483 | Speech synthesis: same-language voice fallback: a late voiceschanged event | UI | P2 | not_run |
| TC-1484 | Speech synthesis: same-language voice fallback: English selected | UI | P2 | not_run |
| TC-1485 | Speech synthesis: same-language voice fallback: Hindi selected | UI | P2 | not_run |
| TC-1486 | Speech synthesis: same-language voice fallback: Bengali selected | UI | P2 | not_run |
| TC-1487 | Speech synthesis: same-language voice fallback: a long reply | UI | P2 | not_run |
| TC-1488 | Speech synthesis: same-language voice fallback: a short reply | UI | P2 | not_run |
| TC-1489 | Speech synthesis: same-language voice fallback: the panel closed | UI | P2 | not_run |
| TC-1490 | Speech synthesis: same-language voice fallback: a language change mid-playback | UI | P2 | not_run |
| TC-1491 | Speech synthesis: utterance language: voices already loaded | UI | P2 | not_run |
| TC-1492 | Speech synthesis: utterance language: an empty voice list | UI | P2 | not_run |
| TC-1493 | Speech synthesis: utterance language: a late voiceschanged event | UI | P2 | not_run |
| TC-1494 | Speech synthesis: utterance language: English selected | UI | P2 | not_run |
| TC-1495 | Speech synthesis: utterance language: Hindi selected | UI | P2 | not_run |
| TC-1496 | Speech synthesis: utterance language: Bengali selected | UI | P2 | not_run |
| TC-1497 | Speech synthesis: utterance language: a long reply | UI | P2 | not_run |
| TC-1498 | Speech synthesis: utterance language: a short reply | UI | P2 | not_run |
| TC-1499 | Speech synthesis: utterance language: the panel closed | UI | P2 | not_run |
| TC-1500 | Speech synthesis: utterance language: a language change mid-playback | UI | P2 | not_run |
| TC-1501 | Speech synthesis: utterance error: voices already loaded | UI | P2 | not_run |
| TC-1502 | Speech synthesis: utterance error: an empty voice list | UI | P2 | not_run |
| TC-1503 | Speech synthesis: utterance error: a late voiceschanged event | UI | P2 | not_run |
| TC-1504 | Speech synthesis: utterance error: English selected | UI | P2 | not_run |
| TC-1505 | Speech synthesis: utterance error: Hindi selected | UI | P2 | not_run |
| TC-1506 | Speech synthesis: utterance error: Bengali selected | UI | P2 | not_run |
| TC-1507 | Speech synthesis: utterance error: a long reply | UI | P2 | not_run |
| TC-1508 | Speech synthesis: utterance error: a short reply | UI | P2 | not_run |
| TC-1509 | Speech synthesis: utterance error: the panel closed | UI | P2 | not_run |
| TC-1510 | Speech synthesis: utterance error: a language change mid-playback | UI | P2 | not_run |

### Auto-speak

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1511 | Auto-speak: auto-speak off by default on a text reply | UI | P2 | not_run |
| TC-1512 | Auto-speak: auto-speak off by default on a voice reply | UI | P2 | not_run |
| TC-1513 | Auto-speak: auto-speak off by default on an error reply | UI | P2 | not_run |
| TC-1514 | Auto-speak: auto-speak off by default on a language switch | UI | P2 | not_run |
| TC-1515 | Auto-speak: auto-speak off by default on clear chat | UI | P2 | not_run |
| TC-1516 | Auto-speak: auto-speak off by default on closing the panel | UI | P2 | not_run |
| TC-1517 | Auto-speak: auto-speak off by default on a retry | UI | P2 | not_run |
| TC-1518 | Auto-speak: auto-speak off by default on a suggestion click | UI | P2 | not_run |
| TC-1519 | Auto-speak: auto-speak off by default on stopping playback | UI | P2 | not_run |
| TC-1520 | Auto-speak: auto-speak off by default on reopening the panel | UI | P2 | not_run |
| TC-1521 | Auto-speak: auto-speak enabled on a text reply | UI | P2 | not_run |
| TC-1522 | Auto-speak: auto-speak enabled on a voice reply | UI | P2 | not_run |
| TC-1523 | Auto-speak: auto-speak enabled on an error reply | UI | P2 | not_run |
| TC-1524 | Auto-speak: auto-speak enabled on a language switch | UI | P2 | not_run |
| TC-1525 | Auto-speak: auto-speak enabled on clear chat | UI | P2 | not_run |
| TC-1526 | Auto-speak: auto-speak enabled on closing the panel | UI | P2 | not_run |
| TC-1527 | Auto-speak: auto-speak enabled on a retry | UI | P2 | not_run |
| TC-1528 | Auto-speak: auto-speak enabled on a suggestion click | UI | P2 | passed |
| TC-1529 | Auto-speak: auto-speak enabled on stopping playback | UI | P2 | not_run |
| TC-1530 | Auto-speak: auto-speak enabled on reopening the panel | UI | P2 | not_run |
| TC-1531 | Auto-speak: auto-speak disabled again on a text reply | UI | P2 | passed |
| TC-1532 | Auto-speak: auto-speak disabled again on a voice reply | UI | P2 | not_run |
| TC-1533 | Auto-speak: auto-speak disabled again on an error reply | UI | P2 | not_run |
| TC-1534 | Auto-speak: auto-speak disabled again on a language switch | UI | P2 | not_run |
| TC-1535 | Auto-speak: auto-speak disabled again on clear chat | UI | P2 | not_run |
| TC-1536 | Auto-speak: auto-speak disabled again on closing the panel | UI | P2 | not_run |
| TC-1537 | Auto-speak: auto-speak disabled again on a retry | UI | P2 | not_run |
| TC-1538 | Auto-speak: auto-speak disabled again on a suggestion click | UI | P2 | not_run |
| TC-1539 | Auto-speak: auto-speak disabled again on stopping playback | UI | P2 | not_run |
| TC-1540 | Auto-speak: auto-speak disabled again on reopening the panel | UI | P2 | not_run |
| TC-1541 | Auto-speak: auto-speak unsupported on a text reply | UI | P2 | not_run |
| TC-1542 | Auto-speak: auto-speak unsupported on a voice reply | UI | P2 | not_run |
| TC-1543 | Auto-speak: auto-speak unsupported on an error reply | UI | P2 | not_run |
| TC-1544 | Auto-speak: auto-speak unsupported on a language switch | UI | P2 | not_run |
| TC-1545 | Auto-speak: auto-speak unsupported on clear chat | UI | P2 | not_run |
| TC-1546 | Auto-speak: auto-speak unsupported on closing the panel | UI | P2 | not_run |
| TC-1547 | Auto-speak: auto-speak unsupported on a retry | UI | P2 | not_run |
| TC-1548 | Auto-speak: auto-speak unsupported on a suggestion click | UI | P2 | not_run |
| TC-1549 | Auto-speak: auto-speak unsupported on stopping playback | UI | P2 | not_run |
| TC-1550 | Auto-speak: auto-speak unsupported on reopening the panel | UI | P2 | not_run |
| TC-1551 | Auto-speak: auto-speak with no installed voice on a text reply | UI | P2 | not_run |
| TC-1552 | Auto-speak: auto-speak with no installed voice on a voice reply | UI | P2 | not_run |
| TC-1553 | Auto-speak: auto-speak with no installed voice on an error reply | UI | P2 | not_run |
| TC-1554 | Auto-speak: auto-speak with no installed voice on a language switch | UI | P2 | not_run |
| TC-1555 | Auto-speak: auto-speak with no installed voice on clear chat | UI | P2 | not_run |
| TC-1556 | Auto-speak: auto-speak with no installed voice on closing the panel | UI | P2 | not_run |
| TC-1557 | Auto-speak: auto-speak with no installed voice on a retry | UI | P2 | not_run |
| TC-1558 | Auto-speak: auto-speak with no installed voice on a suggestion click | UI | P2 | not_run |
| TC-1559 | Auto-speak: auto-speak with no installed voice on stopping playback | UI | P2 | not_run |
| TC-1560 | Auto-speak: auto-speak with no installed voice on reopening the panel | UI | P2 | not_run |
| TC-1561 | Auto-speak: auto-speak toggled twice quickly on a text reply | UI | P2 | not_run |
| TC-1562 | Auto-speak: auto-speak toggled twice quickly on a voice reply | UI | P2 | not_run |
| TC-1563 | Auto-speak: auto-speak toggled twice quickly on an error reply | UI | P2 | not_run |
| TC-1564 | Auto-speak: auto-speak toggled twice quickly on a language switch | UI | P2 | not_run |
| TC-1565 | Auto-speak: auto-speak toggled twice quickly on clear chat | UI | P2 | not_run |
| TC-1566 | Auto-speak: auto-speak toggled twice quickly on closing the panel | UI | P2 | not_run |
| TC-1567 | Auto-speak: auto-speak toggled twice quickly on a retry | UI | P2 | not_run |
| TC-1568 | Auto-speak: auto-speak toggled twice quickly on a suggestion click | UI | P2 | not_run |
| TC-1569 | Auto-speak: auto-speak toggled twice quickly on stopping playback | UI | P2 | not_run |
| TC-1570 | Auto-speak: auto-speak toggled twice quickly on reopening the panel | UI | P2 | not_run |

### Accessibility

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1571 | Accessibility: microphone button aria-label in keyboard-only use | UI | P2 | not_run |
| TC-1572 | Accessibility: microphone button aria-label in screen-reader use | UI | P2 | not_run |
| TC-1573 | Accessibility: microphone button aria-label in 200% zoom | UI | P2 | not_run |
| TC-1574 | Accessibility: microphone button aria-label in mobile portrait | UI | P2 | not_run |
| TC-1575 | Accessibility: microphone button aria-label in mobile landscape | UI | P2 | not_run |
| TC-1576 | Accessibility: microphone button aria-label in reduced motion | UI | P2 | not_run |
| TC-1577 | Accessibility: microphone button aria-label in forced colors | UI | P2 | not_run |
| TC-1578 | Accessibility: microphone button aria-label in RTL text inside the transcript | UI | P2 | not_run |
| TC-1579 | Accessibility: microphone aria-pressed in keyboard-only use | UI | P2 | not_run |
| TC-1580 | Accessibility: microphone aria-pressed in screen-reader use | UI | P2 | not_run |
| TC-1581 | Accessibility: microphone aria-pressed in 200% zoom | UI | P2 | not_run |
| TC-1582 | Accessibility: microphone aria-pressed in mobile portrait | UI | P2 | not_run |
| TC-1583 | Accessibility: microphone aria-pressed in mobile landscape | UI | P2 | not_run |
| TC-1584 | Accessibility: microphone aria-pressed in reduced motion | UI | P2 | not_run |
| TC-1585 | Accessibility: microphone aria-pressed in forced colors | UI | P2 | not_run |
| TC-1586 | Accessibility: microphone aria-pressed in RTL text inside the transcript | UI | P2 | not_run |
| TC-1587 | Accessibility: interim transcript aria-live in keyboard-only use | UI | P2 | not_run |
| TC-1588 | Accessibility: interim transcript aria-live in screen-reader use | UI | P2 | not_run |
| TC-1589 | Accessibility: interim transcript aria-live in 200% zoom | UI | P2 | not_run |
| TC-1590 | Accessibility: interim transcript aria-live in mobile portrait | UI | P2 | not_run |
| TC-1591 | Accessibility: interim transcript aria-live in mobile landscape | UI | P2 | not_run |
| TC-1592 | Accessibility: interim transcript aria-live in reduced motion | UI | P2 | not_run |
| TC-1593 | Accessibility: interim transcript aria-live in forced colors | UI | P2 | not_run |
| TC-1594 | Accessibility: interim transcript aria-live in RTL text inside the transcript | UI | P2 | not_run |
| TC-1595 | Accessibility: error message role alert in keyboard-only use | UI | P2 | not_run |
| TC-1596 | Accessibility: error message role alert in screen-reader use | UI | P2 | not_run |
| TC-1597 | Accessibility: error message role alert in 200% zoom | UI | P2 | not_run |
| TC-1598 | Accessibility: error message role alert in mobile portrait | UI | P2 | not_run |
| TC-1599 | Accessibility: error message role alert in mobile landscape | UI | P2 | not_run |
| TC-1600 | Accessibility: error message role alert in reduced motion | UI | P2 | not_run |
| TC-1601 | Accessibility: error message role alert in forced colors | UI | P2 | not_run |
| TC-1602 | Accessibility: error message role alert in RTL text inside the transcript | UI | P2 | not_run |
| TC-1603 | Accessibility: panel aria-label in keyboard-only use | UI | P2 | not_run |
| TC-1604 | Accessibility: panel aria-label in screen-reader use | UI | P2 | not_run |
| TC-1605 | Accessibility: panel aria-label in 200% zoom | UI | P2 | not_run |
| TC-1606 | Accessibility: panel aria-label in mobile portrait | UI | P2 | not_run |
| TC-1607 | Accessibility: panel aria-label in mobile landscape | UI | P2 | not_run |
| TC-1608 | Accessibility: panel aria-label in reduced motion | UI | P2 | not_run |
| TC-1609 | Accessibility: panel aria-label in forced colors | UI | P2 | not_run |
| TC-1610 | Accessibility: panel aria-label in RTL text inside the transcript | UI | P2 | not_run |
| TC-1611 | Accessibility: conversation log aria-live in keyboard-only use | UI | P2 | not_run |
| TC-1612 | Accessibility: conversation log aria-live in screen-reader use | UI | P2 | not_run |
| TC-1613 | Accessibility: conversation log aria-live in 200% zoom | UI | P2 | not_run |
| TC-1614 | Accessibility: conversation log aria-live in mobile portrait | UI | P2 | not_run |
| TC-1615 | Accessibility: conversation log aria-live in mobile landscape | UI | P2 | not_run |
| TC-1616 | Accessibility: conversation log aria-live in reduced motion | UI | P2 | not_run |
| TC-1617 | Accessibility: conversation log aria-live in forced colors | UI | P2 | not_run |
| TC-1618 | Accessibility: conversation log aria-live in RTL text inside the transcript | UI | P2 | not_run |
| TC-1619 | Accessibility: language select accessible name in keyboard-only use | UI | P2 | not_run |
| TC-1620 | Accessibility: language select accessible name in screen-reader use | UI | P2 | not_run |
| TC-1621 | Accessibility: language select accessible name in 200% zoom | UI | P2 | not_run |
| TC-1622 | Accessibility: language select accessible name in mobile portrait | UI | P2 | not_run |
| TC-1623 | Accessibility: language select accessible name in mobile landscape | UI | P2 | not_run |
| TC-1624 | Accessibility: language select accessible name in reduced motion | UI | P2 | not_run |
| TC-1625 | Accessibility: language select accessible name in forced colors | UI | P2 | not_run |
| TC-1626 | Accessibility: language select accessible name in RTL text inside the transcript | UI | P2 | not_run |
| TC-1627 | Accessibility: auto-speak aria-pressed in keyboard-only use | UI | P2 | not_run |
| TC-1628 | Accessibility: auto-speak aria-pressed in screen-reader use | UI | P2 | not_run |
| TC-1629 | Accessibility: auto-speak aria-pressed in 200% zoom | UI | P2 | not_run |
| TC-1630 | Accessibility: auto-speak aria-pressed in mobile portrait | UI | P2 | not_run |
| TC-1631 | Accessibility: auto-speak aria-pressed in mobile landscape | UI | P2 | not_run |
| TC-1632 | Accessibility: auto-speak aria-pressed in reduced motion | UI | P2 | not_run |
| TC-1633 | Accessibility: auto-speak aria-pressed in forced colors | UI | P2 | not_run |
| TC-1634 | Accessibility: auto-speak aria-pressed in RTL text inside the transcript | UI | P2 | not_run |
| TC-1635 | Accessibility: focus after opening in keyboard-only use | UI | P2 | not_run |
| TC-1636 | Accessibility: focus after opening in screen-reader use | UI | P2 | not_run |
| TC-1637 | Accessibility: focus after opening in 200% zoom | UI | P2 | not_run |
| TC-1638 | Accessibility: focus after opening in mobile portrait | UI | P2 | not_run |
| TC-1639 | Accessibility: focus after opening in mobile landscape | UI | P2 | not_run |
| TC-1640 | Accessibility: focus after opening in reduced motion | UI | P2 | not_run |
| TC-1641 | Accessibility: focus after opening in forced colors | UI | P2 | not_run |
| TC-1642 | Accessibility: focus after opening in RTL text inside the transcript | UI | P2 | not_run |
| TC-1643 | Accessibility: Escape close in keyboard-only use | UI | P2 | passed |
| TC-1644 | Accessibility: Escape close in screen-reader use | UI | P2 | not_run |
| TC-1645 | Accessibility: Escape close in 200% zoom | UI | P2 | not_run |
| TC-1646 | Accessibility: Escape close in mobile portrait | UI | P2 | not_run |
| TC-1647 | Accessibility: Escape close in mobile landscape | UI | P2 | not_run |
| TC-1648 | Accessibility: Escape close in reduced motion | UI | P2 | not_run |
| TC-1649 | Accessibility: Escape close in forced colors | UI | P2 | not_run |
| TC-1650 | Accessibility: Escape close in RTL text inside the transcript | UI | P2 | not_run |

### Voice privacy

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1651 | Voice privacy: microphone permission denial on first load | UI | P2 | not_run |
| TC-1652 | Voice privacy: microphone permission denial after a reload | UI | P2 | not_run |
| TC-1653 | Voice privacy: microphone permission denial after logout | UI | P2 | not_run |
| TC-1654 | Voice privacy: microphone permission denial on the administrator route | UI | P2 | not_run |
| TC-1655 | Voice privacy: microphone permission denial after a language switch | UI | P2 | not_run |
| TC-1656 | Voice privacy: microphone permission denial after a network failure | UI | P2 | not_run |
| TC-1657 | Voice privacy: microphone permission denial after using browser back | UI | P2 | not_run |
| TC-1658 | Voice privacy: audio is not persisted on first load | UI | P2 | not_run |
| TC-1659 | Voice privacy: audio is not persisted after a reload | UI | P2 | not_run |
| TC-1660 | Voice privacy: audio is not persisted after logout | UI | P2 | not_run |
| TC-1661 | Voice privacy: audio is not persisted on the administrator route | UI | P2 | not_run |
| TC-1662 | Voice privacy: audio is not persisted after a language switch | UI | P2 | not_run |
| TC-1663 | Voice privacy: audio is not persisted after a network failure | UI | P2 | not_run |
| TC-1664 | Voice privacy: audio is not persisted after using browser back | UI | P2 | not_run |
| TC-1665 | Voice privacy: transcript stays in the session on first load | UI | P2 | not_run |
| TC-1666 | Voice privacy: transcript stays in the session after a reload | UI | P2 | not_run |
| TC-1667 | Voice privacy: transcript stays in the session after logout | UI | P2 | not_run |
| TC-1668 | Voice privacy: transcript stays in the session on the administrator route | UI | P2 | not_run |
| TC-1669 | Voice privacy: transcript stays in the session after a language switch | UI | P2 | not_run |
| TC-1670 | Voice privacy: transcript stays in the session after a network failure | UI | P2 | not_run |
| TC-1671 | Voice privacy: transcript stays in the session after using browser back | UI | P2 | not_run |
| TC-1672 | Voice privacy: transcript is not placed in the URL on first load | UI | P2 | not_run |
| TC-1673 | Voice privacy: transcript is not placed in the URL after a reload | UI | P2 | not_run |
| TC-1674 | Voice privacy: transcript is not placed in the URL after logout | UI | P2 | not_run |
| TC-1675 | Voice privacy: transcript is not placed in the URL on the administrator route | UI | P2 | not_run |
| TC-1676 | Voice privacy: transcript is not placed in the URL after a language switch | UI | P2 | not_run |
| TC-1677 | Voice privacy: transcript is not placed in the URL after a network failure | UI | P2 | not_run |
| TC-1678 | Voice privacy: transcript is not placed in the URL after using browser back | UI | P2 | not_run |
| TC-1679 | Voice privacy: errors contain no secrets on first load | UI | P2 | not_run |
| TC-1680 | Voice privacy: errors contain no secrets after a reload | UI | P2 | not_run |
| TC-1681 | Voice privacy: errors contain no secrets after logout | UI | P2 | not_run |
| TC-1682 | Voice privacy: errors contain no secrets on the administrator route | UI | P2 | not_run |
| TC-1683 | Voice privacy: errors contain no secrets after a language switch | UI | P2 | not_run |
| TC-1684 | Voice privacy: errors contain no secrets after a network failure | UI | P2 | not_run |
| TC-1685 | Voice privacy: errors contain no secrets after using browser back | UI | P2 | not_run |
| TC-1686 | Voice privacy: XSS transcript is escaped on first load | UI | P2 | passed |
| TC-1687 | Voice privacy: XSS transcript is escaped after a reload | UI | P2 | not_run |
| TC-1688 | Voice privacy: XSS transcript is escaped after logout | UI | P2 | not_run |
| TC-1689 | Voice privacy: XSS transcript is escaped on the administrator route | UI | P2 | not_run |
| TC-1690 | Voice privacy: XSS transcript is escaped after a language switch | UI | P2 | not_run |
| TC-1691 | Voice privacy: XSS transcript is escaped after a network failure | UI | P2 | not_run |
| TC-1692 | Voice privacy: XSS transcript is escaped after using browser back | UI | P2 | not_run |
| TC-1693 | Voice privacy: chat requires authentication on first load | UI | P2 | not_run |
| TC-1694 | Voice privacy: chat requires authentication after a reload | UI | P2 | not_run |
| TC-1695 | Voice privacy: chat requires authentication after logout | UI | P2 | not_run |
| TC-1696 | Voice privacy: chat requires authentication on the administrator route | UI | P2 | not_run |
| TC-1697 | Voice privacy: chat requires authentication after a language switch | UI | P2 | not_run |
| TC-1698 | Voice privacy: chat requires authentication after a network failure | UI | P2 | not_run |
| TC-1699 | Voice privacy: chat requires authentication after using browser back | UI | P2 | not_run |
| TC-1700 | Voice privacy: 401 clears the session token on first load | UI | P2 | not_run |
| TC-1701 | Voice privacy: 401 clears the session token after a reload | UI | P2 | not_run |
| TC-1702 | Voice privacy: 401 clears the session token after logout | UI | P2 | not_run |
| TC-1703 | Voice privacy: 401 clears the session token on the administrator route | UI | P2 | not_run |
| TC-1704 | Voice privacy: 401 clears the session token after a language switch | UI | P2 | not_run |
| TC-1705 | Voice privacy: 401 clears the session token after a network failure | UI | P2 | not_run |
| TC-1706 | Voice privacy: 401 clears the session token after using browser back | UI | P2 | not_run |
| TC-1707 | Voice privacy: 403 inactive account handling on first load | UI | P2 | not_run |
| TC-1708 | Voice privacy: 403 inactive account handling after a reload | UI | P2 | not_run |
| TC-1709 | Voice privacy: 403 inactive account handling after logout | UI | P2 | not_run |
| TC-1710 | Voice privacy: 403 inactive account handling on the administrator route | UI | P2 | not_run |
| TC-1711 | Voice privacy: 403 inactive account handling after a language switch | UI | P2 | not_run |
| TC-1712 | Voice privacy: 403 inactive account handling after a network failure | UI | P2 | not_run |
| TC-1713 | Voice privacy: 403 inactive account handling after using browser back | UI | P2 | not_run |
| TC-1714 | Voice privacy: microphone never auto-starts on first load | UI | P2 | passed |
| TC-1715 | Voice privacy: microphone never auto-starts after a reload | UI | P2 | not_run |
| TC-1716 | Voice privacy: microphone never auto-starts after logout | UI | P2 | not_run |
| TC-1717 | Voice privacy: microphone never auto-starts on the administrator route | UI | P2 | not_run |
| TC-1718 | Voice privacy: microphone never auto-starts after a language switch | UI | P2 | not_run |
| TC-1719 | Voice privacy: microphone never auto-starts after a network failure | UI | P2 | not_run |
| TC-1720 | Voice privacy: microphone never auto-starts after using browser back | UI | P2 | not_run |

### Responsive layout

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1721 | Responsive layout: 320 px width — launcher fits | UI | P3 | not_run |
| TC-1722 | Responsive layout: 320 px width — panel fits | UI | P3 | not_run |
| TC-1723 | Responsive layout: 320 px width — no horizontal overflow | UI | P3 | not_run |
| TC-1724 | Responsive layout: 320 px width — microphone controls visible | UI | P3 | not_run |
| TC-1725 | Responsive layout: 320 px width — interim text wraps | UI | P3 | not_run |
| TC-1726 | Responsive layout: 320 px width — disclaimer readable | UI | P3 | not_run |
| TC-1727 | Responsive layout: 360 px width — launcher fits | UI | P3 | not_run |
| TC-1728 | Responsive layout: 360 px width — panel fits | UI | P3 | not_run |
| TC-1729 | Responsive layout: 360 px width — no horizontal overflow | UI | P3 | not_run |
| TC-1730 | Responsive layout: 360 px width — microphone controls visible | UI | P3 | not_run |
| TC-1731 | Responsive layout: 360 px width — interim text wraps | UI | P3 | not_run |
| TC-1732 | Responsive layout: 360 px width — disclaimer readable | UI | P3 | not_run |
| TC-1733 | Responsive layout: 390 px width — launcher fits | UI | P3 | not_run |
| TC-1734 | Responsive layout: 390 px width — panel fits | UI | P3 | passed |
| TC-1735 | Responsive layout: 390 px width — no horizontal overflow | UI | P3 | passed |
| TC-1736 | Responsive layout: 390 px width — microphone controls visible | UI | P3 | not_run |
| TC-1737 | Responsive layout: 390 px width — interim text wraps | UI | P3 | not_run |
| TC-1738 | Responsive layout: 390 px width — disclaimer readable | UI | P3 | not_run |
| TC-1739 | Responsive layout: 768 px width — launcher fits | UI | P3 | not_run |
| TC-1740 | Responsive layout: 768 px width — panel fits | UI | P3 | not_run |
| TC-1741 | Responsive layout: 768 px width — no horizontal overflow | UI | P3 | not_run |
| TC-1742 | Responsive layout: 768 px width — microphone controls visible | UI | P3 | not_run |
| TC-1743 | Responsive layout: 768 px width — interim text wraps | UI | P3 | not_run |
| TC-1744 | Responsive layout: 768 px width — disclaimer readable | UI | P3 | not_run |
| TC-1745 | Responsive layout: 1024 px width — launcher fits | UI | P3 | not_run |
| TC-1746 | Responsive layout: 1024 px width — panel fits | UI | P3 | not_run |
| TC-1747 | Responsive layout: 1024 px width — no horizontal overflow | UI | P3 | not_run |
| TC-1748 | Responsive layout: 1024 px width — microphone controls visible | UI | P3 | not_run |
| TC-1749 | Responsive layout: 1024 px width — interim text wraps | UI | P3 | not_run |
| TC-1750 | Responsive layout: 1024 px width — disclaimer readable | UI | P3 | not_run |
| TC-1751 | Responsive layout: 1440 px width — launcher fits | UI | P3 | not_run |
| TC-1752 | Responsive layout: 1440 px width — panel fits | UI | P3 | not_run |
| TC-1753 | Responsive layout: 1440 px width — no horizontal overflow | UI | P3 | not_run |
| TC-1754 | Responsive layout: 1440 px width — microphone controls visible | UI | P3 | not_run |
| TC-1755 | Responsive layout: 1440 px width — interim text wraps | UI | P3 | not_run |
| TC-1756 | Responsive layout: 1440 px width — disclaimer readable | UI | P3 | not_run |
| TC-1757 | Responsive layout: tablet landscape — launcher fits | UI | P3 | not_run |
| TC-1758 | Responsive layout: tablet landscape — panel fits | UI | P3 | not_run |
| TC-1759 | Responsive layout: tablet landscape — no horizontal overflow | UI | P3 | not_run |
| TC-1760 | Responsive layout: tablet landscape — microphone controls visible | UI | P3 | not_run |
| TC-1761 | Responsive layout: tablet landscape — interim text wraps | UI | P3 | not_run |
| TC-1762 | Responsive layout: tablet landscape — disclaimer readable | UI | P3 | not_run |
| TC-1763 | Responsive layout: 480 px height — launcher fits | UI | P3 | not_run |
| TC-1764 | Responsive layout: 480 px height — panel fits | UI | P3 | not_run |
| TC-1765 | Responsive layout: 480 px height — no horizontal overflow | UI | P3 | not_run |
| TC-1766 | Responsive layout: 480 px height — microphone controls visible | UI | P3 | not_run |
| TC-1767 | Responsive layout: 480 px height — interim text wraps | UI | P3 | not_run |
| TC-1768 | Responsive layout: 480 px height — disclaimer readable | UI | P3 | not_run |
| TC-1769 | Responsive layout: 200% zoom — launcher fits | UI | P3 | not_run |
| TC-1770 | Responsive layout: 200% zoom — panel fits | UI | P3 | not_run |
| TC-1771 | Responsive layout: 200% zoom — no horizontal overflow | UI | P3 | not_run |
| TC-1772 | Responsive layout: 200% zoom — microphone controls visible | UI | P3 | not_run |
| TC-1773 | Responsive layout: 200% zoom — interim text wraps | UI | P3 | not_run |
| TC-1774 | Responsive layout: 200% zoom — disclaimer readable | UI | P3 | not_run |
| TC-1775 | Responsive layout: 50/50 split view — launcher fits | UI | P3 | not_run |
| TC-1776 | Responsive layout: 50/50 split view — panel fits | UI | P3 | not_run |
| TC-1777 | Responsive layout: 50/50 split view — no horizontal overflow | UI | P3 | not_run |
| TC-1778 | Responsive layout: 50/50 split view — microphone controls visible | UI | P3 | not_run |
| TC-1779 | Responsive layout: 50/50 split view — interim text wraps | UI | P3 | not_run |
| TC-1780 | Responsive layout: 50/50 split view — disclaimer readable | UI | P3 | not_run |

### Reliability

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1781 | Reliability: rapid double-click on the microphone on the first occurrence | UI | P1 | passed |
| TC-1782 | Reliability: rapid double-click on the microphone after a page reload | UI | P1 | not_run |
| TC-1783 | Reliability: rapid double-click on the microphone after a language switch | UI | P1 | not_run |
| TC-1784 | Reliability: rapid double-click on the microphone on a slow device | UI | P1 | not_run |
| TC-1785 | Reliability: rapid double-click on the microphone in a background tab | UI | P1 | not_run |
| TC-1786 | Reliability: rapid double-click on the microphone with the panel reopened | UI | P1 | not_run |
| TC-1787 | Reliability: rapid double-click on the microphone with auto-speak enabled | UI | P1 | not_run |
| TC-1788 | Reliability: rapid double-click on the microphone with an error already visible | UI | P1 | not_run |
| TC-1789 | Reliability: rapid double-click on the microphone after clearing the chat | UI | P1 | not_run |
| TC-1790 | Reliability: rapid double-click on the microphone after an expired session | UI | P1 | not_run |
| TC-1791 | Reliability: start while already starting on the first occurrence | UI | P1 | passed |
| TC-1792 | Reliability: start while already starting after a page reload | UI | P1 | not_run |
| TC-1793 | Reliability: start while already starting after a language switch | UI | P1 | not_run |
| TC-1794 | Reliability: start while already starting on a slow device | UI | P1 | not_run |
| TC-1795 | Reliability: start while already starting in a background tab | UI | P1 | not_run |
| TC-1796 | Reliability: start while already starting with the panel reopened | UI | P1 | not_run |
| TC-1797 | Reliability: start while already starting with auto-speak enabled | UI | P1 | not_run |
| TC-1798 | Reliability: start while already starting with an error already visible | UI | P1 | not_run |
| TC-1799 | Reliability: start while already starting after clearing the chat | UI | P1 | not_run |
| TC-1800 | Reliability: start while already starting after an expired session | UI | P1 | not_run |
| TC-1801 | Reliability: stop before onstart fires on the first occurrence | UI | P1 | not_run |
| TC-1802 | Reliability: stop before onstart fires after a page reload | UI | P1 | not_run |
| TC-1803 | Reliability: stop before onstart fires after a language switch | UI | P1 | not_run |
| TC-1804 | Reliability: stop before onstart fires on a slow device | UI | P1 | not_run |
| TC-1805 | Reliability: stop before onstart fires in a background tab | UI | P1 | not_run |
| TC-1806 | Reliability: stop before onstart fires with the panel reopened | UI | P1 | not_run |
| TC-1807 | Reliability: stop before onstart fires with auto-speak enabled | UI | P1 | not_run |
| TC-1808 | Reliability: stop before onstart fires with an error already visible | UI | P1 | not_run |
| TC-1809 | Reliability: stop before onstart fires after clearing the chat | UI | P1 | not_run |
| TC-1810 | Reliability: stop before onstart fires after an expired session | UI | P1 | not_run |
| TC-1811 | Reliability: a result arrives after stop on the first occurrence | UI | P1 | passed |
| TC-1812 | Reliability: a result arrives after stop after a page reload | UI | P1 | not_run |
| TC-1813 | Reliability: a result arrives after stop after a language switch | UI | P1 | not_run |
| TC-1814 | Reliability: a result arrives after stop on a slow device | UI | P1 | not_run |
| TC-1815 | Reliability: a result arrives after stop in a background tab | UI | P1 | not_run |
| TC-1816 | Reliability: a result arrives after stop with the panel reopened | UI | P1 | not_run |
| TC-1817 | Reliability: a result arrives after stop with auto-speak enabled | UI | P1 | not_run |
| TC-1818 | Reliability: a result arrives after stop with an error already visible | UI | P1 | not_run |
| TC-1819 | Reliability: a result arrives after stop after clearing the chat | UI | P1 | not_run |
| TC-1820 | Reliability: a result arrives after stop after an expired session | UI | P1 | not_run |
| TC-1821 | Reliability: a result arrives after close on the first occurrence | UI | P1 | passed |
| TC-1822 | Reliability: a result arrives after close after a page reload | UI | P1 | not_run |
| TC-1823 | Reliability: a result arrives after close after a language switch | UI | P1 | not_run |
| TC-1824 | Reliability: a result arrives after close on a slow device | UI | P1 | not_run |
| TC-1825 | Reliability: a result arrives after close in a background tab | UI | P1 | not_run |
| TC-1826 | Reliability: a result arrives after close with the panel reopened | UI | P1 | not_run |
| TC-1827 | Reliability: a result arrives after close with auto-speak enabled | UI | P1 | not_run |
| TC-1828 | Reliability: a result arrives after close with an error already visible | UI | P1 | not_run |
| TC-1829 | Reliability: a result arrives after close after clearing the chat | UI | P1 | not_run |
| TC-1830 | Reliability: a result arrives after close after an expired session | UI | P1 | not_run |
| TC-1831 | Reliability: the 15-second timeout fires on the first occurrence | UI | P1 | passed |
| TC-1832 | Reliability: the 15-second timeout fires after a page reload | UI | P1 | not_run |
| TC-1833 | Reliability: the 15-second timeout fires after a language switch | UI | P1 | not_run |
| TC-1834 | Reliability: the 15-second timeout fires on a slow device | UI | P1 | not_run |
| TC-1835 | Reliability: the 15-second timeout fires in a background tab | UI | P1 | not_run |
| TC-1836 | Reliability: the 15-second timeout fires with the panel reopened | UI | P1 | not_run |
| TC-1837 | Reliability: the 15-second timeout fires with auto-speak enabled | UI | P1 | not_run |
| TC-1838 | Reliability: the 15-second timeout fires with an error already visible | UI | P1 | not_run |
| TC-1839 | Reliability: the 15-second timeout fires after clearing the chat | UI | P1 | not_run |
| TC-1840 | Reliability: the 15-second timeout fires after an expired session | UI | P1 | not_run |
| TC-1841 | Reliability: a late result follows the timeout on the first occurrence | UI | P1 | not_run |
| TC-1842 | Reliability: a late result follows the timeout after a page reload | UI | P1 | not_run |
| TC-1843 | Reliability: a late result follows the timeout after a language switch | UI | P1 | not_run |
| TC-1844 | Reliability: a late result follows the timeout on a slow device | UI | P1 | not_run |
| TC-1845 | Reliability: a late result follows the timeout in a background tab | UI | P1 | not_run |
| TC-1846 | Reliability: a late result follows the timeout with the panel reopened | UI | P1 | not_run |
| TC-1847 | Reliability: a late result follows the timeout with auto-speak enabled | UI | P1 | not_run |
| TC-1848 | Reliability: a late result follows the timeout with an error already visible | UI | P1 | not_run |
| TC-1849 | Reliability: a late result follows the timeout after clearing the chat | UI | P1 | not_run |
| TC-1850 | Reliability: a late result follows the timeout after an expired session | UI | P1 | not_run |
| TC-1851 | Reliability: the network drops mid-listen on the first occurrence | UI | P1 | passed |
| TC-1852 | Reliability: the network drops mid-listen after a page reload | UI | P1 | not_run |
| TC-1853 | Reliability: the network drops mid-listen after a language switch | UI | P1 | not_run |
| TC-1854 | Reliability: the network drops mid-listen on a slow device | UI | P1 | not_run |
| TC-1855 | Reliability: the network drops mid-listen in a background tab | UI | P1 | not_run |
| TC-1856 | Reliability: the network drops mid-listen with the panel reopened | UI | P1 | not_run |
| TC-1857 | Reliability: the network drops mid-listen with auto-speak enabled | UI | P1 | not_run |
| TC-1858 | Reliability: the network drops mid-listen with an error already visible | UI | P1 | not_run |
| TC-1859 | Reliability: the network drops mid-listen after clearing the chat | UI | P1 | not_run |
| TC-1860 | Reliability: the network drops mid-listen after an expired session | UI | P1 | not_run |
| TC-1861 | Reliability: the language changes mid-listen on the first occurrence | UI | P1 | passed |
| TC-1862 | Reliability: the language changes mid-listen after a page reload | UI | P1 | not_run |
| TC-1863 | Reliability: the language changes mid-listen after a language switch | UI | P1 | not_run |
| TC-1864 | Reliability: the language changes mid-listen on a slow device | UI | P1 | not_run |
| TC-1865 | Reliability: the language changes mid-listen in a background tab | UI | P1 | not_run |
| TC-1866 | Reliability: the language changes mid-listen with the panel reopened | UI | P1 | not_run |
| TC-1867 | Reliability: the language changes mid-listen with auto-speak enabled | UI | P1 | not_run |
| TC-1868 | Reliability: the language changes mid-listen with an error already visible | UI | P1 | not_run |
| TC-1869 | Reliability: the language changes mid-listen after clearing the chat | UI | P1 | not_run |
| TC-1870 | Reliability: the language changes mid-listen after an expired session | UI | P1 | not_run |
| TC-1871 | Reliability: speech synthesis hangs on the first occurrence | UI | P1 | not_run |
| TC-1872 | Reliability: speech synthesis hangs after a page reload | UI | P1 | not_run |
| TC-1873 | Reliability: speech synthesis hangs after a language switch | UI | P1 | not_run |
| TC-1874 | Reliability: speech synthesis hangs on a slow device | UI | P1 | not_run |
| TC-1875 | Reliability: speech synthesis hangs in a background tab | UI | P1 | not_run |
| TC-1876 | Reliability: speech synthesis hangs with the panel reopened | UI | P1 | not_run |
| TC-1877 | Reliability: speech synthesis hangs with auto-speak enabled | UI | P1 | not_run |
| TC-1878 | Reliability: speech synthesis hangs with an error already visible | UI | P1 | not_run |
| TC-1879 | Reliability: speech synthesis hangs after clearing the chat | UI | P1 | not_run |
| TC-1880 | Reliability: speech synthesis hangs after an expired session | UI | P1 | not_run |
| TC-1881 | Reliability: retry is clicked repeatedly on the first occurrence | UI | P1 | not_run |
| TC-1882 | Reliability: retry is clicked repeatedly after a page reload | UI | P1 | not_run |
| TC-1883 | Reliability: retry is clicked repeatedly after a language switch | UI | P1 | not_run |
| TC-1884 | Reliability: retry is clicked repeatedly on a slow device | UI | P1 | not_run |
| TC-1885 | Reliability: retry is clicked repeatedly in a background tab | UI | P1 | not_run |
| TC-1886 | Reliability: retry is clicked repeatedly with the panel reopened | UI | P1 | not_run |
| TC-1887 | Reliability: retry is clicked repeatedly with auto-speak enabled | UI | P1 | not_run |
| TC-1888 | Reliability: retry is clicked repeatedly with an error already visible | UI | P1 | not_run |
| TC-1889 | Reliability: retry is clicked repeatedly after clearing the chat | UI | P1 | not_run |
| TC-1890 | Reliability: retry is clicked repeatedly after an expired session | UI | P1 | not_run |
| TC-1891 | Reliability: the component unmounts while listening on the first occurrence | UI | P1 | not_run |
| TC-1892 | Reliability: the component unmounts while listening after a page reload | UI | P1 | not_run |
| TC-1893 | Reliability: the component unmounts while listening after a language switch | UI | P1 | not_run |
| TC-1894 | Reliability: the component unmounts while listening on a slow device | UI | P1 | not_run |
| TC-1895 | Reliability: the component unmounts while listening in a background tab | UI | P1 | not_run |
| TC-1896 | Reliability: the component unmounts while listening with the panel reopened | UI | P1 | not_run |
| TC-1897 | Reliability: the component unmounts while listening with auto-speak enabled | UI | P1 | not_run |
| TC-1898 | Reliability: the component unmounts while listening with an error already visible | UI | P1 | not_run |
| TC-1899 | Reliability: the component unmounts while listening after clearing the chat | UI | P1 | not_run |
| TC-1900 | Reliability: the component unmounts while listening after an expired session | UI | P1 | not_run |

## Navigation and UI

### Routes

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1901 | Routes: route: / | UI | P2 | not_run |
| TC-1902 | Routes: route: /forecasting | UI | P2 | not_run |
| TC-1903 | Routes: route: /products | UI | P2 | not_run |
| TC-1904 | Routes: route: /categories | UI | P2 | not_run |
| TC-1905 | Routes: route: /suppliers | UI | P2 | not_run |
| TC-1906 | Routes: route: /sales-orders | UI | P2 | not_run |
| TC-1907 | Routes: route: /purchase-orders | UI | P2 | not_run |
| TC-1908 | Routes: route: /inventory-operations | UI | P2 | not_run |
| TC-1909 | Routes: route: /auth | UI | P2 | not_run |
| TC-1910 | Routes: route: unknown route | UI | P2 | not_run |

### Sidebar and mobile

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1911 | Sidebar and mobile: shell navigation: desktop sidebar | UI | P2 | not_run |
| TC-1912 | Sidebar and mobile: shell navigation: mobile menu opens | UI | P2 | not_run |
| TC-1913 | Sidebar and mobile: shell navigation: mobile menu closes | UI | P2 | not_run |
| TC-1914 | Sidebar and mobile: shell navigation: overlay click closes | UI | P2 | not_run |
| TC-1915 | Sidebar and mobile: shell navigation: active route state | UI | P2 | not_run |
| TC-1916 | Sidebar and mobile: shell navigation: sign out | UI | P2 | not_run |
| TC-1917 | Sidebar and mobile: shell navigation: identity display | UI | P2 | not_run |
| TC-1918 | Sidebar and mobile: shell navigation: logo link | UI | P2 | not_run |

### Search jump

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1919 | Search jump: module search: exact page name | UI | P2 | not_run |
| TC-1920 | Search jump: module search: keyword 'stock' | UI | P2 | not_run |
| TC-1921 | Search jump: module search: keyword 'vendors' | UI | P2 | not_run |
| TC-1922 | Search jump: module search: case-insensitive match | UI | P2 | not_run |
| TC-1923 | Search jump: module search: no-match feedback | UI | P2 | not_run |
| TC-1924 | Search jump: module search: clear feedback | UI | P2 | not_run |
| TC-1925 | Search jump: module search: Enter submits | UI | P2 | not_run |
| TC-1926 | Search jump: module search: mobile hides search | UI | P2 | not_run |

### 404 and error boundary

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1927 | 404 and error boundary: unknown route shows Page not found | UI | P2 | passed |
| TC-1928 | 404 and error boundary: nested unknown route | UI | P2 | not_run |
| TC-1929 | 404 and error boundary: ErrorBoundary fallback | UI | P2 | not_run |
| TC-1930 | 404 and error boundary: ErrorBoundary resets on navigation | UI | P2 | not_run |
| TC-1931 | 404 and error boundary: browser back button | UI | P2 | not_run |
| TC-1932 | 404 and error boundary: direct load of unknown route | UI | P2 | not_run |

### Accessibility

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1933 | Accessibility: shell accessibility: skip link | Accessibility | P2 | not_run |
| TC-1934 | Accessibility: shell accessibility: focus visible | Accessibility | P2 | not_run |
| TC-1935 | Accessibility: shell accessibility: heading order | Accessibility | P2 | not_run |
| TC-1936 | Accessibility: shell accessibility: landmarks | Accessibility | P2 | not_run |
| TC-1937 | Accessibility: shell accessibility: form labels | Accessibility | P2 | not_run |
| TC-1938 | Accessibility: shell accessibility: table headers | Accessibility | P2 | not_run |
| TC-1939 | Accessibility: shell accessibility: aria-live announcements | Accessibility | P2 | not_run |
| TC-1940 | Accessibility: shell accessibility: color contrast | Accessibility | P2 | not_run |
| TC-1941 | Accessibility: shell accessibility: keyboard dialogs | Accessibility | P2 | not_run |
| TC-1942 | Accessibility: shell accessibility: reduced motion | Accessibility | P2 | not_run |

### Responsive

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1943 | Responsive: responsive layout: 320px width | Accessibility | P2 | not_run |
| TC-1944 | Responsive: responsive layout: 390px width | Accessibility | P2 | not_run |
| TC-1945 | Responsive: responsive layout: 768px width | Accessibility | P2 | not_run |
| TC-1946 | Responsive: responsive layout: 1024px width | Accessibility | P2 | not_run |
| TC-1947 | Responsive: responsive layout: 1440px width | Accessibility | P2 | not_run |
| TC-1948 | Responsive: responsive layout: 1920px width | Accessibility | P2 | not_run |
| TC-1949 | Responsive: responsive layout: landscape phone | Accessibility | P2 | not_run |
| TC-1950 | Responsive: responsive layout: 200% zoom | Accessibility | P2 | not_run |

## Security and API

### Authentication required

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1951 | Authentication required: unauthenticated access: GET /products/ | API | P2 | not_run |
| TC-1952 | Authentication required: unauthenticated access: POST /products/ | API | P2 | not_run |
| TC-1953 | Authentication required: unauthenticated access: GET /categories/ | API | P2 | not_run |
| TC-1954 | Authentication required: unauthenticated access: POST /categories/ | API | P2 | not_run |
| TC-1955 | Authentication required: unauthenticated access: GET /suppliers/ | API | P2 | not_run |
| TC-1956 | Authentication required: unauthenticated access: POST /suppliers/ | API | P2 | not_run |
| TC-1957 | Authentication required: unauthenticated access: GET /orders/ | API | P2 | not_run |
| TC-1958 | Authentication required: unauthenticated access: POST /orders/ | API | P2 | not_run |
| TC-1959 | Authentication required: unauthenticated access: GET /purchase-orders/ | API | P2 | not_run |
| TC-1960 | Authentication required: unauthenticated access: GET /inventory-transactions/ | API | P2 | not_run |
| TC-1961 | Authentication required: unauthenticated access: GET /ml/insights | API | P2 | not_run |
| TC-1962 | Authentication required: unauthenticated access: POST /assistant/chat | API | P2 | not_run |

### Input validation

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1963 | Input validation: input attack: SQL injection in username | API | P2 | not_run |
| TC-1964 | Input validation: input attack: SQL injection in product name | API | P2 | not_run |
| TC-1965 | Input validation: input attack: SQL injection in search | API | P2 | not_run |
| TC-1966 | Input validation: input attack: SQL injection in customer name | API | P2 | not_run |
| TC-1967 | Input validation: input attack: SQL injection in supplier name | API | P2 | not_run |
| TC-1968 | Input validation: input attack: SQL injection in category name | API | P2 | not_run |
| TC-1969 | Input validation: input attack: SQL injection in inventory reason | API | P2 | not_run |
| TC-1970 | Input validation: input attack: script tag in assistant message | API | P2 | not_run |
| TC-1971 | Input validation: input attack: deeply nested JSON | API | P2 | not_run |
| TC-1972 | Input validation: input attack: oversized query parameter | API | P2 | not_run |

### CORS

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1973 | CORS: CORS behavior: allowed origin | API | P2 | not_run |
| TC-1974 | CORS: CORS behavior: disallowed origin | API | P2 | not_run |
| TC-1975 | CORS: CORS behavior: wildcard configuration rejected | API | P2 | not_run |
| TC-1976 | CORS: CORS behavior: preflight request | API | P2 | not_run |
| TC-1977 | CORS: CORS behavior: credentials disabled | API | P2 | not_run |
| TC-1978 | CORS: CORS behavior: allowed headers | API | P2 | not_run |

### Secrets and logging

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1979 | Secrets and logging: secret handling: JWT secret absent from responses | API | P2 | not_run |
| TC-1980 | Secrets and logging: secret handling: password absent from logs | API | P2 | not_run |
| TC-1981 | Secrets and logging: secret handling: assistant key absent from logs | API | P2 | not_run |
| TC-1982 | Secrets and logging: secret handling: database URL absent from responses | API | P2 | not_run |
| TC-1983 | Secrets and logging: secret handling: stack trace absent from 500 responses | API | P2 | not_run |
| TC-1984 | Secrets and logging: secret handling: token absent from URLs | API | P2 | not_run |
| TC-1985 | Secrets and logging: secret handling: .env ignored by git | API | P2 | not_run |
| TC-1986 | Secrets and logging: secret handling: sensitive docs skipped by retrieval | API | P2 | not_run |

### XSS and injection

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1987 | XSS and injection: XSS defense: script tag in product name | API | P2 | not_run |
| TC-1988 | XSS and injection: XSS defense: script tag in category name | API | P2 | not_run |
| TC-1989 | XSS and injection: XSS defense: script tag in supplier name | API | P2 | not_run |
| TC-1990 | XSS and injection: XSS defense: script tag in customer name | API | P2 | not_run |
| TC-1991 | XSS and injection: XSS defense: script tag in assistant reply | API | P2 | not_run |
| TC-1992 | XSS and injection: XSS defense: script tag in reason | API | P2 | not_run |
| TC-1993 | XSS and injection: XSS defense: stored XSS rendering | API | P2 | not_run |
| TC-1994 | XSS and injection: XSS defense: missing Content-Security-Policy | API | P2 | not_run |

### Rate limiting

| ID | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| TC-1995 | Rate limiting: rate limiting: login brute force | API | P2 | blocked |
| TC-1996 | Rate limiting: rate limiting: assistant abuse | API | P2 | blocked |
| TC-1997 | Rate limiting: rate limiting: registration spam | API | P2 | blocked |
| TC-1998 | Rate limiting: rate limiting: API burst | API | P2 | blocked |
| TC-1999 | Rate limiting: rate limiting: LLM cost abuse | API | P2 | blocked |
| TC-2000 | Rate limiting: rate limiting: 429 response behavior | API | P2 | blocked |

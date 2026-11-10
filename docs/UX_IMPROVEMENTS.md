# NextGenERP UX Improvements

Date: 2026-11-11

This document lists the user-facing changes made during the stabilization and
assistant work, why they matter, and what is still worth improving. Every item
marked "verified" was checked in the running app.

## 1. App shell and navigation

| Change | Before | After | Why it matters | Status |
| --- | --- | --- | --- | --- |
| Real identity | A hardcoded operator label | Username from `/auth/me` | Users can trust who is signed in | Verified |
| Skip link | None | "Skip to main content" appears on first Tab | Keyboard users bypass repeated navigation | Verified in DOM |
| 404 route | Blank content for unknown URLs | "Page not found" screen with a way back | Users are not stranded | Verified |
| Error boundary | One page error could blank the app | Friendly fallback with reset on navigation | Keeps the shell usable | Implemented |
| Module search feedback | Silent no-match | Visible no-match message and clear action | Users know the search ran | Verified |
| Mobile drawer | Basic open/close | Overlay, Escape/close behavior, focus return | Prevents a trapped or hidden menu | Verified in assistant E2E |
| Nav terminology | Mixed "AI"/"ML" labels | Operational labels such as "Demand Forecast" | Describes the job, not the implementation | Verified |

## 2. Dashboard

### Partial loading

Before: if any one of the five collection requests failed, the whole dashboard
showed an error and no data.

After:

- A banner names the sections that failed.
- Successful sections keep their live values.
- Failed sections show "Unavailable right now" or a section-specific message
  instead of a misleading zero.
- A "Try again" action reloads all sections without discarding good data.

Verified by aborting `/orders/` in the browser: products, categories, low-stock
alerts and counts stayed live, while sales cards and the recent-sales list showed
unavailable states.

### Copy

- Replaced "ML-driven demand signals" with "demand forecasts feeding the reorder
  queue".
- KPI cards distinguish loading (`—`) from a real zero.
- Empty states explain the next action instead of showing a bare table.

### Accessibility

- Stat values use `aria-live="polite"`.
- Failure banner uses `role="alert"`.
- Low-stock and out-of-stock lists have text labels, not color alone.
- The 3D warehouse has a text fallback when WebGL is unavailable.

## 3. Inventory Operations

The page was rebuilt to match the rest of the app shell.

| Area | Improvement |
| --- | --- |
| Structure | Removed the nested `<main>`; the page now has one landmark from the shell |
| Form | Grouped transaction type, product, quantity and reason with visible labels and inline validation |
| Context | Selected product shows current stock and reorder level before saving |
| Feedback | Success and error messages are separated and announced |
| Snapshot | Products, units on hand and low-stock count update after a refresh |
| History | Clear table with type badges, previous/new stock, reason and localized date |
| Load failure | A retryable banner appears without hiding the form |
| Empty state | Explains that the first recorded movement will start the history |
| Mobile | Form stacks cleanly; the history table scrolls horizontally |

Verified in the browser: exactly one `main` landmark, the form, snapshot and
history all render, and the page has no horizontal overflow at the tested
viewports.

## 4. Assistant

The assistant is available from a floating launcher on every authenticated page.
It supports English, Hindi and Bengali, with optional voice input and spoken
replies.

| Element | Behavior |
| --- | --- |
| Launcher | Visible on desktop and mobile; opens the panel; label follows the selected language |
| Header | Names the assistant and states that it covers project help and live workspace data |
| Language selector | English / हिन्दी / বাংলা; changing it resets the conversation and suggestions to the chosen language |
| Suggestions | Project-specific starting points in the selected language |
| Voice input | Microphone button uses the browser Web Speech API and sends the recognized transcript automatically |
| Spoken replies | Per-message speaker button; auto-speak toggle is off by default; playback stops on close, clear, Escape or language change |
| Conversation | Keeps context for follow-up questions; `role="log"`, `aria-live="polite"` and auto-scroll to the latest message |
| Errors | Shows the HTTP status and a Retry action without losing the conversation; microphone errors are shown separately |
| Scope note | Reminds the user that answers can be wrong and should be verified |
| Close | Close button and Escape; mobile panel fits the viewport |
| Read-only | The assistant explains actions but never performs them |

Voice reliability improvements:

- Microphone input is disabled with visible guidance on insecure HTTP origins
  (anything other than HTTPS or localhost). A forced click still cannot create a
  recognition session.
- Voices are loaded again when the browser fires `voiceschanged`, so late voice
  lists are used.
- Playback selects the exact locale voice, then a same-language voice, then a
  safe default.
- The interim transcript is shown while listening but only the final transcript
  is submitted.
- A 15-second silence timeout stops listening and explains what happened.
- Permission, service, no-speech, audio-capture, network,
  language-not-supported, busy and unknown errors each have specific localized
  guidance.
- Stop, Escape, close, language change and unmount abort recognition safely, and
  late results are ignored.
- A synchronous guard prevents a rapid double-click from starting two recognition
  sessions.

Verified with a mocked Web Speech API in headless Edge (41/41 checks), a genuine
insecure origin (8/8 checks), support-detection pages (4/4 checks) and a native
assistant language/layout run. The native run covered Hindi/Bengali welcome,
suggestions, live answers, Bengali scope refusal, Escape close and a 390 px
layout with zero horizontal overflow.

Not automated: real microphone capture and the browser permission prompt. The
voice E2E confirms the controls, language payloads, localized replies and
speaker state; actual audio input remains a manual check.

## 5. Administrator area

A separate administrator experience was added without exposing it to normal
users.

| Change | Before | After | Why it matters | Status |
| --- | --- | --- | --- | --- |
| Separate sign-in | No administrator concept | `/admin/login` with a distinct administrator layout | Keeps elevated access out of the normal workspace | Verified |
| Access denial | Not applicable | Normal users are rejected at sign-in and see an access-denied screen on `/admin` | Prevents accidental or forced entry | Verified |
| Overview | No business-wide view | Realized revenue, pending pipeline, order counts, inventory value, purchase spend and recent activity | Gives a commercial summary without mixing pending and realized revenue | Verified |
| Analytics tabs | None | Daily, monthly, yearly, user, product, inventory and supplier views | Covers the requested reporting dimensions | Verified |
| Charts | None | Lightweight accessible SVG line and bar charts with text summaries | Avoids a new chart dependency and keeps data readable to assistive technology | Verified |
| User management | None | Search, pagination, safe detail modal, activate/deactivate | Supports account administration without deleting business records | Verified |
| Guardrails | None | Self-deactivation disabled; last active administrator protected | Prevents locking the organization out | Verified |
| Mobile layout | None | Administrator shell and tables fit a 390 px viewport | Administrators can check the business from a phone | Verified |

Revenue presentation:

- Realized revenue is labelled separately from pending pipeline.
- Cancelled orders are excluded from both.
- Inventory value is explicitly labelled "at selling price".
- Empty and loading states are distinct from a real zero.

## 6. Authentication

- Split-screen layout with a clear sign-in form and password visibility toggle.
- Inline field validation and API error messages.
- Successful sign-in lands in the app shell; session expiry returns to sign-in.
- No demo credentials are embedded in production code.
- Copy explains the workspace instead of advertising "AI".

## 7. Forecasting

- User-facing labels describe demand planning and reorder suggestions.
- Loading, empty, error and refresh states are explicit.
- The All / Needs-reorder filter reports how many rows are visible.
- The 3D chart has a fallback and does not block the table.
- The frozen model and reported metrics are unchanged.

## 8. Responsive behavior

Checked widths: 390 px mobile and 1440 px desktop for the assistant and shell,
plus a 390 px administrator overview pass. The assistant panel measured
366 × 544 px at 390 px wide with 12 px side margins and zero horizontal overflow.
The administrator overview also fits 390 px without horizontal overflow.

Still recommended:

- Recheck at 320 px, 768 px and 200% zoom.
- Add a tablet-specific pass for the purchase-order table.
- Add a manual microphone-permission and audio-capture pass in a real browser
  session (headless Edge cannot grant or exercise a real microphone).

## 9. Remaining UX opportunities

| Priority | Opportunity | Benefit |
| --- | --- | --- |
| High | Add rate-limit and lockout feedback on the login form | Clear recovery when a user is temporarily blocked |
| High | Add a global toast for background failures | Users notice partial failures outside the dashboard |
| Medium | Paginate or virtualize large product/history tables | Keeps long lists fast |
| Medium | Add column sorting indicators to every table | Makes sort state obvious |
| Medium | Persist assistant conversation per session | Avoids losing context on navigation |
| Medium | Add a "copy answer" action | Useful for sharing troubleshooting steps |
| Low | Add dark-mode polish for the new inventory page | Visual consistency |
| Low | Add skeleton rows instead of dashes during loading | Perceived speed |

## 10. Design principles used

1. Never show a false zero when data failed to load.
2. Name the failed section and keep the rest usable.
3. Put the next action next to the empty or error state.
4. Use text as well as color for status.
5. Keep the assistant inside the product and explicit about its limits.
6. Preserve keyboard access and one main landmark per page.

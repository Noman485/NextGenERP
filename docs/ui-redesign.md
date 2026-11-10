# UI refresh & 3D visuals

This document describes the interface refresh shipped with the demand-forecasting
work: a warmer, denser "ops center" layout plus two Three.js visualisations driven
by live API data.

## What changed

| Area | Change |
| --- | --- |
| App shell (`src/App.jsx`) | New gradient sidebar with SVG icon set, active-route glow, forecast-engine status card, sticky translucent header, module-jump search, mobile drawer with overlay, signed-in user card |
| Icons (`src/components/Icons.jsx`) | Dependency-free inline SVG icon set (replaces the broken mojibake glyphs) |
| Dashboard (`src/pages/Dashboard.jsx`) | Dark hero panel with a live 3D warehouse snapshot, KPI chips, icon stat cards with accent bars, refined alert/health/activity panels |
| Forecasting (`src/pages/Forecasting.jsx`) | Dark hero with a hoverable 3D bar chart of daily demand, KPI cards, reorder table with All / Needs-reorder filter, per-product forecast cards with mini bars |
| Auth (`src/pages/Auth.jsx`) | Split-screen sign-in with brand panel, feature list, 3D preview, password visibility toggle |
| Global styles (`src/index.css`) | Inter-first font stack, warm radial background, custom scrollbars, focus rings, reduced-motion support |

## 3D components

Both components import `three` lazily (`await import('three')`), so the 3D
library is emitted as a separate chunk and only downloaded when a visual is
mounted.

### `Warehouse3D`

- Renders up to 12 crates in an isometric grid on a dark circular stage.
- Crate **height** is proportional to current stock; **colour** encodes health:
  teal = in stock, amber = at/below reorder level, red = out of stock.
- Slow sway animation, soft shadows, pointer parallax, and a graceful
  "3D preview unavailable" fallback when WebGL is not supported.
- Used on the dashboard hero and, with placeholder crates, on the sign-in page.

### `BarChart3D`

- Renders the aggregated 7-day demand forecast as seven hoverable bars.
- Raycasting highlights the hovered bar and updates the corner panel with that
  day's predicted units.
- Auto-sways gently; static when `prefers-reduced-motion` is set.

## Data flow

No API changes were required. Both visuals consume the existing endpoints:

- `GET /products/`, `/categories/`, `/suppliers/`, `/orders/`, `/purchase-orders/`
  → dashboard crate heights and KPI counts.
- `GET /ml/insights` → forecast rows (`date`, `predicted_demand`) and
  recommendations (`current_stock`, `reorder_quantity`, `urgent`, …).

## Accessibility

- 3D hosts expose `role="img"` with descriptive `aria-label` text.
- All controls are real buttons/links with visible focus rings.
- `prefers-reduced-motion` disables auto-animation and shortens transitions.
- Colour is never the only signal: statuses also carry text labels.

## Build notes

```powershell
cd frontend
npm install          # installs three
npm run build        # emits dist/assets/three.module-*.js as a lazy chunk
```

The Vite build reports a >500 kB warning for the lazy `three` chunk. It is not
part of the initial download; it loads only when a 3D visual appears.

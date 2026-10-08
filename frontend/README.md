# Frontend (Member 3) — Tomato-only scope

Plain HTML / CSS / JS + Bootstrap 5. No build step.

## What changed in this version
- **Tomato-only**: crop dropdowns removed (upload page shows a fixed " Tomato"
  label instead), `diseases.html` lists only tomato diseases, and all
  "Crop" table columns were dropped since the crop is always Tomato right now.
  `API.predict()` no longer sends a `crop_type` field — backend can assume Tomato.
- **Scrollable landing page**: `index.html` is now a single scrolling page with
  anchor sections (`#home`, `#about`, `#features`, `#how-it-works`, `#contact`),
  a sticky nav that highlights the active section as you scroll, smooth-scroll
  behavior, and a back-to-top button.

## Pages
| Page | Purpose | Auth required |
|---|---|---|
| `index.html` | Scrollable landing page (Home/About/Features/How It Works/Contact) | No |
| `login.html` | Login | No |
| `register.html` | Sign up | No |
| `dashboard.html` | Stats + recent predictions | Yes |
| `upload.html` | Upload tomato leaf image, run detection | Yes |
| `result.html` | Result of the last detection | Yes |
| `history.html` | Full prediction history with date filters | Yes |
| `diseases.html` | Reference: tomato diseases detected | Yes |
| `quality-guide.html` | Reference: what Good/Average/Poor mean | Yes |
| `profile.html` | View/edit account details | Yes |

## CSS
- `style.css` — shared base + landing page scroll/section styles
- `auth.css` — login/register only
- `dashboard.css` — app pages only
- `responsive.css` — breakpoint overrides, loaded last

## JS
- `api.js` — all backend calls + `API_BASE_URL` (the one line Member 2 edits)
- `auth.js`, `dashboard.js`, `upload.js`, `history.js`, `profile.js` — one script per page
- `result.html`, `diseases.html`, `quality-guide.html` use small inline scripts

## API contract (for Member 2 — Backend)
```
POST /api/auth/register   { name, email, password }        -> { token, user }
POST /api/auth/login      { email, password }               -> { token, user }
PUT  /api/user            { name, email }  (auth required)   -> { user }
GET  /api/predictions?limit=5                                -> [ prediction ]
GET  /api/predictions?from=&to=                               -> [ prediction ]
POST /api/predict         multipart: image                   -> prediction
GET  /api/stats                                               -> { total, diseased, healthy, avg_confidence }
```
`prediction` shape (crop is always "Tomato" for now):
```json
{
  "id": 12, "image_url": "https://.../uploads/xyz.jpg",
  "crop": "Tomato", "disease": "Early Blight", "is_healthy": false,
  "quality": "Good", "confidence": 94.6,
  "description": "...", "recommendation": "...",
  "created_at": "2026-08-20T10:30:00Z"
}
```
Auth: token-based (JWT). Any endpoint must return 401 for a missing/invalid
token — the frontend auto-redirects to `login.html` on 401.

## Assets
Drop real images into `assets/images/`: `hero-leaf.jpg`, `about-tomato.jpg`,
`auth-hero.jpg`, `auth-signup.jpg` (filenames already referenced in the pages).

## Before the backend is ready
Stub `js/api.js` methods to `return Promise.resolve({...})` with fake data.

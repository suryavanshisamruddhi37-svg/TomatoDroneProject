# Frontend (Member 3)

Plain HTML / CSS / JS + Bootstrap 5. No build step — open any `.html`
file directly, or serve the folder with any static server / Flask's
static files once integrated.

## Pages
| Page | Purpose | Auth required |
|---|---|---|
| `index.html` | Landing / marketing home | No |
| `login.html` | Login | No |
| `register.html` | Sign up | No |
| `dashboard.html` | Stats + recent predictions | Yes |
| `upload.html` | Upload image, select crop, run detection | Yes |
| `result.html` | Result of the last detection | Yes |
| `history.html` | Full prediction history with filters | Yes |
| `diseases.html` | Reference: diseases per crop | Yes |
| `quality-guide.html` | Reference: what Good/Average/Poor mean | Yes |
| `profile.html` | View/edit account details | Yes |

## CSS
- `style.css` — shared base (variables, buttons, cards, sidebar, badges)
- `auth.css` — login/register only
- `dashboard.css` — app pages only (stat cards, drop zone, table extras)
- `responsive.css` — breakpoint overrides, loaded last on every page

## JS
- `api.js` — **all** backend communication lives here, including the
  `API_BASE_URL` constant at the top. This is the one file Member 2
  (Backend) needs to point at their Flask server. Also exports
  `requireAuth()`, `logout()`, and `loadUserBadge()`, used by every
  protected page.
- `auth.js` — login/register form submission
- `dashboard.js`, `upload.js`, `history.js`, `profile.js` — one script
  per matching page
- `result.html` and `diseases.html`/`quality-guide.html` use small
  inline `<script>` blocks instead of dedicated files since their logic
  is minimal (rendering sessionStorage data / static reference content).

## API contract (for Member 2 — Backend)
```
POST /api/auth/register   { name, email, password }        -> { token, user }
POST /api/auth/login      { email, password }               -> { token, user }
PUT  /api/user            { name, email }  (auth required)   -> { user }
GET  /api/predictions?limit=5                                -> [ prediction ]
GET  /api/predictions?from=&to=&crop=                        -> [ prediction ]
POST /api/predict         multipart: image, crop_type        -> prediction
GET  /api/stats                                               -> { total, diseased, healthy, avg_confidence }
```

`prediction` object shape:
```json
{
  "id": 12,
  "image_url": "https://.../uploads/xyz.jpg",
  "crop": "Tomato",
  "disease": "Early Blight",
  "is_healthy": false,
  "quality": "Good",
  "confidence": 94.6,
  "description": "...",
  "recommendation": "...",
  "created_at": "2026-08-20T10:30:00Z"
}
```

Auth: token-based (JWT recommended). The frontend stores it in
`localStorage` as `cc_token` and sends `Authorization: Bearer <token>`
on every request after login. **Any endpoint must return 401 (not 403
or 500) for a missing/invalid token** — the frontend auto-redirects to
`login.html` on 401.

## Assets
Drop real images into:
- `assets/images/` — `hero-leaf.jpg`, `auth-hero.jpg`, `auth-signup.jpg`
  (referenced by `index.html`, `login.html` via `auth.css`, `register.html`)
- `assets/logo/` — app logo, if you want to swap the text-only "CropCare AI" brand
- `assets/icons/` — any custom icons beyond the emoji placeholders used for stat cards

## Before the backend is ready
Stub out methods in `js/api.js` to `return Promise.resolve({...})` with
fake data so pages can be built/demoed independently.

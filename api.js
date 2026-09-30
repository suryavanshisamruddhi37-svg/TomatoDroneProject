/**
 * api.js
 * ------
 * API_BASE_URL is the ONE line Member 2 (Backend) needs to change to
 * point the whole frontend at the Flask server.
 */
const API_BASE_URL = "http://127.0.0.1:5000/api";

/**
 * Endpoints expected from the backend:
 *   POST /auth/register  { name, email, password }        -> { token, user }
 *   POST /auth/login     { email, password }                -> { token, user }
 *   PUT  /user            { name, email }  (auth required)   -> { user }
 *   GET  /predictions?limit=5                                -> [ prediction ]
 *   GET  /predictions?from=&to=&crop=                        -> [ prediction ]
 *   POST /predict         multipart: image, crop_type        -> prediction
 *   GET  /stats                                               -> { total, diseased, healthy, avg_confidence }
 *
 * prediction shape:
 *   { id, image_url, crop, disease, is_healthy, quality,
 *     confidence, description, recommendation, created_at }
 */
const API = {
  _token() {
    return localStorage.getItem("cc_token");
  },

  async _request(path, options = {}) {
    const headers = options.headers || {};
    const token = this._token();
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });

    if (res.status === 401) {
      localStorage.removeItem("cc_token");
      localStorage.removeItem("cc_user");
      window.location.href = "login.html";
      throw new Error("Unauthorized");
    }

    let data = null;
    try { data = await res.json(); } catch (_) {}

    if (!res.ok) {
      throw new Error((data && data.message) || `Request failed (${res.status})`);
    }
    return data;
  },

 // --- TEMP STUB for local testing — remove before merging with backend ---
login(email, password) {
  return Promise.resolve({
    token: "fake-token-123",
    user: { id: 1, name: "Test User", email: email }
  });
},
register(name, email, password) {
  return Promise.resolve({
    token: "fake-token-123",
    user: { id: 1, name: name, email: email }
  });
},
// --- END STUB ---

/*
login(email, password) {
  return this._request("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
},

register(name, email, password) {
  return this._request("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
},
*/

  updateProfile(name, email) {
    return this._request("/user", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email }),
    });
  },

  getStats() {
    return this._request("/stats");
  },

  getPredictions(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return this._request(`/predictions${qs ? "?" + qs : ""}`);
  },

  predict(file, cropType) {
    const formData = new FormData();
    formData.append("image", file);
    formData.append("crop_type", cropType);
    return this._request("/predict", { method: "POST", body: formData });
  },
};

/** Redirects to login.html if no token is present. Call at the top of every protected page. */
function requireAuth() {
  if (!localStorage.getItem("cc_token")) {
    window.location.href = "login.html";
  }
}

function logout() {
  localStorage.removeItem("cc_token");
  localStorage.removeItem("cc_user");
  window.location.href = "login.html";
}

/** Fills in the topbar user name on every app page. Call after requireAuth(). */
function loadUserBadge() {
  const user = JSON.parse(localStorage.getItem("cc_user") || "{}");
  const el = document.getElementById("userName");
  if (el) el.textContent = user.name || "User";
}

requireAuth();
loadUserBadge();

function badgeClass(quality) {
  if (quality === "Good") return "badge-good";
  if (quality === "Average") return "badge-average";
  return "badge-poor";
}

function renderRows(predictions) {
  return predictions.map((p) => `
    <tr>
      <td><img src="${p.image_url}" width="42" height="42" class="rounded" style="object-fit:cover;"></td>
      <td>${p.disease}</td>
      <td><span class="badge ${badgeClass(p.quality)}">${p.quality}</span></td>
      <td>${p.confidence}%</td>
      <td class="text-muted small">${new Date(p.created_at).toLocaleString()}</td>
    </tr>`).join("");
}

async function loadDashboard() {
  const loading = document.getElementById("loadingState");
  const empty = document.getElementById("emptyState");
  const tableWrap = document.getElementById("tableWrap");

  try {
    const [stats, recent] = await Promise.all([API.getStats(), API.getPredictions({ limit: 5 })]);

    document.getElementById("statTotal").textContent = stats.total;
    document.getElementById("statDiseased").textContent = stats.diseased;
    document.getElementById("statHealthy").textContent = stats.healthy;
    document.getElementById("statAccuracy").textContent = stats.avg_confidence != null ? `${stats.avg_confidence}%` : "–";

    loading.classList.add("d-none");

    if (!recent || recent.length === 0) {
      empty.classList.remove("d-none");
      return;
    }

    tableWrap.innerHTML = `
      <table class="table align-middle">
        <thead class="text-muted small">
          <tr><th>Image</th><th>Condition</th><th>Quality</th><th>Confidence</th><th>Date</th></tr>
        </thead>
        <tbody>${renderRows(recent)}</tbody>
      </table>`;
  } catch (err) {
    loading.textContent = "Couldn't load dashboard data: " + err.message;
  }
}
loadDashboard();

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

async function loadHistory(filters = {}) {
  const loading = document.getElementById("loadingState");
  const empty = document.getElementById("emptyState");
  const tableWrap = document.getElementById("tableWrap");

  loading.classList.remove("d-none");
  empty.classList.add("d-none");
  tableWrap.innerHTML = "";

  try {
    const predictions = await API.getPredictions(filters);
    loading.classList.add("d-none");
    if (!predictions || predictions.length === 0) { empty.classList.remove("d-none"); return; }

    tableWrap.innerHTML = `
      <table class="table align-middle">
        <thead class="text-muted small">
          <tr><th>Image</th><th>Condition</th><th>Quality</th><th>Confidence</th><th>Date</th></tr>
        </thead>
        <tbody>${renderRows(predictions)}</tbody>
      </table>`;
  } catch (err) {
    loading.textContent = "Couldn't load history: " + err.message;
  }
}

document.getElementById("searchBtn").addEventListener("click", () => {
  const from = document.getElementById("fromDate").value;
  const to = document.getElementById("toDate").value;
  const filters = {};
  if (from) filters.from = from;
  if (to) filters.to = to;
  loadHistory(filters);
});

loadHistory();

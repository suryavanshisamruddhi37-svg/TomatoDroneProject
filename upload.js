requireAuth();
loadUserBadge();

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const chooseBtn = document.getElementById("chooseBtn");
const previewCard = document.getElementById("previewCard");
const previewImg = document.getElementById("previewImg");
const analyzeBtn = document.getElementById("analyzeBtn");
const analyzeBtnText = document.getElementById("analyzeBtnText");
const analyzeSpinner = document.getElementById("analyzeSpinner");
const uploadAlert = document.getElementById("uploadAlert");

let selectedFile = null;

chooseBtn.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("click", (e) => { if (e.target === dropZone) fileInput.click(); });
fileInput.addEventListener("change", (e) => { if (e.target.files[0]) handleFile(e.target.files[0]); });

["dragenter", "dragover"].forEach((evt) =>
  dropZone.addEventListener(evt, (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); }));
["dragleave", "drop"].forEach((evt) =>
  dropZone.addEventListener(evt, (e) => { e.preventDefault(); dropZone.classList.remove("drag-over"); }));
dropZone.addEventListener("drop", (e) => { const file = e.dataTransfer.files[0]; if (file) handleFile(file); });

function handleFile(file) {
  uploadAlert.classList.add("d-none");
  if (!file.type.startsWith("image/")) { showError("Please upload an image file."); return; }
  if (file.size > 10 * 1024 * 1024) { showError("Image must be under 10MB."); return; }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewCard.classList.remove("d-none");
  };
  reader.readAsDataURL(file);
}

document.getElementById("clearBtn").addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  previewCard.classList.add("d-none");
});

function showError(msg) {
  uploadAlert.textContent = msg;
  uploadAlert.classList.remove("d-none");
}

analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;
  const cropType = document.getElementById("cropSelect").value;

  analyzeBtn.disabled = true;
  analyzeBtnText.textContent = "Analyzing...";
  analyzeSpinner.classList.remove("d-none");
  uploadAlert.classList.add("d-none");

  try {
    const result = await API.predict(selectedFile, cropType);
    sessionStorage.setItem("cc_last_result", JSON.stringify(result));
    window.location.href = "result.html";
  } catch (err) {
    showError(err.message || "Detection failed. Please try again.");
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtnText.textContent = "Detect Disease";
    analyzeSpinner.classList.add("d-none");
  }
});

requireAuth();
loadUserBadge();

const user = JSON.parse(localStorage.getItem("cc_user") || "{}");
document.getElementById("profileName").value = user.name || "";
document.getElementById("profileEmail").value = user.email || "";
document.getElementById("profileAvatarLetter").textContent = (user.name || "U").charAt(0).toUpperCase();
document.getElementById("profileHeaderName").textContent = user.name || "—";

const profileForm = document.getElementById("profileForm");
profileForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("profileName").value.trim();
  const email = document.getElementById("profileEmail").value.trim();
  const alertBox = document.getElementById("profileAlert");
  const btn = document.getElementById("saveBtn");

  alertBox.className = "alert d-none py-2";
  btn.disabled = true;
  btn.textContent = "Saving...";

  try {
    const data = await API.updateProfile(name, email);
    localStorage.setItem("cc_user", JSON.stringify(data.user));
    document.getElementById("userName").textContent = data.user.name;
    alertBox.textContent = "Profile updated successfully.";
    alertBox.className = "alert alert-success py-2";
  } catch (err) {
    alertBox.textContent = err.message || "Couldn't update profile.";
    alertBox.className = "alert alert-danger py-2";
  } finally {
    btn.disabled = false;
    btn.textContent = "Save Changes";
  }
});

requireAuth(); loadUserBadge();
const user=JSON.parse(localStorage.getItem("cc_user")||"{}");
document.getElementById("profileName").value=user.name||"";
document.getElementById("profileEmail").value=user.email||"";
document.getElementById("profileAvatarLetter").textContent=(user.name||"U").charAt(0).toUpperCase();
document.getElementById("profileHeaderName").textContent=user.name||"—";
const form=document.getElementById("profileForm");
form.addEventListener("submit",async e=>{
 e.preventDefault(); const name=document.getElementById("profileName").value.trim(),email=document.getElementById("profileEmail").value.trim();
 const box=document.getElementById("profileAlert"),btn=document.getElementById("saveBtn"); box.className="alert d-none py-2";btn.disabled=true;btn.textContent="Saving...";
 try{const data=await API.updateProfile(name,email);localStorage.setItem("cc_user",JSON.stringify(data.user));document.getElementById("userName").textContent=data.user.name;document.getElementById("profileHeaderName").textContent=data.user.name;box.textContent="Profile updated successfully.";box.className="alert alert-success py-2";}
 catch(err){box.textContent=err.message||"Couldn't update profile.";box.className="alert alert-danger py-2";}
 finally{btn.disabled=false;btn.textContent="Save Changes";}
});

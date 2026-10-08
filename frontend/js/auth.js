const loginForm=document.getElementById("loginForm");
if(loginForm){
 loginForm.addEventListener("submit",async e=>{
  e.preventDefault();
  const id=document.getElementById("loginId").value.trim(), password=document.getElementById("password").value;
  const alertBox=document.getElementById("loginAlert"),btn=document.getElementById("loginBtn"),txt=document.getElementById("loginBtnText"),spin=document.getElementById("loginSpinner");
  alertBox.classList.add("d-none");
  if(!id||!password){alertBox.textContent="Please enter your phone number/email and password.";alertBox.classList.remove("d-none");return;}
  btn.disabled=true;txt.textContent="Signing in...";spin.classList.remove("d-none");
  try{const data=await API.login(id,password);localStorage.setItem("cc_token",data.token);localStorage.setItem("cc_user",JSON.stringify(data.user));window.location.href="dashboard.html";}
  catch(err){alertBox.textContent=err.message||"Login failed.";alertBox.classList.remove("d-none");}
  finally{btn.disabled=false;txt.textContent="Sign In";spin.classList.add("d-none");}
 });
}
const registerForm=document.getElementById("registerForm");
if(registerForm){
 registerForm.addEventListener("submit",async e=>{
  e.preventDefault();
  const profile={name:document.getElementById("name").value.trim(),phone:document.getElementById("phone").value.trim(),email:document.getElementById("email").value.trim(),area:document.getElementById("area").value.trim(),district:document.getElementById("district").value.trim(),state:document.getElementById("state").value.trim(),password:document.getElementById("password").value,confirmPassword:document.getElementById("confirmPassword").value};
  const alertBox=document.getElementById("registerAlert"),btn=document.getElementById("registerBtn"),txt=document.getElementById("registerBtnText"),spin=document.getElementById("registerSpinner");
  alertBox.classList.add("d-none");
  if(!profile.name||!profile.phone||!profile.area||!profile.district||!profile.state||!profile.password||!profile.confirmPassword){alertBox.textContent="Please fill in all required fields.";alertBox.classList.remove("d-none");return;}
  if(!/^[0-9]{10}$/.test(profile.phone)){alertBox.textContent="Please enter a valid 10-digit phone number.";alertBox.classList.remove("d-none");return;}
  if(profile.email&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profile.email)){alertBox.textContent="Please enter a valid email address or leave it blank.";alertBox.classList.remove("d-none");return;}
  if(profile.password.length<6){alertBox.textContent="Password must be at least 6 characters.";alertBox.classList.remove("d-none");return;}
  if(profile.password!==profile.confirmPassword){alertBox.textContent="Passwords do not match.";alertBox.classList.remove("d-none");return;}
  btn.disabled=true;txt.textContent="Creating account...";spin.classList.remove("d-none");
  try{const data=await API.register(profile);localStorage.setItem("cc_token",data.token);localStorage.setItem("cc_user",JSON.stringify(data.user));window.location.href="dashboard.html";}
  catch(err){alertBox.textContent=err.message||"Registration failed.";alertBox.classList.remove("d-none");}
  finally{btn.disabled=false;txt.textContent="Create Account";spin.classList.add("d-none");}
 });
}

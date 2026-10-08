const API_BASE_URL = "http://127.0.0.1:5000/api";
const DEMO_MODE = true;

const demoSeed = [
  {id:1,image_url:"",crop:"Tomato",disease:"Healthy",is_healthy:true,quality:"Good",confidence:96,description:"Healthy tomato leaf.",recommendation:"Continue regular monitoring and good crop hygiene.",created_at:new Date().toISOString()},
  {id:2,image_url:"",crop:"Tomato",disease:"Early Blight",is_healthy:false,quality:"Average",confidence:91,description:"Possible early blight symptoms.",recommendation:"Remove affected leaves and monitor nearby plants.",created_at:new Date(Date.now()-86400000).toISOString()}
];

function _demoPredictions(){ return JSON.parse(localStorage.getItem("cc_predictions") || "null") || demoSeed; }
function _savePredictions(p){ localStorage.setItem("cc_predictions", JSON.stringify(p)); }
function _demoUser(){ return JSON.parse(localStorage.getItem("cc_user") || "null"); }

const API = {
  _token(){ return localStorage.getItem("cc_token"); },

  async _request(path, options={}){
    if (DEMO_MODE) throw new Error("Demo mode");
    const headers=options.headers||{}; const token=this._token();
    if(token) headers["Authorization"]=`Bearer ${token}`;
    const res=await fetch(`${API_BASE_URL}${path}`,{...options,headers});
    if(res.status===401){localStorage.removeItem("cc_token");localStorage.removeItem("cc_user");window.location.href="login.html";throw new Error("Unauthorized");}
    let data=null; try{data=await res.json()}catch(_){}
    if(!res.ok) throw new Error((data&&data.message)||`Request failed (${res.status})`);
    return data;
  },

  async login(identifier,password){
    if(DEMO_MODE){
      const user=_demoUser();
      if(!user) throw new Error("No demo account found. Please create an account first.");
      const matches=identifier===user.phone || (user.email && identifier.toLowerCase()===user.email.toLowerCase());
      if(!matches || password!==user.password) throw new Error("Incorrect phone/email or password.");
      return {token:"demo-token",user};
    }
    return this._request("/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:identifier,password})});
  },

  async register(profile){
    if(DEMO_MODE){
      const user={...profile};
      delete user.confirmPassword;
      localStorage.setItem("cc_user",JSON.stringify(user));
      localStorage.setItem("cc_token","demo-token");
      if(!localStorage.getItem("cc_predictions")) _savePredictions(demoSeed);
      return {token:"demo-token",user};
    }
    return this._request("/auth/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(profile)});
  },

  async updateProfile(name,email){
    if(DEMO_MODE){
      const user={...(_demoUser()||{}),name,email};
      localStorage.setItem("cc_user",JSON.stringify(user));
      return {user};
    }
    return this._request("/user",{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({name,email})});
  },

  async getStats(){
    if(DEMO_MODE){
      const p=_demoPredictions();
      const diseased=p.filter(x=>!x.is_healthy).length, healthy=p.filter(x=>x.is_healthy).length;
      return {total:p.length,diseased,healthy,avg_confidence:p.length?Math.round(p.reduce((a,x)=>a+Number(x.confidence||0),0)/p.length):0};
    }
    return this._request("/stats");
  },

  async getPredictions(params={}){
    if(DEMO_MODE){
      let p=_demoPredictions();
      if(params.from) p=p.filter(x=>x.created_at.slice(0,10)>=params.from);
      if(params.to) p=p.filter(x=>x.created_at.slice(0,10)<=params.to);
      if(params.limit) p=p.slice(0,Number(params.limit));
      return p;
    }
    const qs=new URLSearchParams(params).toString(); return this._request(`/predictions${qs?"?"+qs:""}`);
  },

  async predict(file){
    if(DEMO_MODE){
      const image_url=URL.createObjectURL(file);
      const result={id:Date.now(),image_url,crop:"Tomato",disease:"Early Blight",is_healthy:false,quality:"Average",confidence:92,description:"Demo prediction: the uploaded image was accepted by the frontend.",recommendation:"For the real project, connect this action to the trained tomato disease model through the backend.",created_at:new Date().toISOString()};
      const p=_demoPredictions(); p.unshift(result); _savePredictions(p);
      return result;
    }
    const formData=new FormData(); formData.append("image",file); return this._request("/predict",{method:"POST",body:formData});
  }
};

function requireAuth(){ if(!localStorage.getItem("cc_token")) window.location.href="login.html"; }
function logout(){localStorage.removeItem("cc_token");localStorage.removeItem("cc_user");window.location.href="login.html";}
function loadUserBadge(){const user=JSON.parse(localStorage.getItem("cc_user")||"{}");const el=document.getElementById("userName");if(el)el.textContent=user.name||"User";}

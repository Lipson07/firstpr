async function reg() {
  const name = document.getElementById("name").value;
  const password = document.getElementById("password").value;
  const res = await fetch("http://127.0.0.1:8000/registr", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, password })
  });
  const data = await res.json();
  console.log(data);
  if (data.status == "ok") {
     
      localStorage.setItem('registrationData', JSON.stringify(data));
      window.location.href = "/success";
  }
}
setInterval(() => {
let name=document.getElementById("name").value
let password=document.getElementById("password").value
console.log(name,password)
}, 3000);
document.querySelector(".Logh2").addEventListener("click", reg);

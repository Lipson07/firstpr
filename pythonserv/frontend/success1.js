let imgmenu=document.querySelector(".imgmenu")
let krest=document.querySelector(".krest")
imgmenu.addEventListener("click", function() {
      console.log("111")
      document.querySelector(".form1_5").style.display = "flex";
      document.querySelector(".form1").style.display = "none";
})
krest.addEventListener("click", function() {
      document.querySelector(".form1_5").style.display = "none";
      document.querySelector(".form1").style.display = "flex";
})
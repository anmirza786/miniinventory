const collapsable = document.getElementById("navi");
const colla = document.querySelectorAll(".collapsable");
colla.forEach((item) =>
item.addEventListener("click", function (){
  this.classList.toggle("collapsable--expanded");
})
);
function expand(){
    collapsable.classList.add("collapsible--expanded");
}
function collaps(){
    collapsable.classList.remove("collapsible--expanded");
}


function popup(id){
  document.getElementById(id).classList.toggle("active");
}
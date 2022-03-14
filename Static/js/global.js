date = new Date().toLocaleDateString();
document.getElementById("current_date").innerHTML = date;

showTime()
function showTime(){
    myDate = new Date();
    hours = myDate.getHours();
    minutes = myDate.getMinutes();
    seconds = myDate.getSeconds();
    if (hours < 10) hours = "0" + hours;
    if (minutes < 10) minutes = "0" + minutes;
    if (seconds < 10) seconds = "0" + seconds;
    document.getElementById("current_time").innerHTML = hours+ ":" +minutes+ ":" +seconds;    
    setTimeout("showTime()", 1000);
    
    }
    
$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});


function validarValoresMinMax(){
  var mensaje = document.getElementById("mensaje");
  var btnGuardar = document.getElementById("btnGuardar");
  var valMin = document.getElementById("valorMin").value;
  var valMax = document.getElementById("valorMax").value;
 
  if(valMax<= valMin){
    mensaje.innerHTML = "El valor debe ser mayor al valor menor";
    btnGuardar.disabled = true;
  }else{
    mensaje.innerHTML = "";
    btnGuardar.disabled = false;
  }

 
}
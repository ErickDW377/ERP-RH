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
 
  if(valMax<valMin){
    mensaje.innerHTML = "El valor minimo debe ser menor o igual al maximo";
    btnGuardar.disabled = true;
  }else{
    mensaje.innerHTML = "";
    btnGuardar.disabled = false;
  }
}

function validarValoresMinMaxFechas(){
  var mensaje = document.getElementById("mensaje");
  var btnGuardar = document.getElementById("btnGuardar");
  var valMin = document.getElementById("valorMin").value;
  var valMax = document.getElementById("valorMax").value;
  valMin = new Date(valMin)
  valMax = new Date(valMax)
  if(valMax.getFullYear()<valMin.getFullYear()){
    mensaje.innerHTML = "La fecha inicio debe ser menor o a la fehca fin";
    btnGuardar.disabled = true;
  }else if(valMax.getFullYear()==valMin.getFullYear()){
      if(valMax.getMonth()<valMin.getMonth()){
          mensaje.innerHTML = "La fecha inicio debe ser menor o a la fehca fin";
          btnGuardar.disabled = true;
        }else if(valMax.getMonth()==valMin.getMonth()){
          if(valMax.getDate()<=valMin.getDate()){
              mensaje.innerHTML = "La fecha inicio debe ser menor o a la fehca fin";
              btnGuardar.disabled = true;
            }else{
              mensaje.innerHTML = "";
              btnGuardar.disabled = false;
            }      
        }else{
          mensaje.innerHTML = "";
          btnGuardar.disabled = false;
        }      
  }else{
      mensaje.innerHTML = "";
      btnGuardar.disabled = false;
  }
}

function consultarNombre(tabla) { 
  var ajax = new XMLHttpRequest();
  var btnGuardar = document.getElementById("btnGuardar");
  var nombre = document.getElementById("nombre");
  var url = "/"+tabla+"/nombre/" + nombre.value;
  var mensaje = document.getElementById("mensajeNombre");
  ajax.open("get", url, true);
  ajax.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var respuesta=JSON.parse(this.responseText);
      if(respuesta.estatus=="Error" ){
        btnGuardar.disabled = true;   
        mensaje.innerHTML=respuesta.mensaje;
      }else{
        mensaje.innerHTML = "";
        btnGuardar.disabled = false;
      }    
    }
  };
  ajax.send();
} 

$(function(){
  $(".dropdown-menu > li > a.trigger").on("click",function(e){
      var current=$(this).next();
      var grandparent=$(this).parent().parent();
      if($(this).hasClass('left-caret')||$(this).hasClass('right-caret'))
          $(this).toggleClass('right-caret left-caret');
      grandparent.find('.left-caret').not(this).toggleClass('right-caret left-caret');
      grandparent.find(".sub-menu:visible").not(current).hide();
      current.toggle();
      e.stopPropagation();
  });
  $(".dropdown-menu > li > a:not(.trigger)").on("click",function(){
      var root=$(this).closest('.dropdown');
      root.find('.left-caret').toggleClass('right-caret left-caret');
      root.find('.sub-menu:visible').hide();
  });
});
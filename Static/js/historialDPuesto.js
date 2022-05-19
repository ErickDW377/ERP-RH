function validarFechas(fecha1, fecha2, fecha3) {  
    bandera = false;
    if (fecha1.getFullYear()< fecha2.getFullYear() || fecha1.getFullYear()> fecha3.getFullYear() ) {
        bandera = true;
    } else {        
        if (fecha1.getMonth()< fecha2.getMonth() || fecha1.getMonth()> fecha3.getMonth()) {
            bandera = true;
        } else {
            if (fecha1.getDate()< fecha2.getDate() || fecha1.getDate()> fecha3.getDate()) {
                bandera = true
            }

        }

    }
    return bandera
}

function validacion(id,fecha,p,d){
  var ajax = new XMLHttpRequest();
  var btnGuardar = document.getElementById("btnGuardar");
  var mensaje = document.getElementById("mensajeNombre");
  fechaInicio = document.getElementById("fechaInicio").value;
  fechaFin = document.getElementById("fechaFin").value;  
  fechaInicio = new Date(fechaInicio);
  fechaFin = new Date(fechaFin);  
  var url = "/validarFechasHP/" +id+ "/"+ p+"/"+d+"/"+fecha; 
  ajax.open("get", url, true);
  ajax.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var respuesta=JSON.parse(this.responseText);
      console.log(respuesta);
      for(var i in respuesta){
          i.fechaInicio = new Date(i.fechaInicio);
          i.fechaFin = new Date(i.fechaFin);
          if(
            validarFechas(fechaInicio, i.fechaInicio, i.fechaFin)  && validarFechas(fechafin, i.fechaInicio, i.fechaFin) &&
            validarFechas(i.fechaInicio,fechaInicio, fechaFin)  && validarFechas(i.fechafin, fechaInicio, fechaFin)                        
          ){
            mensaje.innerHTML="";
            
            if (getDias(fechaInicio, fechaFin)>=0) {
                mensaje.innerHTML="";
                btnGuardar.disabled = false; 
            }else{
                mensaje.innerHTML = "La fecha fin no puede ser menor a la fecha inicio";
                btnGuardar.disabled = true;
            }   
            

          }else{
            mensaje.innerHTML = "Ya tiene un historial dentro de ese rango de fehcas";
            btnGuardar.disabled = true;
          }
             
      }
      
    }
  };
  ajax.send();
}

function getDias(aFecha1, aFecha2) {    
    
    aFecha1 = (aFecha1.getDate() + 1) + "/" + (aFecha1.getMonth() + 1) + "/" + aFecha1.getFullYear();
    aFecha1 = aFecha1.split('/');


   
    aFecha2 = (aFecha2.getDate() + 1) + "/" + (aFecha2.getMonth() + 1) + "/" + aFecha2.getFullYear();
    aFecha2 = aFecha2.split('/');

    var fFecha1 = Date.UTC(aFecha1[2], aFecha1[1] - 1, aFecha1[0]);
    var fFecha2 = Date.UTC(aFecha2[2], aFecha2[1] - 1, aFecha2[0]);
    var dif = fFecha2 - fFecha1;
    var dias = Math.floor(dif / (1000 * 60 * 60 * 24));
    return dias;
}

function validacion2(){
    var btnGuardar = document.getElementById("btnGuardar");
    var mensaje = document.getElementById("mensajeNombre");
    fechaInicio = document.getElementById("fechaInicio").value;
    fechaFin = document.getElementById("fechaFin").value;  
      
    fechaInicio = new Date(fechaInicio);
    fechaFin = new Date(fechaFin);  
    if (getDias(fechaInicio, fechaFin)>=0) {
        mensaje.innerHTML="";
        btnGuardar.disabled = false; 
    }else{
        mensaje.innerHTML = "La fecha fin no puede ser menor a la fecha inicio";
        btnGuardar.disabled = true;
    }   
}
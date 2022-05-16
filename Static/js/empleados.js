function consultarNombreCompleto() { 
    var ajax = new XMLHttpRequest();
    var btnGuardar = document.getElementById("btnGuardar");
    var nombre = document.getElementById("nombre");
    var paterno = document.getElementById("paterno");
    var materno = document.getElementById("materno");
    var mensaje = document.getElementById("mensajeNombre");

    if(nombre.value != '' && paterno.value!='' && materno.value!='' ){    
        var url = "/empleados/nombre/" + nombre.value + "/" + paterno.value+ "/" + materno.value;
        
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
}

function consultarEmail() { 
  var ajax = new XMLHttpRequest();
  var btnGuardar = document.getElementById("btnGuardar");
  var email = document.getElementById("email");  
  var url = "/empleados/email/" + email.value;
  var mensaje = document.getElementById("mensajeEmail");
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

function consultarCURP() { 
  var ajax = new XMLHttpRequest();
  var btnGuardar = document.getElementById("btnGuardar");
  var curp = document.getElementById("curp");  
  var url = "/empleados/curp/" + curp.value;
  var mensaje = document.getElementById("mensajeCURP");
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

function consultarNSS() { 
    var ajax = new XMLHttpRequest();
    var btnGuardar = document.getElementById("btnGuardar");
    var nss = document.getElementById("nss");  
    var url = "/empleados/nss/" + nss.value;
    var mensaje = document.getElementById("mensajeNSS");
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

function validarSalario() { 
    var ajax = new XMLHttpRequest();
    var btnGuardar = document.getElementById("btnGuardar");
    var salario = document.getElementById("salario");
    var puesto = document.getElementById("puesto"); 
    var url = "/empleados/salario/" + salario.value+"/"+puesto.value;
    var mensaje = document.getElementById("mensajeSalario");
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

function validarEdad(){
    var btnGuardar = document.getElementById("btnGuardar");    
    var nacimiento = document.getElementById("nacimiento").value;
    var mensaje = document.getElementById("mensajeEdad");
    var date = new Date()    
    nacimiento = new Date(nacimiento)
    var edad = (date.getFullYear() - nacimiento.getFullYear())    
    var diferenciaMeses = date.getMonth() - nacimiento.getMonth()
    if (
        diferenciaMeses < 0 ||
        (diferenciaMeses === 0 && date.getDate() < nacimiento.getDate())
    ) {
        edad--
    }    
    if (edad<18){
        mensaje.innerHTML="No puedes registrar a un empleado menor de edad";
        btnGuardar.disabled = true;
    }else{
        mensaje.innerHTML="";
        btnGuardar.disabled = false;
    }
    
}


function consultarDocumento(tabla,id) {  
  var ajax = new XMLHttpRequest();
  var btnGuardar = document.getElementById("btnGuardar");
  var nombre = document.getElementById("nombre");
  var url = "/"+tabla+"/nombre/" + nombre.value+"/"+id; 
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


function llenarSucursales(){
  var ajax = new XMLHttpRequest();
  ciudad = document.getElementById("ciudad");
  select = document.getElementById("sucursales");
  for(i = 0; i<=select.options.length;i++){
    select.remove(0);
  }
  var url = "/sucursalesCiudad/" + ciudad.value; 
  ajax.open("get", url, true);
  ajax.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var respuesta=JSON.parse(this.responseText);
      for(var i in respuesta){
        option = document.createElement("option");
        option.value = respuesta[i].id;
        option.text = respuesta[i].nombre;
        select.appendChild(option);        
      }
      select.disabled = false
    }
  };
  ajax.send();
 
  
}

function llenarCiudades(){
  var ajax = new XMLHttpRequest();
  estado = document.getElementById("estado");
  select = document.getElementById("ciudad");
  for(i = 0; i<=select.options.length;i++){
    select.remove(0);
  }
  var url = "/ciudadesEstado/" + estado.value; 
  ajax.open("get", url, true);
  ajax.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var respuesta=JSON.parse(this.responseText);
      for(var i in respuesta){
        option = document.createElement("option");
        option.value = respuesta[i].id;
        option.text = respuesta[i].nombre;
        select.appendChild(option);        
      }
      select.disabled = false
      llenarSucursales()
    }
  };
  ajax.send();
 
 
}
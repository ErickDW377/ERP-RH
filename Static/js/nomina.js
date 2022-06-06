

var nomina;
var empleado = document.getElementById("empleado");
var percepcion = document.getElementById("percepcion");

var tablaP = document.getElementById("tablaP");
var retenciones =0;
var subtotal=0;
var sueldo=0;
var salario = 0;


var deduccionArr =[];

function registrarDeduccion(idD,idN,importe){
    var ajax = new XMLHttpRequest();    
    var mensaje = document.getElementById("mensajeNombre");
    var url = "/registrarNominaDeduccion/" +idN+ "/"+ idD+"/"+importe; 
    ajax.open("post", url, true);
    ajax.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
       
        console.log(this.responseText);       
        
      }
    };
    ajax.send();
  }


  function registrarPercepciones(idP,idN,importe){
    var ajax = new XMLHttpRequest();    
    var mensaje = document.getElementById("mensajeNombre");
    var url = "/registrarNominaPercepcion/" +idN+ "/"+ idP+"/"+importe; 
    ajax.open("post", url, true);
    ajax.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
       
        console.log(this.responseText);       
        
      }
    };
    ajax.send();
  }

  function eliminarDeduccion(idD,idN){
    var ajax = new XMLHttpRequest();    
    var mensaje = document.getElementById("mensajeNombre");
    var url = "/eliminarNominaDeduccion/" +idN+ "/"+ idD; 
    ajax.open("post", url, true);
    ajax.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
       
        console.log(this.responseText);       
        
      }
    };
    ajax.send();
  }


  function eliminarPercepciones(idP,idN){
    var ajax = new XMLHttpRequest();    
    var mensaje = document.getElementById("mensajeNombre");
    var url = "/eliminarNominaPercepcion/" +idN+ "/"+ idP; 
    ajax.open("post", url, true);
    ajax.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
       
        console.log(this.responseText);       
        
      }
    };
    ajax.send();
  }
function addDeduccion(idN){
    
    var deduccion =document.getElementById("deduccion");
    var porcentaje =document.getElementById("porcentaje").value;
    var importe =document.getElementById("importeD").value;
    var tablaD = document.getElementById("tablaD");
    var retencion = document.getElementById("retenciones");
    registrarDeduccion(deduccion.value,idN,parseInt(importe, 10));
    
    var fila = "<tr > <td>"+
    deduccion.options[deduccion.selectedIndex].text
    + "</td><td>" +
    porcentaje
    + "</td><td>" +
    importe
    + "</td>"+
    "<td> <a  class='btn btn-danger' role='button' onclick='deleteDeduccion("+ idN+ ","+deduccion.value+ ","+ importe+")'> <span class='glyphicon glyphicon-trash'></span></a></td></tr>"    
    ;
    var btn = document.createElement("TR");
    btn.setAttribute('id',deduccion.value);
   	btn.innerHTML=fila;
    tablaD.appendChild(btn);    
    retenciones+= parseInt(importe, 10);
    retencion.value = retenciones;
    setTotal();
    
}

function deleteDeduccion(idN,id,importe){
    
    var deduccion =document.getElementById(id);
    var retencion = document.getElementById("retenciones"); 
    eliminarDeduccion(id,idN)
    deduccion.remove();   
    retenciones-= parseInt(importe, 10);
    retencion.value = retenciones;
    setTotal();
}



function addPercepcion(idN){
    
    var percepcion =document.getElementById("percepcion");
    var dias =document.getElementById("dias").value;
    var importe =document.getElementById("importeP").value;
    var tabla = document.getElementById("tablaP");
    var subtotales = document.getElementById("subtotal");
    registrarPercepciones(percepcion.value,idN,parseInt(importe, 10));
    
    

    var fila = "<tr > <td>"+
    percepcion.options[percepcion.selectedIndex].text
    + "</td><td>" +
    dias
    + "</td><td>" +
    importe
    + "</td>"+
    "<td> <a  class='btn btn-danger' role='button' onclick='deletePercepcion("+ idN+ ","+percepcion.value+ ","+ importe+")'> <span class='glyphicon glyphicon-trash'></span> </a></td></tr>"    
    ;
    var btn = document.createElement("TR");
    btn.setAttribute('id',(percepcion.value+"P"));
   	btn.innerHTML=fila;
    tabla.appendChild(btn);    
    subtotal+= parseInt(importe, 10);
    subtotales.value = subtotal;
    
    setTotal();
}

function deletePercepcion(idN,id,importe){
    
    var percepcion =document.getElementById(id+"P");
    var subtotales = document.getElementById("subtotal"); 
    eliminarPercepciones(id,idN)
    percepcion.remove();   
    subtotal-= parseInt(importe, 10);
    subtotales.value = subtotal;
    setTotal();
}


function setPorcentaje(){
  
  s = document.getElementById('deduccion');
  var porcentaje =document.getElementById("porcentaje");
  var importe =document.getElementById("importeD");
  i = parseInt(importe.value);
  p = parseInt(sl =s.options[s.selectedIndex].id);
  porcentaje.value = p;
  importe.value = sueldo * p / 100;
  

}
function setDias(){
  
  s = document.getElementById('percepcion');
  var porcentaje =document.getElementById("dias");
  var importe =document.getElementById("importeP");
  i = parseInt(importe.value);
  p = parseInt(sl =s.options[s.selectedIndex].id);
  porcentaje.value = p;
  importe.value = sueldo * p;
  

}

function setSueldo(){
s = document.getElementById('empleado');
sl =s.options[s.selectedIndex].id;
sueldo = parseInt(sl);

}

function setTotal(){
  total = subtotal-retenciones+salario;
  document.getElementById('total').value= total;
}

function setCantidades(){
salario = parseInt(document.getElementById('diasTrabajados').value)* sueldo;
subtotal = parseInt(document.getElementById('subtotal').value);
retenciones = parseInt(document.getElementById('retenciones').value);
setTotal();
}


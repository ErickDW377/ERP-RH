function getDia(){
    var fecha = document.getElementById("fecha").value;
    var d = document.getElementById("dia");
    var fecha = new Date(fecha);
    var dia = fecha.getDay();
    
    switch (dia) {
        case 6:
            d.value =  "Domingo";
            break;         
        case 0:
            d.value =  "Lunes";
            break;          
        case 1:
            d.value =  "Martes";
            break;        
        case 2:
            d.value =  "Miercoles";
            break;
        case 3:
            d.value =  "Jueves";
            break;
        case 4:
            d.value =  "Viernes";
            break;
        case 5:
            d.value =  "Sabado";
            break;
         
        default:
            d.value =  "";
            break;
          
      }
      

}
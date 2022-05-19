function validarFechas(fecha1, fecha2, fecha3) {    
    

    
    bandera = false;
    if (fecha1.getFullYear()) {
        bandera = true;
    } else if (diferencia == 0) {
        diferencia = (fechaComparar.getMonth() - fechaInicio.getMonth());
        if (diferencia > 0) {
            bandera = true;
        } else if (diferencia == 0) {
            
                diferencia = (fechaInicio.getDate() - fechaComparar.getDate());
           

            if (diferencia >= dias) {
                bandera = true
            }

        }

    }
    return bandera
}
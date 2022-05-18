
function validarFechas(dias, fecha) {


    var fechaInicio = document.getElementById("fechaInicio").value;
    var fechaComparar = fecha


    fechaInicio = new Date(fechaInicio)

    var diferencia;
    diferencia = (fechaComparar.getFullYear() - fechaInicio.getFullYear());
    bandera = false;
    if (diferencia > 0) {
        bandera = true;
    } else if (diferencia == 0) {
        diferencia = (fechaComparar.getMonth() - fechaInicio.getMonth());
        if (diferencia > 0) {
            bandera = true;
        } else if (diferencia == 0) {
            if (dias > 0) {
                diferencia = (fechaInicio.getDate() - fechaComparar.getDate());
            } else {
                diferencia = (fechaComparar.getDate() - fechaInicio.getDate());
            }

            if (diferencia >= dias) {
                bandera = true
            }

        }

    }
    return bandera
}



function validaciones() {
    var btnGuardar = document.getElementById("btnGuardar");
    var btnGuardar2 = document.getElementById("btnGuardar2");
    var tipo = document.getElementById("tipo");
    tipo = tipo.options[tipo.selectedIndex].innerHTML;
    var mensaje = document.getElementById("mensajeFechas1");


    var validarInicio
    if (tipo == "Incapacidad") {
        validarInicio = true;

    } else {
        validarInicio = validarFechas(6, new Date());
    }
    if (validarInicio) {
        mensaje.innerHTML = "";
        var fechaFin = document.getElementById("fechaFin").value;
        if (fechaFin != "") {
            fechaFin = new Date(fechaFin)
            if (validarFechas(0, fechaFin)) {
                mensaje.innerHTML = "";
                if (tipo != "Incapacidad") {
                    var diasRestantes
                    var ajax = new XMLHttpRequest();
                    var url = "/puedeAusentarce";
                    ajax.open("get", url, true);
                    ajax.onreadystatechange = function () {
                        if (this.readyState == 4 && this.status == 200) {
                            var respuesta = JSON.parse(this.responseText);
                            if (tipo == "Permiso") {

                                diasRestantes = respuesta.diasP
                            } else if (tipo == "Vacaciones") {
                                diasRestantes = respuesta.diasV
                            }
                            var dias = diasRestantes - getDias();

                            if (dias >= 0) {
                                mensaje.innerHTML = "";
                                btnGuardar.disabled = false;
                                btnGuardar2.disabled = false;
                            } else {
                                mensaje.innerHTML = "No tienes suficientes días de " + tipo + ". Solo tienes " + diasRestantes + " días restantes";
                                btnGuardar.disabled = true;
                                btnGuardar2.disabled = true;
                            }
                        }
                    };
                    ajax.send();
                }else{
                    
                    btnGuardar.disabled = false;
                    btnGuardar2.disabled = false;
                }



            } else {

                mensaje.innerHTML = "Periodo invalido, La fecha fin no puede ser menos a la fecha inicio";
                btnGuardar.disabled = true;
                btnGuardar2.disabled = true;
            }
        }



    } else {

        mensaje.innerHTML = "Periodo invalido, Se debe solicitar al menos 7 dias antes del periodo solicitado";
        btnGuardar.disabled = true;
        btnGuardar2.disabled = true;
    }

}

function getDias() {

    var aFecha1 = document.getElementById("fechaInicio").value;
    aFecha1 = new Date(aFecha1);
    aFecha1 = (aFecha1.getDate() + 1) + "/" + (aFecha1.getMonth() + 1) + "/" + aFecha1.getFullYear();
    aFecha1 = aFecha1.split('/');


    var aFecha2 = document.getElementById("fechaFin").value;
    aFecha2 = new Date(aFecha2);
    aFecha2 = (aFecha2.getDate() + 1) + "/" + (aFecha2.getMonth() + 1) + "/" + aFecha2.getFullYear();
    aFecha2 = aFecha2.split('/');

    var fFecha1 = Date.UTC(aFecha1[2], aFecha1[1] - 1, aFecha1[0]);
    var fFecha2 = Date.UTC(aFecha2[2], aFecha2[1] - 1, aFecha2[0]);
    var dif = fFecha2 - fFecha1;
    var dias = Math.floor(dif / (1000 * 60 * 60 * 24));
    return dias + 1;
}



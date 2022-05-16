create database RH_ERP;
use  RH_ERP;

create table RH_Deducciones(
idDeduccion int auto_increment,
nombre varchar(30),
descripcion varchar(80),
porcentaje float,
estatus char,
primary key(idDeduccion),
check(estatus in ('A','I'))
);
create table RH_Periodos(
idPeriodo int auto_increment,
nombre varchar(50),
fechaInicio date,
fechaFin date,
estatus char,
primary key(idPeriodo),
check(fechaInicio<=fechaFin),
check(estatus in ('A','I'))
);
create table RH_FormasPago(
idFormaPago int auto_increment,
nombre varchar(50) unique,
estatus char,
primary key(idFormaPago),
check(estatus in ('A','I'))
);
create table RH_Puestos(
idPuesto int auto_increment,
nombre varchar(60) unique,
salarioMinimo float,
salarioMaximo float,
estatus char,
primary key (idPuesto),
check(salarioMinimo<=salarioMaximo),
check(estatus in ('A','I'))
);

create table RH_Percepciones(
idPercepcion int auto_increment,
nombre varchar(30),
descripcion varchar(80),
diasPagar int,
estatus char,
primary key(idPercepcion),
check(estatus in ('A','I'))
);

create table RH_Turnos(
idTurno int auto_increment,
nombre varchar(20),
horaInicio timestamp,
horaFin timestamp,
dias varchar (30),
estatus char,
primary key(idTurno)
);

create table RH_Departamentos(
idDepartamento int auto_increment,
nombre varchar(20) unique,
estatus char,
primary key (idDepartamento),
check(estatus in ('A','I'))
);
create table RH_Estados(
idEstado int auto_increment,
nombre varchar(60) unique,
siglas varchar(10) unique,
estatus char,
primary key (idEstado),
check(estatus in ('A','I'))
);
create table RH_Ciudades(
idCiudad int auto_increment,
nombre varchar(80),
idEstado int,
estatus char,
primary key (idCiudad),
foreign key (idEstado) references RH_Estados (idEstado),
unique(nombre, idEstado),
check(estatus in ('A','I'))
);
create table RH_Sucursales(
 idSucursal int auto_increment,
 nombre varchar(50),
 telefono varchar(15) unique,
 direccion varchar(80) unique,
 colonia varchar(50),
 codigoPostal varchar(5),
 presupuesto float,
 estatus char,
 idCiudad int,
 Primary key(idSucursal),
 Foreign key (idCiudad) references RH_Ciudades (idCiudad), 
 check(estatus in ('A','I'))
);

create table RH_Empleados(
idEmpleado int auto_increment, 
nombre varchar(30),
apellidoPaterno varchar(30),
apellidoMaterno varchar(30),
sexo char,
fechaNacimiento date,
curp varchar(20) unique,
estadoCivil varchar(20),
fechaContratacion date,
salarioDiario float,
nss varchar(20) unique,
diasVacaciones int,
diasPermiso int,
fotografia mediumblob,
direccion varchar(30),
colonia varchar(50),
codigoPostal  varchar(5),
escolaridad  varchar(80),
especialidad varchar(100),
email  varchar(100) unique,
paassword  varchar(20),
tipo  varchar(10),
estatus char,
idDepartamento int,
idPuesto int,
idCiudad int,
idSucursal int,
idTurno int,
primary key(idEmpleado),
foreign key (idCiudad) references RH_Ciudades(idCiudad),
foreign key (idPuesto) references RH_Puestos(idPuesto),
foreign key (idDepartamento) references RH_Departamentos(idDepartamento),
foreign key (idTurno) references RH_Turnos(idTurno),
foreign key (idSucursal) references RH_Sucursales(idSucursal),
unique(nombre, apellidoPaterno,apellidoMaterno),
check(sexo in ('M','F')),
check(tipo in ('Admin','Staff','Empleado')),
check(estatus in ('A','I'))
);
create table RH_Asistencias(
idAsistencia int auto_increment,
fecha date,
horaEntrada timestamp,
horaSalida timestamp,
dia varchar(20),
idEmpleado int,
primary key (idAsistencia),
foreign key (idEmpleado) references RH_Empleados (idEmpleado),
unique(idEmpleado, fecha)
);
create table RH_Ausencias_Justificadas(
idAusencia int auto_increment,
fechaSolicitud date,
fechaInicio date,
fechaFin date,
tipo char,
idEmpleadoSolicita int,
idEmpleadoAutoriza int,
evidencia blob,
estatus char,
motivo varchar(100),
primary key (idAusencia),
foreign key (idEmpleadoAutoriza) references RH_Empleados(idEmpleado),
foreign key (idEmpleadoSolicita) references RH_Empleados(idEmpleado)
);
create table RH_HistorialPuesto(
idEmpleado int auto_increment,
idPuesto int,
idDepartamento int,
fechaInicio date,
fechaFin date,
primary key (idEmpleado,idPuesto,idDepartamento,fechaInicio),
foreign key (idPuesto) references RH_Puestos(idPuesto),
foreign key (idEmpleado) references RH_Empleados(idEmpleado),
foreign key (idDepartamento) references RH_Departamentos (idDepartamento)
);
create table RH_DocumentacionEmpleado(
idDocumento int auto_increment,
nombreDocumento varchar(80),
fechaEntregga date,
documento mediumblob,
idEmpleado int,
primary key(idDocumento),
foreign key(idEmpleado) references RH_Empleados(IdEmpleado)
);

create table RH_Nominas(
idNomina int auto_increment,
fechaElaboracion date,
fechaPago date,
subtotal float,
retenciones float,
total float,
diasTrabajados int,
estatus char,
idEmpleado int,
idFormaPago int,
idPeriodo int,
primary key (idNomina),
foreign key (idFormaPago) references RH_FormasPago(idFormaPago),
foreign key (idPeriodo) references RH_Periodos(idPeriodo),
foreign key (idEmpleado) references RH_Empleados(idEmpleado),
check(estatus in ('A','I'))
);

create table RH_NominasDeducciones(
idNomina int,
idDeduccion int,
importe float,
primary key (idNomina,idDeduccion),
foreign key (idNomina) references RH_Nominas(idNomina),
foreign key (idDeduccion) references RH_Deducciones(idDeduccion)
);

create table RH_NominasPercepciones(
idNomina int,
idPercepcion int,
importe float,
primary key (idPercepcion,idNomina),
foreign key (idNomina) references RH_Nominas(idNomina),
foreign key (idPercepcion) references RH_Percepciones (idPercepcion)
);

INSERT INTO `rh_erp`.`RH_Puestos` (`nombre`, `salarioMinimo`, `salarioMaximo`, `estatus`) VALUES ('Administrador de BD', '20000', '30000', 'A');
INSERT INTO `rh_erp`.`RH_Departamentos` (`nombre`, `estatus`) VALUES ('Base de Datos', 'A');
INSERT INTO `rh_erp`.`RH_Estados` (`nombre`, `siglas`, `estatus`) VALUES ('Michoacan', 'MICH', 'A');
INSERT INTO `rh_erp`.`RH_Ciudades` (`nombre`, `idEstado`, `estatus`) VALUES ('Zamora', '1', 'A');
INSERT INTO `rh_erp`.`RH_Sucursales` (`nombre`, `telefono`, `direccion`, `colonia`, `codigoPostal`, `presupuesto`, `estatus`, `idCiudad`) VALUES ('Sucursal Zamora', '3511695859', 'Juarez poniente 2257', 'Juarez', '59632', '100000', 'A', '1');
INSERT INTO `rh_erp`.`RH_Turnos` (`nombre`, `horaInicio`, `horaFin`, `dias`,`estatus`) VALUES ('Vespertino', '2000-01-01 08:00:01', '2000-01-01 16:00:01', 'L,M','A');
INSERT INTO `rh_erp`.`RH_Empleados` (`nombre`, `apellidoPaterno`, `apellidoMaterno`, `sexo`, `fechaNacimiento`, `curp`, `estadoCivil`, `fechaContratacion`, `salarioDiario`, `nss`, `diasVacaciones`, `diasPermiso`, `direccion`, `colonia`, `codigoPostal`, `escolaridad`, `email`, `paassword`, `tipo`, `estatus`, `idDepartamento`, `idPuesto`, `idCiudad`, `idSucursal`, `idTurno`) VALUES ('Yuvia', 'Francisco', 'Diaz', 'F', '2000-12-1', 'WEWSDD', 'Soltero', '2021-01-01', '300', '23232123', '10', '10', 'DOMICILIO X', 'X', '58946', 'Ingeniero', 'ydiaz@gmail.com', 'Hola.123', 'Admin', 'A', '1', '1', '1', '1', '1');
















 
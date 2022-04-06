from enum import unique

from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import VARCHAR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BLOB, TIMESTAMP, Column,Integer,String,Date,Float,ForeignKey,Boolean, null
from sqlalchemy.orm import relationship
from flask_login import UserMixin, current_user


db=SQLAlchemy()

#Puestos-------------------------------------
class Puestos(db.Model):
    __tablename__= 'RH_Puestos'
    idPuesto = Column(Integer, primary_key=True)
    nombre = Column(String(60))
    salarioMinimo = Column(Float)
    salarioMaximo = Column(Float)
    estatus = Column(String(1))

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        objeto.estatus = "I"
        db.session.merge(objeto)
        db.session.commit()

    def consultarPagina(self, pagina):
        obj = None;
        if current_user.is_admin():        
            obj = self.query.order_by(Puestos.idPuesto.asc()).paginate(pagina,per_page= 5, error_out=False)
        else:
            obj = self.query.filter(Puestos.estatus=='A').order_by(Puestos.idPuesto.asc()).paginate(pagina,per_page= 5, error_out=False)
        return obj
    
    def consultarNombre(self,nombre):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Puestos.nombre==nombre).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida 
    
        
#Turnos  -------------------------------------------------
class Turnos(db.Model):
    __tablename__= 'RH_Turnos'
    idTurno = Column(Integer, primary_key=True)
    nombre = Column(String(20))
    horaInicio = Column(TIMESTAMP)
    horaFin = Column(TIMESTAMP)
    dias = Column(String(30))
    estatus = Column(String(1))

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        objeto.estatus = "I"
        db.session.merge(objeto)        
        db.session.commit()

    def consultarPagina(self, pagina):
        obj = None
        if current_user.is_admin():
            obj = self.query.order_by(Turnos.idTurno.asc()).paginate(pagina,per_page= 5, error_out=False)        
        else:
            obj = self.query.filter(Turnos.estatus=='A').order_by(Turnos.idTurno.asc()).paginate(pagina,per_page= 5, error_out=False)
        return obj

    def consultarNombre(self,nombre):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Turnos.nombre==nombre).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida 

#Departamentos-----------------------------------------------------------------
class Departamentos(db.Model):
    __tablename__= 'RH_Departamentos'
    idDepartamento = Column(Integer, primary_key=True)
    nombre = Column(String(50))   
    estatus = Column(String(1))

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        objeto.estatus = "I"
        db.session.merge(objeto)
        db.session.commit()

    def consultarPagina(self, pagina):
        obj = None
        if current_user.is_admin():
            obj = self.query.order_by(Departamentos.idDepartamento.asc()).paginate(pagina,per_page= 5, error_out=False)
        else:
            obj = self.query.filter(Departamentos.estatus=='A').order_by(Departamentos.idDepartamento.asc()).paginate(pagina,per_page= 5, error_out=False)
        return obj
    
    def consultarNombre(self,nombre):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Departamentos.nombre==nombre).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida 

#Formas de pago------------------------------------------------------------------
class FormasdePago(db.Model):
    __tablename__= 'RH_FormasPago'
    idFormaPago = Column(Integer, primary_key=True)
    nombre = Column(String(50))   
    estatus = Column(String(1))

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        objeto.estatus = "I"
        db.session.merge(objeto)
        db.session.commit()

    def consultarPagina(self, pagina):
        obj = None
        if current_user.is_admin():
            obj = self.query.order_by(FormasdePago.idFormaPago.asc()).paginate(pagina,per_page= 5, error_out=False)
        else:
             obj = self.query.filter(FormasdePago.estatus=='A').order_by(FormasdePago.idFormaPago.asc()).paginate(pagina,per_page= 5, error_out=False)
        return obj
    
    def consultarNombre(self,nombre):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(FormasdePago.nombre==nombre).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida 
        
#Estados-------------------------------------
class Estado(db.Model):
    __tablename__= 'RH_Estados'
    idEstado = Column(Integer, primary_key=True)
    nombre = Column(String(60))
    siglas = Column(String(10))
    estatus = Column(String(1))

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        objeto.estatus = "I"
        db.session.merge(objeto)
        db.session.commit()

    def consultarPagina(self, pagina):
        obj = None
        if current_user.is_admin():
            obj = self.query.order_by(Estado.idEstado.asc()).paginate(pagina,per_page= 5, error_out=False)
        else:
            obj = self.query.filter(Estado.estatus=='A').order_by(Estado.idEstado.asc()).paginate(pagina,per_page= 5, error_out=False)
        return obj
    
    def consultarNombre(self,nombre):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Estado.nombre==nombre).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida

#Empleados ----------------------------------
class Empleados(db.Model):
    __tablename__= 'RH_Empleados'
    idEmpleado = Column(Integer, primary_key=True)
    nombre = Column(String(30))
    apellidoPaterno= Column(String(35))
    apellidoMaterno = Column(String(30))
    sexo = Column(String(1))
    fechaNacimiento = Column(Date)
    curp = Column(String(20))
    estadoCivil = Column(String(20))
    fechaContratacion = Column(Date)
    salarioDiario = Column(Float)
    nss = Column(String(20))
    diasVacaciones = Column(Integer)
    diasPermiso = Column(Integer)
    fotografia = Column(BLOB)
    direccion = Column(String(20))
    colonia = Column(String(50))
    codigoPostal = Column(String(5))
    escolaridad = Column(String(80))
    especialidad = Column(String(100))
    email = Column(String(100))
    paassword = Column(String(20))
    tipo = Column(String(10))
    estatus = Column(String(1))
    idDepartamento = Column(Integer)
    idPuesto = Column(Integer)
    idCiudad = Column(Integer)
    idSucursal = Column(Integer)
    idTurno = Column(Integer)

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        objeto.estatus = "I"
        db.session.merge(objeto)
        db.session.commit()

    def consultarPagina(self, pagina):
        obj = None;
        if current_user.is_admin():        
            obj = self.query.order_by(Empleados.idPuesto.asc()).paginate(pagina,per_page= 5, error_out=False)
        else:
            obj = self.query.filter(Empleados.estatus=='A').order_by(Empleados.idPuesto.asc()).paginate(pagina,per_page= 5, error_out=False)
        return obj

    def getSucursal(self):
        sucursal = Sucursales()
        return sucursal.consultar(self.idSucursal).nombre

    def getDepartamento(self):
        dep = Departamentos()
        return dep.consultar(self.idDepartamento).nombre
    
    def getTurno(self):
        turno = Turnos()
        return turno.consultar(self.idTurno).nombre
    
    def getPuesto(self):
        puesto = Puestos()
        return puesto.consultar(self.idPuesto).nombre
    
    def getCiudad(self):
        ciudad = Ciudades()
        return ciudad.consultar(self.idCiudad).nombre

    def ExisteEmpleado(self, nombre, apP, apM):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Empleados.nombre==nombre, Empleados.apellidoPaterno == apP, Empleados.apellidoMaterno == apM).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El Empleado "+nombre + " " + apP +" "+ apM+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida

    def ExisteEmail(self, email):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Empleados.email==email).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El enail  "+email+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El email "+email+" esta libre."
        return salida
    
    def ExisteCURP(self, curp):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Empleados.curp==curp).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="La CURP "+ curp+" ya se encuentra registrada."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="La curp "+curp+" esta libre."
        return salida
    
    def ExisteNSS(self, nss):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Empleados.nss==nss).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El NSS "+ nss+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El NSS "+nss+" esta libre."
        return salida

    def ValidarSalario(self, salario, puesto):
        salida={"estatus":"","mensaje":""}
        salarioP = Puestos()
        salarioP = salarioP.consultar(puesto)        
        if salario>= salarioP.salarioMinimo and salario <= salarioP.salarioMaximo:
            salida["estatus"]="Ok"
            salida["mensaje"]="El salario esta dentro de los limites"            
        else:
            salida["estatus"]="Error"
            salida["mensaje"]="El salario esta fuera de los limites del salario permitido para el puesto"
        return salida  


# METODOS DE PERFILAMIENTO PARA EL USUARIO---------------------------------------------------------------------------------
    def validar(self,email,passw):
        usuario=Empleados();
        usuario=self.query.filter(Empleados.email==email,Empleados.paassword==passw,Empleados.estatus=='A').first()
        return usuario

    def is_authenticated(self):
        return True

    def is_active(self):
         return self.estatus

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idEmpleado

    def is_admin(self):
        if self.tipo=='Admin':
            return True
        else:
            return False

    def is_staff(self):
        if self.tipo=='Staff':
            return True
        else:
            return False

    def is_empleado(self):
        if self.tipo=='Empleado':
            return True
        else:
            return False



#Documentacion---------------------------------------------------
class DocumentosEmpleado(db.Model):
    __tablename__= 'RH_DocumentacionEmpleado'
    idDocumento = Column(Integer, primary_key=True)
    nombreDocumento = Column(String(80))
    fechaEntregga = Column(Date)
    documento = Column(BLOB)
    idEmpleado = Column(Integer)

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarPagina(self, pagina):
        obj = None        
        obj = self.query.order_by(DocumentosEmpleado.idDocumento.asc()).paginate(pagina,per_page= 5, error_out=False)        
        return obj
    
    def consultarNombre(self,nombre,id):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(DocumentosEmpleado.nombreDocumento ==nombre,DocumentosEmpleado.idEmpleado ==id ).first()
        if item!=None:
           salida["estatus"]="Error"
           salida["mensaje"]="El docuemnto "+ nombre +" ya se encuentra registrado."
        else:
           salida["estatus"]="Ok"
           salida["mensaje"]="El documento "+ nombre +" esta libre."
        return salida

#Ciudades-----------------------------------
class Ciudades(db.Model):
    __tablename__= 'RH_Ciudades'
    idCiudad = Column(Integer, primary_key=True)
    nombre = Column(String(60))
    idEstado = Column(Integer)
    estatus = Column(String(1))

    def registrar(self):
        db.session.add(self)
        db.session.commit()

    def consultar(self,id):
        return self.query.get(id)

    def consultarAll(self):        
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto=self.consultar(id)
        objeto.estatus = "I"
        db.session.merge(objeto)
        db.session.commit()
        
    def getEstados(self):
        estados =Estado()
        estados= estados.consultar(self.idEstado)
        return estados.nombre

    def consultarPagina(self, pagina):
        obj = None;
        if current_user.is_admin():        
            obj = self.query.order_by(Ciudades.idCiudad.asc()).paginate(pagina,per_page= 5, error_out=False)
        else:
            obj = self.query.filter(Ciudades.estatus=='A').order_by(Ciudades.idCiudad.asc()).paginate(pagina,per_page= 5, error_out=False)
        return obj
    
    def consultarNombre(self,nombre):
        salida={"estatus":"","mensaje":""}
        item=None
        item=self.query.filter(Ciudades.nombre==nombre).first()
        if item!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida 


       



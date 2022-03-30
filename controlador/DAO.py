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

    def is_staff(self):
        if self.tipo=='Empleado':
            return True
        else:
            return False




       



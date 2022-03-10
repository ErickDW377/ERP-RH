from enum import unique

from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import VARCHAR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BLOB, TIMESTAMP, Column,Integer,String,Date,Float,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin


db=SQLAlchemy()

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
        db.session.delete(objeto)
        db.session.commit()
        
      #Turnos  
class Turnos(db.Model):
    __tablename__= 'RH_Turnos'
    idTurno = Column(Integer, primary_key=True)
    nombre = Column(String(20))
    horaInicio = Column(TIMESTAMP)
    horaFin = Column(TIMESTAMP)
    dias = Column(String(30))
    
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

  #Sucursales      
        
class Sucursales(db.Model):
    __tablename__= 'RH_Sucursales'
    idSucursal = Column(Integer, primary_key=True)
    nombre = Column(String(60),nullable= False)
    telefono= Column(String(15),nullable= False)
    direccion = Column(String(80),nullable= False)
    colonoa = Column(String(50),nullable= False)
    codigoPostal = Column(String(5),nullable= False)
    presupuesto = Column(Float,nullable= False)
    estatus = Column(String(1),nullable= False)

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

    #Empleados
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
        db.session.delete(objeto)
        db.session.commit()

    def validar(self,email,passw):
        usuario=Empleados();
        usuario=self.query.filter(Empleados.email==email,Empleados.paassword==passw).first()
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
       



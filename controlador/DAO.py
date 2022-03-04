from enum import unique

from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import VARCHAR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Date,Float,ForeignKey,Boolean
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



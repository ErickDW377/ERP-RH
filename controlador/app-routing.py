from flask import Flask,render_template,request,flash, redirect, url_for, abort
from flask_bootstrap import Bootstrap
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import String
from DAO import db, Puestos,Sucursales,Turnos
from flask_login import LoginManager,current_user,login_required,login_user,logout_user
from array import array

app=Flask(__name__,template_folder='../Pages',static_folder='../Static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Hola.123@127.0.0.1/recuhum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'

#login_manager=LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = "login"
#login_manager.login_message = u"! Debes iniciar sesión !"

@app.route('/')
def iniciar():    
    return  render_template('Inicio/inicio.html')

@app.route('/inicio')
def inicio():    
    return  render_template('inicio/inicio.html')
 
# Enrutamiento login
@app.route('/login')
def login():    
    return  render_template('login/login.html')

#Puestos
@app.route('/puestos')
def puestos():
    p=Puestos()     
    return  render_template('Puestos/puestos.html', puestos =p.consultarAll()  )

@app.route('/registrarPuestos')
def puestosR():  
    return  render_template('Puestos/registrarPuestos.html')

@app.route('/editarPuestos/<int:id>')
def puestosE(id):  
    puesto =  Puestos()
    puesto = puesto.consultar(id)
    return  render_template('Puestos/editarPuestos.html', puesto = puesto)

@app.route('/registrarP',methods=['post'])
def registarP():  
    puesto = Puestos()
    puesto.nombre = request.form['nombrePuesto']
    puesto.salarioMinimo = request.form['salarioMinimo']
    puesto.salarioMaximo = request.form['salarioMaximo']
    estatus = request.values.get('estatus',False)
    if estatus=="True":
        puesto.estatus=True
    else:
        puesto.estatus=False 
    puesto.registrar()
    flash('Puesto registrado con exito')
    return  redirect(url_for('puestosR'))

@app.route('/editarP/<int:id>',methods=['post'])
def editarP(id):  
    puesto = Puestos()
    puesto.nombre = request.form['nombrePuesto']
    puesto.salarioMinimo = request.form['salarioMinimo']
    puesto.salarioMaximo = request.form['salarioMaximo']
    estatus = request.values.get('estatus',False)
    if estatus=="True":
        puesto.estatus=True
    else:
        puesto.estatus=False  
    puesto.idPuesto = id
    puesto.actualizar()
    flash('Puesto actualizado con exito')
    return  redirect(url_for('puestosE', id= puesto.idPuesto))

@app.route('/eliminarP/<int:id>')
def eliminarP(id): 
    puesto = Puestos()
    puesto.eliminar(id)
    flash('Puesto eliminado con exito')
    return  redirect(url_for('puestos'))
#Turnos-----------------------------------------------------
@app.route('/turnos')
def turnos():
    t=Turnos() 
    return  render_template('Turnos/turnos.html', turnos = t.consultarAll())

@app.route('/registrarTurnos')
def turnosR():
    return  render_template('Turnos/registrarTurnos.html')

@app.route('/editarTurnos/<int:id>')
def turnosE(id):  
    turno =  Turnos()
    turno = turno.consultar(id)
    return  render_template('Turnos/editarTurnos.html', turno = turno)

@app.route('/registrarT',methods=['post'])
def registrarT():
    turno=Turnos()
    turno.nombre= request.form['nombreTurno']
    turno.horaInicio=request.form['horaInicioT']                  
    turno.horaFin=request.form['horaFinT']                 
    turno.dias= request.form['diasT']
    turno.registrar()
    flash('Turno registrado con exito')
    return  redirect(url_for('turnosR'))

@app.route('/editarT/<int:id>',methods=['post'])
def editarT(id):  
    turno = Turnos()
    turno.nombre= request.form['nombreTurno']
    turno.horaInicio=request.form['horaInicioT']                  
    turno.horaFin=request.form['horaFinT']                 
    turno.dias= request.form['diasT']  
    turno.idTurno= id
    turno.actualizar()
    flash('Puesto actualizado con exito')
    return  redirect(url_for('turnosE', id= turno.idTurno))

@app.route('/eliminarT/<int:id>')
def eliminarT(id): 
    turno = Turnos()
    turno.eliminar(id)
    flash('Turno eliminado con exito')
    return  redirect(url_for('turnos'))
    
   

# Enrutamiento sucursales
@app.route('/sucursales')
def sucursales():  
    s=Sucursales()
    sucursales= s.consultarAll() 
    return  render_template('sucursales/sucursales.html', sucursales=sucursales) 


if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)
    
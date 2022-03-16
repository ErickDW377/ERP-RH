from flask import Flask,render_template,request,flash, redirect, url_for, abort
from flask_bootstrap import Bootstrap
from sqlalchemy import true
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import String
from DAO import db, Puestos,Sucursales,Turnos,Empleados,Departamentos,Estado,FormasdePago
from flask_login import LoginManager,current_user,login_required,login_user,logout_user
from array import array

import json

app=Flask(__name__,template_folder='../Pages',static_folder='../Static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Hola.123@127.0.0.1/RH_ERP'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"! Debes iniciar sesión !"

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

@app.route('/iniciarSesion',methods=['post'])
def validarUsuario():
    user=Empleados()
    email=request.form['email']
    password=request.form['password']
    user=user.validar(email,password)
    if user!=None:
        login_user(user)
        return redirect(url_for('inicio'))
    else:
        flash('!Datos de la sesión incorrectos!')
        return redirect(url_for('login'))

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('inicio'))

@login_manager.user_loader
def load_user(id):
    return Empleados.query.get(int(id))

#Puestos
@app.route('/puestos')
@login_required
def puestos():
    if current_user.is_authenticated() and current_user.is_admin(): 
        p=Puestos()
        page = request.args.get('page', 1, type=int)
        paginacion = p.consultarPagina(page)         
        return  render_template('Puestos/puestos.html', puestos =paginacion.items, pagination = paginacion  )
    else:
        abort(404)

@app.route('/registrarPuestos')
@login_required
def puestosR():
    if current_user.is_authenticated() and current_user.is_admin():  
        return  render_template('Puestos/registrarPuestos.html')
    else:
        abort(404)

@app.route('/editarPuestos/<int:id>')
@login_required
def puestosE(id):
    if current_user.is_authenticated() and current_user.is_admin():  
        puesto =  Puestos()
        puesto = puesto.consultar(id)
        return  render_template('Puestos/editarPuestos.html', puesto = puesto)
    else:
        abort(404)

@app.route('/registrarP',methods=['post'])
@login_required
def registarP(): 
    if current_user.is_authenticated() and current_user.is_admin():  
        puesto = Puestos()
        puesto.nombre = request.form['nombrePuesto']
        puesto.salarioMinimo = request.form['salarioMinimo']
        puesto.salarioMaximo = request.form['salarioMaximo']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            puesto.estatus='A'
        else:
            puesto.estatus='I' 
        puesto.registrar()
        flash('Puesto registrado con exito')
        return  redirect(url_for('puestosR'))
    else:
        abort(404)

@app.route('/editarP/<int:id>',methods=['post'])
@login_required
def editarP(id): 
    if current_user.is_authenticated() and current_user.is_admin():  
        puesto = Puestos()
        puesto.nombre = request.form['nombrePuesto']
        puesto.salarioMinimo = request.form['salarioMinimo']
        puesto.salarioMaximo = request.form['salarioMaximo']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            puesto.estatus='A'
        else:
            puesto.estatus='I'  
        puesto.idPuesto = id
        puesto.actualizar()
        flash('Puesto actualizado con exito')
        return  redirect(url_for('puestosE', id= puesto.idPuesto))
    else:
        abort(404)

@app.route('/eliminarP/<int:id>')
@login_required
def eliminarP(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        puesto = Puestos()
        puesto.eliminar(id)
        flash('Puesto eliminado con exito')
        return  redirect(url_for('puestos'))
    else:
        abort(404)

@app.route('/puestos/nombre/<string:nombre>',methods=['get'])
def consultarNombreP(nombre):
    item=Puestos()    
    return json.dumps(item.consultarNombre(nombre))

#Turnos-----------------------------------------------------
@app.route('/turnos')
@login_required
def turnos():
    if current_user.is_authenticated() and current_user.is_admin():
        t=Turnos() 
        page = request.args.get('page', 1, type=int)
        paginacion = t.consultarPagina(page)         
        return  render_template('Turnos/turnos.html', turnos = paginacion.items, pagination = paginacion)
    else:
        abort(404)

@app.route('/registrarTurnos')
@login_required
def turnosR():
    if current_user.is_authenticated() and current_user.is_admin():
        return  render_template('Turnos/registrarTurnos.html')
    else:
        abort(404)

@app.route('/editarTurnos/<int:id>')
@login_required
def turnosE(id):
    if current_user.is_authenticated() and current_user.is_admin():
        turno =  Turnos()        
        turno = turno.consultar(id)
        dias={"L":False,"M":False,"X":False,"J":False,"V":False,"S":False,"D":False}
        for d in turno.dias.split(sep=','):
            dias[d]=True
        print(dias)
        return  render_template('Turnos/editarTurnos.html', turno = turno, dias = dias)
    else:
        abort(404)

@app.route('/registrarT',methods=['post'])
@login_required
def registrarT():
    if current_user.is_authenticated() and current_user.is_admin():
        turno=Turnos()
        turno.nombre= request.form['nombreTurno']
        turno.horaInicio= "2000-01-01 " + request.form['horaInicioT']                  
        turno.horaFin= "2000-01-01 " +  request.form['horaFinT']                 
        dia = request.values.get('Lunes',False)        
        if dia=="True":
            turno.dias='L,'
        else:
            turno.dias=''

        dia = request.values.get('Martes',False)        
        if dia=="True":
            turno.dias+='M,'
        else:
            turno.dias+=''
        
        dia = request.values.get('Miercoles',False)        
        if dia=="True":
            turno.dias+='X,'
        else:
            turno.dias+=''
        
        dia = request.values.get('Jueves',False)        
        if dia=="True":
            turno.dias+='J,'
        else:
            turno.dias+=''
        
        dia = request.values.get('Viernes',False)        
        if dia=="True":
            turno.dias+='V,'
        else:
            turno.dias+=''

        dia = request.values.get('Sabado',False)        
        if dia=="True":
            turno.dias+='S,'
        else:
            turno.dias+=''

        dia = request.values.get('Domingo',False)        
        if dia=="True":
            turno.dias+='D'
        else:
            turno.dias+=''      
        
        turno.estatus = 'A'
        turno.registrar()
        flash('Turno registrado con exito')
        return  redirect(url_for('turnosR'))
    else:
        abort(404)

@app.route('/editarT/<int:id>',methods=['post'])
@login_required
def editarT(id):
    if current_user.is_authenticated() and current_user.is_admin():  
        turno = Turnos()
        turno.nombre= request.form['nombreTurno']
        turno.horaInicio="2000-01-01 " + request.form['horaInicioT']                  
        turno.horaFin="2000-01-01 " + request.form['horaFinT']                 
        dia = request.values.get('Lunes',False)        
        if dia=="True":
            turno.dias='L,'
        else:
            turno.dias=''

        dia = request.values.get('Martes',False)        
        if dia=="True":
            turno.dias+='M,'
        else:
            turno.dias+=''
        
        dia = request.values.get('Miercoles',False)        
        if dia=="True":
            turno.dias+='X,'
        else:
            turno.dias+=''
        
        dia = request.values.get('Jueves',False)        
        if dia=="True":
            turno.dias+='J,'
        else:
            turno.dias+=''
        
        dia = request.values.get('Viernes',False)        
        if dia=="True":
            turno.dias+='V,'
        else:
            turno.dias+=''

        dia = request.values.get('Sabado',False)        
        if dia=="True":
            turno.dias+='S,'
        else:
            turno.dias+=''

        dia = request.values.get('Domingo',False)        
        if dia=="True":
            turno.dias+='D'
        else:
            turno.dias+=''

        turno.idTurno= id
        turno.actualizar()
        flash('Turno actualizado con exito')
        return  redirect(url_for('turnosE', id= turno.idTurno))
    else:
        abort(404)

@app.route('/eliminarT/<int:id>')
@login_required
def eliminarT(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        turno = Turnos()
        turno.eliminar(id)
        flash('Turno eliminado con exito')
        return  redirect(url_for('turnos'))
    else:
        abort(404)

@app.route('/turnos/nombre/<string:nombre>',methods=['get'])
def consultarNombreT(nombre):
    item=Turnos()    
    return json.dumps(item.consultarNombre(nombre))

#Departamentos--------------------------------------------------------   
@app.route('/departamentos')
@login_required
def departamentos():
    if current_user.is_authenticated() and current_user.is_admin():
        d=Departamentos() 
        page = request.args.get('page', 1, type=int)
        paginacion = d.consultarPagina(page)         
        return  render_template('Departamentos/departamentos.html', departamentos = paginacion.items, pagination = paginacion)
    else:
        abort(404)

@app.route('/registrarDepartamentos')
@login_required
def departamentosR():
    if current_user.is_authenticated() and current_user.is_admin():
        return  render_template('Departamentos/registrarDepartamentos.html')
    else:
        abort(404)

@app.route('/editarDepartamentos/<int:id>')
@login_required
def departamentosE(id):
    if current_user.is_authenticated() and current_user.is_admin():
        departamento =  Departamentos()        
        departamento = departamento.consultar(id)
        return  render_template('Departamentos/editarDepartamentos.html', departamento = departamento)
    else:
        abort(404)

@app.route('/registrarD',methods=['post'])
@login_required
def registrarD():
    if current_user.is_authenticated() and current_user.is_admin():
        departamento=Departamentos()
        departamento.nombre= request.form['nombreDepartamento']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            departamento.estatus='A'
        else:
            departamento.estatus='I'      
        departamento.registrar()
        flash('Departamento registrado con exito')
        return  redirect(url_for('departamentosR'))
    else:
        abort(404)

@app.route('/editarD/<int:id>',methods=['post'])
@login_required
def editarD(id):
    if current_user.is_authenticated() and current_user.is_admin():  
        departamento = Departamentos()
        departamento.nombre= request.form['nombreDepartamento']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            departamento.estatus='A'
        else:
            departamento.estatus='I'   
        departamento.idDepartamento= id
        departamento.actualizar()
        flash('Departamento actualizado con exito')
        return  redirect(url_for('departamentosE', id= departamento.idDepartamento))
    else:
        abort(404)

@app.route('/eliminarD/<int:id>')
@login_required
def eliminarD(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        departamento = Departamentos()
        departamento.eliminar(id)
        flash('Departamento eliminado con exito')
        return  redirect(url_for('departamentos'))
    else:
        abort(404)

@app.route('/departamentos/nombre/<string:nombre>',methods=['get'])
def consultarNombreD(nombre):
    item=Departamentos()    
    return json.dumps(item.consultarNombre(nombre))

#Estados--------------------------------------------------------------------------
@app.route('/estado')
@login_required
def estado():
    if current_user.is_authenticated() and current_user.is_admin(): 
        e=Estado()
        page = request.args.get('page', 1, type=int)
        paginacion = e.consultarPagina(page)         
        return  render_template('Estado/estado.html', estado =paginacion.items, pagination = paginacion  )
    else:
        abort(404)

@app.route('/registrarEstado')
@login_required
def  estadoR():
    if current_user.is_authenticated() and current_user.is_admin():  
        return  render_template('Estado/registrarEstado.html')
    else:
        abort(404)

@app.route('/editarEstado/<int:id>')
@login_required
def estadoE(id):
    if current_user.is_authenticated() and current_user.is_admin():  
        estado =  Estado()
        estado = estado.consultar(id)
        return  render_template('Estado/editarEstado.html', estado = estado)
    else:
        abort(404)

@app.route('/registrarE',methods=['post'])
@login_required
def registarE(): 
    if current_user.is_authenticated() and current_user.is_admin():  
        estado = Estado()
        estado.nombre = request.form['nombrdelEstado']
        estado.siglas = request.form['siglas']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            estado.estatus='A'
        else:
            estado.estatus='I' 
        estado.registrar()
        flash('Estado registrado con exito')
        return  redirect(url_for('estadoR'))
    else:
        abort(404)

@app.route('/editarE/<int:id>',methods=['post'])
@login_required
def editarE(id): 
    if current_user.is_authenticated() and current_user.is_admin():  
        estado = Estado()
        estado.nombre = request.form['nombredelEstado']
        estado.siglas = request.form['siglas']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            estado.estatus='A'
        else:
            estado.estatus='I'  
        estado.idEstado = id
        estado.actualizar()
        flash('Estado actualizado con exito')
        return  redirect(url_for('estadoE', id= estado.idEstado))
    else:
        abort(404)

@app.route('/eliminarE/<int:id>')
@login_required
def eliminarE(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        estado = Estado()
        estado.eliminar(id)
        flash('Estado eliminado con exito')
        return  redirect(url_for('estado'))
    else:
        abort(404)


@app.route('/estados/nombre/<string:nombre>',methods=['get'])
def consultarNombreE(nombre):
    item=Estado()    
    return json.dumps(item.consultarNombre(nombre))

#Formas de pago--------------------------------------------------------   
@app.route('/formasdePago')
@login_required
def formasdePago():
    if current_user.is_authenticated() and current_user.is_admin():
        fp=FormasdePago() 
        page = request.args.get('page', 1, type=int)
        paginacion = fp.consultarPagina(page)         
        return  render_template('FormasDePago/formasdePago.html', formasdePago = paginacion.items, pagination = paginacion)
    else:
        abort(404)

@app.route('/registrarFormasdePago')
@login_required
def formasdePagoR():
    if current_user.is_authenticated() and current_user.is_admin():
        return  render_template('FormasDePago/registrarFormasdePago.html')
    else:
        abort(404)

@app.route('/editarFormasdePago/<int:id>')
@login_required
def formasdePagoE(id):
    if current_user.is_authenticated() and current_user.is_admin():
        formadepago =  FormasdePago()        
        formadepago = formadepago.consultar(id)
        return  render_template('FormasDePago/editarFormasdePago.html', formadePago = formadepago)
    else:
        abort(404)

@app.route('/registrarFP',methods=['post'])
@login_required
def registrarFP():
    if current_user.is_authenticated() and current_user.is_admin():
        formadepago=FormasdePago()
        formadepago.nombre= request.form['nombreFormadePago']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            formadepago.estatus='A'
        else:
            formadepago.estatus='I'      
        formadepago.registrar()
        flash('Forma de pago registrado con exito')
        return  redirect(url_for('formasdePagoR'))
    else:
        abort(404)

@app.route('/editarFP/<int:id>',methods=['post'])
@login_required
def editarFP(id):
    if current_user.is_authenticated() and current_user.is_admin():  
        formadepago=FormasdePago()
        formadepago.nombre= request.form['nombreFormadePago']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            formadepago.estatus='A'
        else:
            formadepago.estatus='I'     
        formadepago.idFormaPago= id
        formadepago.actualizar()
        flash('Fomra de pago actualizado con exito')
        return  redirect(url_for('formasdePagoE', id= formadepago.idFormaPago))
    else:
        abort(404)

@app.route('/eliminarFP/<int:id>')
@login_required
def eliminarFP(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        formadepago = FormasdePago()
        formadepago.eliminar(id)
        flash('Forma de pago eliminado con exito')
        return  redirect(url_for('formasdePago'))
    else:
        abort(404)

@app.route('/fp/nombre/<string:nombre>',methods=['get'])
def consultarNombreFP(nombre):
    item=FormasdePago()    
    return json.dumps(item.consultarNombre(nombre))

#Error--------------------------------------------------------------------------------------
@app.errorhandler(404)
def error_404(e):
    return redirect(url_for('inicio'))

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)
    
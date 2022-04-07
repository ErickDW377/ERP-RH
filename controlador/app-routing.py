from flask import Flask,render_template,request,flash, redirect, url_for, abort
from flask_bootstrap import Bootstrap
from sqlalchemy import true
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import String
from DAO import db, Puestos,Turnos,Empleados,Departamentos,Estado,FormasdePago,DocumentosEmpleado,Ciudades,Sucursales,Periodos
from flask_login import LoginManager,current_user,login_required,login_user,logout_user
from datetime import datetime

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
 
# Enrutamiento login---------------------------------------------------------------------------------------------
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

#Puestos----------------------------------------------------------------------------------------------------
@app.route('/puestos')
@login_required
def puestos():
    if current_user.is_authenticated(): 
        p=Puestos()
        page = request.args.get('page', 1, type=int)
        paginacion = p.consultarPagina(page)         
        return  render_template('Puestos/puestos.html', puestos =paginacion.items, pagination = paginacion  )
    else:
        abort(404)

@app.route('/registrarPuestos')
@login_required
def puestosR():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        return  render_template('Puestos/registrarPuestos.html')
    else:
        abort(404)

@app.route('/editarPuestos/<int:id>')
@login_required
def puestosE(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        puesto =  Puestos()
        puesto = puesto.consultar(id)
        return  render_template('Puestos/editarPuestos.html', puesto = puesto)
    else:
        abort(404)

@app.route('/registrarP',methods=['post'])
@login_required
def registarP(): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
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
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
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
    if current_user.is_authenticated():
        item=Puestos()    
        return json.dumps(item.consultarNombre(nombre))
    else:
        abort(404)

#Turnos-----------------------------------------------------
@app.route('/turnos')
@login_required
def turnos():
    if current_user.is_authenticated():
        t=Turnos() 
        page = request.args.get('page', 1, type=int)
        paginacion = t.consultarPagina(page)         
        return  render_template('Turnos/turnos.html', turnos = paginacion.items, pagination = paginacion)
    else:
        abort(404)

@app.route('/registrarTurnos')
@login_required
def turnosR():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        return  render_template('Turnos/registrarTurnos.html')
    else:
        abort(404)

@app.route('/editarTurnos/<int:id>')
@login_required
def turnosE(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
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
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
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
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
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
    if current_user.is_authenticated():
        item=Turnos()    
        return json.dumps(item.consultarNombre(nombre))
    else:
        abort(404)
        
#Departamentos--------------------------------------------------------   
@app.route('/departamentos')
@login_required
def departamentos():
    if current_user.is_authenticated():
        d=Departamentos() 
        page = request.args.get('page', 1, type=int)
        paginacion = d.consultarPagina(page)         
        return  render_template('Departamentos/departamentos.html', departamentos = paginacion.items, pagination = paginacion)
    else:
        abort(404)

@app.route('/registrarDepartamentos')
@login_required
def departamentosR():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        return  render_template('Departamentos/registrarDepartamentos.html')
    else:
        abort(404)

@app.route('/editarDepartamentos/<int:id>')
@login_required
def departamentosE(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        departamento =  Departamentos()        
        departamento = departamento.consultar(id)
        return  render_template('Departamentos/editarDepartamentos.html', departamento = departamento)
    else:
        abort(404)

@app.route('/registrarD',methods=['post'])
@login_required
def registrarD():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
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
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
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
    if current_user.is_authenticated(): 
        item=Departamentos()    
        return json.dumps(item.consultarNombre(nombre))
    else:
            abort(404)


#Estados--------------------------------------------------------------------------
@app.route('/estado')
@login_required
def estado():
    if current_user.is_authenticated(): 
        e=Estado()
        page = request.args.get('page', 1, type=int)
        paginacion = e.consultarPagina(page)         
        return  render_template('Estado/estado.html', estado =paginacion.items, pagination = paginacion  )
    else:
        abort(404)

@app.route('/registrarEstado')
@login_required
def  estadoR():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        return  render_template('Estado/registrarEstado.html')
    else:
        abort(404)

@app.route('/editarEstado/<int:id>')
@login_required
def estadoE(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        estado =  Estado()
        estado = estado.consultar(id)
        return  render_template('Estado/editarEstado.html', estado = estado)
    else:
        abort(404)

@app.route('/registrarE',methods=['post'])
@login_required
def registarE(): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
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
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
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
    if current_user.is_authenticated(): 
        item=Estado()    
        return json.dumps(item.consultarNombre(nombre))
    else:
        abort(404)

#Formas de pago--------------------------------------------------------   
@app.route('/formasdePago')
@login_required
def formasdePago():
    if current_user.is_authenticated():
        fp=FormasdePago() 
        page = request.args.get('page', 1, type=int)
        paginacion = fp.consultarPagina(page)         
        return  render_template('FormasDePago/formasdePago.html', formasdePago = paginacion.items, pagination = paginacion)
    else:
        abort(404)

@app.route('/registrarFormasdePago')
@login_required
def formasdePagoR():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        return  render_template('FormasDePago/registrarFormasdePago.html')
    else:
        abort(404)

@app.route('/editarFormasdePago/<int:id>')
@login_required
def formasdePagoE(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        formadepago =  FormasdePago()        
        formadepago = formadepago.consultar(id)
        return  render_template('FormasDePago/editarFormasdePago.html', formadePago = formadepago)
    else:
        abort(404)

@app.route('/registrarFP',methods=['post'])
@login_required
def registrarFP():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
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
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
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
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        formadepago = FormasdePago()
        formadepago.eliminar(id)
        flash('Forma de pago eliminado con exito')
        return  redirect(url_for('formasdePago'))
    else:
        abort(404)

@app.route('/fp/nombre/<string:nombre>',methods=['get'])
def consultarNombreFP(nombre):
    if current_user.is_authenticated():
        item=FormasdePago()    
        return json.dumps(item.consultarNombre(nombre))
    else:
        abort(404)

# Enrutamiento Empleados----------------------------------------------------------------------
@app.route('/empleados')
@login_required
def empleados():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        p=Empleados()
        page = request.args.get('page', 1, type=int)
        paginacion = p.consultarPagina(page)         
        return  render_template('Empleados/empleados.html', empleados =paginacion.items, pagination = paginacion  )
    else:
        abort(404)

@app.route('/empleadosR')
@login_required
def empleadosR():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        p = Puestos()
        d = Departamentos()
        s = Sucursales()
        c = Ciudades()
        t = Turnos()
        return  render_template('Empleados/registrarEmpleados.html', puestos = p, departamentos = d, sucursales = s, ciudades = c, turnos=t)
    else:
        abort(404)

@app.route('/empleadosE/<int:id>')
@login_required
def empleadosE(id):
    if current_user.is_authenticated():  
        empleados =  Empleados()
        p = Puestos()
        d = Departamentos()
        s = Sucursales()
        c = Ciudades()
        t = Turnos()
        empleados = empleados.consultar(id)
        return  render_template('Empleados/editarEmpleados.html', empleado = empleados, puestos = p, departamentos = d, sucursales = s, ciudades = c, turnos=t)
    else:
        abort(404)

@app.route('/registarEmpleado',methods=['post'])
@login_required
def registarEmpleado(): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        empleado = Empleados()        
        empleado.nombre = request.form["nombre"]
        empleado.apellidoPaterno = request.form["apellidoPaterno"]
        empleado.apellidoMaterno = request.form["apellidoMaterno"]
        empleado.sexo = request.form["sexo"]
        empleado.fechaNacimiento = request.form["fechaNacimiento"]
        empleado.curp = request.form["curp"]
        empleado.estadoCivil = request.form["estadoCivil"]
        empleado.fechaContratacion = request.form["fechaContratacion"]
        empleado.salarioDiario = request.form["salarioDiario"]
        empleado.nss = request.form["nss"]
        empleado.diasVacaciones = request.form["diasVacaciones"]
        empleado.diasPermiso = request.form["diasPermiso"]
        empleado.fotografia=request.files['foto'].read()     
        empleado.direccion = request.form["direccion"]
        empleado.colonia = request.form["colonia"]
        empleado.codigoPostal = request.form["codigoPostal"]
        empleado.escolaridad = request.form["escolaridad"]
        empleado.especialidad = request.form["especialidad"]
        empleado.email = request.form["email"]
        empleado.paassword = request.form["paassword"]
        empleado.tipo = request.form["tipo"]
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            empleado.estatus='A'
        else:
            empleado.estatus='I'
        empleado.idDepartamento = request.form["idDepartamento"]
        empleado.idPuesto = request.form["idPuesto"]
        empleado.idCiudad = request.form["idCiudad"]
        empleado.idSucursal = request.form["idSucursal"]
        empleado.idTurno = request.form["idTurno"]
               
         
        empleado.registrar()
        flash('Empleado registrado con exito')
        return  redirect(url_for('empleadosR'))
    else:
        abort(404)

@app.route('/editarEmpleado/<int:id>',methods=['post'])
@login_required
def editarEmpelado(id): 
    if current_user.is_authenticated():  
        empleado = Empleados()        
        empleado.nombre = request.form["nombre"]
        empleado.apellidoPaterno = request.form["apellidoPaterno"]
        empleado.apellidoMaterno = request.form["apellidoMaterno"]
        empleado.sexo = request.form["sexo"]
        empleado.fechaNacimiento = request.form["fechaNacimiento"]
        empleado.curp = request.form["curp"]
        empleado.estadoCivil = request.form["estadoCivil"]
        empleado.fechaContratacion = request.form["fechaContratacion"]
        empleado.salarioDiario = request.form["salarioDiario"]
        empleado.nss = request.form["nss"]
        empleado.diasVacaciones = request.form["diasVacaciones"]
        empleado.diasPermiso = request.form["diasPermiso"]
        imagen = request.files['foto'].read()  
        if imagen:
            empleado.fotografia=  imagen 
        empleado.direccion = request.form["direccion"]
        empleado.colonia = request.form["colonia"]
        empleado.codigoPostal = request.form["codigoPostal"]
        empleado.escolaridad = request.form["escolaridad"]
        empleado.especialidad = request.form["especialidad"]
        empleado.email = request.form["email"]
        empleado.paassword = request.form["paassword"]
        empleado.tipo = request.form["tipo"]
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            empleado.estatus='A'
        else:
            empleado.estatus='I'
        empleado.idDepartamento = request.form["idDepartamento"]
        empleado.idPuesto = request.form["idPuesto"]
        empleado.idCiudad = request.form["idCiudad"]
        empleado.idSucursal = request.form["idSucursal"]
        empleado.idTurno = request.form["idTurno"] 

        empleado.idEmpleado = id
        empleado.actualizar()
        flash('Empleado actualizado con exito')
        return  redirect(url_for('empleadosE', id= empleado.idEmpleado))
    else:
        abort(404)

@app.route('/eliminarEmpleado/<int:id>')
@login_required
def eliminarEmpleado(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        empleado = Empleados()
        empleado.eliminar(id)
        flash('Empleado eliminado con exito')
        return  redirect(url_for('empleados'))
    else:
        abort(404)

@app.route('/empleadosVer/<int:id>')
@login_required
def empleadosVer(id):
    if current_user.is_authenticated():  
        empleados =  Empleados()
        p = Puestos()
        d = Departamentos()
        s = Sucursales()
        c = Ciudades()
        t = Turnos()
        doc = DocumentosEmpleado()
        docs = doc.consultarDocs(id)
        empleados = empleados.consultar(id)
        return  render_template('Empleados/verPerfil.html', empleado = empleados, puestos = p, departamentos = d, sucursales = s, ciudades = c, turnos=t, documentos = docs, len = doc.contarDocs(id))
    else:
        abort(404)

@app.route('/fortografia/<int:id>')
def getFotografia(id):
    e=Empleados()
    return e.consultar(id).fotografia

@app.route('/empleados/nombre/<string:nombre>/<string:apP>/<string:apM>',methods=['get'])
def consultarNombreEm(nombre, apP, apM):
    item=Empleados()    
    return json.dumps(item.ExisteEmpleado(nombre,apP,apM))

@app.route('/empleados/email/<string:email>',methods=['get'])
def consultarEmail(email):
    item=Empleados()    
    return json.dumps(item.ExisteEmail(email))

@app.route('/empleados/curp/<string:curp>',methods=['get'])
def consultarCURP(curp):
    item=Empleados()    
    return json.dumps(item.ExisteCURP(curp))

@app.route('/empleados/nss/<string:nss>',methods=['get'])
def consultarNSS(nss):
    item=Empleados()    
    return json.dumps(item.ExisteNSS(nss))

@app.route('/empleados/salario/<int:salario>/<int:puesto>',methods=['get'])
def validarSalario(salario, puesto):
    item=Empleados()    
    return json.dumps(item.ValidarSalario(salario,puesto))

#Documentos de empleados------------------------------------------------------------------------------------------------
@app.route('/documentacionER/<int:empleado>')
@login_required
def documentacionER(empleado):
    if current_user.is_authenticated():              
        return  render_template('Empleados/registrarDocumentos.html', idEmpleado = empleado)
    else:
        abort(404)

@app.route('/documentacionEE/<int:id>')
@login_required
def documentacionEE(id):
    if current_user.is_authenticated():  
        documento = DocumentosEmpleado()        
        return  render_template('Empleados/editarDocumentos.html',documento = documento.consultar(id) )
    else:
        abort(404)

@app.route('/registrarDocumentacion/<int:empleado>',methods=['post'])
@login_required
def registrarDocumentacion(empleado):
    if current_user.is_authenticated():
        documento=DocumentosEmpleado()
        documento.nombreDocumento= request.form['nombreDocumento']
        documento.fechaEntregga = datetime.today() 
        documento.documento = request.files['documento'].read()
        documento.idEmpleado = empleado            
        documento.registrar()
        flash('Documento registrado con exito')
        return  redirect(url_for('documentacionER', empleado = empleado))
    else:
        abort(404)

@app.route('/editarDocumentacion/<int:id>',methods=['post'])
@login_required
def editarDocumentacion(id):
    if current_user.is_authenticated():  
        documento=DocumentosEmpleado()
        documento.nombreDocumento= request.form['nombreDocumento']
        documento.fechaEntregga = datetime.today() 
        doc = request.files['documento'].read()
        if doc:
            documento.documento = doc
        documento.idDocumento  = id
        documento.actualizar()
        flash('Documento actualizado con exito')
        return  redirect(url_for('documentacionEE', id= id))
    else:
        abort(404)

@app.route('/documento/<int:id>')
def getDocumento(id):
    doc=DocumentosEmpleado()
    doc = doc.consultar(id).documento  
    return doc

@app.route('/documento/nombre/<string:nombre>/<int:id>',methods=['get'])
def consultarNombreDocumento(nombre,id):
    item=DocumentosEmpleado()    
    return json.dumps(item.consultarNombre(nombre,id))

@app.route('/eliminarDocumento/<int:id>')
@login_required
def eliminarDocumento(id):
    if current_user.is_authenticated(): 
        doc = DocumentosEmpleado()
        empleado = doc.consultar(id)
        empleado = empleado.idEmpleado
        doc.eliminar(id)
        flash('Documento eliminado con exito')
        return  redirect(url_for('empleadosVer', id= empleado))
    else:
        abort(404)
#CIUDADES-----------------------------------------------------------------------------------
@app.route('/ciudades')
@login_required
def ciudades():
    if current_user.is_authenticated(): 
        c=Ciudades()
        page = request.args.get('page', 1, type=int)
        paginacion = c.consultarPagina(page)         
        return  render_template('Ciudades/ciudades.html', ciudades =paginacion.items, pagination = paginacion  )
    else:
        abort(404)
        
@app.route('/registrarCiudades')
@login_required
def ciudadesR():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):        
        estados = Estado()
        return  render_template('Ciudades/registrarCiudades.html', estados = estados.consultarAll())
    else:
        abort(404)

@app.route('/editarCiudades/<int:id>')
@login_required
def ciudadesE(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        ciudad = Ciudades()
        ciudad = ciudad.consultar(id)
        estados = Estado()
        return  render_template('Ciudades/editarCiudades.html', ciudad= ciudad, estados = estados.consultarAll())
    else:
        abort(404)

@app.route('/registrarC',methods=['post'])
@login_required
def registarC(): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        ciudad = Ciudades()
        ciudad.nombre = request.form['nombreCiudad']
        ciudad.idEstado = request.form['idEstado']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            ciudad.estatus='A'
        else:
            ciudad.estatus='I' 
        ciudad.registrar()
        flash('Ciudad registrada con exito')
        return  redirect(url_for('ciudadesR'))
    else:
        abort(404)

@app.route('/editarC/<int:id>',methods=['post'])
@login_required
def editarC(id): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        ciudad = Ciudades()
        ciudad.nombre = request.form['nombreCiudad']
        ciudad.idEstado = request.form['idEstado']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            ciudad.estatus='A'
        else:
            ciudad.estatus='I'  
        ciudad.idCiudad = id
        ciudad.actualizar()
        flash('La Ciudad fue actualizado con exito')
        return  redirect(url_for('ciudadesE', id= ciudad.idCiudad))
    else:
        abort(404)

@app.route('/eliminarCiudad/<int:id>')
@login_required
def eliminarCiudad(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        ciudad = Ciudades()
        ciudad.eliminar(id)
        flash('Ciudad eliminada con exito')
        return  redirect(url_for('ciudades'))
    else:
        abort(404)

@app.route('/ciudades/nombre/<string:nombre>',methods=['get'])
def consultarNombreC(nombre):
    item=Ciudades()    
    return json.dumps(item.consultarNombre(nombre))


# Enrutamiento sucursales-------------------------------------------------------------------
@app.route('/sucursales')
@login_required
def sucursales():
    if current_user.is_authenticated():
        S=Sucursales() 
        page = request.args.get('page', 1, type=int)
        paginacion = S.consultarPagina(page)         
        return  render_template('Sucursales/sucursales.html', sucursales = paginacion.items, pagination = paginacion)
    else:
        abort(404)

@app.route('/registrarSucursales')
@login_required
def sucursalesR():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        ciudad = Ciudades()
        ciudad = ciudad.consultarAll()
        return  render_template('Sucursales/registrarSucursales.html', ciudades =ciudad)
    else:
        abort(404)
        
@app.route('/editarSucursal/<int:id>')
@login_required
def sucurE(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        sucursal = Sucursales()        
        sucursal = sucursal.consultar(id)
        ciudad = Ciudades()
        ciudad = ciudad.consultarAll()
        return  render_template('Sucursales/editarSucursal.html', sucursales = sucursal, ciudades =ciudad)
    else:
        abort(404)
        
@app.route('/registrarS',methods=['post'])
@login_required
def registrarS():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        sucursal=Sucursales()
        sucursal.nombre= request.form['nombreSucursales']
        sucursal.telefono=  request.form['telefono']                  
        sucursal.direccion=  request.form['direccion'] 
        sucursal.colonia=  request.form['colonia']                   
        sucursal.codigoPostal= request.form['codigoPostal']
        sucursal.presupuesto=  request.form['presupuesto'] 
        estatus = request.values.get('estatus',False)    
        if estatus=="True":
                sucursal.estatus='A'
        else:
            sucursal.estatus='I'
        sucursal.idCiudad = request.form['idCiudad'] 
        sucursal.registrar()
        flash('Sucursal registrada con exito')
        return  redirect(url_for('sucursalesR'))
    else:
        abort(404)

@app.route('/editaS/<int:id>',methods=['post'])
@login_required
def editaS(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        sucursal=Sucursales()
        sucursal.nombre= request.form['nombreSucursales']
        sucursal.telefono=request.form['telefono']                
        sucursal.direccion=  request.form['direccion'] 
        sucursal.colonia=  request.form['colonia']                   
        sucursal.codigoPostal= request.form['codigoPostal']
        sucursal.presupuesto= request.form['presupuesto'] 
        estatus = request.values.get('estatus',False) 
        if estatus=="True":
                 sucursal.estatus='A'
        else:
            sucursal.estatus='I'  
        sucursal.idCiudad = request.form['idCiudad'] 
        sucursal.idSucursal = id
        sucursal.actualizar()
        flash('Sucursal actualizada con exito')
        return  redirect(url_for('sucurE', id= sucursal.idSucursal))
    else:
        abort(404)

@app.route('/eliminarS/<int:id>')
@login_required
def eliminarS(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        sucursal = Sucursales()
        sucursal.eliminar(id)
        flash('Sucursal eliminado con exito')
        return  redirect(url_for('sucursales'))
    else:
        abort(404)

@app.route('/sucursales/nombre/<string:nombre>',methods=['get'])
def consultarNombreS(nombre):
    item=Sucursales()    
    return json.dumps(item.consultarNombre(nombre))

#Periodos----------------------------------------------------------------------------------------------------
@app.route('/periodos')
@login_required
def periodos():
    if current_user.is_authenticated(): 
        p=Periodos()
        page = request.args.get('page', 1, type=int)
        paginacion = p.consultarPagina(page)         
        return  render_template('Periodos/periodos.html', periodos =paginacion.items, pagination = paginacion  )
    else:
        abort(404)

@app.route('/registrarPeriodos')
@login_required
def registrarPeriodos():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        return  render_template('Periodos/registrarPeriodos.html')
    else:
        abort(404)

@app.route('/editarPeriodos/<int:id>')
@login_required
def editarPeriodos(id):
    if current_user.is_authenticated() (current_user.is_admin() or current_user.is_staff()):  
        periodo =  Periodos()
        periodo = periodo.consultar(id)
        return  render_template('Periodos/editarPeriodos.html', periodo = periodo)
    else:
        abort(404)

@app.route('/registrarPeriodo',methods=['post'])
@login_required
def registrarPeriodo(): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        periodo = Periodos ()
        periodo.nombre = request.form['nombre']
        periodo.fechaInicio = request.form['fechaInicio']
        periodo.fechaFin = request.form['fechaFin']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            periodo.estatus='A'
        else:
            periodo.estatus='I' 
        periodo.registrar()
        flash('Periodo registrado con exito')
        return  redirect(url_for('registrarPeriodos'))
    else:
        abort(404)

@app.route('/editarPeriodo/<int:id>',methods=['post'])
@login_required
def editarPeriodo(id): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        periodo = Periodos ()
        periodo.nombre = request.form['nombre']
        periodo.fechaInicio = request.form['fechaInicio']
        periodo.fechaFin = request.form['fechaFin']
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            periodo.estatus='A'
        else:
            periodo.estatus='I'  
        periodo.idPeriodo = id
        periodo.actualizar()
        flash('Periodo actualizado con exito')
        return  redirect(url_for('editarPeriodos', id= periodo.idPeriodo))
    else:
        abort(404)

@app.route('/eliminarPeriodo/<int:id>')
@login_required
def eliminarPeriodo(id):
    if current_user.is_authenticated() and current_user.is_admin(): 
        periodo = Periodos()
        periodo.eliminar(id)
        flash('Periodo eliminado con exito')
        return  redirect(url_for('periodos'))
    else:
        abort(404)

@app.route('/periodos/nombre/<string:nombre>',methods=['get'])
def consultarNombrePeriodos(nombre):
    item=Periodos()    
    return json.dumps(item.consultarNombre(nombre))


#Error--------------------------------------------------------------------------------------
@app.errorhandler(404)
def error_404(e):
    return redirect(url_for('inicio'))

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)
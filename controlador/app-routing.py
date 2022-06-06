from logging import PercentStyle
from flask import Flask,render_template,request,flash, redirect, template_rendered, url_for, abort
from flask_bootstrap import Bootstrap
from sqlalchemy import true
from DAO import db, Puestos,Turnos,Empleados,Departamentos,Estado,FormasdePago,DocumentosEmpleado,Ciudades,Sucursales,Periodos,AusenciasJustificadas,Asistencias,Percepciones,Deducciones,HistorialPuesto,Nomina, NominaDeducciones, NominaPercepciones
from flask_login import LoginManager,current_user,login_required,login_user,logout_user
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import pdfkit,os,json


app=Flask(__name__,template_folder='../Pages',static_folder='../Static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Hola.123@127.0.0.1/RH_ERP'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"! Debes iniciar sesión !"

ruta= os.path.join(os.getcwd())

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
        e = Estado()
        t = Turnos()
        return  render_template('Empleados/registrarEmpleados.html', puestos = p, departamentos = d, estados = e, turnos=t)
    else:
        abort(404)

@app.route('/empleadosE/<int:id>')
@login_required
def empleadosE(id):
    if current_user.is_authenticated():  
        empleados =  Empleados()
        p = Puestos()
        d = Departamentos()
        e = Estado()
        t = Turnos()
        empleados = empleados.consultar(id)
        return  render_template('Empleados/editarEmpleados.html', empleado = empleados, puestos = p, departamentos = d,  estados = e, turnos=t)
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
        page = request.args.get('page', 1, type=int)
        paginacion = doc.consultarPagina(page)
        #docs = doc.consultarDocs(id)
        empleados = empleados.consultar(id)
        return  render_template('Empleados/verPerfil.html', empleado = empleados, puestos = p, departamentos = d, sucursales = s, ciudades = c, turnos=t, documentos =paginacion.items, pagination = paginacion, len = doc.contarDocs(id))
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

@app.route('/ciudadesEstado/<int:id>',methods=['get'])
def ciudadesEstado(id):
    if current_user.is_authenticated():
        item= Ciudades()        
        return json.dumps(item.consultarCiudadesEstado(id))
    else:
        abort(404)

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

@app.route('/sucursalesCiudad/<int:id>',methods=['get'])
def sucursalesCiudad(id):
    if current_user.is_authenticated():
        item= Sucursales()        
        return json.dumps(item.consultarSucursalesCiudad(id))
    else:
        abort(404)

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
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
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

#Asistencias-----------------------------------------------------
@app.route('/asistencias')
@login_required
def asistencias():
    if current_user.is_authenticated() and  (current_user.is_admin() or current_user.is_staff()):
        asistencias=Asistencias() 
        page = request.args.get('page', 1, type=int)
        paginacion = asistencias.consultarPagina(page)         
        return  render_template('Asistencias/asistencias.html', asistencias = paginacion.items, pagination = paginacion, principal = ".asistencias")
    else:
        abort(404)

@app.route('/misAsistencias')
@login_required
def misAsistencias():
    if current_user.is_authenticated():
        asistencias= Asistencias() 
        page = request.args.get('page', 1, type=int)
        paginacion = asistencias.misAsistencias(page)         
        return  render_template('Asistencias/asistencias.html', asistencias = paginacion.items, pagination = paginacion,principal = ".misAsistencias")
    else:
        abort(404)

@app.route('/registrarAsistencias')
@login_required
def registrarAsistencias():
    if current_user.is_authenticated():
        fecha =datetime.today()
        asistencia = Asistencias()
        respuesta = asistencia.consultarfecha(fecha.date())        
        if respuesta["estatus"] == "Error":
            flash(respuesta["mensaje"])
            return  redirect(url_for('misAsistencias'))
        else:
            turno = Turnos()
            turno = turno.consultar(current_user.idTurno)
            dia = fecha.weekday()
            dias={"L":False,"M":False,"X":False,"J":False,"V":False,"S":False,"D":False}                 
            for d in turno.dias.split(sep=','):
                 dias[d]=True
            valores = list(dias.values())           
            if valores[dia]:
                return  render_template('Asistencias/registrarAsistencias.html', fecha = fecha)
            else:
                flash("El día de hoy no es laboral para usted")
                return  redirect(url_for('misAsistencias')) 
    else:
        abort(404)

@app.route('/libresAsistencias')
@login_required
def libresAsistencias():
    if current_user.is_authenticated() :
        fecha =datetime.today()  
        return  render_template('Asistencias/libresAsistencias.html', fecha = fecha)
    else:
        abort(404)

@app.route('/registrarAsistencia',methods=['post'])
@login_required
def registrarAsistencia():
    if current_user.is_authenticated() :
        asistencia=Asistencias()
        asistencia.fecha= request.form['fecha']
        asistencia.horaEntrada= "2000-01-01 " + request.form['horaEntrada']     
        asistencia.dia= request.form['dia']
        asistencia.idEmpleado = current_user.idEmpleado        
        asistencia.registrar()
        flash('Asistencia registrada con exito')
        return  redirect(url_for('misAsistencias'))
    else:
        abort(404)

@app.route('/libreAsistencia',methods=['post'])
@login_required
def libreAsistencia():
    if current_user.is_authenticated() :  
        asistencia=Asistencias()
        asistencia.fecha= request.form['fecha']
        asistencia.horaEntrada= "2000-01-01 " + request.form['horaEntrada']                  
        asistencia.horaSalida= "2000-01-01 " +  request.form['horaEntrada']
        asistencia.dia= request.form['dia']  
        asistencia.idEmpleado = current_user.idEmpleado       
        asistencia.registrar()
        flash('Asitencia registrada con exito')
        return  redirect(url_for('libresAsistencias'))
    else:
        abort(404)

@app.route('/checarSalidaAsistencia/<int:id>')
@login_required
def checarSalidaAsistencia(id):
    asistencia = Asistencias()
    idE = asistencia.consultar(id).idEmpleado
    if current_user.is_authenticated() and current_user.idEmpleado == idE:                              
        asistencia.horaSalida= "2000-01-01 " +  datetime.today().strftime("%H:%M") + ":00"
        asistencia.idAsistencia= id
        asistencia.actualizar()
        flash('Asitencia actualizada con exito')        
        return  redirect(url_for('misAsistencias'))
    else:
        abort(404)





#Ausencias Justificadas-----------------------------------------------------------------------------------
@app.route('/ausenciasJustificadas')
@login_required
def ausenciasJustificadas():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        ausenciasJ= AusenciasJustificadas() 
        page = request.args.get('page', 1, type=int)
        paginacion = ausenciasJ.consultarPagina(page)         
        return  render_template('AusenciasJustificadas/ausenciasJustificadas.html', ausenciasJ = paginacion.items, pagination = paginacion,principal = ".ausenciasJustificadas")
    else:
        abort(404)

@app.route('/misAusenciasJustificadas')
@login_required
def misAusenciasJustificadas():
    if current_user.is_authenticated():
        ausenciasJ= AusenciasJustificadas() 
        page = request.args.get('page', 1, type=int)
        paginacion = ausenciasJ.misSolicitudes(page)         
        return  render_template('AusenciasJustificadas/ausenciasJustificadas.html', ausenciasJ = paginacion.items, pagination = paginacion,principal = ".misAusenciasJustificadas")
    else:
        abort(404)

@app.route('/registrarAusenciasJustificadas')
@login_required
def registrarAusenciasJustificadas():
    if current_user.is_authenticated():
        solicitudes = AusenciasJustificadas()
        respuesta = solicitudes.puedeSolicitar()
        if respuesta["estatus"] == "Error":
            flash(respuesta["mensaje"])
            return  redirect(url_for('misAusenciasJustificadas'))
        
        return  render_template('AusenciasJustificadas/registrarAusenciasJustificadas.html')           
    else:
        abort(404)

@app.route('/editarAusenciasJustificadas/<int:id>')
@login_required
def editarAusenciasJustificadas(id):
    if current_user.is_authenticated():
        ausenciasJ =  AusenciasJustificadas()        
        ausenciasJ = ausenciasJ.consultar(id)
        
        return  render_template('AusenciasJustificadas/editarAusenciasJustificadas.html', ausenciasJ = ausenciasJ)
    else:
        abort(404)

@app.route('/responderAusenciasJustificadas/<int:id>')
@login_required
def responderAusenciasJustificadas(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        ausenciasJ =  AusenciasJustificadas()        
        ausenciasJ = ausenciasJ.consultar(id)
        
        return  render_template('AusenciasJustificadas/responderAusenciasJustificadas.html', ausenciasJ = ausenciasJ)
    else:
        abort(404)

@app.route('/registrarAusenciaJustificada/<string:btn>',methods=['post'])
@login_required
def registrarAusenciaJustificada(btn):
    if current_user.is_authenticated() :
        ausenciasJ=AusenciasJustificadas()
        ausenciasJ.fechaSolicitud= datetime.now()
        ausenciasJ.fechaInicio= request.form['fechaInicio'] 
        ausenciasJ.fechaFin= request.form['fechaFin']   
        ausenciasJ.tipo= request.form['tipo'] 
        ausenciasJ.idEmpleadoSolicita= current_user.idEmpleado   
        

        doc = request.files['documento'].read()        
        if doc:
            ausenciasJ.evidencia = doc
        ausenciasJ.estatus = btn
        ausenciasJ.motivo= request.form['motivo']        
        ausenciasJ.registrar()
        
        flash('Ausencia Justificada registrada con exito')
        return  redirect(url_for('misAusenciasJustificadas'))
    else:
        abort(404)

@app.route('/editarAusenciaJustificada/<int:id>/<string:btn>',methods=['post'])
@login_required
def editarAusenciaJustificada(id,btn):
    if current_user.is_authenticated():  
        ausenciasJ=AusenciasJustificadas()
        ausenciasJ.fechaSolicitud= datetime.now()
        ausenciasJ.fechaInicio= request.form['fechaInicio'] 
        ausenciasJ.fechaFin= request.form['fechaFin']   
        ausenciasJ.tipo= request.form['tipo']              
        doc = request.files['documento'].read()        
        if doc:
            ausenciasJ.evidencia = doc
        ausenciasJ.estatus = btn
        ausenciasJ.motivo= request.form['motivo']
        ausenciasJ.idAusencia = id

        ausenciasJ.actualizar()
        if btn == "G":
            flash('Ausencia Justificada GUARDADA con exito')
            return  redirect(url_for('editarAusenciasJustificadas', id= ausenciasJ.idAusencia))
        elif btn == "E":
            flash('Ausencia Justificada ENVIADA con exito')
            return  redirect(url_for('misAusenciasJustificadas'))
    else:
        abort(404)

@app.route('/responderAusenciaJustificada/<int:id>/<string:btn>',methods=['post'])
@login_required
def responderAusenciaJustificada(id,btn):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        ausenciasJ=AusenciasJustificadas() 
        ausenciasJ.idEmpleadoAutoriza = current_user.idEmpleado       
        ausenciasJ.estatus = btn        
        ausenciasJ.idAusencia = id
        tipo= request.form['tipo']

        empleado  = AusenciasJustificadas()
        empleado = empleado.consultar(id).idEmpleadoSolicita

        if btn == "A":
            if tipo == 'Vacaciones':
                ausenciasJ.evidencia = docVacaciones(ausenciasJ.idAusencia,empleado,ausenciasJ.idEmpleadoAutoriza) 
            if tipo == 'Permiso':
                ausenciasJ.evidencia = docPermisos(ausenciasJ.idAusencia,empleado,ausenciasJ.idEmpleadoAutoriza)
            flash('Ausencia Justificada ACEPTADA con exito')           
        elif btn == "R":
            flash('Ausencia Justificada RECHAZADA con exito')
        ausenciasJ.actualizar()
        return  redirect(url_for('ausenciasJustificadas'))
    else:
        abort(404)

@app.route('/eliminarAusenciaJustificada/<int:id>')
@login_required
def eliminarAusenciaJustificada(id):
    ausencias = AusenciasJustificadas()
    idE = ausencias.consultar(id).idEmpleadoSolicita
    if current_user.is_authenticated() and  current_user.idEmpleado == idE: 
        ausencias = AusenciasJustificadas()
        ausencias.eliminar(id)
        flash('Ausencia Justificada eliminada con exito')
        return  redirect(url_for('misAusenciasJustificadas'))
    else:
        abort(404)

@app.route('/puedeAusentarce',methods=['get'])
def puedeAusentarce():
    if current_user.is_authenticated():
        salida={"diasP":current_user.diasPermiso,"diasV":current_user.diasVacaciones}       
        return json.dumps(salida)
    else:
        abort(404)
    
@app.route('/evidencia/<int:id>')
def evidencia(id):
    doc=AusenciasJustificadas()
    doc = doc.consultar(id).evidencia  
    return doc


# Enrutamiento Percepcion-------------------------------------------------------------------
@app.route('/percepcion')
@login_required
def  percepcion():
    if current_user.is_authenticated():
        PE=Percepciones() 
        page = request.args.get('page', 1, type=int)
        paginacion = PE.consultarPagina(page)         
        return  render_template('Percepciones/percepcion.html', Percepcion = paginacion.items, pagination = paginacion)
    else:
        abort(404)
        
@app.route('/registroPercepcion')
@login_required
def registroPercepcion():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        percepcion1 = Percepciones()
        percepcion1 = percepcion1.consultarAll()
        return  render_template('Percepciones/registroPercepcion.html')
    else:
        abort(404)
        
@app.route('/editarPercepcion/<int:id>')
@login_required
def editarPercepcion(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        percepcion1 = Percepciones()        
        percepcion1 = percepcion1.consultar(id)
        return  render_template('Percepciones/editarPercepcion.html', percepciones = percepcion1)
    else:
        abort(404)
        
@app.route('/agregaPercepcion',methods=['post'])
@login_required
def agregaPercepcion():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        percepcion1=Percepciones()
        percepcion1.nombre= request.form['nombrePercepcion']         
        percepcion1.descripcion=  request.form['descripcion'] 
        percepcion1.diasPagar=  request.form['diasPagar'] 
        estatus = request.values.get('estatus',False)    
        if estatus=="True":
            percepcion1.estatus='A'
        else:
            percepcion1.estatus='I' 
        percepcion1.registrar()
        flash('Percepcion registrada con exito')
        return  redirect(url_for('registroPercepcion'))
    else:
        abort(404)

@app.route('/modificarPercepcion/<int:id>',methods=['post'])
@login_required
def modificarPercepcion(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        percepcion1=Percepciones()
        percepcion1.nombre=request.form['nombrePercepcion']          
        percepcion1.descripcion=request.form['descripcion'] 
        percepcion1.diasPagar=request.form['diasPagar'] 
        estatus=request.values.get('estatus',False) 
        if estatus=="True":
            percepcion1.estatus='A'
        else:
            percepcion1.estatus='I'  
        percepcion1.idPercepcion = id
        percepcion1.actualizar()
        flash('Percepcion actualizada con exito')
        return  redirect(url_for('editarPercepcion', id= percepcion1.idPercepcion))
    else:
        abort(404)

@app.route('/eliminarPerce/<int:id>')
@login_required
def eliminarPerce(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        percepcion1 = Percepciones()
        percepcion1.eliminar(id)
        flash('Percepcion eliminada con exito')
        return  redirect(url_for('percepcion'))
    else:
        abort(404)

@app.route('/percepcion/nombre/<string:nombre>',methods=['get'])
def consultarNombrePercepcion(nombre):
    item=Percepciones()    
    return json.dumps(item.consultarNombre(nombre))

#Enrutamiento Deducciones--------------------------------------------------------------------------------------
@app.route('/deducciones')
@login_required
def deducciones():
    if current_user.is_authenticated(): 
        d=Deducciones()
        page = request.args.get('page', 1, type=int)
        paginacion = d.consultarPagina(page)         
        return  render_template('Deducciones/deducciones.html', deduccion =paginacion.items, pagination = paginacion  )
    else:
        abort(404)
        
@app.route('/registrarDeducciones')
@login_required
def deduccionesRegistrar():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):        
        return  render_template('Deducciones/registrarDeducciones.html')
    else:
        abort(404)

@app.route('/editarDeducciones/<int:id>')
@login_required
def deduccionesEditar(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        deduccion = Deducciones()
        deduccion = deduccion.consultar(id)
        return  render_template('Deducciones/editarDeducciones.html', deducciones= deduccion)
    else:
        abort(404)

@app.route('/registrarDeduccion',methods=['post'])
@login_required
def registrarDeduccion(): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        deduccion = Deducciones()
        deduccion.nombre = request.form['nombreDeduccion']
        deduccion.descripcion = request.form['descripcion']
        deduccion.porcentaje = request.form['porcentaje'] 
        estatus = request.values.get('estatus',False)
        if estatus=="True":
            deduccion.estatus='A'
        else:
            deduccion.estatus='I' 
        deduccion.registrar()
        flash('Deduccion registrada con exito')
        return  redirect(url_for('deduccionesRegistrar'))
    else:
        abort(404)

@app.route('/editarDeduccion/<int:id>',methods=['post'])
@login_required
def editarDeduccion(id): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        deduccion = Deducciones()
        deduccion.nombre = request.form['nombreDeduccion']
        deduccion.descripcion = request.form['descripcion']
        deduccion.porcentaje = request.form['porcentaje'] 
        estatus = request.values.get('estatus',False)
        if estatus=="True":
                deduccion.estatus='A'
        else:
            deduccion.estatus='I'  
        deduccion.idDeduccion = id
        deduccion.actualizar()
        flash('La Deduccion fue actualizada con exito')
        return  redirect(url_for('deduccionesEditar', id= deduccion.idDeduccion))
    else:
        abort(404)

@app.route('/eliminarDeducciones/<int:id>')
@login_required
def eliminarDeducciones(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        deduccion = Deducciones()
        deduccion.eliminar(id)
        flash('Deduccion eliminada con exito')
        return  redirect(url_for('deducciones'))
    else:
        abort(404)

@app.route('/deducciones/nombre/<string:nombre>',methods=['get'])
def consultarNombrePer(nombre):
    item=Deducciones()    
    return json.dumps(item.consultarNombre(nombre))


    
#Enrutamiento Historial de Puesto----------------------------------------------


@app.route('/historialPuesto')
@login_required
def historialPuesto():
    if current_user.is_authenticated(): 
        hp=HistorialPuesto()
        page = request.args.get('page', 1, type=int)
        paginacion = hp.consultarPagina(page)         
        return  render_template('HistorialPuesto/historialPuesto.html', historialP =paginacion.items, pagination = paginacion  )
    else:
        abort(404)
        

@app.route('/editarhistorialP/<int:idE>/<int:idP>/<int:idD>/<string:fecha>')
@login_required
def editarHistorialP(idE,idP,idD,fecha):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        hp = HistorialPuesto()
        p=Puestos()
        d= Departamentos()
        hp = hp.consultar(idE,idP,idD,fecha)
        return  render_template('HistorialPuesto/editarHistorialP.html', hp=hp, puestos=p, departamentos=d)
    else:
        abort(404)

@app.route('/editarHistorialPu/<int:idE>',methods=['post'])
@login_required
def editarHistorialPu(idE): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        hp = HistorialPuesto()
        hp.idEmpleado= idE
        hp.idPuesto = request.form['idPuesto']
        hp.idDepartamento = request.form['idDepartamento'] 
        hp.fechaInicio= request.form['fechaInicio'] 
        hp.fechaFin= request.form['fechaFin']   
        hp.actualizar()
        flash('El historial de puesto fue actualizada con exito')
        return  redirect(url_for('editarHistorialP', idE= hp.idEmpleado,idP= hp.idPuesto,idD=hp.idDepartamento, fecha=hp.fechaInicio))
    else:
        abort(404)
        
@app.route('/validarFechasHP/<int:id>/<int:idP>/<int:idD>/<string:fecha>',methods=['get'])
def validarFechasHP(id,idP,idD,fecha):
    if current_user.is_authenticated():
        item= HistorialPuesto()        
        return json.dumps(item.consultarHistoriales(id,fecha,idP,idD))
    else:
        abort(404)



#DOCUEMNTO ------------------------------
@app.route('/docNomina/<int:id>')
def docNomina(id):
    env = Environment(loader=FileSystemLoader("Pages"))
    template = env.get_template("docs/docNomina.html")
    nomina = Nomina()
    nomina = nomina.consultar(id)
    empleados = Empleados()   
    periodos = Periodos()
    fp = FormasdePago()
    
    nominaD = NominaDeducciones()
    nominaD = nominaD.cosnsultarNomina(nomina.idNomina) 
    nominaP = NominaPercepciones()
    nominaP= nominaP.cosnsultarNomina(nomina.idNomina) 
    datos={
        'nominaD': nominaD,
        'nominaP': nominaP,
        'empleados': empleados.consultarAll(),
        'nomina': nomina,
        'periodos': periodos.consultarAll(),
        'fp':fp.consultarAll()
    }
    html = template.render(datos)    
    file = open(ruta + '\Pages\docs\docNominaTMP.html',"w")
    file.write(html) 
    file.close()    
    pdfkit.from_file(ruta + '\Pages\docs\docNominaTMP.html',ruta+'\Static\docs\docNomina.pdf') 
    pdf = open(ruta+'\Static\docs\docNomina.pdf',"rb")    
    doc = pdf.read()    
    pdf.close()
    os.remove(ruta + '\Pages\docs\docNominaTMP.html')
    os.remove(ruta+'\Static\docs\docNomina.pdf')
    return  doc

@app.route('/docVacaciones/<int:id>/<int:e>/<int:e2>')
def docVacaciones(id,e,e2):
    env = Environment(loader=FileSystemLoader("Pages"))
    template = env.get_template("docs/solicitudVacaciones.html")
    permiso = AusenciasJustificadas()
    empleado = Empleados()
    empleado2 = Empleados()
    permiso = permiso.consultar(id)
    empleado = empleado.consultar(e)
    empleado2 = empleado2.consultar(e2)

    datos={
        'permiso': permiso,
        'empleado': empleado,
        'empleado2': empleado2
    }
    html = template.render(datos)    
    file = open(ruta + '\Pages\docs\solicitudVacacionesTMP.html',"w")
    file.write(html) 
    file.close()    
    pdfkit.from_file(ruta + '\Pages\docs\solicitudVacacionesTMP.html',ruta+'\Static\docs\solicitudVacaciones.pdf') 
    pdf = open(ruta+'\Static\docs\solicitudVacaciones.pdf',"rb")    
    doc = pdf.read()    
    pdf.close()
    os.remove(ruta + '\Pages\docs\solicitudVacacionesTMP.html')
    os.remove(ruta+'\Static\docs\solicitudVacaciones.pdf')
    return  doc

@app.route('/docPermisos/<int:id>/<int:e>/<int:e2>')
def docPermisos(id,e,e2):
    env = Environment(loader=FileSystemLoader("Pages"))
    template = env.get_template("docs/solicitudPermisos.html")
    permiso = AusenciasJustificadas()
    empleado = Empleados()
    empleado2 = Empleados()
    permiso = permiso.consultar(id)
    empleado = empleado.consultar(e)
    empleado2 = empleado2.consultar(e2)

    datos={
        'permiso': permiso,
        'empleado': empleado,
        'empleado2': empleado2
    }
    html = template.render(datos)    
    file = open(ruta + '\Pages\docs\solicitudPermisosTMP.html',"w")
    file.write(html) 
    file.close()    
    pdfkit.from_file(ruta + '\Pages\docs\solicitudPermisosTMP.html',ruta+'\Static\docs\solicitudPermisos.pdf') 
    pdf = open(ruta+'\Static\docs\solicitudPermisos.pdf',"rb")    
    doc = pdf.read()    
    pdf.close()
    os.remove(ruta + '\Pages\docs\solicitudPermisosTMP.html')
    os.remove(ruta+'\Static\docs\solicitudPermisos.pdf')
    return  doc

@app.route('/excel')
def excel():
    empleados = Empleados()
    empleados = empleados.consultarAll()
    datos = []
    for emp in empleados:
        e = [emp.nombre,emp.sexo,emp.tipo,emp.email]
        datos.append(e)

    archivo = pd.DataFrame(datos,columns=['Nombre','Sexo','Tipo','email'])
    archivo.to_excel(ruta+'\Static\docs\excel.xlsx',index=False)
    excel = open(ruta+'\Static\docs\excel.xlsx', 'rb')
    exc =excel.read()
    excel.close()
    os.remove(ruta+'\Static\docs\excel.xlsx')
    return exc




#NOMINA------------------------------------------------------------------------------------

@app.route('/documentoNomina/<int:id>')
def documentoNomina(id):
    doc=Nomina()
    doc = doc.consultar(id).documento  
    return doc


@app.route('/nominas')
@login_required
def nominas():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        n=Nomina()
        page = request.args.get('page', 1, type=int)
        paginacion = n.consultarPagina(page)         
        return  render_template('Nominas/nomina.html', nomina =paginacion.items, pagination = paginacion, p = '.nominas'  )
    else:
        abort(404)

@app.route('/capturaNominas')
@login_required
def capturaNominas():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        n=Nomina()
        page = request.args.get('page', 1, type=int)
        paginacion = n.consultarCapturaPagina(page)         
        return  render_template('Nominas/nomina.html', nomina =paginacion.items, pagination = paginacion, p = '.capturaNominas'  )
    else:
        abort(404)

@app.route('/misNominas')
@login_required
def misNominas():
    if current_user.is_authenticated(): 
        n=Nomina()
        page = request.args.get('page', 1, type=int)
        paginacion = n.consultarmisNominasPagina(page)         
        return  render_template('Nominas/nomina.html', nomina =paginacion.items, pagination = paginacion, p = '.misNominas'  )
    else:
        abort(404)

@app.route('/revicionNominas')
@login_required
def revicionNominas():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.idPuesto == 2): 
        n=Nomina()
        page = request.args.get('page', 1, type=int)
        paginacion = n.consultarEnviadasPagina(page)         
        return  render_template('Nominas/nomina.html', nomina =paginacion.items, pagination = paginacion, p = '.revicionNominas'  )
    else:
        abort(404)


@app.route('/registrarNomina')
@login_required
def registrarNomina():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        empleados = Empleados()   
        periodos = Periodos()
        fp = FormasdePago()
        deducciones = Deducciones()
        percepciones = Percepciones()    
        return  render_template('Nominas/registrarNomina.html', empleados = empleados.consultarAll(), periodos = periodos.consultarAll(), fp = fp.consultarAll(), deducciones = deducciones.consultarAll(),percepciones = percepciones.consultarAll())
    else:
        abort(404)

@app.route('/altaNomina')
@login_required
def altaNomina():
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):
        empleados = Empleados()   
        periodos = Periodos()
        fp = FormasdePago()          
        return  render_template('Nominas/altaNomina.html', empleados = empleados.consultarAll(), periodos = periodos.consultarAll(), fp = fp.consultarAll())
    else:
        abort(404)

@app.route('/editarNomina/<int:id>')
@login_required
def editarNomina(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        nomina = Nomina()
        nomina = nomina.consultar(id)
        empleados = Empleados()   
        periodos = Periodos()
        fp = FormasdePago()
        deducciones = Deducciones()
        percepciones = Percepciones()
        nominaD = NominaDeducciones()
        nominaD = nominaD.cosnsultarNomina(nomina.idNomina) 
        nominaP = NominaPercepciones()
        nominaP= nominaP.cosnsultarNomina(nomina.idNomina)   
        return  render_template('Nominas/editarNomina.html',nomina = nomina, empleados = empleados.consultarAll(), periodos = periodos.consultarAll(), fp = fp.consultarAll(), deducciones = deducciones.consultarAll(),percepciones = percepciones.consultarAll(), nominaD=nominaD,nominaP=nominaP)
    else:
        abort(404)

@app.route('/revisarNomina/<int:id>')
@login_required
def revisarNomina(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.idPuesto == 2):  
        nomina = Nomina()
        nomina = nomina.consultar(id)
        empleados = Empleados()   
        periodos = Periodos()
        fp = FormasdePago()
        
        nominaD = NominaDeducciones()
        nominaD = nominaD.cosnsultarNomina(nomina.idNomina) 
        nominaP = NominaPercepciones()
        nominaP= nominaP.cosnsultarNomina(nomina.idNomina)   
        return  render_template('Nominas/revisarNomina.html',nomina = nomina, empleados = empleados.consultarAll(), periodos = periodos.consultarAll(), fp = fp.consultarAll(), nominaD=nominaD,nominaP=nominaP)
    else:
        abort(404)

@app.route('/verNomina/<int:id>')
@login_required
def verNomina(id):
    if current_user.is_authenticated() :  
        nomina = Nomina()
        nomina = nomina.consultar(id)
        empleados = Empleados()   
        periodos = Periodos()
        fp = FormasdePago()
        
        nominaD = NominaDeducciones()
        nominaD = nominaD.cosnsultarNomina(nomina.idNomina) 
        nominaP = NominaPercepciones()
        nominaP= nominaP.cosnsultarNomina(nomina.idNomina)   
        return  render_template('Nominas/verNomina.html',nomina = nomina, empleados = empleados.consultarAll(), periodos = periodos.consultarAll(), fp = fp.consultarAll(), nominaD=nominaD,nominaP=nominaP)
    else:
        abort(404)

@app.route('/nominaRegistrar/<string:btn>',methods=['post'])
@login_required
def nominaRegistrar(btn): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        nomina = Nomina()       
        nomina.idEmpleado = request.form['idEmpleado']
        nomina.idFormaPago = request.form['idFormaPago'] 
        nomina.idPeriodo= request.form['idPeriodo'] 
        nomina.fechaElaboracion=datetime.now()
        nomina. fechaPago =request.form['fechaPago']
        nomina.subtotal=request.form['subtotal']
        nomina.retenciones=request.form['subtotal']
        nomina.total=request.form['total']
        nomina.diasTrabajados=request.form['diasTrabajados']
        nomina.estatus = btn
        nomina.registrar()
        flash('Nomina registrada con exito')
        return  redirect(url_for('registrarNomina'))
    else:
        abort(404)

@app.route('/nominaAlta',methods=['post'])
@login_required
def nominaAlta(): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        nomina = Nomina()        
        nomina.idEmpleado = request.form['empleado']
        nomina.idFormaPago = request.form['formaPago'] 
        nomina.idPeriodo= request.form['periodo'] 
        nomina.fechaElaboracion=datetime.now()
        nomina.fechaPago =request.form['fechaPago']        
        nomina.diasTrabajados=request.form['diasTrabajados']
        nomina.subtotal=0
        nomina.retenciones=0
        em = Empleados()
        em = em.consultar(nomina.idEmpleado)
        nomina.total=float(nomina.diasTrabajados) * float(em.salarioDiario)
        nomina.estatus = 'Captura' 
        nomina.estado = "A"
        nomina.registrar()
        flash('Nomina dada de alta con exito')
        return  redirect(url_for('capturaNominas'))
    else:
        abort(404)

@app.route('/nominaEditar/<int:id>/<string:btn>',methods=['post'])
@login_required
def nominaEditar(id,btn): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        nomina = Nomina()        
        nomina.idEmpleado = request.form['empleado']
        nomina.idFormaPago = request.form['formaPago'] 
        nomina.idPeriodo= request.form['periodo'] 
        nomina.fechaElaboracion=  datetime.now()
        nomina.fechaPago =request.form['fechaPago']
        nomina.subtotal=request.form['subtotal']
        nomina.retenciones=request.form['retenciones']
        nomina.total=request.form['total']
        nomina.diasTrabajados=request.form['diasTrabajados']
        nomina.estatus = btn
        nomina.idNomina = id       
        nomina.actualizar()
        flash('La Nomina fue actualizada con exito')
        return  redirect(url_for('editarNomina', id= nomina.idNomina))
    else:
        abort(404)

@app.route('/nominaRevisar/<int:id>/<string:btn>',methods=['post'])
@login_required
def nominaRevisar(id,btn): 
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()):  
        nomina = Nomina()        
        nomina.estatus = btn
        nomina.idNomina = id
        if btn == 'Autorizada':
            nomina.documento = docNomina(id)
        nomina.actualizar()
        flash('La nomina fue revisada con exito')
        return  redirect(url_for('nominas'))
    else:
        abort(404)


@app.route('/eliminarNomina/<int:id>')
@login_required
def eliminarNominas(id):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        nomina = Nomina()
        nomina.eliminar(id)
        flash('Nomina eliminada con exito')
        return  redirect(url_for('nominas'))
    else:
        abort(404)





#NominaDeducciones-----------------------------------------------------------------------------------------------------
@app.route('/registrarNominaDeduccion/<int:idN>/<int:idD>/<int:importe>',methods=['post'])
@login_required
def registrarNominaDeduccion(idN,idD, importe):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        nD = NominaDeducciones()
        nD.idNomina = idN
        nD.idDeduccion = idD
        nD.importe = importe
        print(nD.idNomina)
        print(nD.idDeduccion)
        print(nD.importe)
        nD.registrar()
        obj={
            "estado":"ok","mensaje":"Deduccion agregada con exito"
        }
        return json.dumps(obj)       
    else:
        abort(404)



@app.route('/verNominaDeduccion/<int:idN>/<int:idD>',methods=['get'])
@login_required
def verNominaDeduccion(idN,idD):
    if current_user.is_authenticated():
        item= NominaDeducciones()
        item = item.consultar(idN,idD)
        obj = {
            'deduccion': item.deduccion(),
            'porcentaje': item.porsentaje(),
            'importe': item.importe
        }      
        return json.dumps(obj)
    else:
        abort(404)


@app.route('/eliminarNominaDeduccion/<int:id>/<int:id2>',methods=['post'])
@login_required
def eliminarNominaDeduccion(id, id2):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        nD = NominaDeducciones()
        nD.eliminar(id,id2)
        return json.dumps({"estado":"ok","mensaje":"Deduccion eliminada con exito"} )            
    else:
        abort(404)



#NominaPercepcion-----------------------------------------------------------------------------------------------------
@app.route('/registrarNominaPercepcion/<int:idN>/<int:idP>/<int:importe>',methods=['post'])
@login_required
def registrarNominaPercepcion(idN,idP, importe):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        nD = NominaPercepciones()
        nD.idNomina = idN
        nD.idPercepcion = idP
        nD.importe = importe       
        nD.registrar()
        obj={
            "estado":"ok","mensaje":"Percepcion agregada con exito"
        }
        return json.dumps(obj)       
    else:
        abort(404)



@app.route('/verNominaPercepcion/<int:idN>/<int:idP>',methods=['get'])
@login_required
def verNominaPercepcion(idN,idP):
    if current_user.is_authenticated():
        item= NominaPercepciones()
        item = item.consultar(idN,idP)
        obj = {
            'percepcion': item.percepcion(),
            'dias': item.dias(),
            'importe': item.importe
        }      
        return json.dumps(obj)
    else:
        abort(404)


@app.route('/eliminarNominaPercepcion/<int:id>/<int:id2>',methods=['post'])
@login_required
def eliminarNominaPercepcion(id, id2):
    if current_user.is_authenticated() and (current_user.is_admin() or current_user.is_staff()): 
        nD = NominaPercepciones()
        nD.eliminar(id,id2)
        return json.dumps({"estado":"ok","mensaje":"Percepcion eliminada con exito"} )            
    else:
        abort(404)
        


#Error--------------------------------------------------------------------------------------
@app.errorhandler(404)
def error_404(e):
    return redirect(url_for('inicio'))

if __name__=='__main__':
    db.init_app(app)
    #HOST = os.environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(os.environ.get('SERVER_PORT', '80'))
    #except ValueError:
    #    PORT = 80
    #app.run(HOST, PORT)
    app.run(debug=true)
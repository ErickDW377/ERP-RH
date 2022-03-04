from flask import Flask,render_template,request,flash, redirect, url_for, abort
from flask_bootstrap import Bootstrap
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import String
from DAO import db, Puestos
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

@app.route('/puestos')
def puestos():
    p=Puestos() 
    puestos = p.consultarAll()   
    return  render_template('Puestos/puestos.html', puestos = puestos)

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)
    
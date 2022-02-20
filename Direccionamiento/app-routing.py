from flask import Flask,render_template,request,flash, redirect, url_for, abort

app=Flask(__name__,template_folder='../pages',static_folder='../static')


app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Hola.123@127.0.0.1/checkCar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'

@app.route('/')
def iniciar():    
    return  render_template('Inicio/inicio.html')


if __name__=='__main__':    
    app.run(debug=True)
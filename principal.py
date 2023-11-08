from datetime import datetime,timedelta
import hashlib
from random import randint
from flask import Flask, redirect,render_template,request,send_from_directory,session
from flaskext.mysql import MySQL
from articulos import Articulos
import os
programa = Flask(__name__)
programa.secret_key=str(randint(100000,999999))
programa.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
mysql = MySQL()
programa.config['MYSQL_DATABASE_HOST'] = 'localhost'
programa.config['MYSQL_DATABASE_PORT'] = 3306
programa.config['MYSQL_DATABASE_USER'] = 'root'
programa.config['MYSQL_DATABASE_PASSWORD'] = ''
programa.config['MYSQL_DATABASE_DB'] = 'inventario'
mysql.init_app(programa)
misArticulos = Articulos(programa,mysql)

CARPETAUP = os.path.join('uploads')
programa.config['CARPETAUP']=CARPETAUP

@programa.route('/uploads/<nombre>')
def uploads(nombre):
    return send_from_directory(programa.config['CARPETAUP'],nombre)

@programa.route("/")
def index():
    return render_template("login.html",msg="")

@programa.route("/login", methods=['POST'])
def login():
    id = request.form['id']
    contra = request.form['contra']
    cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
    sql = f"SELECT nombre FROM usuarios WHERE idusuario='{id}' AND contrasena='{cifrada}' AND activo=1"
    con = mysql.connect()
    cur = con.cursor()
    cur.execute(sql)
    resultado = cur.fetchall()
    con.commit()
    if len(resultado)==0:
        return render_template("login.html",msg="Credenciales incorrectas o usuario inactivo")
    else:
        session['loginCorrecto'] = True
        session['nombreUsuario'] = resultado[0][0]
        return redirect("/principal")
#        return render_template("index.html",nom=resultado[0][0])

@programa.route("/principal")
def principal():
    if session.get("loginCorrecto"):
        return render_template("index.html", nom=session.get('nombreUsuario'))
    else:
        return redirect('/')

@programa.route('/articulos')
def articulos():
    if session.get("loginCorrecto"):
        resultado = misArticulos.consultar()
        return render_template("articulos.html",res=resultado)
    else:
        return redirect('/')

@programa.route("/agregararticulo")
def agregaarticulo():
    if session.get("loginCorrecto"):
        return render_template("agregaarticulo.html",msg="")
    else:
        return redirect('/')

@programa.route("/guardaarticulo",methods=['POST'])
def guardaarticulo():
    if session.get("loginCorrecto"):
        id = request.form['id']
        nombre = request.form['nombre']
        precio = request.form['precio']
        saldo = request.form['saldo']
        foto = request.files['foto']
        if len(misArticulos.buscar(id))>0:
            return render_template("agregaarticulo.html",msg="Id de artículo ya existente")
        ahora = datetime.now()
        fnombre,fextension = os.path.splitext(foto.filename)
        nombreFoto = "A"+ahora.strftime("%Y%m%d%H%M%S")+fextension
        print(foto.filename,nombreFoto)
        foto.save("uploads/"+nombreFoto)
        misArticulos.agregar([id,nombre,precio,saldo,nombreFoto])
        return redirect("/articulos")
    else:
        return redirect('/')

@programa.route('/borrararticulo/<id>')
def borrararticulo(id):
    if session.get("loginCorrecto"):
        misArticulos.borrar(id)
        return redirect('/articulos')
    else:
        return redirect('/')

@programa.route('/editararticulo/<id>')
def editararticulo(id):
    if session.get("loginCorrecto"):
        articulo = misArticulos.buscar(id)
        return render_template("editaarticulo.html",art=articulo[0])
    else:
        return redirect('/')

@programa.route('/actualizaarticulo',methods=['POST'])
def actualizaarticulo():
    id = request.form['id']
    nombre = request.form['nombre']
    precio = request.form['precio']
    saldo = request.form['saldo']
    foto = request.files['foto']
    art = [id,nombre,precio,saldo,foto]
    misArticulos.modificar(art)
    return redirect("/articulos")

if __name__=='__main__':
    programa.run(host='0.0.0.0',debug=True,port=5080)
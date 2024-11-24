import os
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory

app = Flask (__name__)


app = Flask(__name__, template_folder ='./templates')
app.secret_key="MoiseJr"
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sitio_web'
mysql.init_app(app)


@app.route('/')
def Inicio():
    return render_template('sitio/index.html')

@app.route('/imagenes/<imagen>')
def imagenes(imagen):
    return send_from_directory(os.path.join('sitio/imagenes'), imagen)

@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join('sitio/css'), archivocss)

@app.route('/autos/')
def autos():
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `autos`")
    autos = cursor.fetchall()
    conexion.commit()
    print(conexion)
    
    return render_template('sitio/autos.html', autos=autos)
    

@app.route('/nosotros/')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():
    
    if not 'login'  in session:
        return redirect('admin/login')
    
    return render_template('admin/index.html')

@app.route('/admin/login/')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login/', methods=['POST'])
def admin_login_post():
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    
    if _usuario == "admin" and _password == "123":
        session["login"] = True
        session["usuario"] = "Administrador"
        return redirect("admin/login")
        
    return render_template('admin/login.html', mensaje="Usuario o contraseña incorrecta")

@app.route('/admin/cerrar/')
def login_cerrar():
    session.clear()
    return redirect('admin/login')

@app.route('/admin/autos/')
def admin_autos():
    
    if not 'login'  in session:
        return redirect('admin/login')
    
    conexion =mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `autos` WHERE 1")
    autos = cursor.fetchall()
    return render_template('admin/autos.html', autos=autos)

@app.route('/admin/autos/guardar/', methods=['POST'])
def admin_autos_guardar():
    
    if not 'login'  in session:
        return redirect('admin/login')
    
    _nombre = request.form['txtNombre']
    _url = request.form['txtURL']
    _archivo = request.files['txtImagen']
    
    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')
    
    if _archivo.filename != "":
        nuevoNombre = horaActual + "_" + _archivo.filename
        _archivo.save('templates/sitio/images/' + nuevoNombre)  # Cambiado a un directorio estático
    
    sql = "INSERT INTO `autos` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre, nuevoNombre, _url)  # Usar nuevoNombre para la imagen
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    
    return redirect('/admin/autos')

@app.route('/admin/autos/borrar/', methods=['POST'])
def admin_autos_borrar():
    
    if not 'login'  in session:
        return redirect('admin/login')
    
    _id = request.form['txtID']
    print(_id)
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen FROM `autos` WHERE id=%s", (_id))
    autos = cursor.fetchall()
    conexion.commit()
    print(autos)
    
    if os.path.exists('templates/sitio/images/' +str(autos[0][0])):
        os.unlink('templates/sitio/images/' +str(autos[0][0]))
        
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `autos` WHERE id=%s", (_id))
    conexion.commit()
    
    return redirect('/admin/autos')

if __name__ == '__main__':
    app.run(debug=True)
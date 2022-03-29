import os
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, json, url_for
from flaskext.mysql import MySQL
from passlib.hash import sha256_crypt
import mysql.connector as db

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0221'
app.config['MYSQL_DATABASE_DB'] = 'cadastro'
app.config['MYSQL_DATABASE_HOST'] = 'localhost' #172.17.0.1
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql.init_app(app)

@app.route('/inicio')
def inicio():
    return render_template('home.html')

@app.route('/register', methods=['POST','GET'])
def register():
    title = 'Formulário de Cadastro'
    if request.method == "POST":
        usuario_form = request.form['usuario']
        email_form = request.form['email']
        senha_form = request.form['senha']
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = ("INSERT INTO cadastros (usuario, email, senha)" "VALUES (%s,%s,%s)")
            val = (usuario_form, email_form, senha_form)
            cursor.execute(query, val)
            conn.commit()
            conn.close()
            return sucess()
        except:
            return "Erro ao adicionar"
    else:
        return render_template("register.html", title = title)


@app.route('/')
def home():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    login = request.form
    _usuario = login['usuario']
    _senha = login['senha']
    conn = mysql.connect()
    cursor = conn.cursor()
    data = cursor.execute('SELECT * FROM cadastros WHERE usuario=%s', (_usuario))
    data = cursor.fetchone()[3]
    if str(_senha) == str(data):
        account = True
        if account:
            session['logged_in'] = True
    else:
        return False
    return home()

@app.route('/logout')
def logout():
  session['logged_in'] = False
  return home()

@app.route('/successful_registration')
def sucess():
  return render_template("sucess.html")


if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True, use_debugger=False, use_reloader=False)
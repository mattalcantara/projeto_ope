import os
from requests import *
from webbrowser import Chrome
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, json, url_for
from flaskext.mysql import MySQL
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from tratamentos import tratar
from enviar_email import *

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0221'
app.config['MYSQL_DATABASE_DB'] = 'cadastro'
app.config['MYSQL_DATABASE_HOST'] = 'localhost' #172.17.0.1
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql.init_app(app)

def exec(command):
  conn = mysql.connect()
  cursor.execute(command)
  cursor = conn.cursor()
  return cursor.fetchall()

@app.route('/inicio', methods=['POST','GET'])
def inicio():
    return render_template('home.html')

@app.route('/cancel', methods=['POST','GET'])
def cancel():
  if request.method == "POST": 
    nome = tratar(request.form['name-label'])
    email = request.form['email-label'].upper()
    telefone = request.form['number-label']
    produto = tratar(request.form['answer'])
    tipo_solic = tratar(request.form['tipo'])
    motivo = tratar(request.form['motivo'])
    conn = mysql.connect()
    cursor = conn.cursor()
    query = ("INSERT INTO cancelamentos (nome, email, telefone, produto, tipo_solic, motivo)" "VALUES (%s,%s,%s,%s,%s,%s)")
    val = (nome, email, telefone, produto, tipo_solic, motivo)
    enviar_email_cancelamento(email, produto)
    cursor.execute(query, val)
    conn.commit()
    conn.close()
    return sucess()
  return render_template('cancelamento.html')

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
    if session.get('admin'):
      conn = mysql.connect()
      cursor = conn.cursor()
      print(cursor.execute("SELECT * FROM solicitacoes"))
      registros = cursor.fetchall()
      print(registros[0])
      for x in range(len(registros)):
          print(registros[x])
      return render_template('admin.html', registros = registros)
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
    data2 = cursor.execute('SELECT * FROM cadastros WHERE usuario=%s', (_usuario))
    data2 = cursor.fetchone()[4]
    if str(_senha) == str(data):
        account = True
        if account:
            session['logged_in'] = True
            if str(data2) == '1':
              session['admin'] = True
            else:
              session['admin'] = False
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

@app.route('/requests', methods=['POST', 'GET'])
def chamados():
    if request.method == "POST": 
      nome = tratar(request.form['name-label'])
      email = request.form['email-label'].upper()
      telefone = request.form['number-label']
      produto = tratar(request.form['answer'])
      tipo_solic = tratar(request.form['tipo'])
      descr_solic = tratar(request.form['descr_solic'])
      conn = mysql.connect()
      cursor = conn.cursor()
      query = ("INSERT INTO solicitacoes (nome, email, telefone, produto, tipo_solic, descr_solic)" "VALUES (%s,%s,%s,%s,%s,%s)")
      val = (nome, email, telefone, produto, tipo_solic, descr_solic)
      enviar_email(email, produto)
      cursor.execute(query, val)
      conn.commit()
      conn.close()
      return sucess()
    return render_template("chamado.html")

@app.route('/admin', methods=['POST', 'GET'])
def index_2():
  login = request.form
  _usuario = login['usuario']
  data = exec('select * from cadastros where usuario = %s', (_usuario)) 
  data = data.fetchone()[4]
  print(_usuario)
  print(data)
  if data == 1:
    return render_template("admin.html")
  else:
    flash('Você não tem acesso de administrador! Redirecionando.')
    return home()

if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True, use_debugger=False, use_reloader=False)
import os
from webbrowser import Chrome
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, json, url_for
from flaskext.mysql import MySQL
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

#driver = webdriver.Chrome(ChromeDriverManager().install())
#driver.implicitly_wait(10)
#driver.get("localhost:5000/requests")
#driver = webdriver.Chrome(executable_path= r'C:\\Utility\\BrowserDrivers\\chromedriver.exe')
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

@app.route('/requests', methods=['POST', 'GET'])
def chamados():
    if request.method == "POST": 
      nome = request.form['name-label']
      email = request.form['email-label']
      telefone = request.form['number-label']
      produto = request.form['answer']
      #tipo = (request.form.get['tipo_solic'])
      #tipo = Select(driver.find_element_by_id('tipo_solic'))
      #tipo = Select(driver.find_element("tipo_solic"))
      #print(tipo.select_by_value("Value"))
      tipo_solic = request.form['tipo']
      descr_solic = request.form['descr_solic']

      conn = mysql.connect()
      cursor = conn.cursor()
      query = ("INSERT INTO solicitacoes (nome, email, telefone, produto, tipo_solic, descr_solic)" "VALUES (%s,%s,%s,%s,%s,%s)")
      val = (nome, email, telefone, produto, tipo_solic, descr_solic)
      cursor.execute(query, val)
      conn.commit()
      conn.close()
      return sucess()
    return render_template("chamado.html")

@app.route('/index')
def index_2():
  return render_template ("index_2.html")


if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True, use_debugger=False, use_reloader=False)
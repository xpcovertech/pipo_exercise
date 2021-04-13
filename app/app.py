from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True 


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create Database engine and Session
engine = create_engine('sqlite:///db/pipo.db')
db = scoped_session(sessionmaker(bind=engine))

@app.teardown_request
def remove_session(ex=None):
    db.remove()


# UTILITIES 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id_usuario") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_admin_title(nivel):
	if nivel == 2:
		headtitle = "System Admin"
	elif nivel == 1:
		headtitle = "Admin"
	else:
		headtitle = "Colaborador"
	return headtitle

def get_header(session):
	try: 
		header = {"nome": session["nome"],
					"empresa": session["empresa"],
					"admin": get_admin_title(session["admin"]),
					"id_usuario": session["id_usuario"]}
	except:
		header = {"nome": "",
					"empresa": "",
					"admin": "",
					"id_usuario": ""}
	return header


# SQL QUERIES
def get_all(table):
	if table.isalpha() is not True:
		return None
	table_all = db.execute("""SELECT * FROM {}""".format(table)).fetchall()
	return table_all	

def search_like(table, like):
	if table.isalpha() is not True:
		return None
	table_search_like = db.execute("""SELECT * FROM {} WHERE nome 
								LIKE :nome""".format(table),
								{"nome": '%'+like+'%'}).fetchall()
	return table_search_like

def search_cpf(table, cpf):
	if table.isalpha() is not True:
		return None
	table_search_cpf = db.execute("""SELECT * FROM {} WHERE cpf = :cpf""".format(table),
								{"cpf": cpf}).fetchall()
	return table_search_cpf

def cadastro_empresa(nome):
	try:
		lista_empresas = get_all("empresa")
		for empresa in lista_empresas:
			if empresa["nome"].lower() == nome.lower():
				return False
		db.execute("""INSERT INTO empresa (nome) VALUES (:nome)""", {"nome": nome})
		db.commit()
		return True
	except:
		return False

def cadastro_beneficio(nome):
	try:
		lista_beneficios = get_all("beneficio")
		for beneficio in lista_beneficios:
			if beneficio["nome"].lower() == nome.lower():
				return False
		db.execute("""INSERT INTO beneficio (nome) VALUES (:nome)""", {"nome": nome})
		db.commit()
		return True
	except:
		return False

def get_colaboradores(id_empresa):
	colaboradores = db.execute("""SELECT * FROM colaborador WHERE id_empresa = :id_empresa 
								ORDER BY nome""", {"id_empresa": id_empresa}).fetchall()
	return colaboradores

def cadastro_colaborador(nome, cpf, id_empresa):
	try:
		lista_colaboradores = db.execute("""SELECT nome FROM colaborador WHERE cpf = :cpf""",
										{"cpf": cpf}).fetchone()
		if lista_colaboradores is not None:
			return False
		db.execute("""INSERT INTO colaborador (nome, id_empresa, cpf, ativo) 
						VALUES (:nome, :id_empresa, :cpf, :ativo)""", 
						{"nome": nome, "id_empresa": id_empresa, "cpf": cpf, "ativo": "s"})
		db.commit()
		return True
	except:
		return False

def get_perfil(id_usuario):
	colaborador = db.execute("""SELECT * FROM colaborador WHERE id = :id""",
							{"id": id_usuario}).fetchone()
	admin = db.execute("""SELECT nivel FROM admin WHERE id_colaborador = :id_colaborador""",
						{"id_colaborador": id_usuario}).fetchone()
	if admin is not None:
		user_admin = admin["nivel"]
	else:
		user_admin = 0
	perfil = {"nome": colaborador["nome"],
				"id": colaborador["id"],
				"cpf": colaborador["cpf"],
				"admin": get_admin_title(user_admin)}
	return perfil

def get_beneficios(id_empresa):
	beneficios = db.execute("""SELECT id, nome FROM beneficio JOIN beneficio_empresa ON id = id_beneficio 
							IN (SELECT id_beneficio FROM beneficio_empresa WHERE id_empresa = :id_empresa)
							ORDER BY nome""", {"id_empresa": id_empresa}).fetchall()
	return beneficios


# INDEX
@app.route("/", methods=['GET'])
@login_required
def index():
	return render_template("index.html", header = get_header(session))


# EMPRESAS
@app.route("/empresas", methods=['GET'])
@login_required
def empresas():
	return render_template("empresas.html", header = get_header(session))

@app.route("/empresas/lista", methods=['GET'])
@login_required
def empresaslista():
	return render_template("empresaslista.html", header = get_header(session),
							lista_empresas = get_all("empresa"))

@app.route("/empresas/busca", methods=["GET", "POST"])
@login_required
def empresasbusca():
	if request.method == "POST":
		if not request.form.get("nome"):
			return "Por favor insira o nome da empresa"
		return render_template("empresasresultado.html", header = get_header(session),
							lista_empresas = search_like("empresa", request.form.get("nome")))
	else:
		return render_template("empresasbusca.html", header = get_header(session))

@app.route("/empresas/cadastro", methods=["GET", "POST"])
@login_required
def empresascadastro():
	if request.method == "POST":
		if session["admin"] == 0:
			return "Você não está autorizado a incluir novas empresas"
		if not request.form.get("nome"):
			return "Por favor insira o nome da empresa"
		if cadastro_empresa(request.form.get("nome")):
			return redirect("/empresas/lista")
		else:
			return "Erro no cadastro. Talvez essa empresa já esteja cadastrada."
	else:
		return render_template("empresascadastro.html", header = get_header(session))


# PESSOAS
@app.route("/pessoas", methods=['GET'])
@login_required
def pessoas():
	return render_template("colaboradores.html", header = get_header(session))

@app.route("/pessoas/lista", methods=['GET'])
@login_required
def pessoaslista():
	return render_template("colaboradoreslista.html", header = get_header(session),
							lista_colaboradores = get_colaboradores(session["id_empresa"]))

@app.route("/pessoas/busca", methods=["GET", "POST"])
@login_required
def pessoasbusca():
	if request.method == "POST":
		if not request.form.get("nome") and not request.form.get("cpf"):
			return "Por favor insira o nome ou cpf da pessoa"
		if request.form.get("nome"):
			return render_template("colaboradoresresultado.html", header = get_header(session),
							lista_colaboradores = search_like("colaborador", request.form.get("nome")))
		else:
			return render_template("colaboradoresresultado.html", header = get_header(session),
							lista_colaboradores = search_cpf("colaborador", request.form.get("cpf")))

	else:
		return render_template("colaboradoresbusca.html", header = get_header(session))

@app.route("/pessoas/cadastro", methods=["GET", "POST"])
@login_required
def pessoascadastro():
	if request.method == "POST":
		if session["admin"] == 0:
			return "Você não está autorizado a incluir novas pessoas"
		if not request.form.get("nome") or not request.form.get("cpf"):
			return "Por favor complete o formulário com todos os dados"
		if request.form.get("cpf").isdigit() is not True:
			return "O cpf deve conter somente números"
		if cadastro_colaborador(request.form.get("nome"), request.form.get("cpf"),
						session["id_empresa"]):
			return redirect("/pessoas/lista")
		else:
			return "Erro no cadastro. Talvez essa pessoa já esteja cadastrada."
	else:
		return render_template("colaboradorescadastro.html", header = get_header(session),
								lista_beneficios = get_beneficios(session["id_empresa"]))

@app.route("/pessoas/perfil/<id_pessoa>", methods=["GET"])
@login_required
def pessoasperfil(id_pessoa):
	return render_template("colaboradoresperfil.html", header = get_header(session),
								perfil = get_perfil(id_pessoa))

@app.route("/pessoas/editar/<id_pessoa>", methods=["GET", "POST"])
@login_required
def pessoaseditar(id_pessoa):
	if request.method == "POST":
		if session["admin"] == 0:
			return "Você não está autorizado a editar perfis"
		return redirect("/pessoas/perfil/{}").format(id_pessoa)
	else:
		if session["admin"] == 0:
			return "Você não está autorizado a editar perfis"
		return render_template("colaboradoreseditar.html", header = get_header(session),
								perfil = get_perfil(id_pessoa))


#beneficios
@app.route("/beneficios", methods=['GET'])
@login_required
def beneficios():
	return render_template("beneficios.html", header = get_header(session))

@app.route("/beneficios/lista", methods=['GET'])
@login_required
def beneficioslista():
	return render_template("beneficioslista.html", header = get_header(session),
							lista_beneficios = get_all("beneficio"))

@app.route("/beneficios/busca", methods=["GET", "POST"])
@login_required
def beneficiosbusca():
	if request.method == "POST":
		if not request.form.get("nome"):
			return "Por favor insira o nome do beneficio"
		return render_template("beneficiosresultado.html", header = get_header(session),
							lista_beneficios = search_like("beneficio", request.form.get("nome")))
	else:
		return render_template("beneficiosbusca.html", header = get_header(session))

@app.route("/beneficios/cadastro", methods=["GET", "POST"])
@login_required
def beneficioscadastro():
	if request.method == "POST":
		if session["admin"] == 0:
			return "Você não está autorizado a incluir novos beneficios"
		if not request.form.get("nome"):
			return "Por favor insira o nome do beneficio"
		if cadastro_beneficio(request.form.get("nome")):
			return redirect("/beneficios/lista")
		else:
			return "Erro no cadastro. Talvez esse beneficio já esteja cadastrado."
	else:
		return render_template("beneficioscadastro.html", header = get_header(session))

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

	session.clear()

	if request.method == "POST":

		if not request.form.get("cpf"):
			return "Por favor insira seu CPF"

		cpf = request.form.get("cpf")

		usuario = db.execute("""SELECT id, nome, id_empresa FROM colaborador WHERE cpf = :cpf""",
							{"cpf": cpf}).fetchone()
		if usuario is None:
			return "Número de CPF não encontrado"

		empresa = db.execute("""SELECT nome FROM empresa WHERE id = :id""", 
							{"id": usuario["id_empresa"]}).fetchone()
		if empresa is None:
			return "Erro no cadastro do usuário: Empresa Inexistente"

		admin = db.execute("""SELECT nivel FROM admin WHERE id_colaborador = :id_usuario""",
							{"id_usuario": usuario[0]}).fetchone()
		if admin is None:	
			session["admin"] = 0
		else: 
			session["admin"] = admin[0]

		session["id_usuario"] = usuario["id"]
		session["id_empresa"] = usuario["id_empresa"]
		session["nome"] = usuario["nome"]
		session["empresa"] = empresa[0]

		return redirect("/")

	else:

		#header = {"empresa": "Login", "admin": ""}

		return render_template("login.html", header = get_header(session))


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run()
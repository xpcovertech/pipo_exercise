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

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id_usuario") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_headtitle(nivel):
	if nivel == 2:
		headtitle = "Godmode"
	elif nivel == 1:
		headtitle = "Admin"
	else:
		headtitle = "Colaborador"
	return headtitle

@app.route("/", methods=['GET'])
@login_required
def index():

	colaborador = db.execute("""SELECT nome FROM colaborador WHERE id = :id""",
								{"id": session["id_usuario"]}).fetchone()
	

	return render_template("index.html", colaborador = colaborador[0], 
							headtitle = get_headtitle(session["admin"]))

@app.route("/empresas", methods=['GET'])
@login_required
def empresas():
	return render_template("empresas.html", 
							headtitle = get_headtitle(session["admin"]))

@app.route("/empresas/lista", methods=['GET'])
@login_required
def empresaslista():
	empresas = db.execute("""SELECT nome FROM empresa""").fetchall()

	return render_template("empresaslista.html", empresas = empresas, 
							headtitle = get_headtitle(session["admin"]))

@app.route("/empresas/busca", methods=["GET", "POST"])
@login_required
def empresasbusca():
	if request.method == "POST":
		if not request.form.get("nome"):
			return "Por favor insira o nome da empresa"
		nome = request.form.get("nome")
		empresas = db.execute("""SELECT nome FROM empresa WHERE nome LIKE :nome""",
								{"nome": '%'+nome+'%'}).fetchall()
		if empresas is None:
			return render_template("empresasresultado.html", empresa = "Empresa não encontrada :(",
								headtitle = get_headtitle(session["admin"]))
		return render_template("empresasresultado.html", empresas = empresas,
								headtitle = get_headtitle(session["admin"]))
	else:
		return render_template("empresasbusca.html", 
								headtitle = get_headtitle(session["admin"]))

@app.route("/empresas/cadastro", methods=["GET", "POST"])
@login_required
def empresascadastro():
	if request.method == "POST":
		if session["admin"] == 0:
			return "Você não está autorizado a incluir novas empresas"
		if not request.form.get("nome"):
			return "Por favor insira o nome da empresa"
		nome = request.form.get("nome")
		empresas = db.execute("""SELECT nome FROM empresa""").fetchall()
		for empresa in empresas:
			if empresa[0].lower() == nome.lower():
				return "Essa empresa já existe em nosso banco de dados"
		db.execute("""INSERT INTO empresa (nome) VALUES (:nome)""", {"nome": nome})
		db.commit()
		return redirect("/empresas")

	else:
		return render_template("empresascadastro.html", 
								headtitle = get_headtitle(session["admin"]))

@app.route("/colaboradores", methods=['GET'])
@login_required
def colaboradores():

	colaboradores = db.execute("""SELECT nome FROM colaborador""").fetchall()

	return render_template("colaboradores.html", colaboradores = colaboradores, 
							headtitle = get_headtitle(session["admin"]))

@app.route("/login", methods=["GET", "POST"])
def login():

	session.clear()

	if request.method == "POST":

		if not request.form.get("cpf"):
			return "Por favor insira seu CPF"

		cpf = request.form.get("cpf")

		usuario = db.execute("""SELECT id FROM colaborador WHERE cpf = :cpf""",
							{"cpf": cpf}).fetchone()

		if usuario is None:
			return "Número de CPF não encontrado"

		admin = db.execute("""SELECT nivel FROM admin WHERE id_colaborador = :id_usuario""",
							{"id_usuario": usuario[0]}).fetchone()

		session["id_usuario"] = usuario[0]

		if admin is None:	
			session["admin"] = 0
		else: 
			session["admin"] = admin[0]

		return redirect("/")

	else:

		return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run()
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
# UTILITIES
# UTILITIES
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_admin_title(level):
	if level == 1:
		headtitle = "Admin"
	else:
		headtitle = "Colaborador"
	return headtitle


def get_header(session):
	try: 
		header = {"name": session["name"],
					"company": session["company"],
					"admin": get_admin_title(session["admin"]),
					"id": session["id"]}
	except:
		header = {"name": "",
					"company": "",
					"admin": "",
					"id": ""}
	return header


def split_str(word):
	return [char for char in word]


def is_it_bad(string):
	not_safe = ";\\"
	for letter in string:
		if letter in split_str(not_safe):
			raise ValueError("Not a safe character")



# GENERIC SQL QUERIES
# GENERIC SQL QUERIES
# GENERIC SQL QUERIES
def get_all_table(table):
	#try:
		is_it_bad(table)
		table_all = db.execute("""SELECT * FROM {}""".format(table)).fetchall()
		return table_all
	#except:
	#	raise Exception("Undefined SQL query error")


def get_one_from(table, where, data):
	#try:
		is_it_bad(table); is_it_bad(where); is_it_bad(data)
		one_from = db.execute("""SELECT * FROM {} WHERE {} = :{}""".format(table, 
							where, where), {"{}".format(where): data}).fetchone()
		return one_from
	#except:
	#	raise Exception("Undefined SQL query error")


def get_all_from(table, where, data):
	#try:
		is_it_bad(table); is_it_bad(where); is_it_bad(data)
		all_from = db.execute("""SELECT * FROM {} WHERE {} = :{}""".format(table, 
							where, where), {"{}".format(where): data}).fetchall()
		return all_from
	#except:
	#	raise Exception("Undefined SQL query error")


def search_like(table, like):
	try:
		is_it_bad(table); is_it_bad(like)
		table_search_like = db.execute("""SELECT * FROM {} WHERE name 
								LIKE :name""".format(table),
								{"name": '%'+like+'%'}).fetchall()
		return table_search_like
	except:
		raise Exception("Undefined SQL query error")



# REGISTER QUERIES
# REGISTER QUERIES
# REGISTER QUERIES
def register_person(name, cpf, benefits):
	is_it_bad(name); is_it_bad(cpf); is_it_bad(benefits)
	people = get_one_from("person", "cpf", cpf)
	if people is not None:
		return False
	db.execute("""INSERT INTO person (name, idCompany, cpf) 
					VALUES (:name, :idCompany, :cpf)""", 
					{"name": name, "idCompany": session["idCompany"], "cpf": cpf})
	db.commit()
	new_person = get_one_from("person", "cpf", cpf)
	if benefits:
		register_person_benefits(benefits, new_person["id"])
	return new_person["id"]


def register_person_benefits(benefits, idPerson):
	for benefit in benefits:
		db.execute("""INSERT INTO personBenefit (idPerson, idBenefit)
					VALUES (:idPerson, :idBenefit)""",
					{"idPerson": idPerson, "idBenefit": benefit})
	db.commit()


# Confirma se dado já está cadastrado antes // dados vindos do formulário são type(str)
# Revisar se der tempo
def register_person_data(idPerson, ids_datatype, data_values):
	registered_data = db.execute("""SELECT idDatatype FROM personData 
								WHERE idPerson = :idPerson""",
								{"idPerson": idPerson}).fetchall()
	if registered_data == None:
		registered_data = []
	for i in range(len(ids_datatype)):
		if (int(ids_datatype[i]),) in registered_data:
			if data_values[i] == get_data(idPerson, ids_datatype[i]):
				pass
			else:
				db.execute("""UPDATE personData SET data = :data WHERE 
					idDatatype = :idDatatype AND idPerson = :idPerson""",
					{"data": data_values[i], "idDatatype": ids_datatype[i],
					"idPerson": idPerson})
		else:
			db.execute("""INSERT INTO personData (idPerson, idDatatype, data)
				VALUES (:idPerson, :idDatatype, :data)""",
				{"idPerson": idPerson, "idDatatype": ids_datatype[i],
				"data": data_values[i]})
	db.commit()


def register_benefit(name):
	try:
		benefits = get_all_table("benefit")
		for benefit in benefits:
			if benefit["name"].lower() == name.lower():
				return False
		db.execute("""INSERT INTO benefit (name) VALUES (:name)""", {"name": name})
		new_benefit = get_one_from("benefit", "name", name)
		db.execute("""INSERT INTO companyBenefit (idCompany, idBenefit) 
					VALUES (:idCompany, :idBenefit)""", 
					{"idCompany": session["idCompany"], "idBenefit": new_benefit["id"]})
		db.commit()
		return new_benefit["id"]
	except:
		return False

def register_datatype(name, example):
	datatypes = get_all_table("datatype")
	for datatype in datatypes:
		if datatype["name"].lower() == name.lower():
			return False
	db.execute("""INSERT INTO datatype (name, example) VALUES (:name, :example)""",
				{"name": name, "example": example})
	db.commit()
	return True


# DELETE QUERIES
# DELETE QUERIES
# DELETE QUERIES
def delete_person(idPerson):
	personData = get_all_person_data(idPerson)
	if personData:
		db.execute("""DELETE FROM personData WHERE idPerson = :idPerson""",
					{"idPerson": idPerson}) 
	personBenefit = get_person_benefits(idPerson)
	if personBenefit:
		db.execute("""DELETE FROM personBenefit WHERE idPerson = :idPerson""",
					{"idPerson": idPerson})
	db.execute("""DELETE FROM person WHERE id = :id""", {"id": idPerson})
	db.commit()


def delete_benefit(idBenefit):
	profile = get_benefit_profile(idBenefit)
	if profile["data"]:
		db.execute("""DELETE FROM benefitData WHERE idBenefit = :idBenefit""",
					{"idBenefit": idBenefit}) 
	if profile["clients"]:
		db.execute("""DELETE FROM personBenefit WHERE idBenefit = :idBenefit""",
					{"idBenefit": idBenefit})
	if profile["companies"]:
		db.execute("""DELETE FROM companyBenefit WHERE idBenefit = :idBenefit""",
					{"idBenefit": idBenefit})
	db.execute("""DELETE FROM benefit WHERE id = :id""", {"id": idBenefit})
	db.commit()



# UPDATE QUERIES
# UPDATE QUERIES
# UPDATE QUERIES
def update_benefit_data(idBenefit, ids_datatype):
	current_datatypes = db.execute("""SELECT idDatatype FROM benefitData 
								WHERE idBenefit = :idBenefit""",
								{"idBenefit": idBenefit}).fetchall()
	if current_datatypes is None:
		current_datatypes = []
	for id_data in ids_datatype:
		if (int(id_data),) in current_datatypes:
			pass
		elif (int(id_data),) not in current_datatypes:
			db.execute("""INSERT INTO benefitData (idBenefit, idDatatype)
						VALUES (:idBenefit, :idDatatype)""",
						{"idBenefit": idBenefit, "idDatatype": id_data})
	for datatype in current_datatypes:
		if str(datatype[0]) not in ids_datatype:
			db.execute("""DELETE FROM benefitData WHERE idBenefit = :idBenefit 
						AND idDatatype = :idDatatype""", {"idBenefit": idBenefit,
						"idDatatype": datatype[0]})
	db.commit()
	return True


# Form data is type(str).
def update_person_benefits(idPerson, ids_benefit):
	flag = 0
	current_benefits = db.execute("""SELECT idBenefit FROM personBenefit 
								WHERE idPerson = :idPerson""",
								{"idPerson": idPerson}).fetchall()
	# Check if person had benefits and got them all taken away
	if len(ids_benefit) == 0 and current_benefits is not None:
		for benefit in current_benefits:
			db.execute("""DELETE FROM personBenefit WHERE idPerson = :idPerson
						AND idBenefit = :idBenefit""", 
						{"idBenefit": benefit["idBenefit"], "idPerson": idPerson})
	else:
		if current_benefits is None:
			current_benefits = []
		for benefit in ids_benefit:
			if (int(benefit),) in current_benefits:
				pass
			elif (int(benefit),) not in current_benefits:
				db.execute("""INSERT INTO personBenefit (idPerson, idBenefit) 
							VALUES (:idPerson, :idBenefit)""",
							{"idPerson": idPerson, "idBenefit": benefit})
				flag = 1
		for current in current_benefits:
			if str(current[0]) not in ids_benefit:
				db.execute("""DELETE FROM personBenefit WHERE idBenefit = :idBenefit 
							AND idPerson = :idPerson""", {"idBenefit": current[0],
							"idPerson": idPerson})
	db.commit()
	if flag == 1:
		return True
	else:
		return False



# SEARCH QUERIES
# SEARCH QUERIES
# SEARCH QUERIES
def search_people(idCompany, like):
	try:
		people = db.execute("""SELECT * FROM person WHERE idCompany = :idCompany 
								AND name LIKE :name""", 
								{"name": '%'+like+'%', 
								"idCompany": idCompany}).fetchall()
		return people
	except:
		raise Exception("Undefined SQL query error")


def search_benefits(idCompany, like):
	try:
		benefits = db.execute("""SELECT id, name FROM benefit WHERE name LIKE :name 
								AND id IN (SELECT id FROM companyBenefit 
								WHERE idCompany = :idCompany) 
								ORDER BY name""",
								{"name": '%'+like+'%', 
								"idCompany": idCompany}).fetchall()
		return benefits
	except:
		raise Exception("Undefined SQL query error")



# GET QUERIES
# GET QUERIES
# GET QUERIES
def get_person_data(profile, datalist):
	all_data = []
	for data in datalist:
		if data[0] == 1:
			data_value = profile["name"]
			example = get_data_example(data[0])
		elif data[0] == 2:
			data_value = profile["cpf"]
			example = get_data_example(data[0])
		else:
			data_value = get_data(profile["id"], data[0])
			example = get_data_example(data[0])
		all_data.append({"idDatatype": data[0], "name": data[1], "data": data_value,
							"example": example})
	return all_data

def get_all_person_data(idPerson):
	all_data = db.execute("""SELECT name, idDatatype, data 
							FROM personData JOIN datatype ON idDatatype = id
							WHERE idPerson = :idPerson""",
							{"idPerson": idPerson}).fetchall()
	return all_data

def get_data_example(idDatatype):
	data_example = db.execute("""SELECT example FROM datatype WHERE id = :id""",
								{"id": idDatatype}).fetchone()
	return data_example[0]

def get_data(idPerson, idDatatype):
	person_data = db.execute("""SELECT data FROM personData WHERE idPerson = :idPerson
							AND idDatatype = :idDatatype""",
							{"idPerson": idPerson, "idDatatype": idDatatype}).fetchone()
	if person_data is None: 
		return None 
	else:
		return person_data[0]


def get_person_benefits(idPerson):
	benefits = db.execute("""SELECT id, name FROM benefit WHERE id  
							IN (SELECT idBenefit FROM personBenefit 
							WHERE idPerson = :idPerson)
							ORDER BY name""", {"idPerson": idPerson}).fetchall()
	return benefits


def get_profile(idPerson):
	person = get_one_from("person", "id", str(idPerson))
	benefits = get_person_benefits(idPerson)
	personData = get_all_person_data(idPerson)
	admin = get_one_from("admin", "idPerson", str(idPerson))
	if admin is not None:
		level = admin["level"]
	else:
		level = 0
	profile = {"name": person["name"],
				"id": person["id"],
				"cpf": person["cpf"],
				"company": session["company"],
				"admin": get_admin_title(admin),
				"benefits": benefits,
				"data": personData}
	return profile


def get_company_benefits(idCompany):
	try:
		benefits = db.execute("""SELECT id, name FROM benefit WHERE id 
								IN (SELECT idBenefit FROM companyBenefit 
								WHERE idCompany = :idCompany)
								GROUP BY name ORDER BY name""", 
								{"idCompany": idCompany}).fetchall()
		return benefits
	except:
		raise Exception("Undefined SQL query error")


def get_benefits_data(benefits):
	all_data = []
	for idBenefit in benefits:
		benefits_data = db.execute("""SELECT id, name FROM datatype WHERE id IN
								(SELECT idDatatype FROM benefitData 
								WHERE idBenefit = :idBenefit)""",
								{"idBenefit": idBenefit}).fetchall()
		for data in benefits_data:
			if (data["id"],data["name"]) not in all_data:
				all_data.append((data["id"],data["name"]))
	return all_data


def get_benefit_profile(idBenefit):
	benefit = get_one_from("benefit", "id", str(idBenefit))
	benefitData = db.execute("""SELECT id, name, example FROM datatype WHERE id IN
								(SELECT idDatatype FROM benefitData 
								WHERE idBenefit = :idBenefit)""",
								{"idBenefit": idBenefit}).fetchall()
	clients = db.execute("""SELECT id, name FROM person WHERE idCompany = :idCompany 
							AND id IN (SELECT idPerson FROM personBenefit 
							WHERE idBenefit = :idBenefit) ORDER BY name""", 
							{"idCompany": session["idCompany"] ,
							"idBenefit": idBenefit}).fetchall()
	companies = db.execute("""SELECT idCompany FROM companyBenefit 
							WHERE idBenefit = :idBenefit""",
							{"idBenefit": idBenefit}).fetchall()
	profile = {"name": benefit["name"],
				"id": benefit["id"],
				"data": benefitData,
				"clients": clients,
				"companies": companies}
	return profile

"""
def get_form_profile(idBenefit, idPerson):
	person_profile = get_profile(idPerson)
	benefit_profile = get_benefit_profile(idBenefit) 
	if not person_profile or not benefit_profile:
		return None
	for ben_data in benefit_profile["data"]:
		for person_data in benefit_profile["data"]:
			print(ben_data["id"])
			print(benefit_profile["id"])
"""



# INDEX
# INDEX
# INDEX
@app.route("/", methods=['GET'])
@login_required
def index():
	return render_template("index.html", header = get_header(session))


# HOME
@app.route("/<who>", methods=['GET'])
@login_required
def home(who):
	if who not in ['empresas', 'pessoas', 'beneficios']:
		return "Essa página não existe"
	return render_template("home.html", header = get_header(session), who = who)


# LIST
@app.route("/<who>/lista", methods=['GET'])
@login_required
def list(who):
	if who == "beneficios":
		who_list = get_company_benefits(session["idCompany"])
	elif who == "pessoas":
		who_list = get_all_from("person", "idCompany", str(session["idCompany"]))
	else:
		return "Essa página não existe"
	return render_template("list.html", header = get_header(session), who = who,
										who_list = who_list)


# SEARCH
@app.route("/<who>/busca", methods=['GET', 'POST'])
@login_required
def search(who):
	if request.method == "POST":
		name = request.form.get("name")
		if not name:
			return "Por favor insira um nome"
		if who == "beneficios":
			who_list = search_benefits(session["idCompany"], name)
		elif who == "pessoas":
			who_list = search_people(session["idCompany"], name)
		else:
			return "Essa página não existe"
		return render_template("searchresult.html", header = get_header(session),
													who = who,who_list = who_list)
	else:
		return render_template("search.html", header = get_header(session), 
												who = who)


# REGISTRATION
@app.route("/<who>/cadastro", methods=['GET', 'POST'])
@login_required
def registration(who):
	if request.method == "POST":
		name = request.form.get("name")
		if not name:
			return "Por favor insira um nome"
		if who == "beneficios":
			idBenefit = register_benefit(name)
			if idBenefit:
				return redirect("/{}/perfil/{}".format(who, idBenefit))
			else:
				return "Erro no cadastro. Talvez esse benefício já esteja cadastrado."
		elif who == "pessoas":
			cpf = request.form.get("cpf")
			benefits = request.form.getlist("benefits")
			if not cpf or not cpf.isdigit():
				return "Por favor insira o número de cpf corretamente"
			idPerson = register_person(name, cpf, benefits)
			if idPerson: 
				if benefits: # because a person could have been registered without it
					profile = get_profile(idPerson)
					benefits_data = get_benefits_data(benefits)
					person_data = get_person_data(profile, benefits_data)
					return render_template("registerpersondata.html",
										header = get_header(session),
										profile = profile,
										person_data = person_data)
				return redirect("/{}/lista".format(who))
		else:
			return "Essa página não existe"
	else:
		if who == "pessoas":
			benefits = get_company_benefits(session["idCompany"])
			return render_template("registerperson.html", 
									header = get_header(session), who = who,
									benefits = benefits)
		elif who == "beneficios":
			return render_template("registration.html", 
									header = get_header(session), who = who)
		else:
			return "Essa página não existe"


# REGISTER PERSON DATA
@app.route("/pessoas/cadastro/beneficio", methods=['POST'])
@login_required
def regiterpersondata():
	idPerson = request.form.get("idPerson")
	ids_datatype = request.form.getlist("idDatatype")
	data_values = request.form.getlist("data_value")
	if ids_datatype and data_values:
		register_person_data(idPerson, ids_datatype, data_values)
		return redirect("/pessoas/perfil/{}".format(idPerson))
	else:
		return redirect("/pessoas/lista")


# REGISTER NEW DATATYPE
@app.route("/beneficios/cadastro/dado", methods=['GET','POST'])
@login_required
def registernewdatatype():
	if request.method == "POST":
		name = request.form.get("name")
		example = request.form.get("example")
		if not name or not example:
			return "Você precisa preencher os dois campos"
		if register_datatype(name, example):
			return redirect("/beneficios/lista")
		else:
			return "Houve um erro no cadastro, por favor tente novamente"
	else:
		data_list = get_all_table("datatype")
		return render_template("registernewdatatype.html", 
											header = get_header(session),
											data_list = data_list)


# BENEFIT FORM PROFILE
@app.route("/beneficios/<idBenefit>/pessoas/<idPerson>", methods=['GET'])
@login_required
def benefitformprofile(idBenefit, idPerson):
	benefit_profile = get_benefit_profile(idBenefit)
	person_profile = get_profile(idPerson)
	# checar se colaborador está cadastrado no plano antes de prosseguir
	return render_template("benefitformprofile.html", header = get_header(session),
												benefit = benefit_profile,
												person = person_profile)


# PROFILES
@app.route("/<who>/perfil/<idWho>", methods=['GET'])
@login_required
def profile(who, idWho):
	if who == "pessoas":
		profile = get_profile(idWho)
		if not profile:
			return "Esse perfil não existe"
		return render_template("personprofile.html", header = get_header(session),
								profile = profile, who = who)
	elif who == "beneficios":
		profile = get_benefit_profile(idWho)
		if not profile:
			return "Esse perfil não existe"
		return render_template("benefitprofile.html", header = get_header(session),
								profile = profile, who = who)
	else:
		return redirect("/pessoas/lista")


# EDIT PROFILES
@app.route("/<who>/editar/<idWho>", methods=['GET', 'POST'])
@login_required
def editprofile(who, idWho):
	if request.method == "POST":
		if who == "pessoas":
			ids_benefit = request.form.getlist("idBenefit")
			if update_person_benefits(idWho, ids_benefit):
				profile = get_profile(idWho)
				benefits_data = get_benefits_data(ids_benefit)
				person_data_to_fill = get_person_data(profile, benefits_data)
				return render_template("registerpersondata.html", 
								person_data = person_data_to_fill, 
								header = get_header(session),
								profile = profile, who = who)
			return redirect("/pessoas/perfil/{}".format(idWho))
		elif who == "beneficios":
			ids_datatype = request.form.getlist("idDatatype")
			if not ids_datatype:
				return "Você não pode eliminar todos os dados"
			update_benefit_data(idWho, ids_datatype)
			return redirect("/beneficios/perfil/{}".format(idWho))
	else:
		if who == "pessoas":
			return render_template("editpersonbenefits.html", 
								header = get_header(session),
								profile = get_profile(idWho),
								benefits_list = get_company_benefits(session["idCompany"]))
		elif who == "dados":
			profile = get_profile(idWho)
			return render_template("registerpersondata.html", 
									person_data = profile["data"], 
									profile = profile, who = "pessoas", 
									header = get_header(session))
		elif who == "beneficios":
			profile = get_benefit_profile(idWho)
			if not profile:
				return "Esse perfil não existe"
			return render_template("editbenefit.html", header = get_header(session),
									profile = profile, who = who, 
									data_list = get_all_table("datatype"))
		else:
			return redirect("/pessoas/lista")

# DELETE PROFILE
@app.route("/<who>/deletar", methods=['POST'])
@login_required
def deleteprofile(who):
	if request.method == "POST":
		if who == "pessoas":
			idPerson = request.form.get("idPerson")
			if idPerson:
				delete_person(idPerson)
			return redirect("/pessoas/lista")
		elif who == "beneficios":
			idBenefit = request.form.get("idBenefit")
			if idBenefit:
				delete_benefit(idBenefit)
			return redirect("/pessoas/lista")
		else:
			return "Essa página não existe"



# LOGIN
# Login autorizado somente para administradores cadastrados
@app.route("/login", methods=["GET", "POST"])
def login():
	session.clear()
	if request.method == "POST":
		cpf = request.form.get("cpf")
		if not cpf:
			return "Por favor insira seu CPF"
		person = get_one_from("person", "cpf", cpf)
		if person is None:
			return "Número de CPF não encontrado"
		else:
			admin = get_one_from("admin", "idPerson", str(person["id"]))
			if admin is None:
				return "Você não está autorizado a entrar no sistema"
		company = get_one_from("company", "id", str(person["idCompany"]))
		session["id"] = person["id"]
		session["idCompany"] = person["idCompany"]
		session["name"] = person["name"]
		session["company"] = company["name"]
		session["admin"] = 1
		return redirect("/")
	else:
		return render_template("login.html", header = get_header(session))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run()

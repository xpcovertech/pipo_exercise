import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from functools import wraps

from models_company import CompanyProfile
from models_person import PersonProfile
from models_benefit import BenefitProfile
from models_util import *

from utils import get_header, str_to_int, str_list_to_int

'''
This is a webapp that manages employees' benefits.
For more visit https://github.com/leorapini/pipo_exercise
Code written by Leo Rapini

*Glossary:
Glossary: A person is every employee registered in the database. 
The benefit is the name of any type of benefit plan. Ex. Health Insurance. 
The company is an employer of people that have benefits registered to them, 
allowing people to be enrolled in those benefits. Type of data or Datatype 
is the type of information that a benefit plan requires from a person at 
enrollment. Ex. Date of Birth

Please check the SQL schema in the folder Documentation before reading the code. 
It will make it a more pleasant experience, I promise. 
'''

# SETUP
app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

Session(app)

# Set responses not to be cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Ensure the app is "refreshed" after every request
@app.teardown_request
def remove_session(ex=None):
    db.remove()

# Wrap to allow only logged users to see pages
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# INDEX
@app.route("/", methods=['GET'])
@login_required
def index():
	""" Returns index.html with header information """
	return render_template("index.html", header = get_header(session))


# HOME BENEFITS
@app.route("/beneficios", methods=['GET'])
@login_required
def benefits_home():
	""" Returns home.html with header for beneficios. The 'who' is simply a place holder 
	for the name of the page. The same html file is used for both beneficios and pessoas."""
	return render_template("home.html", header = get_header(session), who = "beneficios")


# LIST BENEFITS
@app.route("/beneficios/lista", methods=['GET'])
@login_required
def benefits_list():
	""" Returns a list of all benefits registered to company. """
	benefits_list = CompanyProfile(session["idCompany"]).get_benefits()
	return render_template("benefits_list.html", header = get_header(session), 
												benefits_list = benefits_list)

# SEARCH BENEFITS
@app.route("/beneficios/busca", methods=['GET', 'POST'])
@login_required
def benefits_search():
	""" If 'GET' method, returns the search page, if 'POST' method, returns the result of 
	that search for Benefits """
	if request.method == "POST":
		benefit_name = request.form.get("name")
		if benefit_name:
			benefits_list = search_benefit_by_name_by_company(benefit_name, session['idCompany'])
			return render_template("benefits_search_result.html", header = get_header(session),
																benefits_list = benefits_list)
		else:
			whoops = "Por favor insira um nome"
			return render_template("search.html", header = get_header(session), 
											who = "beneficios", whoops = whoops)
	else: # 'GET'
		return render_template("search.html", header = get_header(session), who = "beneficios")


# BENEFITS REGISTRATION
@app.route("/beneficios/cadastro", methods=['GET', 'POST'])
@login_required
def benefits_registration():
	""" If 'GET' method, returns the benefits registration page. If 'POST', it first checks if a
	Benefit name has been entered, if not returns the registration page with an alert (whoops). If
	so it calls the register new benefit function which will procced to check the validity of the 
	name entered. If everything goes well, the new benefit profile is returned. Otherwise the
	registration page is reloaded with an alert."""
	if request.method == "POST":
		name = request.form.get("name")
		if name:
			idBenefit = register_new_benefit(name, session['idCompany'])
			if idBenefit:
				return redirect("/beneficios/perfil/{}".format(idBenefit))
			else:
				whoops = "Este beneficio já está cadastrado para essa empresa"
				return render_template("benefits_registration.html", header = get_header(session),
																whoops = whoops)
		else:
			whoops = "Por favor insira um nome"
			return render_template("benefits_registration.html", header = get_header(session),
																whoops = whoops)
	else: # 'GET'
		return render_template("benefits_registration.html", header = get_header(session))


# BENEFIT PROFILE
@app.route("/beneficios/perfil/<idWho>", methods=['GET'])
@login_required
def benefits_profile(idWho):
	""" Receives the benefit's id (idWho) and checks if the user is allowed to see
	that benefit's profile. This is an upgrade from the last version in which anyone could 
	see any benefit, even if the user's company wasn't registered with that benefit. If that
	is the case an alert is shown to the user. Otherwise the benefit profile is returned."""
	idWho = validate_benefit_idwho(idWho, session['idCompany'])
	if idWho:
		profile = BenefitProfile(idWho).get_profile()
		benefit_people = BenefitProfile(idWho).get_people_by_company(session['idCompany'])
		return render_template("benefits_profile.html", header = get_header(session),
								profile = profile, benefit_people = benefit_people)
	else:
		whoops = "Este perfil não existe, por favor selecione um benefício da lista."
		benefits_list = CompanyProfile(session["idCompany"]).get_benefits()
		return render_template("benefits_list.html", header = get_header(session), 
								benefits_list = benefits_list, whoops = whoops)


# EDIT BENEFIT DATA TYPES
@app.route("/beneficios/editar/<idWho>", methods=['GET', 'POST'])
@login_required
def benefits_data_types(idWho):
	""" Receives the benefit's id (idWho) and checks if the user is allowed to edit that
	benefits types of data. If 'GET' method, a list of all data types available and a list of the
	Benefit's pre selected types of data is returned. If 'POST' method, the information received 
	is checked and then updated to the database."""
	idWho = validate_benefit_idwho(idWho, session['idCompany'])
	if idWho:
		if request.method == "POST":
			ids_datatype = request.form.getlist("idDatatype")
			ids_datatype_check = data_types_exist(ids_datatype)
			if ids_datatype_check is not None:
				update_benefit_data_types(idWho, ids_datatype_check)
				return redirect("/beneficios/perfil/{}".format(idWho))
			else: 
				whoops = "Houve um erro na atualização dos tipos de dado. Selecione outro do menu."
				profile = BenefitProfile(idWho).get_profile()
				available_datatypes = get_available_data_types_for_benefit(idWho)
				return render_template("benefits_edit_data_types.html", 
										header = get_header(session), profile = profile, 
										available_datatypes = available_datatypes)
		else: # 'GET'
			profile = BenefitProfile(idWho).get_profile()
			available_datatypes = get_available_data_types_for_benefit(idWho)
			return render_template("benefits_edit_data_types.html", 
									header = get_header(session), profile = profile, 
									available_datatypes = available_datatypes)
	else:
		whoops = "Este perfil não existe, por favor selecione um benefício da lista."
		benefits_list = CompanyProfile(session["idCompany"]).get_benefits()
		return render_template("benefits_list.html", header = get_header(session), 
								benefits_list = benefits_list, whoops = whoops)


# REGISTER NEW DATA TYPE
@app.route("/beneficios/cadastro/dado/<idWho>", methods=['GET','POST'])
@login_required
def benefits_register_new_data_type(idWho):
	""" Receives the benefit's id (idWho) and checks if the user is allowed to register a new 
 	type of data for that benefit. If 'GET' method, a list of all data types registered in
 	the database is returned. If 'POST' method, the new data type is checked before being
 	registered in the database and added to the list of data types of the benefit"""
	idWho = validate_benefit_idwho(idWho, session['idCompany'])
	if idWho:
		if request.method == "POST":
			name = request.form.get("name")
			example = request.form.get("example")
			if name and example:
				register_new_data_type(name, example, idWho)
				return redirect("/beneficios/perfil/{}".format(idWho))
			else:
				data_list = get_all_data_types()
				whoops = "Você precisa preencher os dois campos"
				return render_template("benefits_register_new_data_type.html", 
												header = get_header(session),
												data_list = data_list,
												idWho = idWho, whoops = whoops)
		else: # 'GET'
			data_list = get_all_data_types()
			return render_template("benefits_register_new_data_type.html", 
												header = get_header(session),
												data_list = data_list,
												idWho = idWho)
	else:
		whoops = "Este perfil não existe, por favor selecione um benefício da lista."
		benefits_list = CompanyProfile(session["idCompany"]).get_benefits()
		return render_template("benefits_list.html", header = get_header(session), 
								benefits_list = benefits_list, whoops = whoops)


# BENEFIT REGISTRATION CARD
@app.route("/beneficios/<idBenefit>/pessoas/<idPerson>", methods=['GET'])
@login_required
def benefits_registration_card(idBenefit, idPerson):
	""" Receives idBenefit and idPerson and checks if the user can see that benefit's 
	registration card (benefit must be registered with the user's company as well as the person must
	be a company employee). If the information checks out, the employee's (person) benefit 
	registration card is returned with all correlated data """
	if validate_registration_card(idBenefit, idPerson, session['idCompany']):
		idBenefit = int(idBenefit)
		idPerson = int(idPerson)
		benefit_profile = BenefitProfile(idBenefit).get_profile()
		person_profile = PersonProfile(idPerson).get_profile()
		person_data = get_combined_data_for_person([idBenefit,], idPerson)
		admission_date = get_person_admission_date(idPerson, idBenefit)
		return render_template("benefits_registration_card.html", header = get_header(session),
												benefit = benefit_profile,
												person = person_profile,
												person_data = person_data,
												admission_date = admission_date)
	else:
		whoops = "Este Cartão de Registro não existe."
		return render_template("index.html", header = get_header(session),
												whoops = whoops)
	return render_template("benefits_registration_card.html", header = get_header(session),
												benefit = benefit_profile,
												person = person_profile,
												admission_date = admission_date)


# DELETE BENEFIT PROFILE
@app.route("/beneficios/deletar", methods=['POST'])
@login_required
def benefits_delete_profile():
	""" Receives (through form) the id of the benefit to be deleted. First the
	benefit id is checked and then deleted. Benefit is not truly deleted from database, 
	for it can still be used by other companies. Only the company's registration with
	that benefit is deleted """
	idBenefit = str_to_int(request.form.get("idBenefit"))
	if benefit_exists(idBenefit):
		delete_benefit_profile(idBenefit, session["idCompany"])
		return redirect("/beneficios/lista")
	else: 
		whoops = """Este perfil não existe, por favor selecione outro da lista."""
		benefits_list = CompanyProfile(session["idCompany"]).get_benefits()
		return render_template("people_list.html", header = get_header(session), 
								benefits_list = benefits_list, whoops = whoops)


# HOME PEOPLE
@app.route("/pessoas", methods=['GET'])
@login_required
def people_home():
	""" Returns home.html with header for pessoas. The 'who' is simply a place holder 
	for the name of the page. The same html file is used for both beneficios and pessoas."""
	return render_template("home.html", header = get_header(session), who = "pessoas")


# LIST PEOPLE
@app.route("/pessoas/lista", methods=['GET'])
@login_required
def people_list():
	""" Returns a list of all people registered to company. """
	people_list = CompanyProfile(session["idCompany"]).get_people()
	return render_template("people_list.html", header = get_header(session), 
											people_list = people_list)

# SEARCH PEOPLE
@app.route("/pessoas/busca", methods=['GET', 'POST'])
@login_required
def people_search():
	""" If 'GET' returns the search page, if 'POST' returns the result of that search for 
	People """
	who = "pessoas"
	if request.method == "POST":
		person_name = request.form.get("name")
		if person_name:
			people_list = search_person_by_name_by_company(person_name, session['idCompany'])
			return render_template("people_search_result.html", header = get_header(session),
															people_list = people_list)
		else:
			whoops = "Por favor insira um nome"
			return render_template("search.html", header = get_header(session), 
												who = who, whoops = whoops)
	else:
		return render_template("search.html", header = get_header(session), who = who)


# REGISTER PERSON
@app.route("/pessoas/cadastro", methods=['GET', 'POST'])
@login_required
def people_registration():
	""" This is a more complex function. First a list of all benefits registered with the 
	company is generated. If 'GET' method, returns the people registration page along with 
	the list of all benefits registered with the user's company. 
	If 'POST', it checks if both Person' name has been entered and if the cpf is a valid 
	cpf number in the correct cpf format, if not returns the registration page with an alert 
	(whoops). If valid, it calls the register new person function which will procced to check the 
	validity of the cpf entered against the person database/table. If everything goes well, 
	the function checks if a benefit was selected (or more) during registration. 
	If so, the person is also registered with those benefits. If that is the case the
	people_register_data page is returned to continue the data registration process. If not,
	an updated list of all company people is returned."""
	company_benefits = CompanyProfile(session['idCompany']).get_benefits()
	if request.method == 'POST':
		name = request.form.get("name")
		cpf = request.form.get("cpf")
		chosen_benefits = str_list_to_int(request.form.getlist("benefits"))
		if name and isCpfValid(cpf):
			if not get_person_id_by_cpf(cpf):
				new_person_id = register_new_person(name, cpf, session['idCompany'])
				if len(chosen_benefits) > 0:
					for benefit_id in chosen_benefits:
						register_person_to_benefit(new_person_id, benefit_id)
					combined_data = get_combined_data_for_person(chosen_benefits, new_person_id)
					return render_template("people_register_data.html",
															header = get_header(session),
															person_id = new_person_id,
															combined_data = combined_data)
				else:
					return redirect("/pessoas/lista")
			else:
				whoops = "Essa pessoa já está registrada"
				return render_template("people_registration.html", header = get_header(session), 
																whoops = whoops)
		else:
			whoops = "Por favor insira um nome e um número de cpf válido"
			return render_template("people_registration.html", header = get_header(session), 
															whoops = whoops)
	else: # 'GET'
		return render_template("people_registration.html", header = get_header(session), 
														benefits = company_benefits)


# REGISTER PERSON DATA IN DATABASE 
@app.route("/pessoas/cadastro/beneficio", methods=['POST'])
@login_required
def people_data_registration():
	""" This function simply registers the additional data for person submitted by calling 
	register_data_to_person() and returns the persons updated profile """
	idPerson = str_to_int(request.form.get("idPerson"))
	ids_datatype = str_list_to_int(request.form.getlist("idDatatype"))
	data_values = request.form.getlist("data_value")
	if len(ids_datatype) > 0 and len(data_values) > 0:
		for i in range(len(data_values)):
			if ids_datatype[i] not in [1, 2, 3]: # reserved data types
				try:
					register_data_to_person(ids_datatype[i], data_values[i], idPerson)
				except:
					update_data_from_person(ids_datatype[i], data_values[i], idPerson)
		return redirect("/pessoas/perfil/{}".format(idPerson))
	else:
		whoops = "Você não terminou o cadastro. Clique no plano selecionado e termine o cadastro."
		profile = PersonProfile(idPerson).get_profile()
		return render_template("people_profile.html", header = get_header(session),
													profile = profile, whoops = whoops)


# PERSON PROFILE
@app.route("/pessoas/perfil/<idWho>", methods=['GET'])
@login_required
def people_profile(idWho):
	""" Receives the person's id (idWho) and checks if the user is allowed to see
	that person's profile. This is an upgrade from the last version in which anyone could 
	see any person, even if the person wasn't part of the company. If that is the case an 
	alert is shown to the user. Otherwise the person's profile is returned."""
	idWho = validate_person_idwho(idWho, session['idCompany'])
	if idWho:
		profile = PersonProfile(idWho).get_profile()
		return render_template("people_profile.html", header = get_header(session),
													profile = profile)
	else:
		whoops = "Este perfil não existe, por favor selecione uma pessoa da lista."
		people_list = CompanyProfile(session["idCompany"]).get_people()
		return render_template("people_list.html", header = get_header(session), 
										people_list = people_list, whoops = whoops)


# EDIT PERSON BENEFITS
@app.route("/pessoas/editar/<idWho>", methods=['GET', 'POST'])
@login_required
def people_edit_benefits(idWho):
	""" It receives the person's id and checks if the user can edit that person's
	benefits. Then it proceeds in checking the list of benefits added and or excluded
	from the person's profile. If new data might be necessary (needs_data_check), it
	returns the people_register_data with a list of all combined data (new and current)
	for data input. Benefit_updated_data_types is only True when the benefit updates its
	list of data types and those data types don't match the person's data in the database,
	requiring new data inputs """
	idWho = validate_person_idwho(idWho, session['idCompany'])
	if idWho:
		if request.method == "POST":
			ids_benefits = str_list_to_int(request.form.getlist("idBenefit"))
			needs_data_check = update_person_benefits(idWho, ids_benefits)
			benefit_updated_data_types = request.form.get("force_update")
			if needs_data_check or benefit_updated_data_types:
				combined_data = get_combined_data_for_person(ids_benefits, idWho)
				return render_template("people_register_data.html", 
										combined_data = combined_data, 
										header = get_header(session),
										person_id = idWho)
			return redirect("/pessoas/perfil/{}".format(idWho))
		else: # 'GET'
			return render_template("people_edit_benefits.html", 
							header = get_header(session),
							profile = PersonProfile(idWho).get_profile(),
							benefits_list = CompanyProfile(session['idCompany']).get_benefits())
	else:
		whoops = "Este perfil não existe, por favor selecione uma pessoa da lista."
		people_list = CompanyProfile(session["idCompany"]).get_people()
		return render_template("people_list.html", header = get_header(session), 
									people_list = people_list, whoops = whoops)


# EDIT PERSON DATA
@app.route("/dados/editar/<idWho>", methods=['GET'])
@login_required
def people_edit_data(idWho):
	""" It receives the person's id and checks if the user can edit that person's
	data. Then it proceeds in getting a list of all data for that person 
	and returns the people_register_data page """
	idWho = validate_person_idwho(idWho, session['idCompany'])
	if idWho:
		person_data = PersonProfile(idWho).get_data()
		return render_template("people_register_data.html", 
								combined_data = person_data, 
								header = get_header(session),
								person_id = idWho)
	else: 
		whoops = "Este perfil não existe, por favor selecione uma pessoa da lista."
		people_list = CompanyProfile(session["idCompany"]).get_people()
		return render_template("people_list.html", header = get_header(session), 
								people_list = people_list, whoops = whoops)


# DELETE PERSON PROFILE
@app.route("/pessoas/deletar", methods=['POST'])
@login_required
def people_delete_profile():
	""" Receives (through form) the id of the person to be deleted. First the
	person id is checked and then deleted. The person's row in the person table,
	and all other data connected to that person is also deleted. """
	idPerson = str_to_int(request.form.get("idPerson"))
	person_admin = PersonProfile(idPerson).get_admin()
	if person_admin['name'] != "Admin":
		delete_person_profile(idPerson)
		return redirect("/pessoas/lista")
	else: 
		whoops = """Este perfil não pode ser deletado, por favor selecione outra pessoa 
					da lista."""
		people_list = CompanyProfile(session["idCompany"]).get_people()
		return render_template("people_list.html", header = get_header(session), 
								people_list = people_list, whoops = whoops)


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
	""" This function receives the user's cpf and checks it's values before 
	allowing them to login. There's no security measure implemented whatsoever. 
	If the cpf matches one of the admins, it proceeds to load all information 
	necessary on the session (dict) for further use regarding the user and 
	their company."""
	session.clear()
	if request.method == "POST":
		cpf = request.form.get("cpf")
		if not cpf:
			whoops = "Por favor insira seu CPF"
			return render_template("login.html", header = get_header(session),
												whoops = whoops)
		if not isCpfValid(cpf):
			whoops = "Número de CPF não válido"
			return render_template("login.html", header = get_header(session),
												whoops = whoops)
		person_id = get_person_id_by_cpf(cpf)
		if person_id is None:
			whoops = "Número de CPF não encontrado"
			return render_template("login.html", header = get_header(session),
												whoops = whoops)
		person_profile = PersonProfile(person_id).get_profile()
		if person_profile['admin']['level'] == 0:
			whoops = (person_profile['name'] + ", você não tem autorização para entrar no sistema")
			return render_template("login.html", header = get_header(session),
											whoops = whoops)
		company_name = CompanyProfile(person_profile['idCompany']).get_name()
		session["id"] = person_profile['id']
		session["name"] = person_profile['name']
		session["idCompany"] = person_profile['idCompany']
		session["company"] = company_name
		session["admin_name"] = person_profile['admin']['name']
		return redirect("/")
	else: # 'GET'
		return render_template("login.html", header = get_header(session))


@app.route("/logout")
def logout():
	""" Logs the user out and clears the flask session """
	session.clear()
	return redirect("/")


def apology(message, code=400):
    """ Render error message as a meme apology to user. """
    def escape(string):
        """
        Escape special characters for memegen.
        Created by Jace Browning:
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            string = string.replace(old, new)
        return string
    return render_template("apology.html", top = code, bottom = escape(message),
    										header = get_header(session)), code

def errorhandler(error):
    """ Handle errors """
    if not isinstance(error, HTTPException):
        error = InternalServerError()
    return apology(error.name, error.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == '__main__':
	""" Hello World! """
	secret_key = app.config.get("SECRET_KEY")
	app.run()


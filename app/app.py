from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps

from cpf import isCpfValid

'''
This is a webapp that manages employees' benefits.
For more visit https://github.com/leorapini/pipo_exercise
Code written by Leo Rapini

Names:
Person is every person registered in the database. 
Benefit is the name of any "benefício". Ex. Plano Dental Sorriso.
Company is an employer of of persons that have benefists registered to them,
allowing person to be enrolled in those benefits. 

Type of Data is the kind of data benefits require for someone to be enrolled.
Data is any value vinculated to a type of data. Ex. Type of Data: Nome or Peso.

Please check the SQL schema in the folder Documentation before reading the code. 
It will be a more pleasant experience, I promise. 
'''

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True 

# Set responses not to be cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Set sessions to use filesystem (not cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create database engine and session
engine = create_engine('sqlite:///db/pipo.db')
db = scoped_session(sessionmaker(bind=engine))

# Ensure the app is "refreshed" after every request
@app.teardown_request
def remove_session(ex=None):
    db.remove()



# UTILITIES
# UTILITIES
# UTILITIES
# Wrap to allow only logged users to see pages
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_admin_title(level):
	""" Receives admin level (int) and returns their respective description (str)."""
	if level == 1:
		headtitle = "Admin"
	else:
		headtitle = "Colaborador"
	return headtitle


def get_header(session):
	""" Receives session (dict) generated at login and returns the header (dict) 
	that will be used across the website"""
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


def is_it_bad(string):
	""" Receives data (str) that will be used in sql queries to protect 
	from SQL injection and other errors. Returns True or False"""
	if string is None:
		return True
	not_safe = "; \\ ' '' %"
	for letter in string:
		if letter in not_safe.split():
			return True
	return False

def it_isnt_id(may_be_id):
	""" Receives id number (int) that will be used in sql queries to protect 
	from SQL injection and other errors. Returns True or False"""
	if may_be_id is None:
		return True
	if not str(may_be_id).isdigit():
		return True
	return False



# GENERIC SQL QUERIES
# GENERIC SQL QUERIES
# GENERIC SQL QUERIES
def get_all_table(table):
	""" Receives name of table (str) and returns result of SQL 
	query (list)"""
	try:
		table_names = ["admin", "benefit", "benefitdata", "company", "companybenefit",
						"datatype", "person", "personbenefit", "persondata"]
		if table.lower() not in table_names:
			return None
		table_all = db.execute("""SELECT * FROM {}""".format(table)).fetchall()
		return table_all
	except:
		raise Exception("Undefined SQL query error")


def get_one_from(table, where, data):
	""" Receives name of table (str), condition (str) and data (str) and returns 
	result of fetchone() SQL query (list)"""
	try:
		table_names = ["admin", "benefit", "benefitdata", "company", "companybenefit",
						"datatype", "person", "personbenefit", "persondata"]
		if table.lower() not in table_names:
			return None
		if is_it_bad(where) or is_it_bad(data):
			return None
		one_from = db.execute("""SELECT * FROM {} WHERE {} = :{}""".format(table, 
							where, where), {"{}".format(where): data}).fetchone()
		return one_from
	except:
		raise Exception("Undefined SQL query error")


def get_all_from(table, where, data):
	""" Receives name of table (str), condition (str) and data (str) and returns 
	result of fetchall() SQL query (list)"""
	try:
		if (is_it_bad(table) or is_it_bad(where)) or is_it_bad(data):
			return None
		table_names = ["admin", "benefit", "benefitdata", "company", "companybenefit",
						"datatype", "person", "personbenefit", "persondata"]
		if table.lower() not in table_names:
			return None
		all_from = db.execute("""SELECT * FROM {} WHERE {} = :{}""".format(table, 
							where, where), {"{}".format(where): data}).fetchall()
		return all_from
	except:
		raise Exception("Undefined SQL query error")


def search_like(table, like):
	""" Receives name of table (str) and word-like (str) and returns result of 
	fetchall() SQL query (list)"""
	try:
		table_names = ["admin", "benefit", "benefitdata", "company", "companybenefit",
						"datatype", "person", "personbenefit", "persondata"]
		if table.lower() not in table_names:
			return None
		if is_it_bad(like):
			return None
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
	""" Receives name of name of person (str), cpf number (str) and list of benefits and 
	registers said person (insert in sql person table). Calls register_person_benefits 
	in case of any in the list. Returns person id (int)"""
	try:
		if (is_it_bad(name) or is_it_bad(cpf)):
			return None
		is_it_registered = get_one_from("person", "cpf", cpf)
		if is_it_registered is not None:
			return None
		db.execute("""INSERT INTO person (name, idCompany, cpf) 
						VALUES (:name, :idCompany, :cpf)""", 
						{"name": name, "idCompany": session["idCompany"], "cpf": cpf})
		db.commit()
		new_person = get_one_from("person", "cpf", cpf)
		if new_person is None:
			return None
		if benefits:
			register_person_benefits(benefits, new_person["id"])
		return new_person["id"]
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")


def register_person_benefits(benefits, idPerson):
	""" Receives list of benefits and person's id (int) and registers said person 
	(insert in sql perosonBenefit table) in every benefit on the list, if any. 
	Returns True"""
	try:
		if not benefits or it_isnt_id(idPerson):
			return None
		for benefit in benefits:
			db.execute("""INSERT INTO personBenefit (idPerson, idBenefit)
						VALUES (:idPerson, :idBenefit)""",
						{"idPerson": idPerson, "idBenefit": benefit})
		db.commit()
		return True
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")


# Confirma se dado já está cadastrado antes // dados vindos do formulário são type(str)
def register_person_data(idPerson, ids_datatype, data_values):
	""" Receives person's id (int), list of datatypes (types of data) and a list of 
	data values. Those values are necessary for enrollment in benefit plans. The list 
	is generated by the benefit's requirement for enrollment. Items in ids_datatype 
	are (str), therefore should be typecasted to (int) for comparisons. Returns True. """
	try:
		if it_isnt_id(idPerson) or (not ids_datatype or not data_values):
			return None
		registered_data = db.execute("""SELECT idDatatype FROM personData 
									WHERE idPerson = :idPerson""",
									{"idPerson": idPerson}).fetchall()
		if registered_data is None:
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
		return True
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")


def register_benefit(name):
	"""Receives name of new benefit (str) for registration (insert in sql benefit table). 
	It also registers the benefit with the current company which user is signed in at 
	the moment. It uses session['idCompany'] to get the company's id. Returns the new
	benefit's id (int)"""
	try:
		if name is None:
			return None
		benefits = get_all_table("benefit")
		if benefits is None:
			benefits = []
		for benefit in benefits:
			if benefit["name"].lower() == name.lower():
				return False
		db.execute("""INSERT INTO benefit (name) VALUES (:name)""", {"name": name})
		new_benefit = get_one_from("benefit", "name", name)
		if new_benefit is None:
			return None
		db.execute("""INSERT INTO companyBenefit (idCompany, idBenefit) 
					VALUES (:idCompany, :idBenefit)""", 
					{"idCompany": session["idCompany"], "idBenefit": new_benefit["id"]})
		db.commit()
		return new_benefit["id"]
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")


def register_datatype(name, example, idBenefit):
	"""Receives name of new type of data (str), example of type of data (str) and benefit's id,
	for registration (insert in sql datatype table). It also registers the type of data with 
	the benefit. Returns True."""
	try:
		if (not name or not example) or not idBenefit:
			return None
		datatypes = get_all_table("datatype")
		if datatypes is None:
			datatypes = []
		for datatype in datatypes:
			if datatype["name"].lower() == name.lower():
				return False
		db.execute("""INSERT INTO datatype (name, example) VALUES (:name, :example)""",
					{"name": name, "example": example})
		db.commit()
		new_datatype = get_one_from("datatype", "name", name)
		if new_datatype is None:
			return None
		db.execute("""INSERT INTO benefitData (idBenefit, idDatatype)
							VALUES (:idBenefit, :idDatatype)""",
							{"idBenefit": idBenefit, "idDatatype": new_datatype["id"]})
		db.commit()
		return True
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")


# DELETE QUERIES
# DELETE QUERIES
# DELETE QUERIES
def delete_person(idPerson):
	"""Receive's person's id (int) and deletes it from the database along all other
	data vinculated to that id. Returns nothing (void)"""
	try:
		if it_isnt_id(idPerson):
			return None
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
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")


def delete_benefit(idBenefit):
	"""Receive's benefit's id (int) and deletes it from the database along all other
	data vinculated to that id. Returns nothing (void)"""
	try:
		if it_isnt_id(idPerson):
			return None
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
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")



# UPDATE QUERIES
# UPDATE QUERIES
# UPDATE QUERIES
def update_benefit_data(idBenefit, ids_datatype):
	""" Receives a benefit's id (int) and a list of ids (int) of types of data (datatypes). 
	This function is called when benefits want to change the type of data they require
	for enrollment, this should be reflected in the database. This function first checks
	if any changes are necessary. Returns true."""
	try:
		if it_isnt_id(idBenefit):
			return None
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
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")


# Form data is type(str).
def update_person_benefits(idPerson, ids_benefit):
	""" Receives a person's id (int) and a list of ids of benefits (ids). 
	This function is called when a person is enrolling in new benefits or 
	unenrolling in current ones. This function first checksif any changes are 
	necessary. Returns true if a new plan was added so we can later get the
	new data necessary for enrollment. Returns false in case there's no new
	benefit enrollment."""
	try:
		if it_isnt_id(idPerson):
			return None
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
	except:
		raise Exception("Undefined SQL query error. Data may not been registered.")


# SEARCH QUERIES
# SEARCH QUERIES
# SEARCH QUERIES
def search_people(idCompany, like):
	""" Receives company's id (int) and name-like (str) to search for a person 
	with that name in a specific company. In the current system, as described in 
	the README, the company will always be the one recorded in session['company'], 
	but the function can get any other company in the database. Returns list of
	people."""
	try:
		if is_it_bad(like) or it_isnt_id(idCompany):
			return None

		people = db.execute("""SELECT * FROM person WHERE idCompany = :idCompany 
								AND name LIKE :name""", 
								{"name": '%'+like+'%', 
								"idCompany": idCompany}).fetchall()
		return people
	except:
		raise Exception("Undefined SQL query error")


def search_benefits(idCompany, like):
	""" Receives benefits's id (int) and name-like (str) to search for a benefit 
	with that name vinculated a specific company. In the current system, as described in 
	the README, the company will always be the one recorded in session['company'], 
	but the function can get benefits for any other company in the database.
	Returns list of benefits."""
	try:
		if it_isnt_id(idCompany) or is_it_bad(like):
			return None
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
	"""Receives person's profile (dict) and a list of ids of types of data to get
	each data in the list. Returns a list of dictionaries with the id, name and data 
	value"""
	try:
		all_data = []
		if not datalist or not profile:
			return None
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
	except:
		raise Exception("Undefined SQL query error")


def get_all_person_data(idPerson):
	""" Receives a person's id (int) and returns a list of all data found on personData 
	table with name, id and data. It's similar to get_person_data() but this one doesn't
	require a list of datatypes. Returns a list with the data."""
	try:
		if it_isnt_id(idPerson):
			return None
		all_data = db.execute("""SELECT name, idDatatype, data 
								FROM personData JOIN datatype ON idDatatype = id
								WHERE idPerson = :idPerson""",
								{"idPerson": idPerson}).fetchall()
		return all_data
	except:
		raise Exception("Undefined SQL query error")

def get_data_example(idDatatype):
	""" Receives a type of data's id (int) and returns the value o that type of data
	(str or int). This function shouldn't exist, but someone (read me) only thought 
	about adding examples to the datatypes later on. Therefore this is a quick fix. :)"""
	try:
		if it_isnt_id(idDatatype):
			return None
		data_example = db.execute("""SELECT example FROM datatype WHERE id = :id""",
								{"id": idDatatype}).fetchone()
		if data_example is None:
			return None
		return data_example[0]
	except:
		raise Exception("Undefined SQL query error")


def get_data(idPerson, idDatatype):
	""" Receives a person's id (int) and an id for a type of data and returns that data
	(int or str) """
	try:
		if it_isnt_id(idPerson) or it_isnt_id(idDatatype):
			return None
		person_data = db.execute("""SELECT data FROM personData WHERE idPerson = :idPerson
								AND idDatatype = :idDatatype""",
								{"idPerson": idPerson, "idDatatype": idDatatype}).fetchone()
		if person_data is None: 
			return None 
		else:
			return person_data[0]
	except:
		raise Exception("Undefined SQL query error")


def get_person_benefits(idPerson):
	""" Recebices a person's id and returns a list of all benefits vinculated to 
	that person """
	try:
		if it_isnt_id(idPerson):
			return None
		benefits = db.execute("""SELECT id, name FROM benefit WHERE id  
							IN (SELECT idBenefit FROM personBenefit 
							WHERE idPerson = :idPerson)
							ORDER BY name""", {"idPerson": idPerson}).fetchall()
		return benefits
	except:
		raise Exception("Undefined SQL query error")


def get_profile(idPerson):
	""" Receives a person's id (int) and returns their profile (dict) with all
	their information.""" 
	try:
		if it_isnt_id(idPerson):
			return None
		person = get_one_from("person", "id", str(idPerson))
		benefits = get_person_benefits(idPerson)
		personData = get_all_person_data(idPerson)
		if person is None:
			return None
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
	except:
		raise Exception("Undefined SQL query error")


def get_company_benefits(idCompany):
	""" Receives a company's id (int) and returns a list of all benefits 
	vinculated to that company """
	try:
		if it_isnt_id(idCompany):
			return None
		benefits = db.execute("""SELECT id, name FROM benefit WHERE id 
								IN (SELECT idBenefit FROM companyBenefit 
								WHERE idCompany = :idCompany)
								GROUP BY name ORDER BY name""", 
								{"idCompany": idCompany}).fetchall()
		return benefits
	except:
		raise Exception("Undefined SQL query error")


def get_benefits_data(benefits):
	""" Receives a list of benefits and returns a list of all types of data 
	vinculated to those benefits. It is called when a person is registering 
	for a new benefit."""
	try:
		all_data = []
		if benefits is None:
			return None
		for idBenefit in benefits:
			benefits_data = db.execute("""SELECT id, name FROM datatype WHERE id IN
									(SELECT idDatatype FROM benefitData 
									WHERE idBenefit = :idBenefit)""",
									{"idBenefit": idBenefit}).fetchall()
			for data in benefits_data:
				if (data["id"],data["name"]) not in all_data:
					all_data.append((data["id"],data["name"]))
		return all_data
	except:
		raise Exception("Undefined SQL query error")


def get_benefit_profile(idBenefit):
	""" Receives a benefit's id (int) and returns it's profile (dict) with all
	their information."""
	try:
		if it_isnt_id(idBenefit):
			return None
		benefit = get_one_from("benefit", "id", str(idBenefit))
		if benefit is None:
			return None
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
	except:
		raise Exception("Undefined SQL query error")


def get_admission_date(idPerson, idBenefit):
	""" Receives a person's id (int) and a benefit's id (int) and returns the date (str) of
	when the person enrolled in that benefit. Look how beautifully implemented 
	was the formatting of the date :)"""
	try:
		if it_isnt_id(idPerson) or it_isnt_id(idBenefit):
			return None
		date = db.execute("""SELECT timestamp FROM personBenefit WHERE idPerson = :idPerson
							AND idBenefit = :idBenefit""", {"idPerson": idPerson, 
							"idBenefit": idBenefit}).fetchone()
		if date is None:
			return None
		formated = date[0][0:10]
		return formated
	except:
		raise Exception("Undefined SQL query error")


# INDEX
# INDEX
# INDEX
@app.route("/", methods=['GET'])
@login_required
def index():
	""" Returns index.html with header information """
	return render_template("index.html", header = get_header(session))


# HOME
@app.route("/<who>", methods=['GET'])
@login_required
def home(who):
	""" Returns home.html with header and who in case of pesssoas e beneficios.
	This was done so I didn't have to create a html file for each page. Thank you Jinja2!"""
	if who not in ['pessoas', 'beneficios']:
		whoops = "Página Inexistente"
		return render_template("index.html", header = get_header(session), whoops = whoops)
	return render_template("home.html", header = get_header(session), who = who)


# LIST
@app.route("/<who>/lista", methods=['GET'])
@login_required
def list(who):
	""" Returns a list of all people or benefits, depending on who 'who' is. """
	if who == "beneficios":
		who_list = get_company_benefits(session["idCompany"])
	elif who == "pessoas":
		who_list = get_all_from("person", "idCompany", str(session["idCompany"]))
	else:
		whoops = "Página Inexistente"
		return render_template("index.html", header = get_header(session), whoops = whoops)
	return render_template("list.html", header = get_header(session), who = who,
										who_list = who_list)


# SEARCH
@app.route("/<who>/busca", methods=['GET', 'POST'])
@login_required
def search(who):
	""" If 'GET' returns the search page, if 'POST' returns the result of that search for 
	both People and Benefits """
	if request.method == "POST":
		name = request.form.get("name")
		if not name:
			whoops = "Por favor insira um nome"
			return render_template("search.html", header = get_header(session), 
												who = who, whoops = whoops)
		if who == "beneficios":
			who_list = search_benefits(session["idCompany"], name)
		elif who == "pessoas":
			who_list = search_people(session["idCompany"], name)
		else:
			whoops = "Página Inexistente"
			return render_template("index.html", header = get_header(session), whoops = whoops)
		return render_template("searchresult.html", header = get_header(session),
													who = who,who_list = who_list)
	else:
		return render_template("search.html", header = get_header(session), 
												who = who)


# REGISTRATION
@app.route("/<who>/cadastro", methods=['GET', 'POST'])
@login_required
def registration(who):
	""" This is a complicated one but in summary it is the registration function/router for both
	benefits and people. I suggest first reading the bottom part of the function with the 'else' 
	bellow if request.. That is the 'GET', what is loaded before any form is submitted. On the
	person registration part, in POST, it receives the information and checks it before calling
	all other functions necessary for a complete registration. Once that it occurs successfully,
	it returns the form for additional data to be inputed."""
	if request.method == "POST":
		name = request.form.get("name")
		if who == "beneficios":
			if not name:
				whoops = "Por favor insira um nome"
				return render_template("registration.html", 
									header = get_header(session), who = who,
									whoops = whoops)
			idBenefit = register_benefit(name)
			if idBenefit:
				return redirect("/{}/perfil/{}".format(who, idBenefit))
			else:
				whoops = "Erro no cadastro. Talvez esse benefício já esteja cadastrado."
				return render_template("registration.html", header = get_header(session), 
									who = who, whoops = whoops)
		elif who == "pessoas":
			company_benefits = get_company_benefits(session["idCompany"])
			if not name:
				whoops = "Por favor insira um nome"
				return render_template("registerperson.html", 
									header = get_header(session), who = who,
									benefits = company_benefits, whoops = whoops)
			cpf = request.form.get("cpf")
			if not cpf or not isCpfValid(cpf):
				whoops = "Por favor insira o número de cpf corretamente"
				return render_template("registerperson.html", 
									header = get_header(session), who = who,
									benefits = company_benefits, whoops = whoops)
			chosen_benefits = request.form.getlist("benefits")
			idPerson = register_person(name, cpf, chosen_benefits)
			if idPerson: 
				if chosen_benefits:
					profile = get_profile(idPerson)
					benefits_data = get_benefits_data(chosen_benefits)
					person_data = get_person_data(profile, benefits_data)
					return render_template("registerpersondata.html",
										header = get_header(session),
										profile = profile,
										person_data = person_data)
				return redirect("/{}/lista".format(who))
			else:
				whoops = "Erro no cadastro. Por favor confira já o cadastro já não foi feito."
				return render_template("registerperson.html", header = get_header(session), 
									who = who, benefits = company_benefits, whoops = whoops)
		else:
			whoops = "Página Inexistente"
			return render_template("index.html", header = get_header(session), whoops = whoops)
	else:
		if who == "pessoas":
			company_benefits = get_company_benefits(session["idCompany"])
			return render_template("registerperson.html", 
									header = get_header(session), who = who,
									benefits = company_benefits)
		elif who == "beneficios":
			return render_template("registration.html", 
									header = get_header(session), who = who)
		else:
			whoops = "Página Inexistente"
			return render_template("index.html", header = get_header(session), whoops = whoops)


# REGISTER PERSON DATA
@app.route("/pessoas/cadastro/beneficio", methods=['POST'])
@login_required
def regiterpersondata():
	""" This function simply registers the aditional data for person
	submitted by calling register_person_data() and returns the persons profile """
	idPerson = request.form.get("idPerson")
	ids_datatype = request.form.getlist("idDatatype")
	data_values = request.form.getlist("data_value")
	if ids_datatype and data_values:
		register_person_data(idPerson, ids_datatype, data_values)
		return redirect("/pessoas/perfil/{}".format(idPerson))
	else:
		return redirect("/pessoas/lista")


# REGISTER NEW DATATYPE
@app.route("/beneficios/cadastro/dado/<idWho>", methods=['GET','POST'])
@login_required
def registernewdatatype(idWho):
	""" This function registers new types of data and returns the benefits 
	profile aka idWho"""
	if it_isnt_id(idWho):
		return redirect("/")
	if request.method == "POST":
		data_list = get_all_table("datatype")
		name = request.form.get("name")
		example = request.form.get("example")
		if not name or not example:
			whoops = "Você precisa preencher os dois campos"
			return render_template("registernewdatatype.html", 
											header = get_header(session),
											data_list = data_list,
											idWho = idWho, whoops = whoops)
		if register_datatype(name, example, idWho):
			return redirect("/beneficios/perfil/{}".format(idWho))
		else:
			whoops = "Houve um erro no cadastro, por favor tente novamente"
			return render_template("registernewdatatype.html", 
											header = get_header(session),
											data_list = data_list,
											idWho = idWho, whoops = whoops)
	else:
		data_list = get_all_table("datatype")
		return render_template("registernewdatatype.html", 
											header = get_header(session),
											data_list = data_list,
											idWho = idWho)



# PROFILES
@app.route("/<who>/perfil/<idWho>", methods=['GET'])
@login_required
def profile(who, idWho):
	""" Receives id (idWho) and who (Person or Benefit) and loads it's profile page"""
	if it_isnt_id(idWho):
		return redirect("/")
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



# BENEFIT REGISTRATION INFORMATION (PROFILE)
@app.route("/beneficios/<idBenefit>/pessoas/<idPerson>", methods=['GET'])
@login_required
def benefitformprofile(idBenefit, idPerson):
	""" Receives idBenefit and idPerson to show the persons registration form
	(ficha de cadastro) with the information necessary to send over to the 
	benefit provider """
	if not idBenefit.isdigit() or not idPerson.isdigit():
		whoops = "Perfil ou página não encontrado"
		return render_template("index.html", header = get_header(session),
								whoops = whoops)
	benefit_profile = get_benefit_profile(idBenefit)
	person_profile = get_profile(idPerson)
	if not benefit_profile or not person_profile:
		whoops = "Perfil ou página não encontrado"
		return render_template("index.html", header = get_header(session),
								whoops = whoops)
	admission_date = get_admission_date(idPerson, idBenefit)
	if not admission_date:
		admission_date = "Erro no cadastro."
	return render_template("benefitformprofile.html", header = get_header(session),
												benefit = benefit_profile,
												person = person_profile,
												admission_date = admission_date)



# EDIT PROFILES
@app.route("/<who>/editar/<idWho>", methods=['GET', 'POST'])
@login_required
def editprofile(who, idWho):
	""" This is another complicated one, and in another time, could be refactored 
	into smaller functions. It receives who (benefit or person) and idWho (it's id),
	then it proceeds in checking the values before calling other functions to
	update its profile """
	if it_isnt_id(idWho):
		return redirect("/")
	if request.method == "POST":
		if who == "pessoas":
			profile = get_profile(idWho)
			if not profile:
				whoops = "Este perfil não existe."
				return render_template("list.html", who = who,
						header = get_header(session), whoops = whoops)
			ids_benefit = request.form.getlist("idBenefit")
			force_update = request.form.get("force_update")
			updated = update_person_benefits(idWho, ids_benefit)
			if updated or force_update:
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
				whoops = "Você não pode eliminar todos os dados"
				return render_template("list.html", header = get_header(session),
										whoops = whoops, who = who)
			if update_benefit_data(idWho, ids_datatype):
				return redirect("/beneficios/perfil/{}".format(idWho))
			else:
				whoops = "Erro na atualização do perfil."
				return render_template("list.html", header = get_header(session),
										whoops = whoops, who = who)
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
				whoops = "Esse perfil não existe"
				return render_template("list.html", header = get_header(session),
										whoops = whoops, who = who)
			return render_template("editbenefit.html", header = get_header(session),
									profile = profile, who = who, 
									data_list = get_all_table("datatype"))
		else:
			return redirect("/pessoas/lista")

# DELETE PROFILE
@app.route("/<who>/deletar", methods=['POST'])
@login_required
def deleteprofile(who):
	""" Receives who (pessoas or beneficios) and call a function to delete it's profile
	and data from the database. That's why it's at the end of the code. """
	if request.method == "POST":
		if who == "pessoas":
			idPerson = request.form.get("idPerson")
			if idPerson:
				delete_person(idPerson)
			return redirect("/{}/lista".format(who))
		elif who == "beneficios":
			idBenefit = request.form.get("idBenefit")
			if idBenefit:
				delete_benefit(idBenefit)
			return redirect("/{}/lista".format(who))
		else:
			return redirect("/")




# LOGIN
# Login autorizado somente para administradores cadastrados
@app.route("/login", methods=["GET", "POST"])
def login():
	""" The beginning at the end. Who knew! This function receives the user's
	cpf and checks it's values before allowing them to login. There's no 
	security measure implemented whatsoever. If the cpf matches one of the 
	admins, it proceeds to load all information necessary on the session (dict)
	for further use regarding the user and their company."""
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
		person = get_one_from("person", "cpf", cpf)
		if person is None:
			whoops = "Número de CPF não encontrado"
			return render_template("login.html", header = get_header(session),
												whoops = whoops)
		else:
			admin = get_one_from("admin", "idPerson", str(person["id"]))
			if admin is None:
				whoops = "Você não está autorizado a entrar no sistema"
				return render_template("login.html", header = get_header(session),
												whoops = whoops)
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
	""" Hello World! """
	app.secret_key='secret123'
	app.run()

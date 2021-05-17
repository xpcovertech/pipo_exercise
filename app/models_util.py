from db import *
from utils import is_int, is_string, isCpfValid, str_list_to_int
from datetime import datetime

from models_company import CompanyProfile
from models_benefit import BenefitProfile
from models_person import PersonProfile

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

'''
models_util.py

Assorted funcions that that are used to combine data retrieved from the 
database and return results to the routes in app.py. 
'''

def get_available_data_types_for_benefit(idBenefit):
	""" Receives a Benefit id and returns all data types
	not currently registered with that Benefit"""
	if not benefit_exists(idBenefit):
		raise Exception
	all_data_types = query_all_data_types()
	benefit_data_types = query_benefit_data_types(idBenefit)
	available_data_types = []
	for data_type in all_data_types:
		if data_type not in benefit_data_types:
			available_data_types.append(data_type)
	return available_data_types


def register_new_benefit(benefit_name, idCompany):
	""" Receives a new benefit name and a company id (the current
	user's company id) and returns the new benefit id. It checks
	the validity of the information and if the new benefit is already
	registered in the database with that company. """
	if not is_string(benefit_name) or not company_exists(idCompany):
		raise TypeError
	benefit_check = query_benefit_id_by_name(benefit_name)
	if len(benefit_check) > 0:
		if validate_benefit_idwho(benefit_check[0]['id'], idCompany):
			return None
	else:
		insert_benefit(benefit_name)
	new_benefit = query_benefit_id_by_name(benefit_name)
	if len(new_benefit) == 0:
		raise Exception("Registration failed")
	add_new_benefit_to_company(new_benefit[0]['id'], idCompany)
	return new_benefit[0]['id']


def add_new_benefit_to_company(idBenefit, idCompany):
	""" Receives an already registered Benefit id and registers it
	with the company. Returns <void> """
	if not benefit_exists(idBenefit) or not company_exists(idCompany):
		raise Exception("Company id and/or benefit id are incorrect")
	company_benefits = query_company_benefits(idCompany)
	for c_benefit in company_benefits:
		if c_benefit['id'] == idBenefit:
			raise Exception("This benefit is already registered to this company")
	insert_benefit_to_company(idBenefit, idCompany)


def register_new_data_type(datatype_name, datatype_example, idBenefit):
	""" Receives a new type of data along with it's example and a Benefit id.
	It adds the new type of data to the database and registers it with the
	Benefit. Returns <void> """
	if (not is_string(datatype_name) or not is_string(datatype_example) 
		or not benefit_exists(idBenefit)):
			raise TypeError
	datatype_check = query_data_type_id_by_name_like(datatype_name)
	if len(datatype_check) > 0:
		raise Exception("This data type is already registered")
	insert_data_type(datatype_name, datatype_example)
	new_datatype = query_data_type_id_by_name(datatype_name)
	if len(new_datatype) == 0:
		raise Exception("Registration failed")
	add_new_data_type_to_benefit(new_datatype[0]['id'], idBenefit)


def add_new_data_type_to_benefit(idDatatype, idBenefit):
	""" Receives an already registered Datatype id and a Benefit id and 
	registers it with the Benefit. Returns <void>"""
	if not benefit_exists(idBenefit) or not datatype_exists(idDatatype):
		raise Exception
	available_data_types = get_available_data_types_for_benefit(idBenefit)
	new_data_type = query_datatype_details(idDatatype)
	if new_data_type[0] not in available_data_types:
		raise Exception("This data type is already registered with the benefit")		
	insert_data_type_to_benefit(idDatatype, idBenefit)


def delete_benefit_profile(idBenefit, idCompany):
	""" Receives a Benefit id and a company's id and 'deletes' benefit from 
	company profile. It doesn't delete the Benefit from the database, 
	for it might still be used by other companies. Returns <void>"""
	if not benefit_exists(idBenefit):
		raise Exception
	company_benefit_people = query_benefit_people_by_company(idBenefit, idCompany)
	if len(company_benefit_people) > 0:
		for person in company_benefit_people:
			delete_person_from_benefit(person['id'], idBenefit)
	delete_company_from_benefit(idCompany, idBenefit)


def remove_data_type_from_benefit(idDatatype, idBenefit):
	""" Receives a Data Type id and a Benefit id and deletes the data type
	from the Benefit's profile. Returns <void> """
	if not benefit_exists(idBenefit) or not datatype_exists(idDatatype):
		raise Exception
	current_data_types = query_benefit_data_types(idBenefit)
	current_data_type = query_datatype_details(idDatatype)
	if current_data_type[0] not in current_data_types:
		raise Exception("This data type has not yet been added to the benefit yet")
	delete_data_type_from_benefit(idDatatype, idBenefit)


def register_new_person(person_name, person_cpf, idCompany):
	""" Receives a new person's name and cpf and a company id (the current users
	company). It registers the new person with the company's id and 
	returns the new person's id """
	if not is_string(person_name) or not company_exists(idCompany):
		raise TypeError
	if not isCpfValid(person_cpf):
		raise Exception("CPF is not valid")
	person_check = query_person_id_by_cpf(person_cpf)	
	if len(person_check) > 0:
		raise Exception("This CPF number is already registered")
	insert_person(person_name, person_cpf, idCompany)
	new_person = query_person_id_by_cpf(person_cpf)
	if len(new_person) == 0:
		raise Exception("Registration failed")
	return new_person[0]['id']

def register_person_to_benefit(idPerson, idBenefit):
	""" Receives a person's id and a benefit's id and registers the person
	with the benefit. Returns <void> """
	if not person_exists(idPerson) or not benefit_exists(idBenefit):
		raise Exception
	person_is_registered_to_benefit = query_person_one_benefit(idPerson, idBenefit)
	if len(person_is_registered_to_benefit) > 0:
		raise Exception("Person is already registered to benefit")
	insert_person_to_benefit(idPerson, idBenefit)
	person_is_registered_to_benefit = query_person_one_benefit(idPerson, idBenefit)
	if len(person_is_registered_to_benefit) == 0:
		raise Exception("Registration failed")

def register_data_to_person(idDatatype, data, idPerson):
	""" Reveives a data type id, the related data and a person id and registers 
	the data for that person. Before, it checks if the datatype id is a reserved 
	data type (Name, CPF or Admission Date) and checks if that data type has already
	been registered (for those cases, another function 'update_data_from_person()'
	should be used). Returns <void> """
	if not person_exists(idPerson) or not datatype_exists(idDatatype):
		raise Exception
	if not is_string(data):
		raise TypeError
	reserved_data_types_ids = [1, 2, 3]
	if idDatatype in reserved_data_types_ids:
		raise Exception("You can't add a new name, cpf or admission date")
	data_is_registered = query_person_one_data(idPerson, idDatatype)
	if len(data_is_registered) > 0:
		raise Exception("This data has already been registered")
	insert_data_to_person(idDatatype, data, idPerson)
	data_is_registered = query_person_one_data(idPerson, idDatatype)
	if len(data_is_registered) == 0:
		raise Exception("Registration failed")

def update_data_from_person(idDatatype, new_data, idPerson):
	""" Reveives a data type id, the related data and a person id and it updates 
	the data for that person. Before, it checks if the datatype id is a reserved 
	data type (Name, CPF or Admission Date) and checks if that data type has NOT 
	been registered (for those cases, another function 'register_data_to_person()'
	should be used). Returns <void> """
	if not person_exists(idPerson) or not datatype_exists(idDatatype):
		raise Exception
	if not is_string(new_data):
		raise TypeError
	reserved_data_types_ids = [1, 2, 3]
	if idDatatype in reserved_data_types_ids:
		raise Exception("You can't update a name, cpf or admission date")
	data_is_registered = query_person_one_data(idPerson, idDatatype)
	if len(data_is_registered) == 0:
		raise Exception("This data has not been registered yet")
	update_person_data(data_is_registered[0]['id'], new_data)


def remove_person_from_benefit(idPerson, idBenefit):
	""" Receives a person's id and a benefit's id and removes the person from
	that benefit. Returns <void> """
	if not person_exists(idPerson) or not benefit_exists(idBenefit):
		raise Exception
	person_is_registered_to_benefit = query_person_one_benefit(idPerson, idBenefit)
	if len(person_is_registered_to_benefit) == 0:
		raise Exception("Person has not been registered to benefit")
	delete_person_from_benefit(idPerson, idBenefit)
	person_deleted_from_benefit = query_person_one_benefit(idPerson, idBenefit)
	if len(person_deleted_from_benefit) != 0:
		raise Exception("Deletion failed")

def delete_person_profile(idPerson):
	""" Receives a person's id and deletes ALL data related to that person 
	from the database. Returns <void> """
	if not person_exists(idPerson):
		raise Exception
	all_person_data = query_person_data_get_persondata_id(idPerson)
	if len(all_person_data) > 0:
		for person_data in all_person_data:
			delete_data_with_persondata_id(person_data['id'])
	all_person_benefits = query_person_benefits(idPerson)
	if len(all_person_benefits) > 0:
		for benefit in all_person_benefits:
			delete_person_from_benefit(idPerson, benefit['id'])
	delete_person_from_person_table(idPerson)
	person_deleted = query_person_name_idcompany_cpf(idPerson)
	if len(person_deleted) != 0:
		raise("Deletion failed")


def get_person_id_by_cpf(person_cpf):
	""" Receives a valid CPF number in the correct format and returns the person's
	id. In case the cpf has not been registered in the database, it returns None"""
	person_id = query_person_id_by_cpf(person_cpf)
	if len(person_id) > 0:
		return person_id[0]['id']
	else:
		return None

def search_person_by_name_by_company(person_name, idCompany):
	""" Receives a person's name and a company ID and returns a list of
	dictionaries of people registered with that company with a similar name.
	Ex. person_name = "Alex", Results = [{"idPerson": 4, "name": "Alexandre Santana"}, 
	{"idPerson": 7, "name": "Alexsandro Gonçalves"}] """
	results = query_person_name_like_by_company(person_name, idCompany)
	return results

def search_benefit_by_name_by_company(benefit_name, idCompany):
	""" Receives a benefit's name and a company ID and returns a list of
	dictionaries of benefits registered with that company with a similar name. 
	Ex. person_name = "Dental",
	Results = [{"idBenefit": 2, "name": "Plano Dental Sorriso"}, 
	{"idBenefit": 1, "name": "Programa Dental de Saúde Amaranto"}] """
	results = query_benefit_name_like_by_company(benefit_name, idCompany)
	return results

def get_person_one_data(idPerson, idDatatype):
	""" Receives a person's id and a data type id and returns the exact data value
	related to that person id and that datatype id. Returns string."""
	results = query_person_one_data(idPerson, idDatatype)
	if len(results) == 0:
		return None
	else:
		return results[0]['data']

def get_combined_data_for_person(chosen_benefits, new_person_id):
	""" This is a tricky one. Receives a list of benefit ids and a person's
	id and returns a list of dictionaries with the combined information
	(data types) between benefits and person. Reserved data types such as
	name, cpf and data admissão are treated differently according """
	all_benefits_data = []
	for benefit_id in chosen_benefits:
		benefit_data = BenefitProfile(benefit_id).get_data_types()
		for data_type in benefit_data:
			if data_type not in all_benefits_data:
				all_benefits_data.append(data_type)
	person_profile = PersonProfile(new_person_id).get_profile()
	combined_data = []
	for data_type in all_benefits_data:
		if data_type['name'] == 'Nome':
			combined_data.append({'idDatatype': data_type['idDatatype'], 
			'name': data_type['name'], 
			'data': person_profile['name'],
			'example': data_type['example']})
		elif data_type['name'] == 'CPF':
			combined_data.append({'idDatatype': data_type['idDatatype'], 
			'name': data_type['name'], 
			'data': person_profile['cpf'],
			'example': data_type['example']})
		elif data_type['name'] == 'Data Admissão':
			combined_data.append({'idDatatype': data_type['idDatatype'], 
			'name': data_type['name'], 
			'data': data_type['example'],
			'example': data_type['example']})
		else:
			combined_data.append({'idDatatype': data_type['idDatatype'], 
			'name': data_type['name'], 
			'data': get_person_one_data(new_person_id, data_type['idDatatype']),
			'example': data_type['example']})
	return (combined_data)


def update_person_benefits(idPerson, ids_benefit):
	""" Receives a person's id and a list of ids of benefits. 
	This function is called when a person is enrolling in new benefits or 
	unenrolling in current ones. This function first checks if any changes are 
	necessary. Returns true if a new benefit was added so we can later get the
	new data necessary for enrollment. Returns false in case there's no new
	benefit enrollment, and True if there is."""
	if not person_exists(idPerson):
		raise Exception("Person doesn't exist")
	flag = 0
	current_benefits = PersonProfile(idPerson).get_benefits()
	submitted_benefits = []
	if len(ids_benefit) > 0:
		for id_benefit in ids_benefit:
			submitted_benefits.append({"idBenefit": id_benefit, 
							"name": BenefitProfile(id_benefit).get_name()})
	# Check if person had benefits and got them all taken away
	if len(submitted_benefits) == 0 and len(current_benefits) > 0:
		for benefit in current_benefits:
			remove_person_from_benefit(idPerson, benefit['idBenefit'])
	else:
		for benefit in submitted_benefits:
			if benefit in current_benefits:
				pass
			elif benefit not in current_benefits:
				register_person_to_benefit(idPerson, benefit['idBenefit'])
				flag = 1
		for current_benefit in current_benefits:
			if current_benefit not in submitted_benefits:
				remove_person_from_benefit(idPerson, current_benefit['idBenefit'])
	if flag == 1:
		return True
	else:
		return False


def update_benefit_data_types(idBenefit, ids_datatypes):
	""" Receives a benefit's id and a list of ids of types of data (datatypes). 
	This function is called when benefits want to change the type of data they require
	for enrollment, this should be reflected in the database. This function first checks
	if any changes are necessary. Returns <void>"""
	if not benefit_exists(idBenefit):
		raise Exception("Benefit doesn't exist")
	current_data_types = BenefitProfile(idBenefit).get_data_types()
	submitted_data_types = []
	if len(ids_datatypes) > 0:
		for id_datatype in ids_datatypes:
			datatype = query_datatype_details(id_datatype)
			submitted_data_types.append({"idDatatype": id_datatype,
										"name": datatype[0]['name'], 
										"example": datatype[0]['example']})
	# Check if benefit had datatypes and got them all taken away
	if len(submitted_data_types) == 0 and len(current_data_types) > 0:
		for data_type in current_data_types:
			remove_data_type_from_benefit(data_type['idDatatype'], idBenefit)
	else:
		for data_type in submitted_data_types:
			if data_type in current_data_types:
				pass
			elif data_type not in current_data_types:
				add_new_data_type_to_benefit(data_type['idDatatype'], idBenefit)
		for data_type in current_data_types:
			if data_type not in submitted_data_types:
				remove_data_type_from_benefit(data_type['idDatatype'], idBenefit)


def get_all_data_types():
	""" Receives <void> and returns a list of dictionaries with all types of data
	registered in the database Ex. [{'idDatatype': 1, "name": "Nome", 
	"example": "Ex. João Fernando Farias"}] """
	results = query_all_data_types()
	return results

def get_person_admission_date(idPerson, idBenefit):
	""" Receives a person's id and a benefit's id and returns the date (str) of
	when the person enrolled in that benefit. """
	date = query_person_admission_date(idPerson, idBenefit)
	if date is None:
		raise Exception("Couldn't find the date")
	date = date[0]
	formated = date.strftime("%d/%m/%Y")
	return formated

def validate_registration_card(idBenefit, idPerson, idCompany):
	""" Receives a benefit's id, a person's id and a company's id and returns True
	if the person is registered with the company and if the person is registered with
	the benefit. Returns None otherwise."""
	try:
		idBenefit = int(idBenefit)
		idPerson = int(idPerson)
		if query_person_in_company(idPerson, idCompany):
			if query_person_admission_date(idPerson, idBenefit):
				return True
		return None
	except:
		return None

def validate_person_idwho(idWho, idCompany):
	""" Receives a person's id (idWho) as a string and a company id (int) and returns 
	that person's id as an int if the person is registered with the company. Returns 
	None otherwise. This function is called in the beginning of most routes in order to
	also check if a number was entered in the address bar. """
	try:
		idWho = int(idWho)
		results = query_person_in_company(idWho, idCompany)
		if results is None:
			return None
		else:
			return idWho
	except:
		return None

def validate_benefit_idwho(idWho, idCompany):
	""" Receives a benefit's id (idWho) as a string and a company id (int) and returns 
	that benefit's id as an int if the benefit is registered with the company. Returns 
	None otherwise. This function is called in the beginning of most routes in order to
	also check if a number was entered in the address bar. """
	try:
		idWho = int(idWho)
		results = query_benefit_in_company(idWho, idCompany)
		if results is None:
			return None
		else:
			return idWho
	except:
		return None

def data_types_exist(ids_datatypes):
	""" Receives a list of strings/chars of ids of datatypes and returns a list of ints
	of the same data types. Ex. ["1", "2", "3"] -> [1, 2, 3] This function is called
	when forms are submitted in the routes to both validate the id numbers and to
	convert the ids from string/char to ints """
	if len(ids_datatypes) == 0:
		return []
	ids_datatypes = str_list_to_int(ids_datatypes)
	if not ids_datatypes:
		return None
	for datatype in ids_datatypes:
		if datatype_exists(datatype):
			pass
		else:
			return None
	return ids_datatypes



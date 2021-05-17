from utils import is_int

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

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
db.py

SQLAlchemy ORM implementation for SQLite database. Except when noted otherwise
all functions return a list of dictionaries or an empty dictionary.
'''

engine = create_engine('sqlite:///db/pipo.db')
Base = declarative_base()
Base.metadata.reflect(engine)
db = scoped_session(sessionmaker(bind=engine))

class Company(Base):
	__table__ = Base.metadata.tables['company']

class Person(Base):
	__table__ = Base.metadata.tables['person']

class Admin(Base):
	__table__ = Base.metadata.tables['admin']

class Benefit(Base):
	__table__ = Base.metadata.tables['benefit']

class Datatype(Base):
	__table__ = Base.metadata.tables['datatype']

class BenefitData(Base):
	__table__ = Base.metadata.tables['benefitData']

class PersonBenefit(Base):
	__table__ = Base.metadata.tables['personBenefit']

class PersonData(Base):
	__table__ = Base.metadata.tables['personData']

class CompanyBenefit(Base):
	__table__ = Base.metadata.tables['companyBenefit']


# COMPANY QUERIES
# COMPANY QUERIES
def company_exists(idCompany):
	""" Receives a company id and returns True if the company exists
	and False if it doesn't """
	if not is_int(idCompany):
			raise TypeError
	results = (db.query(Company.id)
				.filter(Company.id == idCompany).all())
	if len(results) == 1:
		return True
	elif len(results) > 1:
		raise Exception("Database is compromised")
	else:
		return False

def query_company_name(idCompany):
	results = (db.query(Company.id, Company.name)
				.filter(Company.id == idCompany).all())
	return results

def query_company_people(idCompany):
	results = (db.query(Person.id, Person.name)
				.filter(Person.idCompany == idCompany)
				.order_by(Person.name).all())
	return results

def query_company_benefits(idCompany):
	results = (db.query(Benefit.id, Benefit.name)
				.filter(Benefit.id == CompanyBenefit.idBenefit)
				.filter(CompanyBenefit.idCompany == idCompany)
				.order_by(Benefit.name).all())
	return results



# PERSON QUERIES
# PERSON QUERIES
def person_exists(idPerson):
	""" Receives a person id and returns True if the person exists
	and False if it doesn't """
	if not is_int(idPerson):
			raise TypeError
	results = (db.query(Person.id)
				.filter(Person.id == idPerson).all())
	if len(results) == 1:
		return True
	elif len(results) > 1:
		raise Exception("Database is compromised")
	else:
		return False

def query_person_name_idcompany_cpf(idPerson):
	results = (db.query(Person.id, Person.name, Person.idCompany, Person.cpf)
				.filter(Person.id == idPerson).all())
	return results

def query_person_admin(idPerson):
	results = (db.query(Admin.idPerson)
				.filter(Admin.idPerson == idPerson).all())
	return results

def query_person_benefits(idPerson):
	results = (db.query(Benefit.id, Benefit.name)
			.filter(Benefit.id == PersonBenefit.idBenefit)
			.filter(PersonBenefit.idPerson == idPerson)
			.order_by(Benefit.name).all())
	return results

def query_person_data(idPerson):
	results = (db.query(Datatype.id, Datatype.name, PersonData.data)
				.filter(Datatype.id == PersonData.idDatatype)
				.filter(PersonData.idPerson == idPerson)
				.order_by(Datatype.id).all())
	return results

def query_person_data_get_persondata_id(idPerson):
	results = (db.query(PersonData.id)
				.filter(PersonData.idPerson == idPerson).all())
	return results

def query_person_one_data(idPerson, idDatatype):
	results = (db.query(PersonData.id, PersonData.data)
				.filter(PersonData.idPerson == idPerson,
						PersonData.idDatatype == idDatatype).all())
	return results

def query_person_one_benefit(idPerson, idBenefit):
	results = (db.query(PersonBenefit.idBenefit)
				.filter(PersonBenefit.idPerson == idPerson,
						PersonBenefit.idBenefit == idBenefit).all())
	return results

def query_person_id_by_cpf(person_cpf):
	results = (db.query(Person.id)
				.filter(Person.cpf == person_cpf).all())
	return results

def query_person_name_like_by_company(person_name, idCompany):
	results = (db.query(Person.id, Person.name)
				.filter(Person.idCompany == idCompany)
				.filter(Person.name.like('%'+person_name+'%'))
				.order_by(Person.name).all())
	return results	

def query_person_in_company(idPerson, idCompany):
	""" Returns None in case no result is found """
	results = (db.query(Person.id)
				.filter(Person.idCompany == idCompany)
				.filter(Person.id == idPerson).first())
	return results


# PERSON INSERT & DELETE
# PERSON INSERT & DELETE
def insert_person_to_benefit(idPerson, idBenefit):
	new_person_to_benefit = PersonBenefit(idPerson = idPerson, 
							idBenefit = idBenefit)
	db.add(new_person_to_benefit)
	db.commit()

def insert_person(person_name, person_cpf, idCompany):
	new_person = Person(name = person_name, cpf = person_cpf, idCompany = idCompany)
	db.add(new_person)
	db.commit()

def insert_data_to_person(idDatatype, data, idPerson):
	new_data = PersonData(idDatatype = idDatatype, 
							data = data, 
							idPerson = idPerson)
	db.add(new_data)
	db.commit()

def update_person_data(dataId, new_data):
	person_from_benefit = (db.query(PersonData)
					.filter(PersonData.id == dataId)
					.update({'data': new_data}))
	db.commit()

def delete_person_from_benefit(idPerson, idBenefit):
	person_from_benefit = (db.query(PersonBenefit)
					.filter(PersonBenefit.idPerson == idPerson, 
							PersonBenefit.idBenefit == idBenefit).first())
	db.delete(person_from_benefit)
	db.commit()

def delete_person_from_person_table(idPerson):
	person = (db.query(Person)
			.filter(Person.id == idPerson).first())
	db.delete(person)
	db.commit()

def delete_data_with_persondata_id(persondata_id):
	data = (db.query(PersonData)
			.filter(PersonData.id == persondata_id).first())
	db.delete(data)
	db.commit




# BENEFIT & DATATYPE QUERIES
# BENEFIT & DATATYPE QUERIES
def benefit_exists(idBenefit):
	""" Receives a beenfit id and returns True if the benefit exists
	and False if it doesn't """
	if not is_int(idBenefit):
			raise TypeError
	results = (db.query(Benefit.id)
				.filter(Benefit.id == idBenefit).all())
	if len(results) == 1:
		return True
	elif len(results) > 1:
		raise Exception("Database is compromised")
	else:
		return False

def datatype_exists(idDatatype): #this has been tested
	if not is_int(idDatatype):
		raise TypeError
	results = (db.query(Datatype.id)
				.filter(Datatype.id == idDatatype).all())
	if len(results) == 1:
		return True
	elif len(results) > 1:
		raise Exception("Database is compromised")
	else:
		return False

def query_benefit_name(idBenefit):
	results = (db.query(Benefit.id, Benefit.name)
				.filter(Benefit.id == idBenefit).all())
	return results

def query_benefit_companies(idBenefit):
	results = (db.query(Company.id, Company.name)
				.filter(Company.id == CompanyBenefit.idCompany)
				.filter(CompanyBenefit.idBenefit == idBenefit)
				.order_by(Company.name).all())
	return results

def query_benefit_people(idBenefit):
	results = (db.query(Person.id, Person.idCompany, Person.name)
				.filter(Person.id == PersonBenefit.idPerson)
				.filter(PersonBenefit.idBenefit == idBenefit)
				.order_by(Person.name).all())
	return results

def query_benefit_people_by_company(idBenefit, idCompany):
	results = (db.query(Person.id, Person.idCompany, Person.name)
				.filter(Person.idCompany == idCompany)
				.filter(Person.id == PersonBenefit.idPerson)
				.filter(PersonBenefit.idBenefit == idBenefit)
				.order_by(Person.name).all())
	return results

def query_benefit_data_types(idBenefit):
	results = (db.query(Datatype.id, Datatype.name, Datatype.example)
				.filter(Datatype.id == BenefitData.idDatatype)
				.filter(BenefitData.idBenefit == idBenefit)
				.order_by(Datatype.id).all())
	return results

def query_all_data_types():
	results = (db.query(Datatype.id, Datatype.name, Datatype.example).all())
	return results

def query_datatype_details(idDatatype):
	results = (db.query(Datatype.id, Datatype.name, Datatype.example)
				.filter(Datatype.id == idDatatype).all())
	return results

def query_benefit_id_by_name(benefit_name):
	results = (db.query(Benefit.id, Benefit.name)
				.filter(Benefit.name == benefit_name).all())
	return results

def query_benefit_id_by_name_like(benefit_name):
	results = (db.query(Benefit.id, Benefit.name)
				.filter(Benefit.name.like('%'+benefit_name+'%')).all())
	return results

def query_data_type_id_by_name(datatype_name):
	results = (db.query(Datatype.id, Datatype.name)
				.filter(Datatype.name == datatype_name).all())
	return results

def query_data_type_id_by_name_like(datatype_name):
	results = (db.query(Datatype.id, Datatype.name)
				.filter(Datatype.name.like('%'+datatype_name+'%')).all())
	return results

def query_all_benefits():
	results = (db.query(Benefit.id, Benefit.name).order_by(Benefit.name).all())
	return results

def query_benefit_name_like_by_company(benefit_name, idCompany):
	results = (db.query(Benefit.id, Benefit.name)
				.filter(Benefit.id == CompanyBenefit.idBenefit)
				.filter(CompanyBenefit.idCompany == idCompany)
				.filter(Benefit.name.like('%'+benefit_name+'%'))
				.order_by(Benefit.name).all())
	return results	

def query_person_admission_date(idPerson, idBenefit):
	""" Returns None in case no result is found """
	results = (db.query(PersonBenefit.timestamp)
				.filter(PersonBenefit.idPerson == idPerson)
				.filter(PersonBenefit.idBenefit == idBenefit).first())
	return results

def query_benefit_in_company(idBenefit, idCompany):
	""" Returns None in case no result is found """
	results = (db.query(CompanyBenefit.id)
				.filter(CompanyBenefit.idBenefit == idBenefit)
				.filter(CompanyBenefit.idCompany == idCompany).first())
	return results


# BENEFIT AND DATATYPE INSERT & DELETE
# BENEFIT AND DATATYPE INSERT & DELETE

def delete_benefit_from_benefit_table(idBenefit):
	benefit = (db.query(Benefit)
			.filter(Benefit.id == idBenefit).first())
	db.delete(benefit)
	db.commit()

def delete_company_from_benefit(idCompany, idBenefit):
	company_from_benefit = (db.query(CompanyBenefit)
					.filter(CompanyBenefit.idCompany == idCompany, 
							CompanyBenefit.idBenefit == idBenefit).first())
	db.delete(company_from_benefit)
	db.commit()

def delete_data_type_from_benefit(idDatatype, idBenefit):
	current_data_type = (db.query(BenefitData)
					.filter(BenefitData.idDatatype == idDatatype, 
							BenefitData.idBenefit == idBenefit).first())
	db.delete(current_data_type)
	db.commit()

def insert_data_type_to_benefit(idDatatype, idBenefit):
	new_data_type = BenefitData(idDatatype = idDatatype, idBenefit = idBenefit)
	db.add(new_data_type)
	db.commit()

def insert_benefit_to_company(idBenefit, idCompany):
	new_benefit = CompanyBenefit(idCompany = idCompany, 
								idBenefit = idBenefit)
	db.add(new_benefit)
	db.commit()

def insert_benefit(benefit_name):
	new_benefit = Benefit(name = benefit_name)
	db.add(new_benefit)
	db.commit()

def insert_data_type(datatype_name, datatype_example):
	new_datatype = Datatype(name = datatype_name, example = datatype_example)
	db.add(new_datatype)
	db.commit()


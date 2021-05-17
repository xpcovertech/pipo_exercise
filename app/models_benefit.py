from db import benefit_exists, query_benefit_name, query_benefit_companies
from db import query_benefit_people_by_company, query_benefit_data_types
from utils import is_int

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
models_benefit.py

Benefit Profile object and its correlated methods. 
'''

class BenefitProfile():
	def __init__(self, idBenefit):
		self.idBenefit = idBenefit

	def get_profile(self):
		if not is_int(self.idBenefit):
			raise TypeError
		if not benefit_exists(self.idBenefit):
			raise Exception("This benefit id doesn't exist")
		idBenefit = self.idBenefit
		name = self.get_name()
		companies = self.get_companies()
		data_types = self.get_data_types()
		profile = {"id": idBenefit,
					"name": name,
					"companies": companies,
					"data_types": data_types}
		return profile

	def get_name(self):
		if not is_int(self.idBenefit):
			raise TypeError
		benefit_name = query_benefit_name(self.idBenefit)
		if len(benefit_name) == 0:
			raise Exception("This benefit id doesn't exist")
		return benefit_name[0]["name"]

	def get_companies(self):
		if not is_int(self.idBenefit):
			raise TypeError
		if not benefit_exists(self.idBenefit):
			raise Exception("This benefit id doesn't exist")
		benefit_companies = query_benefit_companies(self.idBenefit)
		companies = []
		if len(benefit_companies) > 0:
			for company in benefit_companies:
				companies.append({"idCompany": company['id'], "name": company["name"]})
		return companies

	def get_people_by_company(self, idCompany):
		if not is_int(self.idBenefit):
			raise TypeError
		if not benefit_exists(self.idBenefit):
			raise Exception("This benefit id doesn't exist")
		benefit_people = query_benefit_people_by_company(self.idBenefit, idCompany)
		people_by_company = []
		if len(benefit_people) > 0:
			for person in benefit_people:
				people_by_company.append({"idPerson": person['id'], 
											"idCompany": person['idCompany'],
											"name": person['name']})
		return people_by_company

	def get_data_types(self):
		if not is_int(self.idBenefit):
			raise TypeError
		if not benefit_exists(self.idBenefit):
			raise Exception("This benefit id doesn't exist")
		benefit_data_types = query_benefit_data_types(self.idBenefit)
		data_types = []
		if len(benefit_data_types) > 0:
			for data_type in benefit_data_types:
				data_types.append({"idDatatype": data_type['id'], 
									"name": data_type["name"],
									"example": data_type["example"]})
		return data_types

from db import company_exists, query_company_name, query_company_people, query_company_benefits
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
models_company.py

Company Profile object and its correlated methods. 
'''

class CompanyProfile():
	def __init__(self, idCompany):
		self.idCompany = idCompany

	def get_profile(self):
		if not is_int(self.idCompany):
			raise TypeError
		if not company_exists(self.idCompany):
			raise Exception("This company id doesn't exist")
		idCompany = self.idCompany
		name = self.get_name()
		people = self.get_people()
		benefits = self.get_benefits()
		profile = {"id": idCompany,
					"name": name,
					"people": people,
					"benefits": benefits}
		return (profile)

	def get_name(self):
		if not is_int(self.idCompany):
			raise TypeError
		company_name = query_company_name(self.idCompany)
		if len(company_name) == 0:
			raise Exception("This company id doesn't exist")
		return company_name[0]["name"]

	def get_people(self):
		if not is_int(self.idCompany):
			raise TypeError
		if not company_exists(self.idCompany):
			raise Exception("This company id doesn't exist")
		company_people = query_company_people(self.idCompany)
		people = []
		if len(company_people) > 0:
			for person in company_people:
				people.append({"idPerson": person['id'], "name": person["name"]})
		return people

	def get_benefits(self):
		if not is_int(self.idCompany):
			raise TypeError
		if not company_exists(self.idCompany):
			raise Exception("This company id doesn't exist")
		company_benefits = query_company_benefits(self.idCompany)
		benefits = []
		if len(company_benefits) > 0:
			for benefit in company_benefits:
				benefits.append({"idBenefit": benefit['id'], "name": benefit["name"]})
		return benefits


from db import company_exists, query_company_name, query_company_people, query_company_benefits
from utils import is_int

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

	# Is it possible for companys to have no employees? No, it shouldnt be.
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


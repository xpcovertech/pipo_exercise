from db import person_exists, query_person_name_idcompany_cpf, query_person_admin
from db import query_person_benefits, query_person_data
from utils import is_int

class PersonProfile():
	def __init__(self, idPerson):
		self.idPerson = idPerson

	def get_profile(self):
		if not is_int(self.idPerson):
			raise TypeError
		if not person_exists(self.idPerson):
			raise Exception("This person id doesn't exist")
		idPerson = self.idPerson
		details = self.get_details()
		admin = self.get_admin()
		benefits = self.get_benefits()
		data = self.get_data()
		profile = {"id": idPerson,
					"name": details['name'],
					"idCompany": details['idCompany'],
					"cpf": details['cpf'],
					"admin": admin,
					"benefits": benefits,
					"data": data}
		return profile

	def get_details(self):
		if not is_int(self.idPerson):
			raise TypeError
		person_details = query_person_name_idcompany_cpf(self.idPerson)
		if len(person_details) == 0:
			raise Exception("This person id doesn't exist")
		return {"name": person_details[0]['name'],
				"idCompany": person_details[0]['idCompany'],
				"cpf": person_details[0]['cpf']}

	def get_admin(self):
		if not is_int(self.idPerson):
			raise TypeError
		if not person_exists(self.idPerson):
			raise Exception("This person id doesn't exist")
		person_admin = query_person_admin(self.idPerson)
		if len(person_admin) == 0:
			return {"level": 0, "name": "Colaborador"}
		else:
			return {"level": 1, "name": "Admin"}

	def get_benefits(self):
		if not is_int(self.idPerson):
			raise TypeError
		if not person_exists(self.idPerson):
			raise Exception("This person id doesn't exist")
		person_benefits = query_person_benefits(self.idPerson)
		benefits = []
		if len(person_benefits) > 0:
			for person_benefit in person_benefits:
				benefits.append({"idBenefit": person_benefit['id'],
									"name": person_benefit['name']})
		return benefits

	def get_data(self):
		if not is_int(self.idPerson):
			raise TypeError
		if not person_exists(self.idPerson):
			raise Exception("This person id doesn't exist")
		person_data = query_person_data(self.idPerson)
		data = []
		if len(person_data) > 0:
			for p_data in person_data:
				data.append({"idDatatype": p_data['id'], 
								"name": p_data['name'],
								"data": p_data['data']})
		return data

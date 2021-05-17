import unittest
from subprocess import call

from models_benefit import BenefitProfile

class TestGetProfile(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = BenefitProfile(1)
		self.profile_two = BenefitProfile(2)
		self.profile_three = BenefitProfile(3)

		self.profile_one_data = {
								"id": 1,
								"name": "Plano de Saúde Norte Europa",
								"companies": [{"idCompany": 3, "name": "Acme Co"},
												{"idCompany": 1, "name": "Wonka Industries"}],
								"data_types": [{"idDatatype": 1, "name": "Nome", "example": "Ex. Ronaldo Farias Azevedo"},
										{"idDatatype": 2, "name": "CPF", "example": "Digite o número do CPF no padrão. Ex. 000.000.000-00"},
										{"idDatatype": 3, "name": "Data Admissão", "example": "Este dado é gerado automaticamente"},
										{"idDatatype": 8, "name": "Email", "example": "Ex. nome@email.com.br"}]
								}
		self.profile_two_data = {
								"id": 2,
								"name": "Plano de Saúde Pampulha Intermédica",
								"companies": [{"idCompany": 2, "name": "Tio Patinhas Bank"},
												{"idCompany": 1, "name": "Wonka Industries"}],
								"data_types": [{"idDatatype": 1, "name": "Nome", "example": "Ex. Ronaldo Farias Azevedo"},
										{"idDatatype": 2, "name": "CPF", "example": "Digite o número do CPF no padrão. Ex. 000.000.000-00"},
										{"idDatatype": 3, "name": "Data Admissão", "example": "Este dado é gerado automaticamente"},
										{"idDatatype": 4, "name": "Endereço", "example": "Ex. Av. Rebouças, 1020, ap 23, São Paulo - SP"}]
								}
		self.profile_three_data = {
								"id": 3,
								"name": "Plano Dental Sorriso",
								"companies": [{"idCompany": 3, "name": "Acme Co"},
												{"idCompany": 2, "name": "Tio Patinhas Bank"},
												{"idCompany": 1, "name": "Wonka Industries"}],
								"data_types": [{"idDatatype": 1, "name": "Nome", "example": "Ex. Ronaldo Farias Azevedo"},
										{"idDatatype": 2, "name": "CPF", "example": "Digite o número do CPF no padrão. Ex. 000.000.000-00"},
										{"idDatatype": 5, "name": "Peso (kg)", "example": "Digite somente os números. Ex. 75"},
										{"idDatatype": 6, "name": "Altura (cm)", "example": "Digite somente os números em centímetros. Ex. 175"}]
								}

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_profile_one(self):
		for key in self.profile_one_data.keys():
			actual_result = self.profile_one.get_profile().get(key)
			expected_result = self.profile_one_data.get(key)
			self.assertEqual(actual_result, expected_result)

	def test_get_profile_two(self):
		for key in self.profile_two_data.keys():
			actual_result = self.profile_two.get_profile().get(key)
			expected_result = self.profile_two_data.get(key)
			self.assertEqual(actual_result, expected_result)

	def test_get_profile_three(self):
		for key in self.profile_three_data.keys():
			actual_result = self.profile_three.get_profile().get(key)
			expected_result = self.profile_three_data.get(key)
			self.assertEqual(actual_result, expected_result)

class TestGetName(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = BenefitProfile(1)
		self.profile_two = BenefitProfile(2)
		self.profile_three = BenefitProfile(3)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_benefit_name_one(self):
		actual_result = self.profile_one.get_name()
		expected_result = "Plano de Saúde Norte Europa"
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_name_two(self):
		actual_result = self.profile_two.get_name()
		expected_result = "Plano de Saúde Pampulha Intermédica"
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_name_three(self):
		actual_result = self.profile_three.get_name()
		expected_result = "Plano Dental Sorriso"
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_name_benefit_doesnt_exist(self):
		with self.assertRaises(Exception):
			BenefitProfile(9999).get_name()

	def test_get_benefit_name_string_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile("1").get_name()

	def test_get_benefit_name_float_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(99.2).get_name()

	def test_get_benefit_name_datatype_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(str).get_name()

	def test_get_benefit_name_none_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(None).get_name()

	def test_get_benefit_name_empty_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile().get_name()

	def test_get_benefit_name_boolean_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(True).get_name()


class TestGetCompanies(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = BenefitProfile(1)
		self.profile_two = BenefitProfile(2)
		self.profile_three = BenefitProfile(3)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_benefit_companies_one(self):
		actual_result = self.profile_one.get_companies()
		expected_result = [{"idCompany": 3, "name": "Acme Co"},
							{"idCompany": 1, "name": "Wonka Industries"}]
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_companies_two(self):
		actual_result = self.profile_two.get_companies()
		expected_result = [{"idCompany": 2, "name": "Tio Patinhas Bank"},
							{"idCompany": 1, "name": "Wonka Industries"}]
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_companies_three(self):
		actual_result = self.profile_three.get_companies()
		expected_result = [{"idCompany": 3, "name": "Acme Co"},
							{"idCompany": 2, "name": "Tio Patinhas Bank"},
							{"idCompany": 1, "name": "Wonka Industries"}]
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_companies_company_doesnt_exist(self):
		with self.assertRaises(Exception):
			BenefitProfile(9999).get_companies()

	def test_get_benefit_companies_string_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile("1").get_companies()

	def test_get_benefit_companies_float_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(1.3).get_companies()

	def test_get_benefit_companies_datatype_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(str).get_companies()

	def test_get_benefit_companies_none_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(None).get_companies()

	def test_get_benefit_companies_empy_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile().get_companies()

	def test_get_benefit_companies_boolean_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(True).get_companies()


class TestGetPeopleByCompany(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = BenefitProfile(1)
		self.profile_two = BenefitProfile(2)
		self.profile_three = BenefitProfile(3)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_benefit_people_by_company_one(self):
		actual_result = self.profile_one.get_people_by_company(1)
		expected_result = [{'idPerson': 1, 'idCompany': 1, 'name': 'Pessoa da Wonka'}]
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_people_by_company_two(self):
		actual_result = self.profile_two.get_people_by_company(2)
		expected_result = []
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_people_by_company_three(self):
		actual_result = self.profile_three.get_people_by_company(1)
		expected_result = [{'idPerson': 1, 'idCompany': 1, 'name': 'Pessoa da Wonka'}]
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_people_by_company_company_doesnt_exist(self):
		with self.assertRaises(Exception):
			BenefitProfile(9999).get_people_by_company()

	def test_get_benefit_people_by_company_string_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile("1").get_people_by_company()

	def test_get_benefit_people_by_company_float_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(1.3).get_people_by_company()

	def test_get_benefit_people_by_company_datatype_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(str).get_people_by_company()

	def test_get_benefit_people_by_company_none_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(None).get_people_by_company()

	def test_get_benefit_people_by_company_empy_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile().get_people_by_company()

	def test_get_benefit_people_by_company_boolean_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(True).get_people_by_company()


class TestGetDataTypes(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = BenefitProfile(1)
		self.profile_two = BenefitProfile(2)
		self.profile_three = BenefitProfile(3)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_benefit_data_types_one(self):
		actual_result = self.profile_one.get_data_types()
		expected_result = [{"idDatatype": 1, "name": "Nome", "example": "Ex. Ronaldo Farias Azevedo"},
							{"idDatatype": 2, "name": "CPF", "example": "Digite o número do CPF no padrão. Ex. 000.000.000-00"},
							{"idDatatype": 3, "name": "Data Admissão", "example": "Este dado é gerado automaticamente"},
							{"idDatatype": 8, "name": "Email", "example": "Ex. nome@email.com.br"}]
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_data_types_two(self):
		actual_result = self.profile_two.get_data_types()
		expected_result = [{"idDatatype": 1, "name": "Nome", "example": "Ex. Ronaldo Farias Azevedo"},
							{"idDatatype": 2, "name": "CPF", "example": "Digite o número do CPF no padrão. Ex. 000.000.000-00"},
							{"idDatatype": 3, "name": "Data Admissão", "example": "Este dado é gerado automaticamente"},
							{"idDatatype": 4, "name": "Endereço", "example": "Ex. Av. Rebouças, 1020, ap 23, São Paulo - SP"}]
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_data_types_three(self):
		actual_result = self.profile_three.get_data_types()
		expected_result = [{"idDatatype": 1, "name": "Nome", "example": "Ex. Ronaldo Farias Azevedo"},
							{"idDatatype": 2, "name": "CPF", "example": "Digite o número do CPF no padrão. Ex. 000.000.000-00"},
							{"idDatatype": 5, "name": "Peso (kg)", "example": "Digite somente os números. Ex. 75"},
							{"idDatatype": 6, "name": "Altura (cm)", "example": "Digite somente os números em centímetros. Ex. 175"}]
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_data_types_company_doesnt_exist(self):
		with self.assertRaises(Exception):
			BenefitProfile(9999).get_data_types()

	def test_get_benefit_data_types_string_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile("1").get_data_types()

	def test_get_benefit_data_types_float_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(1.3).get_data_types()

	def test_get_benefit_data_types_datatype_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(str).get_data_types()

	def test_get_benefit_data_types_none_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(None).get_data_types()

	def test_get_benefit_data_types_empy_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile().get_data_types()

	def test_get_benefit_data_types_boolean_input(self):
		with self.assertRaises(TypeError):
			BenefitProfile(True).get_data_types()


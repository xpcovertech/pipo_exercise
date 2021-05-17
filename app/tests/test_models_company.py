import unittest
from subprocess import call

from models_company import CompanyProfile

class TestGetProfile(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = CompanyProfile(1)
		self.profile_two = CompanyProfile(2)
		self.profile_three = CompanyProfile(3)

		self.profile_one_data = {
								"id": 1,
								"name": "Wonka Industries",
								"people": 
									[{'idPerson': 5, 'name': 'Fernando Augusto Rodrigues'}, 
									{'idPerson': 13, 'name': 'João Patricio'}, 
									{'idPerson': 4, 'name': 'Mariana Fagundes'}, 
									{'idPerson': 14, 'name': 'Marília Roberta Almeida'}, 
									{'idPerson': 6, 'name': 'Paula Macedo Gomes'}, 
									{'idPerson': 1, 'name': 'Pessoa da Wonka'}],
								"benefits":
									[{'idBenefit': 3, 'name': 'Plano Dental Sorriso'}, 
									{'idBenefit': 4, 'name': 'Plano de Saúde Mente Sã, Corpo São'}, 
									{'idBenefit': 1, 'name': 'Plano de Saúde Norte Europa'}, 
									{'idBenefit': 2, 'name': 'Plano de Saúde Pampulha Intermédica'}]
								}
		self.profile_two_data = {
								"id": 2,
								"name": "Tio Patinhas Bank",
								"people": 
									[{'idPerson': 2, 'name': 'Pessoa da Tio Patinhas'}, 
									{'idPerson': 8, 'name': 'Rafaela Dias Silva'}, 
									{'idPerson': 7, 'name': 'Ricardo Pontes'}, 
									{'idPerson': 9, 'name': 'Romario Pacheco'}],
								"benefits":
									[{'idBenefit': 3, 'name': 'Plano Dental Sorriso'}, 
									{'idBenefit': 4, 'name': 'Plano de Saúde Mente Sã, Corpo São'}, 
									{'idBenefit': 2, 'name': 'Plano de Saúde Pampulha Intermédica'}]
								}
		self.profile_three_data = {
								"id": 3,
								"name": "Acme Co",
								"people": 
									[{'idPerson': 10, 'name': 'Augusto Wozniak'}, 
									{'idPerson': 11, 'name': 'Otavio Oliveira'}, 
									{'idPerson': 3, 'name': 'Pessoa da Acme'},
									{'idPerson': 12, 'name': 'Waldisney Gates'}],
								"benefits":
									[{'idBenefit': 3, 'name': 'Plano Dental Sorriso'}, 
									{'idBenefit': 1, 'name': 'Plano de Saúde Norte Europa'}]
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

	def test_get_profile_company_doesnt_exist(self):
		with self.assertRaises(Exception):
			CompanyProfile(0).get_name()

	def test_get_profile_string_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile("hello").get_name()

	def test_get_profile_float_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(9.9203984).get_name()

	def test_get_profile_datatype_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(int).get_name()

	def test_get_profile_name_none_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(None).get_name()

	def test_get_profile_name_empy_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile().get_name()

	def test_get_profile_name_boolean_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(False).get_name()


class TestGetName(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = CompanyProfile(1)
		self.profile_two = CompanyProfile(2)
		self.profile_three = CompanyProfile(3)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_company_name_one(self):
		actual_result = self.profile_one.get_name()
		expected_result = "Wonka Industries"
		self.assertEqual(actual_result, expected_result)

	def test_get_company_name_two(self):
		actual_result = self.profile_two.get_name()
		expected_result = "Tio Patinhas Bank"
		self.assertEqual(actual_result, expected_result)

	def test_get_company_name_three(self):
		actual_result = self.profile_three.get_name()
		expected_result = "Acme Co"
		self.assertEqual(actual_result, expected_result)

	def test_get_company_name_company_doesnt_exist(self):
		with self.assertRaises(Exception):
			CompanyProfile(9999).get_name()

	def test_get_company_name_string_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile("1").get_name()

	def test_get_company_name_float_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(1.3).get_name()

	def test_get_company_name_datatype_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(str).get_name()

	def test_get_company_name_none_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(None).get_name()

	def test_get_company_name_empy_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile().get_name()

	def test_get_company_name_boolean_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(True).get_name()


class TestGetPeople(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = CompanyProfile(1)
		self.profile_two = CompanyProfile(2)
		self.profile_three = CompanyProfile(3)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_company_people_one(self):
		actual_result = self.profile_one.get_people()
		expected_result = [{'idPerson': 5, 'name': 'Fernando Augusto Rodrigues'}, 
							{'idPerson': 13, 'name': 'João Patricio'}, 
							{'idPerson': 4, 'name': 'Mariana Fagundes'}, 
							{'idPerson': 14, 'name': 'Marília Roberta Almeida'}, 
							{'idPerson': 6, 'name': 'Paula Macedo Gomes'}, 
							{'idPerson': 1, 'name': 'Pessoa da Wonka'}]
		self.assertEqual(actual_result, expected_result)

	def test_get_company_people_two(self):
		actual_result = self.profile_two.get_people()
		expected_result = [{'idPerson': 2, 'name': 'Pessoa da Tio Patinhas'}, 
							{'idPerson': 8, 'name': 'Rafaela Dias Silva'}, 
							{'idPerson': 7, 'name': 'Ricardo Pontes'}, 
							{'idPerson': 9, 'name': 'Romario Pacheco'}]
		self.assertEqual(actual_result, expected_result)

	def test_get_company_people_three(self):
		actual_result = self.profile_three.get_people()
		expected_result = [{'idPerson': 10, 'name': 'Augusto Wozniak'}, 
							{'idPerson': 11, 'name': 'Otavio Oliveira'}, 
							{'idPerson': 3, 'name': 'Pessoa da Acme'},
							{'idPerson': 12, 'name': 'Waldisney Gates'}]
		self.assertEqual(actual_result, expected_result)

	def test_get_company_people_company_doesnt_exist(self):
		with self.assertRaises(Exception):
			CompanyProfile(9999).get_people()

	def test_get_company_people_string_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile("1").get_people()

	def test_get_company_people_float_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(1.3).get_people()

	def test_get_company_people_datatype_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(str).get_people()

	def test_get_company_people_none_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(None).get_people()

	def test_get_company_people_empy_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile().get_people()

	def test_get_company_people_boolean_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(True).get_people()


class TestGetBenefits(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = CompanyProfile(1)
		self.profile_two = CompanyProfile(2)
		self.profile_three = CompanyProfile(3)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_company_benefits_one(self):
		actual_result = self.profile_one.get_benefits()
		expected_result = [{'idBenefit': 3, 'name': 'Plano Dental Sorriso'}, 
							{'idBenefit': 4, 'name': 'Plano de Saúde Mente Sã, Corpo São'}, 
							{'idBenefit': 1, 'name': 'Plano de Saúde Norte Europa'}, 
							{'idBenefit': 2, 'name': 'Plano de Saúde Pampulha Intermédica'}]
		self.assertEqual(actual_result, expected_result)

	def test_get_company_benefits_two(self):
		actual_result = self.profile_two.get_benefits()
		expected_result = [{'idBenefit': 3, 'name': 'Plano Dental Sorriso'}, 
							{'idBenefit': 4, 'name': 'Plano de Saúde Mente Sã, Corpo São'}, 
							{'idBenefit': 2, 'name': 'Plano de Saúde Pampulha Intermédica'}]
		self.assertEqual(actual_result, expected_result)

	def test_get_company_benefits_three(self):
		actual_result = self.profile_three.get_benefits()
		expected_result = [{'idBenefit': 3, 'name': 'Plano Dental Sorriso'}, 
							{'idBenefit': 1, 'name': 'Plano de Saúde Norte Europa'}]
		self.assertEqual(actual_result, expected_result)

	def test_get_company_benefits_company_doesnt_exist(self):
		with self.assertRaises(Exception):
			CompanyProfile(911111123999).get_benefits()

	def test_get_company_benefits_string_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile("1").get_benefits()

	def test_get_company_benefits_float_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(1.3).get_benefits()

	def test_get_company_benefits_datatype_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(str).get_benefits()

	def test_get_company_benefits_none_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(None).get_benefits()

	def test_get_company_benefits_empy_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile().get_benefits()

	def test_get_company_benefits_boolean_input(self):
		with self.assertRaises(TypeError):
			CompanyProfile(False).get_benefits()


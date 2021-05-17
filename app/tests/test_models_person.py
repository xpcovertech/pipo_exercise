import unittest
from subprocess import call

from models_person import PersonProfile

class TestPersonProfile(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

		self.profile_one_data = {"id": 1,
								"name": "Pessoa da Wonka",
								"idCompany": 1,
								"cpf": "230.841.911-31",
								"admin": {"level": 1, "name": "Admin"},
								"benefits": [{"idBenefit": 3, "name": "Plano Dental Sorriso"},
											{"idBenefit": 1, "name": "Plano de Saúde Norte Europa"}],
								"data": [{"idDatatype": 5, "name": "Peso (kg)", "data": "78"},
										{"idDatatype": 6, "name": "Altura (cm)", "data": "180"},
										{"idDatatype": 8, "name": "Email", "data": "pessoa@wonka.com"}]
								}

		self.profile_two_data = {"id": 2, 
								"name": "Pessoa da Tio Patinhas",
								"idCompany": 2,
								"cpf": "985.105.727-47",
								"admin": {"level": 1, "name": "Admin"},
								"benefits": [],
								"data": []
								}

		self.profile_three_data = {"id": 10, 
								"name": "Augusto Wozniak",
								"idCompany": 3,
								"cpf": "007.123.232-12",
								"admin": {"level": 0, "name": "Colaborador"},
								"benefits": [],
								"data": []
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


class TestGetPersonNameIdcompanyCpf(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_person_name_idcompany_cpf_one(self):
		actual_result = self.profile_one.get_details()
		expected_result = {"name": "Pessoa da Wonka", "idCompany": 1, "cpf": "230.841.911-31"}
		self.assertEqual(actual_result, expected_result)

	def test_get_person_name_idcompany_cpf_two(self):
		actual_result = self.profile_two.get_details()
		expected_result = {"name": "Pessoa da Tio Patinhas", "idCompany": 2, "cpf": "985.105.727-47"}
		self.assertEqual(actual_result, expected_result)

	def test_get_person_name_idcompany_cpf_three(self):
		actual_result = self.profile_three.get_details()
		expected_result = {"name": "Augusto Wozniak", "idCompany": 3, "cpf": "007.123.232-12"}
		self.assertEqual(actual_result, expected_result)


class TestGetPersonNameIdcompanyCpfError(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_person_name_doesnt_exist(self):
		with self.assertRaises(Exception):
			PersonProfile(1111111111).get_details()

	def test_get_person_name_string_input(self):
		with self.assertRaises(TypeError):
			PersonProfile("274q38").get_details()

	def test_get_person_name_float_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(1.0).get_details()

	def test_get_person_name_datatype_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(float).get_details()

	def test_get_person_name_none_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(None).get_details()

	def test_get_person_name_empy_input(self):
		with self.assertRaises(TypeError):
			PersonProfile().get_details()

	def test_get_person_name_boolean_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(True).get_details()


class TestGetPersonAdmin(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_person_admin_one(self):
		actual_result = self.profile_one.get_admin()
		expected_result = {"level": 1, "name": "Admin"}
		self.assertEqual(actual_result, expected_result)

	def test_get_person_admin_two(self):
		actual_result = self.profile_two.get_admin()
		expected_result = {"level": 1, "name": "Admin"}
		self.assertEqual(actual_result, expected_result)

	def test_get_person_admin_three(self):
		actual_result = self.profile_three.get_admin()
		expected_result = {"level": 0, "name": "Colaborador"}
		self.assertEqual(actual_result, expected_result)


class TestGetPersonAdminError(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_person_name_doesnt_exist(self):
		with self.assertRaises(Exception):
			PersonProfile(1111111111).get_admin()

	def test_get_person_name_string_input(self):
		with self.assertRaises(TypeError):
			PersonProfile("274q38").get_admin()

	def test_get_person_name_float_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(1.0).get_admin()

	def test_get_person_name_datatype_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(float).get_admin()

	def test_get_person_name_none_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(None).get_admin()

	def test_get_person_name_empy_input(self):
		with self.assertRaises(TypeError):
			PersonProfile().get_admin()

	def test_get_person_name_boolean_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(True).get_admin()


class TestGetPersonBenefits(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_person_benefits_one(self):
		actual_result = self.profile_one.get_benefits()
		expected_result = [{"idBenefit": 3, "name": "Plano Dental Sorriso"},
							{"idBenefit": 1, "name": "Plano de Saúde Norte Europa"}]
		self.assertEqual(actual_result, expected_result)

	def test_get_person_benefits_two(self):
		actual_result = self.profile_two.get_benefits()
		expected_result = []
		self.assertEqual(actual_result, expected_result)

	def test_get_person_benefits_three(self):
		actual_result = self.profile_three.get_benefits()
		expected_result = []
		self.assertEqual(actual_result, expected_result)


class TestGetPersonBenefitsError(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_person_benefits_doesnt_exist(self):
		with self.assertRaises(Exception):
			PersonProfile(1111111111).get_benefits()

	def test_get_person_benefits_string_input(self):
		with self.assertRaises(TypeError):
			PersonProfile("274q38").get_benefits()

	def test_get_person_benefits_float_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(1.0).get_benefits()

	def test_get_person_benefits_datatype_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(float).get_benefits()

	def test_get_person_benefits_none_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(None).get_benefits()

	def test_get_person_benefits_empy_input(self):
		with self.assertRaises(TypeError):
			PersonProfile().get_benefits()

	def test_get_person_benefits_boolean_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(True).get_benefits()


class TestGetPersonData(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_person_data_one(self):
		actual_result = self.profile_one.get_data()
		expected_result = [{"idDatatype": 5, "name": "Peso (kg)", "data": "78"},
							{"idDatatype": 6, "name": "Altura (cm)", "data": "180"},
							{"idDatatype": 8, "name": "Email", "data": "pessoa@wonka.com"}]
		self.assertEqual(actual_result, expected_result)

	def test_get_person_data_two(self):
		actual_result = self.profile_two.get_data()
		expected_result = []
		self.assertEqual(actual_result, expected_result)

	def test_get_person_data_three(self):
		actual_result = self.profile_three.get_data()
		expected_result = []
		self.assertEqual(actual_result, expected_result)


class TestGetPersonDataError(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.profile_one = PersonProfile(1)
		self.profile_two = PersonProfile(2)
		self.profile_three = PersonProfile(10)

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_get_person_data_doesnt_exist(self):
		with self.assertRaises(Exception):
			PersonProfile(10292).get_data()

	def test_get_person_data_string_input(self):
		with self.assertRaises(TypeError):
			PersonProfile('whoops').get_data()

	def test_get_person_data_float_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(13.9).get_data()

	def test_get_person_data_datatype_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(list).get_data()

	def test_get_person_data_none_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(None).get_data()

	def test_get_person_data_empy_input(self):
		with self.assertRaises(TypeError):
			PersonProfile().get_data()

	def test_get_person_data_boolean_input(self):
		with self.assertRaises(TypeError):
			PersonProfile(False).get_data()


import unittest
from subprocess import call

from models_util import *

class TestCompanyExists(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_get_company_exists_true_one(self):
		actual_result = company_exists(2)
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_get_company_exists_out_of_range(self):
		actual_result = company_exists(998)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_get_company_exists_zero_input(self):
		actual_result = company_exists(0)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_get_company_exists_string_input(self):
		with self.assertRaises(TypeError):
			company_exists("whoops")

	def test_get_company_exists_float_input(self):
		with self.assertRaises(TypeError):
			company_exists(9283.2222)

	def test_get_company_exists_none_input(self):
		with self.assertRaises(TypeError):
			company_exists(None)

	def test_get_company_exists_empy_input(self):
		with self.assertRaises(TypeError):
			company_exists()

	def test_get_company_exists_boolean_input(self):
		with self.assertRaises(TypeError):
			company_exists(True)


class TestBenefitExists(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_get_benefit_exists_true_one(self):
		actual_result = benefit_exists(2)
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_exists_out_of_range(self):
		actual_result = benefit_exists(998)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_exists_zero_input(self):
		actual_result = benefit_exists(0)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_get_benefit_exists_string_input(self):
		with self.assertRaises(TypeError):
			benefit_exists("whoops")

	def test_get_benefit_exists_float_input(self):
		with self.assertRaises(TypeError):
			benefit_exists(9283.2222)

	def test_get_benefit_exists_none_input(self):
		with self.assertRaises(TypeError):
			benefit_exists(None)

	def test_get_benefit_exists_empy_input(self):
		with self.assertRaises(TypeError):
			benefit_exists()

	def test_get_benefit_exists_boolean_input(self):
		with self.assertRaises(TypeError):
			benefit_exists(True)


class TestDatatypeExists(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_get_datatype_exists_true_one(self):
		actual_result = datatype_exists(2)
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_get_datatype_exists_out_of_range(self):
		actual_result = datatype_exists(998)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_get_datatype_exists_zero_input(self):
		actual_result = datatype_exists(0)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_get_datatype_exists_string_input(self):
		with self.assertRaises(TypeError):
			datatype_exists("whoops")

	def test_get_datatype_exists_float_input(self):
		with self.assertRaises(TypeError):
			datatype_exists(9283.2222)

	def test_get_datatype_exists_none_input(self):
		with self.assertRaises(TypeError):
			datatype_exists(None)

	def test_get_datatype_exists_empy_input(self):
		with self.assertRaises(TypeError):
			datatype_exists()

	def test_get_datatype_exists_boolean_input(self):
		with self.assertRaises(TypeError):
			datatype_exists(True)


class TestGetAvailableDataTypesForBenefit(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.real_benefit_one = 1
		self.real_benefit_two = 2
		self.benefit_doesnt_exist = 77

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_get_available_data_types_for_real_benefit_one(self):
		actual_result = get_available_data_types_for_benefit(self.real_benefit_one)
		expected_result = [(4, 'Endereço', 'Ex. Av. Rebouças, 1020, ap 23, São Paulo - SP'), 
							(5, 'Peso (kg)', 'Digite somente os números. Ex. 75'), 
							(6, 'Altura (cm)', 'Digite somente os números em centímetros. Ex. 175'), 
							(7, 'Horas meditadas nos últimos 7 dias', 'Digite somente o número de horas. Ex. 3')]
		self.assertEqual(actual_result, expected_result)

	def test_get_available_data_types_for_real_benefit_two(self):
		actual_result = get_available_data_types_for_benefit(self.real_benefit_two)
		expected_result = [(5, 'Peso (kg)', 'Digite somente os números. Ex. 75'), 
							(6, 'Altura (cm)', 'Digite somente os números em centímetros. Ex. 175'), 
							(7, 'Horas meditadas nos últimos 7 dias', 'Digite somente o número de horas. Ex. 3'), 
							(8, 'Email', 'Ex. nome@email.com.br')]
		self.assertEqual(actual_result, expected_result)

	def test_get_available_data_types_for_benefit_doesnt_exist(self):
		with self.assertRaises(Exception):
			get_available_data_types_for_benefit(self.benefit_doesnt_exist)

	def test_get_available_data_types_for_benefit_string_input(self):
		with self.assertRaises(TypeError):
			get_available_data_types_for_benefit("12")

	def test_get_available_data_types_for_benefit_float_input(self):
		with self.assertRaises(TypeError):
			get_available_data_types_for_benefit(9283.2222)

	def test_get_available_data_types_for_benefit_none_input(self):
		with self.assertRaises(TypeError):
			get_available_data_types_for_benefit(None)

	def test_get_available_data_types_for_benefit_empy_input(self):
		with self.assertRaises(TypeError):
			get_available_data_types_for_benefit()

	def test_get_available_data_types_for_benefit_boolean_input(self):
		with self.assertRaises(TypeError):
			get_available_data_types_for_benefit(True)


class TestAddNewDataTypeToBenefit(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.real_new_datatype = 3
		self.real_current_datatype = 2
		self.real_benefit = 3
		self.datatype_doesnt_exist = 542
		self.benefit_doesnt_exist = 2378

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_add_new_data_type_to_benefit_both_real(self):
		add_new_data_type_to_benefit(self.real_new_datatype, self.real_benefit)
		actual_result = BenefitProfile(self.real_benefit).get_data_types()
		expected_result = [{"idDatatype": 1, "name": "Nome", "example": "Ex. Ronaldo Farias Azevedo"},
										{"idDatatype": 2, "name": "CPF", "example": "Digite o número do CPF no padrão. Ex. 000.000.000-00"},
										{"idDatatype": 3, "name": "Data Admissão", "example": "Este dado é gerado automaticamente"},
										{"idDatatype": 5, "name": "Peso (kg)", "example": "Digite somente os números. Ex. 75"},
										{"idDatatype": 6, "name": "Altura (cm)", "example": "Digite somente os números em centímetros. Ex. 175"}]
		self.assertEqual(actual_result, expected_result)

	def test_add_new_data_type_to_benefit_both_already_added(self):
		with self.assertRaises(Exception):
			add_new_data_type_to_benefit(self.real_current_datatype, self.real_benefit)

	def test_add_new_data_type_to_benefit_datatype_doesnt_exist(self):
		with self.assertRaises(Exception):
			add_new_data_type_to_benefit(self.datatype_doesnt_exist, self.real_benefit)

	def test_add_new_data_type_to_benefit_benefit_doesnt_exist(self):
		with self.assertRaises(Exception):
			add_new_data_type_to_benefit(self.real_new_datatype, self.benefit_doesnt_exist)

	def test_add_new_data_type_to_benefit_neither_exist(self):
		with self.assertRaises(Exception):
			add_new_data_type_to_benefit(self.datatype_doesnt_exist, self.benefit_doesnt_exist)

	def test_get_add_new_data_type_to_benefit_string_input(self):
		with self.assertRaises(TypeError):
			add_new_data_type_to_benefit("8390832", self.real_benefit)

	def test_get_add_new_data_type_to_benefit_float_input(self):
		with self.assertRaises(TypeError):
			add_new_data_type_to_benefit(0.0, self.real_benefit)

	def test_get_add_new_data_type_to_benefit_none_input(self):
		with self.assertRaises(TypeError):
			add_new_data_type_to_benefit(self.real_new_datatype, None)

	def test_get_add_new_data_type_to_benefit_empy_input(self):
		with self.assertRaises(TypeError):
			add_new_data_type_to_benefit()

	def test_get_add_new_data_type_to_benefit_boolean_input(self):
		with self.assertRaises(TypeError):
			add_new_data_type_to_benefit(False, self.real_benefit)



class TestRemoveDataTypeFromBenefit(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.real_current_datatype = 3
		self.real_not_current_datatype = 6 #datatype exists but it is not registered to benefit
		self.real_benefit = 1
		self.datatype_doesnt_exist = 542
		self.benefit_doesnt_exist = 2378

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_remove_data_type_from_benefit_both_real(self):
		remove_data_type_from_benefit(self.real_current_datatype, self.real_benefit)
		actual_result = query_benefit_data_types(self.real_benefit)
		expected_result = [(1, 'Nome', 'Ex. Ronaldo Farias Azevedo'), 
							(2, 'CPF', 'Digite o número do CPF no padrão. Ex. 000.000.000-00'), 
							(8, 'Email', 'Ex. nome@email.com.br')]
		self.assertEqual(actual_result, expected_result)

	def test_remove_data_type_from_benefit_both_already_added(self):
		with self.assertRaises(Exception):
			remove_data_type_from_benefit(self.real_not_current_datatype, self.real_benefit)

	def test_remove_data_type_from_benefit_datatype_doesnt_exist(self):
		with self.assertRaises(Exception):
			remove_data_type_from_benefit(self.datatype_doesnt_exist, self.real_benefit)

	def test_remove_data_type_from_benefit_benefit_doesnt_exist(self):
		with self.assertRaises(Exception):
			remove_data_type_from_benefit(self.real_current_datatype, self.benefit_doesnt_exist)

	def test_remove_data_type_from_benefit_neither_exist(self):
		with self.assertRaises(Exception):
			remove_data_type_from_benefit(self.datatype_doesnt_exist, self.benefit_doesnt_exist)

	def test_get_remove_data_type_from_benefit_string_input(self):
		with self.assertRaises(TypeError):
			remove_data_type_from_benefit("8390832", self.real_benefit)

	def test_get_remove_data_type_from_benefit_float_input(self):
		with self.assertRaises(TypeError):
			remove_data_type_from_benefit(0.0, self.real_benefit)

	def test_get_remove_data_type_from_benefit_none_input(self):
		with self.assertRaises(TypeError):
			remove_data_type_from_benefit(self.real_current_datatype, None)

	def test_get_remove_data_type_from_benefit_empy_input(self):
		with self.assertRaises(TypeError):
			remove_data_type_from_benefit()

	def test_get_remove_data_type_from_benefit_boolean_input(self):
		with self.assertRaises(TypeError):
			remove_data_type_from_benefit(False, self.real_benefit)

class TestAddNewBenefitToCompany(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.real_new_benefit = 2
		self.real_current_benefit = 3
		self.real_company = 3
		self.company_doesnt_exist = 99
		self.benefit_doesnt_exist = 77

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_add_new_benefit_to_company_both_real(self):
		add_new_benefit_to_company(self.real_new_benefit, self.real_company)
		actual_result = query_company_benefits(self.real_company)
		expected_result = [(3, 'Plano Dental Sorriso'), (1, 'Plano de Saúde Norte Europa'),
						(2, 'Plano de Saúde Pampulha Intermédica')]
		self.assertEqual(actual_result, expected_result)

	def test_add_new_benefit_to_company_both_already_added(self):
		with self.assertRaises(Exception):
			add_new_benefit_to_company(self.real_current_benefit, self.real_company)

	def test_add_new_benefit_to_company_company_doesnt_exist(self):
		with self.assertRaises(Exception):
			add_new_benefit_to_company(self.real_benefit, self.company_doesnt_exist)

	def test_add_new_benefit_to_company_benefit_doesnt_exist(self):
		with self.assertRaises(Exception):
			add_new_benefit_to_company(self.benefit_doesnt_exist, self.real_company)

	def test_add_new_benefit_to_company_neither_exist(self):
		with self.assertRaises(Exception):
			add_new_benefit_to_company(self.benefit_doesnt_exist, self.company_doesnt_exist)

	def test_get_add_new_benefit_to_company_string_input(self):
		with self.assertRaises(TypeError):
			add_new_benefit_to_company("3", self.real_company)

	def test_get_add_new_benefit_to_company_float_input(self):
		with self.assertRaises(TypeError):
			add_new_benefit_to_company(9283.2222, self.real_company)

	def test_get_add_new_benefit_to_company_none_input(self):
		with self.assertRaises(TypeError):
			add_new_benefit_to_company(self.real_new_benefit, None)

	def test_get_add_new_benefit_to_company_empy_input(self):
		with self.assertRaises(TypeError):
			add_new_benefit_to_company()

	def test_get_add_new_benefit_to_company_boolean_input(self):
		with self.assertRaises(TypeError):
			add_new_benefit_to_company(True, self.real_company)


class TestRegisterNewBenefit(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.real_new_benefit = "Plano da Pipo"
		self.real_benefit_exists = "Plano de Saúde Norte Europa"
		self.real_company = 3

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_register_new_benefit_both_are_real(self):
		register_new_benefit(self.real_new_benefit, self.real_company)
		actual_result = query_company_benefits(self.real_company)
		expected_result = [(3, 'Plano Dental Sorriso'), (5, 'Plano da Pipo'),
							(1, 'Plano de Saúde Norte Europa')]
		self.assertEqual(actual_result, expected_result)

	def test_register_new_benefit_name_is_int(self):
		with self.assertRaises(TypeError):
			register_new_benefit(2222, self.real_company)

	def test_register_new_benefit_idcompany_is_string(self):
		with self.assertRaises(TypeError):
			register_new_benefit(self.real_new_benefit, "1")

	def test_register_new_benefit_name_is_empty(self):
		with self.assertRaises(Exception):
			register_new_benefit("", self.real_company)

	def test_register_new_benefit_idcompany_is_none(self):
		with self.assertRaises(TypeError):
			register_new_benefit(self.real_new_benefit, None)

	def test_register_new_benefit_idcompany_is_boolean(self):
		with self.assertRaises(TypeError):
			register_new_benefit(self.real_new_benefit, True)

	def test_register_new_benefit_name_is_boolean(self):
		with self.assertRaises(TypeError):
			register_new_benefit(False, self.real_company)

	def test_register_new_benefit_name_is_empty(self):
		with self.assertRaises(TypeError):
			register_new_benefit()


class RegisterNewDataType(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.new_data_type_name_one = "Signo"
		self.new_data_type_example_one = "Ex. Sagitário"
		self.data_type_already_exists = "nomE"
		self.real_benefit = 2

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_register_new_data_type_both_are_real(self):
		register_new_data_type(self.new_data_type_name_one, 
								self.new_data_type_example_one, 
								self.real_benefit)
		actual_result = query_benefit_data_types(self.real_benefit)
		expected_result = [(1, 'Nome', 'Ex. Ronaldo Farias Azevedo'), 
							(2, 'CPF', 'Digite o número do CPF no padrão. Ex. 000.000.000-00'), 
							(3, 'Data Admissão', 'Este dado é gerado automaticamente'), 
							(4, 'Endereço', 'Ex. Av. Rebouças, 1020, ap 23, São Paulo - SP'),
							(9, 'Signo', 'Ex. Sagitário')]
		self.assertEqual(actual_result, expected_result)

	def test_register_new_data_type_benefit_exists_already(self):
		with self.assertRaises(Exception):
			register_new_data_type(self.data_type_already_exists, 
									self.new_data_type_example_one, 
									self.real_benefit)

	def test_register_new_data_type_name_is_int(self):
		with self.assertRaises(TypeError):
			register_new_data_type(2222, 
									self.new_data_type_example_one, 
									self.real_benefit)

	def test_register_new_data_type_example_is_int(self):
		with self.assertRaises(TypeError):
			register_new_data_type(self.new_data_type_name_one,
									12839, 
									self.real_benefit)

	def test_register_new_data_type_name_is_empty(self):
		with self.assertRaises(Exception):
			register_new_data_type("", 
									self.new_data_type_example_one,
									self.real_benefit)

	def test_register_new_data_type_idbenefit_is_none(self):
		with self.assertRaises(TypeError):
			register_new_data_type(self.new_data_type_name_one,
									self.new_data_type_example_one, 
									None)

	def test_register_new_data_type_name_is_boolean(self):
		with self.assertRaises(TypeError):
			register_new_data_type(True, 
									self.new_data_type_example_one,
									self.real_benefit)

	def test_register_new_data_type_example_is_boolean(self):
		with self.assertRaises(TypeError):
			register_new_data_type(self.new_data_type_name_one,
									False,
									 self.real_benefit)

	def test_register_new_data_type_is_empty(self):
		with self.assertRaises(TypeError):
			register_new_data_type()


class TestPersonExists(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_get_person_exists_true_one(self):
		actual_result = person_exists(2)
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_get_person_exists_out_of_range(self):
		actual_result = person_exists(998)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_get_person_exists_zero_input(self):
		actual_result = person_exists(0)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_get_person_exists_string_input(self):
		with self.assertRaises(TypeError):
			person_exists("whoops")

	def test_get_person_exists_float_input(self):
		with self.assertRaises(TypeError):
			person_exists(9283.2222)

	def test_get_person_exists_none_input(self):
		with self.assertRaises(TypeError):
			person_exists(None)

	def test_get_person_exists_empy_input(self):
		with self.assertRaises(TypeError):
			person_exists()

	def test_get_person_exists_boolean_input(self):
		with self.assertRaises(TypeError):
			person_exists(True)


class TestRegisterNewPerson(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.new_person_name_one = "Matias Franco"
		self.new_person_cpf_one = "786.684.633-22"
		self.new_person_name_two = "Adriana Gomes"
		self.new_person_cpf_two = "366.287.020-73"
		self.person_cpf_already_registered = "985.105.727-47"
		self.cpf_is_not_valid = "545.997.833-09"
		self.real_company_id = 2

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")
	
	def test_register_new_person_valid_new_cpf_one(self):
		register_new_person(self.new_person_name_one, 
							self.new_person_cpf_one, 
							self.real_company_id)
		actual_result = query_company_people(self.real_company_id)
		expected_result = [(15, 'Matias Franco'),
							(2, 'Pessoa da Tio Patinhas'),
							(8, 'Rafaela Dias Silva'),
							(7, 'Ricardo Pontes'),
							(9, 'Romario Pacheco')]
		self.assertEqual(actual_result, expected_result)

	def test_register_new_person_valid_new_cpf_two(self):
		register_new_person(self.new_person_name_two, 
							self.new_person_cpf_two, 
							self.real_company_id)
		actual_result = query_company_people(self.real_company_id)
		expected_result = [(15, 'Adriana Gomes'),
							(2, 'Pessoa da Tio Patinhas'),
							(8, 'Rafaela Dias Silva'),
							(7, 'Ricardo Pontes'),
							(9, 'Romario Pacheco')]
		self.assertEqual(actual_result, expected_result)

	def test_register_new_person_valid_new_cpf_return_id_result(self):
		actual_result = register_new_person(self.new_person_name_two, 
											self.new_person_cpf_two, 
											self.real_company_id)
		expected_result = 15
		self.assertEqual(actual_result, expected_result)

	def test_register_new_person_cpf_exists_already(self):
		with self.assertRaises(Exception):
			register_new_person(self.new_person_name_one, 
							self.person_cpf_already_registered, 
							self.real_company_id)

	def test_register_new_person_cpf_is_not_valid(self):
		with self.assertRaises(Exception):
			register_new_person(self.new_person_name_one, 
							self.cpf_is_not_valid, 
							self.real_company_id)

	def test_register_new_person_name_is_int(self):
		with self.assertRaises(TypeError):
			register_new_person(100, 
							self.new_person_cpf_one, 
							self.real_company_id)

	def test_register_new_person_cpf_is_int(self):
		with self.assertRaises(Exception):
			register_new_person(self.new_person_name_two, 
							36628702073, 
							self.real_company_id)

	def test_register_new_person_idcompany_is_string(self):
		with self.assertRaises(TypeError):
			register_new_person(self.new_person_name_one, 
							self.new_person_cpf_one, 
							"9")

	def test_register_new_person_name_is_empty(self):
		with self.assertRaises(Exception):
			register_new_person("", 
							self.new_person_cpf_one, 
							self.real_company_id)

	def test_register_new_person_cpf_is_empty(self):
		with self.assertRaises(Exception):
			register_new_person(self.new_person_name_two, 
							"", 
							self.real_company_id)

	def test_register_new_person_cpf_is_none(self):
		with self.assertRaises(Exception):
			register_new_person(self.new_person_name_one, 
							None, 
							self.real_company_id)

	def test_register_new_person_name_is_boolean(self):
		with self.assertRaises(TypeError):
			register_new_person(True, 
							self.new_person_cpf_one, 
							self.real_company_id)

	def test_register_new_person_cpf_is_boolean(self):
		with self.assertRaises(Exception):
			register_new_person(self.new_person_name_one, 
							False, 
							self.real_company_id)

	def test_register_new_person_name_is_empty(self):
		with self.assertRaises(TypeError):
			register_new_person()

class TestRegisterPersonToBenefit(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.person_id_new_to_benefit = 2
		self.person_id_already_registered = 1
		self.person_doesnt_exist = 99
		self.real_benefit = 1
		self.benefit_doesnt_exist = 99

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_register_person_to_benefit_valid(self):
		register_person_to_benefit(self.person_id_new_to_benefit, self.real_benefit)
		actual_result = query_person_benefits(self.person_id_new_to_benefit)
		expected_result = [(1, 'Plano de Saúde Norte Europa')]
		self.assertEqual(actual_result, expected_result)

	def test_register_person_to_benefit_person_is_already_registered(self):
		with self.assertRaises(Exception):
			register_person_to_benefit(self.person_id_already_registered, 
										self.real_benefit)

	def test_register_person_to_benefit_person_doesnt_exist(self):
		with self.assertRaises(Exception):
			register_person_to_benefit(self.person_doesnt_exist, 
										self.real_benefit)

	def test_register_person_to_benefit_benefit_doesnt_exist(self):
		with self.assertRaises(Exception):
			register_person_to_benefit(self.person_id_new_to_benefit, 
										self.benefit_doesnt_exist)

	def test_register_person_to_benefit_person_id_is_string(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit("3", self.real_benefit)

	def test_register_person_to_benefit_benefit_id_is_boolean(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit(self.person_id_new_to_benefit, True)

	def test_register_person_to_benefit_person_id_is_datatype(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit(str, self.real_benefit)

	def test_register_person_to_benefit_both_are_none(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit(None, None)

	def test_register_person_to_benefit_empty(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit()


class TestRemovePersonFromBenefit(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.person_id_registered = 1
		self.person_id_not_registered = 2
		self.real_benefit_one = 3
		self.real_benefit_two = 1
		self.person_doesnt_exist = 83
		self.benefit_doesnt_exist = 77

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_remove_person_from_benefit_valid_benefit_one(self):
		remove_person_from_benefit(self.person_id_registered, self.real_benefit_one)
		actual_result = query_person_benefits(self.person_id_registered)
		expected_result = [(1, 'Plano de Saúde Norte Europa')]
		self.assertEqual(actual_result, expected_result)

	def test_remove_person_from_benefit_valid_benefit_two(self):
		remove_person_from_benefit(self.person_id_registered, self.real_benefit_two)
		actual_result = query_person_benefits(self.person_id_registered)
		expected_result = [(3, 'Plano Dental Sorriso')]
		self.assertEqual(actual_result, expected_result)

	def test_remove_person_from_benefit_person_not_registered(self):
		with self.assertRaises(Exception):
			remove_person_from_benefit(self.person_id_not_registered, 
										self.real_benefit_one)

	def test_register_person_to_benefit_person_doesnt_exist(self):
		with self.assertRaises(Exception):
			register_person_to_benefit(self.person_doesnt_exist, 
										self.real_benefit)

	def test_register_person_to_benefit_benefit_doesnt_exist(self):
		with self.assertRaises(Exception):
			register_person_to_benefit(self.person_id_registered, 
										self.benefit_doesnt_exist)

	def test_register_person_to_benefit_person_id_is_string(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit("3", self.real_benefit_two)

	def test_register_person_to_benefit_benefit_id_is_boolean(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit(self.person_id_registered, True)

	def test_register_person_to_benefit_person_id_is_datatype(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit(str, self.real_benefit_one)

	def test_register_person_to_benefit_both_are_none(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit(None, None)

	def test_register_person_to_benefit_empty(self):
		with self.assertRaises(TypeError):
			register_person_to_benefit()



class TestRegisterDataToPerson(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.person_id_one = 1
		self.person_id_two = 2
		self.available_data_type_id = 4 #endereço
		self.new_data = "Rua Afonso Camargo, 97, Curitiba - PR"
		self.reserved_data_type_id = 2 #cpf
		self.already_registered_data_type_id = 8 #Email
		self.person_doesnt_exist = 188002983
		self.datatype_doesnt_exist = 12373636

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_register_data_to_person_one(self):
		register_data_to_person(self.available_data_type_id,
								self.new_data,
								self.person_id_one)
		actual_result = query_person_data(self.person_id_one)
		expected_result = [(4, 'Endereço', 'Rua Afonso Camargo, 97, Curitiba - PR'),
							(5, 'Peso (kg)', '78'), 
							(6, 'Altura (cm)', '180'), 
							(8, 'Email', 'pessoa@wonka.com')]
		self.assertEqual(actual_result, expected_result)

	def test_register_data_to_person_two(self):
		register_data_to_person(self.available_data_type_id,
								self.new_data,
								self.person_id_two)
		actual_result = query_person_data(self.person_id_two)
		expected_result = [(4, 'Endereço', 'Rua Afonso Camargo, 97, Curitiba - PR')]
		self.assertEqual(actual_result, expected_result)

	def test_register_data_to_person_reserved_data_type(self):
		with self.assertRaises(Exception):
			register_data_to_person(self.reserved_data_type_id,
									self.new_data,
									self.person_id_one)

	def test_register_data_to_person_already_registered_data_type_id(self):
		with self.assertRaises(Exception):
			register_data_to_person(self.already_registered_data_type_id,
									self.new_data,
									self.person_id_one)

	def test_register_data_to_person_person_doesnt_exist(self):
		with self.assertRaises(Exception):
			register_data_to_person(self.available_data_type_id,
									self.new_data,
									self.person_doesnt_exist)

	def test_register_data_to_person_data_type_doesnt_exist(self):
		with self.assertRaises(Exception):
			register_data_to_person(self.datatype_doesnt_exist,
									self.new_data,
									self.person_id_one)

	def test_register_data_to_person_person_data_is_int(self):
		with self.assertRaises(TypeError):
			register_data_to_person(self.available_data_type_id,
									1283920,
									self.person_id_one)

	def test_register_data_to_person_data_data_is_boolean(self):
		with self.assertRaises(TypeError):
			register_data_to_person(self.available_data_type_id,
									True,
									self.person_id_one)

	def test_register_data_to_person_person_data_is_datatype(self):
		with self.assertRaises(TypeError):
			register_data_to_person(self.available_data_type_id,
									str,
									self.person_id_one)

	def test_register_data_to_person_all_are_none(self):
		with self.assertRaises(TypeError):
			register_data_to_person(None,
									None,
									None)

	def test_register_data_to_person_empty(self):
		with self.assertRaises(TypeError):
			register_data_to_person()

class TestUpdateDataFromPersonSuccess(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.person_id = 1
		self.datatype_id = 5 #Peso
		self.datatype_not_registered = 4 #Endereço
		self.new_data = "73"
		self.datatype_doesnt_exist = 1826
		self.person_doesnt_exist = 32838

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_update_data_from_person_valid(self):
		update_data_from_person(self.datatype_id, self.new_data, self.person_id)
		actual_result = query_person_data(self.person_id)
		expected_result = [(5, 'Peso (kg)', '73'), 
							(6, 'Altura (cm)', '180'), 
							(8, 'Email', 'pessoa@wonka.com')]
		self.assertEqual(actual_result, expected_result)
	
	def test_update_data_from_person_datatype_id_not_registered(self):
		with self.assertRaises(Exception):
			update_data_from_person(self.datatype_not_registered, 
									self.new_data,
									self.person_id)
	
	def test_update_data_from_person_datatype_doesnt_exist(self):
		with self.assertRaises(Exception):
			update_data_from_person(self.datatype_doesnt_exist, 
									self.new_data,
									self.person_id)

	def test_update_data_from_person_person_doesnt_exist(self):
		with self.assertRaises(Exception):
			update_data_from_person(self.datatype_id, 
									self.new_data,
									self.person_doesnt_exist)

	def test_update_data_from_person_new_data_is_emtpy(self):
		with self.assertRaises(Exception):
			update_data_from_person(self.datatype_id, 
									"",
									self.person_id)

	def test_update_data_from_person_new_data_is_int(self):
		with self.assertRaises(TypeError):
			update_data_from_person(self.datatype_id, 
									1893,
									self.person_id)

	def test_update_data_from_person_new_data_is_boolean(self):
		with self.assertRaises(TypeError):
			update_data_from_person(self.datatype_id, 
									True,
									self.person_id)

	def test_update_data_from_person_new_data_is_none(self):
		with self.assertRaises(TypeError):
			update_data_from_person(self.datatype_id, 
									None,
									self.person_id)

	def test_update_data_from_person_is_emtpy(self):
		with self.assertRaises(TypeError):
			update_data_from_person()


class TestDeletePersonProfile(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.person_with_benefit_and_data = 1 # Pessoa da Wonka
		self.person_no_benefit_or_data = 4 # Mariana Fagundes
		self.person_doesnt_exist = 18209
		self.company_id = 1 # For querying employees list

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_delete_person_profile_with_data_and_benefit_check_person_table(self):
		delete_person_profile(self.person_with_benefit_and_data)
		actual_result = query_company_people(self.company_id)
		expected_result = [(5, 'Fernando Augusto Rodrigues'), 
							(13, 'João Patricio'), 
							(4, 'Mariana Fagundes'), 
							(14, 'Marília Roberta Almeida'), 
							(6, 'Paula Macedo Gomes')]
		self.assertEqual(actual_result, expected_result)

	def test_delete_person_profile_with_data_and_benefit_check_data(self):
		delete_person_profile(self.person_with_benefit_and_data)
		actual_result = query_person_data(self.person_with_benefit_and_data)
		expected_result = []
		self.assertEqual(actual_result, expected_result)

	def test_delete_person_profile_with_data_and_benefit_check_benefit(self):
		delete_person_profile(self.person_with_benefit_and_data)
		actual_result = query_person_benefits(self.person_with_benefit_and_data)
		expected_result = []
		self.assertEqual(actual_result, expected_result)

	def test_delete_person_profile_no_benefit_or_data_check_person_table(self):
		delete_person_profile(self.person_no_benefit_or_data)
		actual_result = query_company_people(self.company_id)
		expected_result = [(5, 'Fernando Augusto Rodrigues'), 
							(13, 'João Patricio'), 
							(14, 'Marília Roberta Almeida'), 
							(6, 'Paula Macedo Gomes'),
							(1, 'Pessoa da Wonka')]
		self.assertEqual(actual_result, expected_result)

	def test_delete_person_profile_no_benefit_or_data_check_data(self):
		delete_person_profile(self.person_no_benefit_or_data)
		actual_result = query_person_data(self.person_no_benefit_or_data)
		expected_result = []
		self.assertEqual(actual_result, expected_result)

	def test_delete_person_profile_no_benefit_or_data_check_benefit(self):
		delete_person_profile(self.person_no_benefit_or_data)
		actual_result = query_person_benefits(self.person_no_benefit_or_data)
		expected_result = []
		self.assertEqual(actual_result, expected_result)

	def test_delete_person_profile_person_doesnt_exist(self):
		with self.assertRaises(Exception):
			delete_person_profile(self.person_doesnt_exist)

	def test_delete_person_profile_person_zero_input(self):
		with self.assertRaises(Exception):
			delete_person_profile(0)

	def test_delete_person_profile_person_string_input(self):
		with self.assertRaises(TypeError):
			delete_person_profile("1")

	def test_delete_person_profile_person_boolan_input(self):
		with self.assertRaises(TypeError):
			delete_person_profile(True)

	def test_delete_person_profile_person_empty_input(self):
		with self.assertRaises(TypeError):
			delete_person_profile()


class TestDeleteBenefitProfile(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")

		self.benefit_id_one = 3 # Plano Dental Sorriso
		self.benefit_doesnt_exist = 18209
		self.company_id = 3 # Acme
		self.company_id_wonka = 1
		self.person_id = 1 # Pessoa da Wonka

	def tearDown(self):
		db.rollback()
		call("./setup/finish_testing.sh")

	def test_delete_benefit_profile_check_benefits_table(self):
		delete_benefit_profile(self.benefit_id_one, self.company_id)
		actual_result = query_all_benefits()
		expected_result = [(3, 'Plano Dental Sorriso'), 
							(4, 'Plano de Saúde Mente Sã, Corpo São'), 
							(1, 'Plano de Saúde Norte Europa'), 
							(2, 'Plano de Saúde Pampulha Intermédica')]
		self.assertEqual(actual_result, expected_result)

	def test_delete_benefit_profile_check_companybenefit_table(self):
		delete_benefit_profile(self.benefit_id_one, self.company_id)
		actual_result = query_company_benefits(self.company_id)
		expected_result = [(1, 'Plano de Saúde Norte Europa')]
		self.assertEqual(actual_result, expected_result)

	def test_delete_benefit_profile_check_personbenefit_table(self):
		delete_benefit_profile(self.benefit_id_one, self.company_id_wonka)
		actual_result = query_person_benefits(self.person_id)
		expected_result = [(1, 'Plano de Saúde Norte Europa')]
		self.assertEqual(actual_result, expected_result)

	def test_delete_benefit_profile_benefit_doesnt_exist(self):
		with self.assertRaises(Exception):
			delete_benefit_profile(self.benefit_doesnt_exist, self.company_id)

	def test_delete_benefit_profile_zero_input(self):
		with self.assertRaises(Exception):
			delete_person_profile(0)

	def test_delete_benefit_profile_string_input(self):
		with self.assertRaises(TypeError):
			delete_person_profile("1")

	def test_delete_benefit_profile_boolean_input(self):
		with self.assertRaises(TypeError):
			delete_person_profile(True)

	def test_delete_benefit_profile_boolean_input(self):
		with self.assertRaises(TypeError):
			delete_person_profile(None)

	def test_delete_benefit_profile_emtpy_input(self):
		with self.assertRaises(TypeError):
			delete_person_profile()





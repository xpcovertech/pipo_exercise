import unittest
from utils import is_int, is_string, isCpfValid, get_header, str_to_int, str_list_to_int

class TestIsInt(unittest.TestCase):

	def test_is_int_true_one(self):
		actual_result = is_int(2)
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_is_int_out_of_range(self):
		actual_result = is_int(998)
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_is_int_zero_input(self):
		actual_result = is_int(0)
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_is_int_string_input(self):
		actual_result = is_int("hello")
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_int_float_input(self):
		actual_result = is_int(1.2)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_int_none_input(self):
		with self.assertRaises(TypeError):
			is_int(None)

	def test_is_int_empy_input(self):
		with self.assertRaises(TypeError):
			is_int()
		
	def test_is_int_boolean_input(self):
		actual_result = is_int(True)
		expected_result = False
		self.assertEqual(actual_result, expected_result)


class TestIsString(unittest.TestCase):

	def test_is_string_true_one(self):
		actual_result = is_string("hello my friend!*@*#*\n")
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_is_string_true_two(self):
		actual_result = is_string('1111')
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_is_string_int_input(self):
		actual_result = is_string(" ")
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_is_string_float_input(self):
		actual_result = is_string(1.2)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_string_int_input(self):
		actual_result = is_string(2)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_string_empty_string_input(self):
		with self.assertRaises(Exception):
			is_string("")

	def test_is_string_none_input(self):
		with self.assertRaises(TypeError):
			is_string(None)

	def test_is_string_empy_input(self):
		with self.assertRaises(TypeError):
			is_string()
		
	def test_is_string_boolean_input(self):
		actual_result = is_string(True)
		expected_result = False
		self.assertEqual(actual_result, expected_result)


class TestIsCpfValid(unittest.TestCase):

	def test_is_cpf_valid_valid_cpf_one(self):
		actual_result = isCpfValid("886.192.713-00")
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_is_cpf_valid_valid_cpf_two(self):
		actual_result = isCpfValid("544.596.375-61")
		expected_result = True
		self.assertEqual(actual_result, expected_result)

	def test_is_cpf_valid_not_valid_cpf(self):
		actual_result = isCpfValid("942.392.323-07")
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_cpf_valid_empty_string_input(self):
		actual_result = isCpfValid("")
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_cpf_valid_empty_int_input(self):
		actual_result = isCpfValid(88619271300)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_cpf_valid_empty_boolean_input(self):
		actual_result = isCpfValid(True)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_cpf_valid_empty_datatype_input(self):
		actual_result = isCpfValid(str)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_cpf_valid_empty_none_input(self):
		actual_result = isCpfValid(None)
		expected_result = False
		self.assertEqual(actual_result, expected_result)

	def test_is_cpf_valid_empty_empty_input(self):
		with self.assertRaises(TypeError):
			actual_result = isCpfValid()


class TestGetHeader(unittest.TestCase):

	def setUp(self):
		self.session_full = {"id": 3,
							"name": "Leo Rapini",
							"idCompany": 1,
							"company": "Pipo",
							"admin_name": "Admin"}

		self.session_partial = {"id": 3,
							"name": "Leo Rapini",
							"idCompany": 1}

		self.session_empty = {}

	def test_get_header_session_full_success(self):
		actual_result = get_header(self.session_full)
		expected_result = {"name": "Leo Rapini",
							"company": "Pipo",
							"admin": "Admin",
							"id": 3}
		self.assertEqual(actual_result, expected_result)

	def test_get_header_session_partial(self):
		actual_result = get_header(self.session_partial)
		expected_result = {"name": "",
							"company": "",
							"admin": "",
							"id": ""}
		self.assertEqual(actual_result, expected_result)

	def test_get_header_session_empty_dictionary(self):
		actual_result = get_header(self.session_empty)
		expected_result = {"name": "",
							"company": "",
							"admin": "",
							"id": ""}
		self.assertEqual(actual_result, expected_result)

	def test_get_header_session_string_input(self):
		actual_result = get_header("hello")
		expected_result = {"name": "",
							"company": "",
							"admin": "",
							"id": ""}
		self.assertEqual(actual_result, expected_result)

	def test_get_header_session_int_input(self):
		actual_result = get_header(3)
		expected_result = {"name": "",
							"company": "",
							"admin": "",
							"id": ""}
		self.assertEqual(actual_result, expected_result)

	def test_get_header_session_boolean_input(self):
		actual_result = get_header(True)
		expected_result = {"name": "",
							"company": "",
							"admin": "",
							"id": ""}
		self.assertEqual(actual_result, expected_result)

	def test_get_header_session_no_input(self):
		with self.assertRaises(TypeError):
			get_header()


class TestStrToInt(unittest.TestCase):

	def test_str_to_int_str_input_success_one(self):
		actual_result = str_to_int("12345")
		expected_result = 12345
		self.assertEqual(actual_result, expected_result)

	def test_str_to_int_str_input_success_two(self):
		actual_result = str_to_int("1234511192838")
		expected_result = 1234511192838
		self.assertEqual(actual_result, expected_result)

	def test_str_to_int_str_zero_input(self):
		actual_result = str_to_int("0")
		expected_result = 0
		self.assertEqual(actual_result, expected_result)

	def test_str_to_int_word_input(self):
		actual_result = str_to_int("hithere")
		expected_result = 0
		self.assertEqual(actual_result, expected_result)

	def test_str_to_int_str_boolean_input(self):
		actual_result = str_to_int(True)
		expected_result = 0
		self.assertEqual(actual_result, expected_result)

	def test_str_to_int_str_none_input(self):
		actual_result = str_to_int(None)
		expected_result = 0
		self.assertEqual(actual_result, expected_result)

	def test_str_to_int_str_list_input(self):
		actual_result = str_to_int([1,])
		expected_result = 0
		self.assertEqual(actual_result, expected_result)


class TestStrListToInt(unittest.TestCase):

	def test_str_list_to_int_input_suceess_opne(self):
		actual_result = str_list_to_int(["1", "2", "3", "4", "5"])
		expected_result = [1, 2, 3, 4, 5]
		self.assertEqual(actual_result, expected_result)




















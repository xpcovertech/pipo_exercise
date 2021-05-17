import unittest
from subprocess import call

from app import app
from db import db


class TestLayout(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def test_layout_header_menu(self):
		response = self.app.get("/login", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Pessoas', response.data)

	def test_layout_logout_button_exists(self):
		response = self.app.get("/login", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'logout', response.data)

	def test_layout_footer(self):
		response = self.app.get("/login", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Made with love by <a href="https://github.com/leorapini"', 
																response.data)

class TestLogin(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf), follow_redirects=True)

	def test_login_status_code_success(self):
		response = self.app.get("/login", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_login_status_code_typo(self):
		response = self.app.get("/lgin", follow_redirects=True)
		self.assertEqual(response.status_code, 404)

	def test_login_success_one(self):
		response = self.login("230.841.911-31") # admin Wonka
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Pessoa da Wonka', response.data)

	def test_login_success_two(self):
		response = self.login("985.105.727-47") # admin Wonka
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Pessoa da Tio Patinhas', response.data)

	def test_login_user_cpf_not_valid(self):
		response = self.login("1234456778") # admin Wonka
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'mero de CPF n', response.data) 
		# Número de CPF não válido

	def test_login_user_person_not_authorized(self):
		response = self.login("353.362.283-54") # admin Wonka
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'para entrar no sistema', response.data) 
		# [Nome], você não tem autorização para entrar no sistema

	def test_login_user_person_blank(self):
		response = self.login("") # admin Wonka
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Por favor insira seu CPF', response.data) 

	def test_login_user_person_not_registered(self):
		response = self.login("640.483.500-21")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'mero de CPF n', response.data)
		# Número de CPF não encontrado


class TestLogout(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf), 
									follow_redirects=True)

	def test_lougout_status_code_success(self):
		self.login("841.753.318-40") # Admin da Acme
		self.app.get("/", follow_redirects=True)
		response = self.app.get("/logout", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_lougout_redirects_to_login(self):
		self.login("841.753.318-40") # Admin da Acme
		self.app.get("/pessoas", follow_redirects=True)
		response = self.app.get("/logout", follow_redirects=True)
		self.assertIn(b'Login', response.data)


class TestIndex(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf), 
									follow_redirects=True)

	def test_index_status_code_success(self):
		response = self.app.get("/", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_index_redirects_to_login(self):
		response = self.app.get("/", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Login', response.data)

	def test_index_get_header(self):
		response = self.login("841.753.318-40") # Admin da Acme
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Acme Co', response.data)

	def test_index_body_text(self):
		response = self.login("841.753.318-40") # Admin da Acme
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Chegou a hora de simplificar', response.data)




### BENEFITS
### BENEFITS
### BENEFITS

class TestBenefitsHome(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf), follow_redirects=True)

	def test_benefits_home_status_code_success(self):
		response = self.app.get("/beneficios", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_benefits_home_to_login(self):
		response = self.app.get("/beneficios", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Login', response.data)

	def test_benefits_home_get_header(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/beneficios")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Wonka Industries', response.data)

	def test_benefits_body_text(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/beneficios")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'beneficios, fazer uma', response.data)
		# Você deseja cadastrar beneficios, fazer uma busca ou ver uma lista completa?


	
class TestBenefitsList(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf), follow_redirects=True)

	def test_benefits_list_status_code_success(self):
		response = self.app.get("/beneficios/lista", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_benefits_list_to_login(self):
		response = self.app.get("/beneficios/lista", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Login', response.data)

	def test_benefits_list_get_header(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/lista")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Tio Patinhas Bank', response.data)

	def test_benefits_body_text(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/lista")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Clique no nome para ver o perfil.', response.data)

	def test_benefits_benefits_list_result_one(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/lista")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Plano Dental Sorriso', response.data)

	def test_benefits_benefits_list_result_two(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.app.get("/beneficios/lista")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Norte Europa', response.data)
		# Plano de Saúde Norte Europa



class TestBenefitsSearch(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf),
									follow_redirects=True)
	def search(self, name):
		return self.app.post('/beneficios/busca', 
						data=dict(name = name),
										follow_redirects=True)

	def test_benefits_search_status_code_success(self):
		response = self.app.get("/beneficios/busca", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_benefits_search_body_text(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/beneficios/busca", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Busca por beneficios', response.data)

	def test_benefits_search_results_one(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.search("dental")
		self.assertIn(b'Plano Dental Sorriso', response.data)

	def test_benefits_search_results_two(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.search("pam")
		self.assertIn(b'Pampulha', response.data)
		# Plano de Saúde Pampulha Intermédica

	def test_benefits_search_results_not_found(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.search("000")
		self.assertIn(b'Nenhum resultado encontrado', response.data)

	def test_benefits_search_results_empty(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.search("")
		self.assertIn(b'Por favor insira um nome', response.data)



class TestBenefitsRegistration(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data = dict(cpf = cpf),
									follow_redirects = True)

	def register(self, name):
		return self.app.post('/beneficios/cadastro', 
								data = dict(name = name),
								follow_redirects = True)

	def test_benefits_registration_status_code_success(self):
		response = self.app.get("/beneficios/cadastro", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
	
	def test_benefits_registration_body_text(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.app.get("/beneficios/cadastro", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Cadastro beneficios', response.data)

	def test_benefits_registration_empty_input(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.register("")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Por favor insira um nome', response.data)

	def test_benefits_registration_successful_one(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.register("Plano de Sáude da Pipo")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Nenhum dado cadastrado.', response.data)

	def test_benefits_registration_successful_two(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.register("Horizon Health")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Nenhum dado cadastrado.', response.data)

	def test_benefits_registration_fail_benefit_registered_to_company(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.register("Plano de Saúde Norte Europa")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este beneficio j', response.data)
		# Este beneficio já está cadastrado para essa empresa

	def test_benefits_registration_succsesss_benefit_in_db_but_not_registered_to_company(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.register("Plano de Saúde Mente Sã, Corpo São")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Horas meditadas ', response.data)
		# Este beneficio já está cadastrado para essa empresa


class TestBenefitsProfile(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf),
									follow_redirects=True)

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def test_benefits_profile_status_code_success(self):
		response = self.app.get("/beneficios/perfil/3", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_benefits_profile_status_code_404(self):
		response = self.app.get("/beneficios/perfil/", follow_redirects=True)
		self.assertEqual(response.status_code, 404)
		self.assertIn(b'meme', response.data)
		# Error message made by meme generator

	def test_benefits_profile_body_text(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/perfil/2", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Pessoas Cadastradas no Plano', response.data)

	def test_benefits_profile_benefit_data_pampulha(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/perfil/2", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Nome', response.data)

	def test_benefits_profile_profile_doesnt_exist(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/perfil/999", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_benefits_profile_benefit_not_registered_to_company(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/perfil/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.



# ONLY GET METHOD TESTED
class TestBenefitsDataTypes(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf),
									follow_redirects=True)

	def change_data_types(self, idDatatype, idWho):
		return self.app.post('/beneficios/editar/{}'.format(idWho), 
								data = dict(idDatatype = idDatatype),
								follow_redirects = True)

	def test_benefits_data_types_status_code_success(self):
		response = self.app.get("/beneficios/editar/4", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_benefits_data_types_status_code_404(self):
		response = self.app.get("/beneficios/editar/", follow_redirects=True)
		self.assertEqual(response.status_code, 404)
		self.assertIn(b'meme', response.data)
		# Error message made by meme generator

	def test_benefits_data_types_body_text(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/editar/4", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Selecione os dados que gostaria de remover ou adicionar', 
																response.data)
	
	def test_benefits_data_types_benefit_data_mente_sa(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/editar/4", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'value="2" checked', response.data)
		# CPF checkbox checked

	def test_benefits_data_types_profile_doesnt_exist(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/beneficios/editar/999", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_benefits_data_types_delete_datatype_name_from_norte_europa(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.change_data_types([2, 3, 8], 1)
		self.assertEqual(response.status_code, 200)
		self.assertNotIn(b'Nome', response.data)
		self.assertIn(b'CPF', response.data)

	def test_benefits_data_types_add_datatype_horas_meditadas_to_norte_europa(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.change_data_types([1, 2, 3, 7, 8], 1)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Horas meditadas', response.data)
		# Horas meditadas nos últimos 7 dias

	def test_benefits_data_types_delete_all_datatypes_from_norte_europa(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.change_data_types([], 1)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Nenhum dado cadastrado.', response.data)

	def test_benefits_data_types_add_horas_delete_name_from_norte_europa(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.change_data_types(["2", "3", "7", "8"], 1)
		self.assertEqual(response.status_code, 200)
		self.assertNotIn(b'Nome', response.data)
		self.assertIn(b'Horas meditadas', response.data)
		# Horas meditadas nos últimos 7 dias


class TestBenefitsRegisterNewDataType(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf),
									follow_redirects=True)

	def register(self, name, example, idBenefit):
		return self.app.post('/beneficios/cadastro/dado/{}'.format(idBenefit), 
								data = dict(name = name, example = example),
								follow_redirects = True)

	def test_benefits_register_new_data_type_status_code_success(self):
		response = self.app.get("/beneficios/cadastro/dado/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_benefits_register_new_data_type_status_code_404(self):
		response = self.app.get("/beneficios/cadastro/dado/", follow_redirects=True)
		self.assertEqual(response.status_code, 404)
		self.assertIn(b'meme', response.data)
		# Error message made by meme generator

	def test_benefits_register_new_data_type_body_text(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/cadastro/dado/3", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Novo Tipo de Dado', response.data)

	def test_benefits_register_new_data_type_data_list(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/cadastro/dado/2", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Email', response.data)

	def test_benefits_register_new_data_type_benefit_doesnt_exist(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/cadastro/dado/999", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b' por favor selecione um bene', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_benefits_register_new_data_type_str_instead_of_id(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/cadastro/dado/nine", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b' por favor selecione um bene', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_benefits_register_new_data_type_empty_inputs(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.register("", "", 2) # Plano de Saúde Norte Europa
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'recisa preencher os dois campos', response.data)
		# Você precisa preencher os dois campos

	def test_benefits_register_new_data_type_one_empty(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.register("Signo", "", 2) # Plano de Saúde Norte Europa
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'recisa preencher os dois campos', response.data)
		# Você precisa preencher os dois campos

	def test_benefits_register_new_data_type_signo_success(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.register("Signo", "Ex. Aquário", 3) # Plano Dental Sorriso
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Signo', response.data)

	def test_benefits_register_new_data_type_signo_success(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.register("Cor Favorita", "Ex. Amarelo", 2) # Pampulha Intermédica
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Cor Favorita', response.data)



class TestBenefitsRegistrationCard(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf),
									follow_redirects=True)

	def test_benefits_registration_card_status_code_success(self):
		response = self.app.get("/beneficios/1/pessoas/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_benefits_registration_card_status_code_404(self):
		response = self.app.get("/beneficios/3/pessoas/", follow_redirects=True)
		self.assertEqual(response.status_code, 404)
		self.assertIn(b'meme', response.data)
		# Error message made by meme generator

	def test_benefits_registration_card_body_text(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/beneficios/1/pessoas/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Ficha de Cadastro de Pessoa da Wonka', response.data)
		# Plano de Saúde Norte Europa

	def test_benefits_registration_card_data_list_one(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/beneficios/3/pessoas/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'180', response.data)
		# Plano Dental Sorriso requests height in cm

	def test_benefits_registration_card_benefit_doesnt_exist(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/999/pessoas/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'o de Registro n', response.data)
		# Este Cartão de Registro não existe.

	def test_benefits_registration_card_both_ids_dont_exist(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/999/pessoas/999", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'o de Registro n', response.data)
		# Este Cartão de Registro não existe.

	def test_benefits_registration_card_str_instead_of_id(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("/beneficios/a/pessoas/a", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'o de Registro n', response.data)
		# Este Cartão de Registro não existe.


class TestBenefitsDeleteProfile(unittest.TestCase):
	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf),
									follow_redirects=True)

	def delete_benefit(self, idBenefit):
		return self.app.post('/beneficios/deletar', 
								data = dict(idBenefit = idBenefit),
								follow_redirects = True)


	def test_benefits_delete_profile_test_delete_norte_europa(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.delete_benefit(1) # Delete Norte Europa
		self.assertNotIn(b'Norte Europa', response.data)

	def test_benefits_delete_profile_test_delete_dental_sorriso(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.delete_benefit(3) # Delete Norte Europa
		self.assertNotIn(b'Plano Dental Sorriso', response.data)

	def test_benefits_delete_profile_test_delete_pampulha(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.delete_benefit(2) # Delete Pampulha Intermédica
		self.assertNotIn(b'Pampulha', response.data)






### PEOPLE
### PEOPLE
### PEOPLE
class TestPeopleHome(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf),
									follow_redirects=True)

	def test_people_home_status_code_success(self):
		response = self.app.get("/pessoas", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_people_home_to_login(self):
		response = self.app.get("/pessoas", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Login', response.data)

	def test_people_home_get_header(self):
		self.login("985.105.727-47") # Admin da Wonka
		response = self.app.get("/pessoas")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Tio Patinhas', response.data)

	def test_people_home_body_text(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'pessoas, fazer uma', response.data)
		# Você deseja cadastrar pessoas, fazer uma busca ou ver uma lista completa?



class TestPeopleList(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")



	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf), follow_redirects=True)

	def test_people_list_status_code_success(self):
		response = self.app.get("/pessoas/lista", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_people_list_to_login(self):
		response = self.app.get("/pessoas/lista", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Login', response.data)

	def test_people_list_get_header(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.app.get("/pessoas/lista")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Acme Co', response.data)

	def test_people_body_text(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.app.get("/pessoas/lista")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Clique no nome para ver o perfil.', response.data)

	def test_people_people_list_result_one(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.app.get("/pessoas/lista")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Pessoa da Acme', response.data)

	def test_people_people_list_result_two(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.app.get("/pessoas/lista")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Augusto Wozniak', response.data)



class TestPeopleSearch(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data=dict(cpf = cpf),
									follow_redirects=True)
	def search(self, name):
		return self.app.post('/pessoas/busca', 
						data=dict(name = name),
										follow_redirects=True)

	def test_people_search_status_code_success(self):
		response = self.app.get("/pessoas/busca", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_people_search_body_text(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/busca", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Busca por pessoas', response.data)

	def test_people_search_results_one(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.search("nando")
		self.assertIn(b'Fernando Augusto Rodrigues', response.data)

	def test_people_search_results_two(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.search("wONKa")
		self.assertIn(b'Pessoa da Wonka', response.data)
		# Plano de Saúde Pampulha Intermédica

	def test_people_search_results_not_found(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.search("000")
		self.assertIn(b'Nenhum resultado encontrado', response.data)

	def test_people_search_results_empty(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.search("")
		self.assertIn(b'Por favor insira um nome', response.data)



class TestPeopleRegistration(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")


	def login(self, cpf):
		return self.app.post('/login', data = dict(cpf = cpf),
									follow_redirects = True)

	def registration(self, name, cpf, benefits):
		return self.app.post('/pessoas/cadastro',
						data = dict(name = name, cpf = cpf,
									benefits = benefits),
									follow_redirects = True)

	def test_people_registration_status_code_success(self):
		response = self.app.get("pessoas/cadastro", follow_redirects = True)
		self.assertEqual(response.status_code, 200)

	def test_people_registration_body_text(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.app.get("pessoas/cadastro", follow_redirects = True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Cadastro Pessoa', response.data)

	def test_people_registration_benefits_are_present_one(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.app.get("pessoas/cadastro", follow_redirects = True)
		self.assertIn(b'Norte Europa', response.data)
		# Plano de Saúde Norte Europa

	def test_people_registration_benefits_are_present_two(self):
		self.login("985.105.727-47") # Admin da Tio Patinhas
		response = self.app.get("pessoas/cadastro", follow_redirects = True)
		self.assertIn(b'Pampulha', response.data)
		# Plano de Saúde Pampulha Intermédica

	def test_people_registration_empty_input(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.registration("", "", [])
		self.assertIn(b'Por favor insira um nome e um n', response.data)
		# Por favor insira um nome e um número de cpf válido

	def test_people_registration_cpf_not_valid(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.registration("Joana Augusta", "111.111.111-11", [])
		self.assertIn(b'Por favor insira um nome e um n', response.data)
		# Por favor insira um nome e um número de cpf válido

	def test_people_registration_new_person_no_benefits_one(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.registration("Mariana Farias", "588.338.356-42", [])
		self.assertIn(b'Mariana Farias', response.data)

	def test_people_registration_new_person_no_benefits_two(self):
		self.login("841.753.318-40") # Admin da Acme
		response = self.registration("Romulo Grazi", "871.175.293-93", [])
		self.assertIn(b'Romulo Grazi', response.data)

	def test_people_registration_new_person_benefit_norte_europa(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.registration("Barbara Zana", "132.423.300-13", ["1",])
		self.assertIn(b'Email', response.data)

	def test_people_registration_new_person_benefit_norte_europa_and_sorriso(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.registration("Bruno Brenildo", "691.181.649-19", ["1", 3])
		self.assertIn(b'Email', response.data)
		self.assertIn(b'Peso (kg)', response.data)


class TestPeopleDataRegistration(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data = dict(cpf = cpf),
									follow_redirects = True)

	def data_registration(self, idPerson, idDatatype, data_value):
		return self.app.post('/pessoas/cadastro/beneficio',
						data = dict(idPerson = idPerson, 
									idDatatype = idDatatype,
									data_value = data_value),
									follow_redirects = True)

	def test_people_data_registration_fernando_email(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.data_registration("5", ["8",], ["fer@email.com",]) # Fernando Augusto Rodrigues
		self.assertIn(b'fer@email.com', response.data)

	def test_people_data_registration_paula_altura_peso(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.data_registration(6, ["5", "6"], ["60","165"]) # Paula Macedo Gomes
		self.assertIn(b'60', response.data)
		self.assertIn(b'165', response.data)

	def test_people_data_registration_paula_data_not_filled(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.data_registration("4", ["4",], []) # Mariana Fagundes
		self.assertIn(b'Clique no plano selecionado e termine o cadastro.', response.data)

	def test_people_data_registration_admin_update_email(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.data_registration("1", ["5","6","8"], ["78","180","new@email.com"]) # Mariana Fagundes
		self.assertIn(b'78', response.data)
		self.assertIn(b'180', response.data)
		self.assertIn(b'new@email.com', response.data)


class TestPeopleProfile(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data = dict(cpf = cpf),
									follow_redirects = True)

	def test_people_profile_status_code_success(self):
		response = self.app.get("/pessoas/perfil/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_people_profile_status_code_404(self):
		response = self.app.get("/pessoas/perfil/", follow_redirects=True)
		self.assertEqual(response.status_code, 404)
		self.assertIn(b'meme', response.data)
		# Error message made by meme generator

	def test_people_profile_body_text(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/perfil/4", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Nenhum dado adicional cadastrado.', response.data)

	def test_people_profile_registered_benefit_dental_sorriso(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/perfil/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Plano Dental Sorriso', response.data)

	def test_people_profile_profile_doesnt_exist(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/perfil/999", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_people_profile_person_not_part_of_company(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/perfil/2", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_people_profile_id_is_not_a_number(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/perfil/two", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.


class TestPeopleEditBenefits(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data = dict(cpf = cpf),
									follow_redirects = True)

	def register_benefit(self, idBenefit, idWho):
		return self.app.post('/pessoas/editar/{}'.format(idWho),
						data = dict(idBenefit = idBenefit),
									follow_redirects = True)

	def test_people_edit_benefits_status_code_success(self):
		response = self.app.get("/pessoas/editar/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_people_edit_benefits_status_code_404(self):
		response = self.app.get("/pessoas/editar/", follow_redirects=True)
		self.assertEqual(response.status_code, 404)
		self.assertIn(b'meme', response.data)
		# Error message made by meme generator

	def test_people_edit_benefits_person_not_registered_to_any(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/editar/4", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Nenhum benef', response.data)
		# Nenhum benefício cadastrado :(

	def test_people_edit_benefits_registered_benefit_norte_europa(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/editar/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'name="idBenefit" value="3" checked', response.data)
		# Plano de Saúde Norte Europa idBenefit 1 checked

	def test_people_edit_benefits_profile_doesnt_exist(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/editar/999", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_people_edit_benefits_person_not_part_of_company(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/editar/2", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_people_edit_benefits_id_is_not_a_number(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/editar/two", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_people_edit_benefits_id_is_not_a_number(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/pessoas/editar/two", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)

	def test_people_edit_benefits_remove_dental_sorriso_from_admin_wonka(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.register_benefit([1,], 1)
		self.assertEqual(response.status_code, 200)
		self.assertNotIn(b'Plano Dental Sorriso', response.data)
		self.assertIn(b'Norte Europa', response.data)

	def test_people_edit_benefits_add_dental_sorriso_to_fernando_augusto(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.register_benefit([3,], 5)
		self.assertIn(b'Peso', response.data)



class TestPeopleEditData(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data = dict(cpf = cpf),
									follow_redirects = True)

	def test_people_edit_data_status_code_success(self):
		response = self.app.get("/dados/editar/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_people_edit_data_status_code_404(self):
		response = self.app.get("/dados/editar/", follow_redirects=True)
		self.assertEqual(response.status_code, 404)
		self.assertIn(b'meme', response.data)
		# Error message made by meme generator

	def test_people_edit_data_body_text(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/dados/editar/6", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Dados para Cadastro nos Benef', response.data)
		# Dados para Cadastro nos Benefícios Selecionados

	def test_people_edit_data_person_has_no_aditional_data(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/dados/editar/4", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'dados cadastrados ou para cadastro.', response.data)
		# Não há dados cadastrados ou para cadastro.

	def test_people_edit_data_registered_email(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/dados/editar/1", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'pessoa@wonka.com', response.data)

	def test_people_edit_data_profile_doesnt_exist(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/dados/editar/999", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_people_edit_data_person_not_part_of_company(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/dados/editar/9", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.

	def test_people_edit_data_id_is_not_a_number(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.app.get("/dados/editar/two", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Este perfil n', response.data)
		# Este perfil não existe, por favor selecione um benefício da lista.



class TestPeopleDeleteProfile(unittest.TestCase):

	def setUp(self):
		call("./setup/start_testing.sh")
		self.app = app.test_client()

	def tearDown(self):
		self.app.get("/logout", follow_redirects=True)
		call("./setup/finish_testing.sh")

	def login(self, cpf):
		return self.app.post('/login', data = dict(cpf = cpf),
									follow_redirects = True)

	def delete_person(self, idPerson):
		return self.app.post('/pessoas/deletar', 
								data = dict(idPerson = idPerson),
								follow_redirects = True)


	def test_benefits_delete_profile_test_delete_admin_wonka_fail(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.delete_person(1) # Delete Pessoa da Wonka
		self.assertIn(b'o pode ser deletado, por favor selecione', response.data)
		# Este perfil não pode ser deletado, por favor selecione outra pessoa da lista.

	def test_benefits_delete_profile_test_delete_mariana_fagundes_success(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.delete_person(4) # Delete Mariana Fagundes
		self.assertNotIn(b'Mariana Fagundes', response.data)

	def test_benefits_delete_profile_test_delete_fernando_augusto_success(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.delete_person(5) # Delete Fernando Augusto
		self.assertNotIn(b'Fernando Augusto Rodrigues', response.data)

	def test_benefits_delete_profile_test_delete_paula_macedo_success(self):
		self.login("230.841.911-31") # Admin da Wonka
		response = self.delete_person(6) # Delete Paula Macedo Gomes
		self.assertNotIn(b'Paula Macedo Gomes', response.data)





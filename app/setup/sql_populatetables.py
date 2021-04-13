import sqlite3
import csv
import time

def populate_empresa(db):
	print("Populating empresa...")
	with open("data/empresas.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			nome = row["nome"]
			db.execute("""INSERT INTO empresa 
						(nome) 
						VALUES (:nome)""",
						{"nome": nome})
			time.sleep(2) # sleep para que o timestamp seja diferente
	print("Empresa populated")

def populate_colaborador(db):
	print("Populating colaborador...")
	with open("data/colaboradores.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			id_empresa = row["id_empresa"]
			nome = row["nome"]
			cpf = row["cpf"]
			ativo = row["ativo"]
			db.execute("""INSERT INTO colaborador 
						(id_empresa, nome, cpf, ativo) 
						VALUES (:id_empresa, :nome, :cpf, :ativo)""",
						{"id_empresa": id_empresa, "nome": nome, "cpf": cpf, 
						"ativo": ativo})
			time.sleep(2)
	print("Colaborador populated")

def populate_admin(db):
	print("Populating admin...")
	with open("data/admin.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			id_empresa = row["id_empresa"]
			id_colaborador = row["id_colaborador"]
			nivel = row["nivel"]
			db.execute("""INSERT INTO admin 
						(id_empresa, id_colaborador, nivel) 
						VALUES (:id_empresa, :id_colaborador, :nivel)""",
						{"id_empresa": id_empresa, "id_colaborador": id_colaborador,
						"nivel": nivel})
	print("Admin populated")

def populate_beneficio(db):
	print("Populating beneficio...")
	with open("data/beneficios.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			nome = row["nome"]
			db.execute("""INSERT INTO beneficio 
						(nome) 
						VALUES (:nome)""",
						{"nome": nome})
	print("Beneficio populated")

def populate_tipo_de_dado(db):
	print("Populating tipo de dado...")
	with open("data/tipos_de_dados.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			nome = row["nome"]
			db.execute("""INSERT INTO tipo_de_dado 
						(nome) 
						VALUES (:nome)""",
						{"nome": nome})
	print("Tipo de dado populated")

if __name__ == '__main__':
	con = sqlite3.connect(r"../db/pipo.db")
	cur = con.cursor()
	#populate_beneficio(cur)
	#populate_empresa(cur)
	#populate_colaborador(cur)
	#populate_admin(cur)
	populate_tipo_de_dado(cur)
	con.commit()
	con.close()

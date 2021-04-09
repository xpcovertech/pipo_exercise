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

if __name__ == '__main__':
    con = sqlite3.connect(r"../db/pipo.db")
    cur = con.cursor()
#    populate_empresa(cur)
#    populate_colaborador(cur)
    populate_admin(cur)
    con.commit()
    con.close()

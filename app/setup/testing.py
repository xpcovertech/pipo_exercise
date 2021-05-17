import sqlite3
from sqlite3 import Error
import sqlite3
import csv


def populate_company(db):
	with open("./setup/data/company.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			db.execute("""INSERT INTO company 
						(name) 
						VALUES (:name)""",
						{"name": name})

def populate_person(db):
	with open("./setup/data/person.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idCompany = row["idCompany"]
			name = row["name"]
			cpf = row["cpf"]
			db.execute("""INSERT INTO person 
						(idCompany, name, cpf) 
						VALUES (:idCompany, :name, :cpf)""",
						{"idCompany": idCompany, "name": name, "cpf": cpf})

def populate_admin(db):
	with open("./setup/data/admin.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idCompany = row["idCompany"]
			idPerson = row["idPerson"]
			level = row["level"]
			db.execute("""INSERT INTO admin 
						(idCompany, idPerson, level) 
						VALUES (:idCompany, :idPerson, :level)""",
						{"idCompany": idCompany, "idPerson": idPerson,
						"level": level})

def populate_benefit(db):
	with open("./setup/data/benefit.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			db.execute("""INSERT INTO benefit 
						(name) 
						VALUES (:name)""",
						{"name": name})

def populate_datatype(db):
	with open("./setup/data/datatype.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			example = row["example"]
			db.execute("""INSERT INTO datatype 
						(name, example) 
						VALUES (:name, :example)""",
						{"name": name, "example": example})

def populate_company_benefit(db):
	with open("./setup/data/company_benefit.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idCompany = row["idCompany"]
			idBenefit = row["idBenefit"]
			db.execute("""INSERT INTO companyBenefit
						(idCompany, idBenefit) 
						VALUES (:idCompany, :idBenefit)""",
						{"idBenefit": idBenefit, "idCompany": idCompany})

def populate_benefit_datatype(db):
	with open("./setup/data/benefit_datatype.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idBenefit = row["idBenefit"]
			idDatatype = row["idDatatype"]
			db.execute("""INSERT INTO benefitData
						(idBenefit, idDatatype) 
						VALUES (:idBenefit, :idDatatype)""",
						{"idBenefit": idBenefit, "idDatatype": idDatatype})

def populate_person_benefit(db):
	with open("./setup/data/person_benefit.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idPerson = row["idPerson"]
			idBenefit = row["idBenefit"]
			db.execute("""INSERT INTO personBenefit
						(idPerson, idBenefit) 
						VALUES (:idPerson, :idBenefit)""",
						{"idPerson": idPerson, "idBenefit": idBenefit})

def populate_person_data(db):
	with open("./setup/data/person_data.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idPerson = row["idPerson"]
			idDatatype = row["idDatatype"]
			data = row["data"]
			db.execute("""INSERT INTO personData
						(idPerson, idDatatype, data) 
						VALUES (:idPerson, :idDatatype, :data)""",
						{"idPerson": idPerson, "idDatatype": idDatatype,
						"data": data})

def create_sysadmin_tables(db):
	db.execute("""CREATE TABLE IF NOT EXISTS company
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) NOT NULL,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS person
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	idCompany INTEGER NOT NULL,
	name VARCHAR(255) NOT NULL,
	cpf VARCHAR(14) NOT NULL,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (idCompany) REFERENCES company(id))
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS admin
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	idCompany INTEGER NOT NULL,
	idPerson INTEGER NOT NULL,
	level INTEGER NOT NULL,
	FOREIGN KEY (idCompany) REFERENCES company(id),
	FOREIGN KEY (idPerson) REFERENCES person(id))
	""")

def create_pipo_tables(db):
	db.execute("""CREATE TABLE IF NOT EXISTS benefit
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255) NOT NULL,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS datatype
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(100) NOT NULL,
	example VARCHAR(144) NOT NULL)
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS benefitData
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	idBenefit INTEGER NOT NULL,
	idDatatype INTEGER NOT NULL,
	FOREIGN KEY (idBenefit) REFERENCES benefit(id),
	FOREIGN KEY (idDatatype) REFERENCES datatype(id))
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS personBenefit
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	idPerson INTEGER NOT NULL,
	idBenefit INTEGER NOT NULL,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (idPerson) REFERENCES person(id),
	FOREIGN KEY (idBenefit) REFERENCES benefit(id))
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS personData
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	idPerson INTEGER NOT NULL,
	idDatatype INTEGER NOT NULL,
	data VARCHAR(255) NOT NULL,
	FOREIGN KEY (idPerson) REFERENCES person(id),
	FOREIGN KEY (idDatatype) REFERENCES datatype(id))
	""")

def create_benefit_company_table(db):
	db.execute("""CREATE TABLE IF NOT EXISTS companyBenefit
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	idCompany INTEGER NOT NULL,
	idBenefit INTEGER NOT NULL,
	FOREIGN KEY (idCompany) REFERENCES company(id),
	FOREIGN KEY (idBenefit) REFERENCES benefit(id))
	""")

def create_connection(db_file):
    """ create a database connection to SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("Error creating database.")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
	create_connection(r"./db/pipo.db")
	con = sqlite3.connect(r"./db/pipo.db")
	cur = con.cursor()
	create_sysadmin_tables(cur)
	create_pipo_tables(cur)
	create_benefit_company_table(cur)
	con.commit()
	populate_company(cur)
	populate_person(cur)
	populate_admin(cur)
	populate_benefit(cur)
	populate_datatype(cur)
	populate_company_benefit(cur)
	populate_benefit_datatype(cur)
	populate_person_benefit(cur)
	populate_person_data(cur)
	con.commit()
	con.close()

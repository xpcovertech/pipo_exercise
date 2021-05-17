import sqlite3

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

if __name__ == '__main__':
	con = sqlite3.connect(r"../db/pipo.db")
	cur = con.cursor()
	create_sysadmin_tables(cur)
	create_pipo_tables(cur)
	create_benefit_company_table(cur)
	con.commit()
	con.close()

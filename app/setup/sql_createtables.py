import sqlite3

def create_sysadmin_tables(db):
	print("Creating systemadmin tables...")
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
	(idCompany INTEGER NOT NULL,
	idPerson INTEGER NOT NULL,
	level INTEGER NOT NULL,
	FOREIGN KEY (idCompany) REFERENCES company(id),
	FOREIGN KEY (idPerson) REFERENCES person(id))
	""")
	print("Tables Created!")

def create_pipo_tables(db):
	print("Creating pipo tables...")
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
	(idBenefit INTEGER NOT NULL,
	idDatatype INTEGER NOT NULL,
	FOREIGN KEY (idBenefit) REFERENCES benefit(id),
	FOREIGN KEY (idDatatype) REFERENCES datatype(id))
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS personBenefit
	(idPerson INTEGER NOT NULL,
	idBenefit INTEGER NOT NULL,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (idPerson) REFERENCES person(id),
	FOREIGN KEY (idBenefit) REFERENCES benefit(id))
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS personData
	(idPerson INTEGER NOT NULL,
	idDatatype INTEGER NOT NULL,
	data VARCHAR(255) NOT NULL,
	FOREIGN KEY (idPerson) REFERENCES person(id),
	FOREIGN KEY (idDatatype) REFERENCES datatype(id))
	""")
	print("Tables Created!")

def create_benefit_company_table(db):
	print("Creating benefit - company table...")
	db.execute("""CREATE TABLE IF NOT EXISTS companyBenefit
	(idCompany INTEGER NOT NULL,
	idBenefit INTEGER NOT NULL,
	FOREIGN KEY (idCompany) REFERENCES company(id),
	FOREIGN KEY (idBenefit) REFERENCES benefit(id))
	""")
	print("Table Created!")

if __name__ == '__main__':
	con = sqlite3.connect(r"../db/pipo.db")
	cur = con.cursor()
	create_sysadmin_tables(cur)
	create_pipo_tables(cur)
	create_benefit_company_table(cur)
	con.commit()
	con.close()

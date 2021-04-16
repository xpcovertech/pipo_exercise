import sqlite3
import csv
import time

def populate_company(db):
	print("Populating company... time.sleep(2)")
	with open("data/company.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			db.execute("""INSERT INTO company 
						(name) 
						VALUES (:name)""",
						{"name": name})
			time.sleep(1) # sleep para que o timestamp seja diferente
	print("Company populated!")

def populate_person(db):
	print("Populating person... time.sleep(1)")
	with open("data/person.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idCompany = row["idCompany"]
			name = row["name"]
			cpf = row["cpf"]
			db.execute("""INSERT INTO person 
						(idCompany, name, cpf) 
						VALUES (:idCompany, :name, :cpf)""",
						{"idCompany": idCompany, "name": name, "cpf": cpf})
			time.sleep(1)
	print("Person populated!")

def populate_admin(db):
	print("Populating admin...")
	with open("data/admin.csv", "r") as data:
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
	print("Admin populated!")

def populate_benefit(db):
	print("Populating benefit...")
	with open("data/benefit.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			db.execute("""INSERT INTO benefit 
						(name) 
						VALUES (:name)""",
						{"name": name})
	print("Benefit populated!")

def populate_datatype(db):
	print("Populating datatype...")
	with open("data/datatype.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			example = row["example"]
			db.execute("""INSERT INTO datatype 
						(name, example) 
						VALUES (:name, :example)""",
						{"name": name, "example": example})
	print("Datatype populated!")

def populate_company_benefit(db):
	print("Populating company_benefit...")
	with open("data/company_benefit.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idCompany = row["idCompany"]
			idBenefit = row["idBenefit"]
			db.execute("""INSERT INTO companyBenefit
						(idCompany, idBenefit) 
						VALUES (:idCompany, :idBenefit)""",
						{"idBenefit": idBenefit, "idCompany": idCompany})
	print("Company_benefit populated!")

def populate_benefit_datatype(db):
	print("Populating benefit datatype...")
	with open("data/benefit_datatype.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idBenefit = row["idBenefit"]
			idDatatype = row["idDatatype"]
			db.execute("""INSERT INTO benefitData
						(idBenefit, idDatatype) 
						VALUES (:idBenefit, :idDatatype)""",
						{"idBenefit": idBenefit, "idDatatype": idDatatype})
	print("Benefit datatype populated!")

if __name__ == '__main__':
	con = sqlite3.connect(r"../db/pipo.db")
	cur = con.cursor()
	populate_company(cur)
	populate_person(cur)
	populate_admin(cur)
	populate_benefit(cur)
	populate_datatype(cur)
	populate_company_benefit(cur)
	populate_benefit_datatype(cur)
	con.commit()
	con.close()

import sqlite3
import csv

def populate_company(db):
	with open("data/company.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			db.execute("""INSERT INTO company 
						(name) 
						VALUES (:name)""",
						{"name": name})

def populate_person(db):
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

def populate_admin(db):
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

def populate_benefit(db):
	with open("data/benefit.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			db.execute("""INSERT INTO benefit 
						(name) 
						VALUES (:name)""",
						{"name": name})

def populate_datatype(db):
	with open("data/datatype.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			name = row["name"]
			example = row["example"]
			db.execute("""INSERT INTO datatype 
						(name, example) 
						VALUES (:name, :example)""",
						{"name": name, "example": example})

def populate_company_benefit(db):
	with open("data/company_benefit.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idCompany = row["idCompany"]
			idBenefit = row["idBenefit"]
			db.execute("""INSERT INTO companyBenefit
						(idCompany, idBenefit) 
						VALUES (:idCompany, :idBenefit)""",
						{"idBenefit": idBenefit, "idCompany": idCompany})

def populate_benefit_datatype(db):
	with open("data/benefit_datatype.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idBenefit = row["idBenefit"]
			idDatatype = row["idDatatype"]
			db.execute("""INSERT INTO benefitData
						(idBenefit, idDatatype) 
						VALUES (:idBenefit, :idDatatype)""",
						{"idBenefit": idBenefit, "idDatatype": idDatatype})

def populate_person_benefit(db):
	with open("data/person_benefit.csv", "r") as data:
		reader = csv.DictReader(data)
		for row in reader:
			idPerson = row["idPerson"]
			idBenefit = row["idBenefit"]
			db.execute("""INSERT INTO personBenefit
						(idPerson, idBenefit) 
						VALUES (:idPerson, :idBenefit)""",
						{"idPerson": idPerson, "idBenefit": idBenefit})

def populate_person_data(db):
	with open("data/person_data.csv", "r") as data:
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
	populate_person_benefit(cur)
	populate_person_data(cur)
	con.commit()
	con.close()

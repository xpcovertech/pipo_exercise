import sqlite3

con = sqlite3.connect(r"./db/pipo.db")
cur = con.cursor()
db = cur

def get_all_from(table, where, data):
	got_all = db.execute("""SELECT * FROM {} WHERE {} = :{}""".format(table, where, where),
					{"{}".format(where): data}).fetchall()
	return got_all

def get_people(idCompany):
	people = db.execute("""SELECT * FROM person WHERE idCompany = :idCompany 
								ORDER BY name""", {"idCompany": idCompany}).fetchall()
	return people

result = get_people(1)
resul2 = get_all_from("person", "idCompany", "1")

#print(result[0][2])
#print(resul2[0][2])

def is_it_bad(string):
	if not string.isalpha() and not string.isdigit():
		raise ValueError
	print("PASS: {}".format(string))

lista = ["123454", "Hello", "12345", "eita_"]

for item in lista:
	is_it_bad(item)

print("FIM")


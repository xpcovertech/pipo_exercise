import sqlite3

def create_sysadmin_tables(db):
	print("Creating tables...")

	db.execute("""CREATE TABLE IF NOT EXISTS empresa
   				(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   				nome VARCHAR(255) NOT NULL,
   				timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
   				""")

	db.execute("""CREATE TABLE IF NOT EXISTS colaborador
   				(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   				id_empresa INTEGER NOT NULL,
   				nome VARCHAR(255) NOT NULL,
   				cpf VARCHAR(11) NOT NULL,
   				ativo VARCHAR(1) NOT NULL,
   				timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
   				""")

	db.execute("""CREATE TABLE IF NOT EXISTS admin
   				(id_empresa INTEGER NOT NULL,
   				id_colaborador INTEGER NOT NULL,
   				nivel INTEGER NOT NULL,
   				FOREIGN KEY (id_empresa) REFERENCES empresa(id),
   				FOREIGN KEY (id_colaborador) REFERENCES colaborador(id))
   				""")

	print("Tables Created!")

if __name__ == '__main__':
    con = sqlite3.connect(r"../db/pipo.db")
    cur = con.cursor()
    create_sysadmin_tables(cur)
    con.commit()
    con.close()

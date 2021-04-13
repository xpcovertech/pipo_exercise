import sqlite3

def create_sysadmin_tables(db):
	print("Creating systemadmin tables...")
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

def create_pipo_tables(db):
	print("Creating pipo tables...")
	db.execute("""CREATE TABLE IF NOT EXISTS beneficio
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nome VARCHAR(255) NOT NULL,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS tipo_de_dado
	(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nome VARCHAR(100) NOT NULL)
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS dado_beneficio
	(id_beneficio INTEGER NOT NULL,
	id_tipo_de_dado INTEGER NOT NULL,
	FOREIGN KEY (id_beneficio) REFERENCES beneficio(id),
	FOREIGN KEY (id_tipo_de_dado) REFERENCES tipo_de_dado(id))
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS beneficio_colaborador
	(id_colaborador INTEGER NOT NULL,
	id_beneficio INTEGER NOT NULL,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (id_colaborador) REFERENCES colaborador(id),
	FOREIGN KEY (id_beneficio) REFERENCES beneficio(id))
	""")
	db.execute("""CREATE TABLE IF NOT EXISTS dado_colaborador
	(id_colaborador INTEGER NOT NULL,
	id_tipo_de_dado INTEGER NOT NULL,
	dado VARCHAR(255) NOT NULL,
	FOREIGN KEY (id_colaborador) REFERENCES colaborador(id),
	FOREIGN KEY (id_tipo_de_dado) REFERENCES tipo_de_dado(id))
	""")
	print("Tables Created!")

def create_beneficio_empresa_table(db):
	print("Creating beneficio - empresa table...")
	db.execute("""CREATE TABLE IF NOT EXISTS beneficio_empresa
	(id_empresa INTEGER NOT NULL,
	id_beneficio INTEGER NOT NULL,
	FOREIGN KEY (id_empresa) REFERENCES empresa(id),
	FOREIGN KEY (id_beneficio) REFERENCES beneficio(id))
	""")
	print("Table Created!")

if __name__ == '__main__':
	con = sqlite3.connect(r"../db/pipo.db")
	cur = con.cursor()
	#create_sysadmin_tables(cur)
	#create_pipo_tables(cur)
	create_beneficio_empresa_table(cur)
	con.commit()
	con.close()

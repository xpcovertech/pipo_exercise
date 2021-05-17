#!/bin/sh

echo "Starting..."
echo "Deleting old database..."
rm ../db/pipo.db
echo "Old database deleted!"
echo "Creating new database file..."
python3 createdb.py
echo "New database created!"
echo "Creating tables..."
python3 sql_createtables.py
echo "Tables Created!"
echo "Populating tables..."
python3 sql_populatetables.py
echo "Tables populated!"
echo "Done!"

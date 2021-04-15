echo "Starting..."
rm ../db/pipo.db
echo "Old database deleted."
python3 dont_createdb.py
python3 sql_createtables.py
python3 sql_populatetables.py
echo "Done!"

sleep 30 # Need time for postgesql server to create database and start to accept TCP connections
echo "Filling DB with values..."
python /usr/src/app/fill_db.py
echo "Starting server..."
python /usr/src/app/app.py

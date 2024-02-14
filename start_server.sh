sleep 60 # Need time for postgesql server to create database and start to accept TCP connections
python /usr/src/app/fill_db.py
python /usr/src/app/app.py

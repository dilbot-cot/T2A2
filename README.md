# T2A2



python3 -m venv venv && source venv/bin/activate

Create the database
open psql in terminal
CREATE DATABASE <database_name>;

Create an admin user
CREATE USER <user_name> WITH PASSWORD '<yourpassword>';

Grant all permissions
GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <user_name>;
GRANT ALL ON SCHEMA public TO <user_name>;

exit psql with \q
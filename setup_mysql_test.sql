--Create test database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

--Create test user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

--Grant privileges
GRANT ALL PRIVILEGES  ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

--Grant select privilege on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

--Flush everything to apply
FLUSH PRIVILEGES;

--setup development database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

--create user
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

--grant priviledges
GRANT ALL  ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

--grant select privilege on prformance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

FLUSH PRIVILEGES;

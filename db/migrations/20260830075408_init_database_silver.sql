-- migrate:up
CREATE DATABASE IF NOT EXISTS silver;

-- migrate:down
DROP DATABASE IF EXISTS silver; 


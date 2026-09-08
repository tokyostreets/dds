-- migrate:up
CREATE DATABASE IF NOT EXISTS gold;

-- migrate:down
DROP DATABASE IF EXISTS gold; 

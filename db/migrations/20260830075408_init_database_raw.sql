-- migrate:up
CREATE DATABASE IF NOT EXISTS raw;

-- migrate:down
DROP DATABASE IF EXISTS raw; 

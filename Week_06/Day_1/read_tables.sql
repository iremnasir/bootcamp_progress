-- Run this as:
--psql -U iremn -f shippers.sql -d northwind                              


-- Delete the shippers table if it already exists

DROP TABLE shippers;

-- CREATE THE TABLE

CREATE TABLE shippers(

  shipperid SERIAL PRIMARY KEY,
  company_name VARCHAR(100),
  phone VARCHAR(20)
);

-- INSERT THE DATA

COPY shippers FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/shippers.csv'
 DELIMITER ',' CSV HEADER;

 -- Delete categories table if it exists

 DROP TABLE categories;

 -- CREATE the table

 CREATE TABLE categories(
   categoryid SERIAL PRIMARY KEY,
   category_name VARCHAR(20),
   description VARCHAR(100),
   picture VARCHAR(256)
 );

 -- INSERT DATA

COPY categories FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/categories.csv'
DELIMITER ',' CSV HEADER;

-- Delete customers table if it exists

DROP TABLE customers;

CREATE TABLE customers(
  customer_id CHAR(5) NOT NULL,
  company_name VARCHAR(40),
  contact_name VARCHAR(40),
  contact_title VARCHAR(40),
  address VARCHAR(100),
  city CHAR(30),
  region CHAR(20),
  postal_code VARCHAR(10),
  country VARCHAR(20),
  phone VARCHAR(20),
  fax VARCHAR(20)
);

-- INSERT DATA

COPY customers FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/customers.csv'
DELIMITER ',' CSV HEADER;

-- ALTER TABLE
ALTER TABLE customers
ADD COLUMN id SERIAL PRIMARY KEY;

-- Delete Employee Territories if exists
DROP TABLE employee_territories;

CREATE TABLE employee_territories(
  employee_id INT NOT NULL,
  territory_id INT NOT NULL
);
-- INSERT DATA

COPY employee_territories FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/employee_territories.csv'
DELIMITER ',' CSV HEADER;

-- ALTER TABLE
ALTER TABLE employee_territories
ADD COLUMN id SERIAL PRIMARY KEY;

-- Delete Employee Territories if exists
DROP TABLE employees;

CREATE TABLE employees(
  employee_id INT NOT NULL,
  last_name CHAR(10) NOT NULL,
  first_name CHAR(10) NOT NULL,
  title VARCHAR(30),
  title_of_courtesy VARCHAR(5),
  birth_date TIMESTAMP,
  hire_date TIMESTAMP,
  address VARCHAR(40),
  city CHAR(30),
  region CHAR(20),
  postal_code VARCHAR(10),
  country VARCHAR(5),
  home_phone VARCHAR(20),
  extension INT NOT NULL,
  photo VARCHAR(256),
  notes VARCHAR(256),
  reports_to REAL NULL,
  photo_path VARCHAR(60)
);
-- INSERT DATA

COPY employees FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/employees_modified.csv'
DELIMITER ',' CSV HEADER;

-- Delete order_details table if it exists
DROP TABLE order_details;

CREATE TABLE order_details(
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  unit_price REAL NOT NULL,
  quantity INT NOT NULL,
  discount REAL
);

-- INSERT DATA

COPY order_details FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/order_details.csv'
DELIMITER ',' CSV HEADER;
-- ALTER TABLE
ALTER TABLE order_details
ADD COLUMN id SERIAL PRIMARY KEY;

-- Delete orders table if it exists
DROP TABLE orders;

CREATE TABLE orders(
  order_id INT NOT NULL,
  customer_id VARCHAR(5),
  employee_id INT NOT NULL,
  order_date TIMESTAMP,
  required_date TIMESTAMP,
  shipped_date TIMESTAMP,
  ship_via INT,
  freight REAL,
  ship_name VARCHAR(50),
  ship_address VARCHAR(100),
  ship_city VARCHAR(20),
  ship_region VARCHAR(20),
  ship_pc VARCHAR(15),
  ship_country VARCHAR(15)
);

-- INSERT DATA

COPY orders FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/orders_modified.csv'
DELIMITER ',' CSV HEADER;

-- Delete products table if it exists
DROP TABLE products;

CREATE TABLE products(
  product_id INT NOT NULL,
  product_name VARCHAR(50),
  supplier_id INT NOT NULL,
  category_id INT NOT NULL,
  qpu VARCHAR(50),
  unit_price REAL,
  units_in_stock INT,
  units_on_order INT,
  reorder_level INT,
  discontinued BOOLEAN
);

-- Insert DATA
COPY products FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/products.csv'
DELIMITER ',' CSV HEADER;

-- Delete regions table if it exists
DROP TABLE regions;

CREATE TABLE regions(
  region_id INT NOT NULL,
  region_description VARCHAR(10)
);

-- Insert DATA
COPY regions FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/regions.csv'
DELIMITER ',' CSV HEADER;

-- Delete suppliers table if it exists
DROP TABLE suppliers;

CREATE TABLE suppliers(
  supplier_id INT NOT NULL,
  company_name VARCHAR(50),
  contact_name VARCHAR(40),
  contact_title VARCHAR(40),
  address VARCHAR(100),
  city VARCHAR(20),
  region VARCHAR(15),
  postal_code VARCHAR(15),
  country VARCHAR(15),
  phone VARCHAR(20),
  fax VARCHAR(20),
  home_page VARCHAR(100)
);

-- Insert DATA
COPY suppliers FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/suppliers.csv'
DELIMITER ',' CSV HEADER;

--Delete Territories if it exists
DROP TABLE territories;

CREATE TABLE territories(
  territory_id INT NOT NULL,
  territory_description VARCHAR(20),
  region_id INT NOT NULL
);

-- Insert DATA
COPY territories FROM
'/Users/iremn/PythonClass/Spiced/Personal_Projects/Northwind/northwind_data_clean/data/territories.csv'
DELIMITER ',' CSV HEADER;

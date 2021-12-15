CREATE TABLE IF NOT EXISTS
customer (cust_id VARCHAR(255) NOT NULL, -- both local and foreigner can buy cars in SG
           cust_name  VARCHAR(255) NOT NULL,
           cust_birth_date DATE,
           cust_gender_code CHAR(2) NOT NULL,
           cust_phone_num VARCHAR(255) NOT NULL,
           cust_address VARCHAR(255),
           cust_postal_code VARCHAR(255) NOT NULL,
           PRIMARY KEY (cust_id)
         );

CREATE TABLE IF NOT EXISTS
salesperson (salesperson_id VARCHAR(255) NOT NULL, --can extract from employee system
             salesperson_name VARCHAR(255) NOT NULL,
             salesperson_phone_num VARCHAR(255) NOT NULL,
             PRIMARY KEY (salesperson_id)
           );


 CREATE TABLE IF NOT EXISTS
 manufacturer (manufacturer_code VARCHAR(255) NOT NULL,
               manufacturer_name VARCHAR(255) NOT NULL,
               manufacturer_location VARCHAR (255) NOT NULL,
               PRIMARY KEY (manufacturer_code)
             );

 CREATE TABLE IF NOT EXISTS
 car (car_serial_num VARCHAR(255) NOT NULL,
       car_manufacturer_code VARCHAR(255) NOT NULL, -- fk
       car_model_name VARCHAR(255),
       car_weight_in_kg NUMERIC(10,2),
       car_colour VARCHAR(255),
       car_unit_price NUMERIC(10,2) NOT NULL,
       record_created_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       record_updated_datetime TIMESTAMP DEFAULT NULL,
       PRIMARY KEY (car_serial_num),
       CONSTRAINT fk_car_manufacturer_manufacturer_code FOREIGN KEY (car_manufacturer_code) REFERENCES manufacturer (manufacturer_code)
     );

-- ALTER TABLE car
--  ADD CONSTRAINT fk_car_manufacturer_manufacturer_code FOREIGN KEY (car_manufacturer_code) REFERENCES manufacturer (manufacturer_code);


CREATE TABLE IF NOT EXISTS
sales_order (sales_order_id BIGSERIAL NOT NULL, -- INT GENERATED ALWAYS AS IDENTITY (PostgreSQL 10 onwards)
              sales_order_customer_id VARCHAR(255) NOT NULL, --fk
              sales_order_salesperson_id VARCHAR(255) NOT NULL, --fk
              sales_order_total_amt NUMERIC(10,2) NULL,
              sales_order_date DATE NOT NULL DEFAULT CURRENT_DATE,
              record_created_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              record_updated_datetime TIMESTAMP DEFAULT NULL,
              PRIMARY KEY (sales_order_id),
              CONSTRAINT fk_sales_order_customer_customer_id FOREIGN KEY (sales_order_customer_id) REFERENCES customer (cust_id),
              CONSTRAINT fk_sales_order_salesperson_salesperson_id FOREIGN KEY (sales_order_salesperson_id) REFERENCES salesperson (salesperson_id)
            );

--ALTER TABLE sales_or bbvder
  --RENAME COLUMN sales_order_sales_total_amt TO sales_order_total_amt;

-- ALTER TABLE sales_order
--   ADD CONSTRAINT fk_sales_order_customer_customer_id FOREIGN KEY (sales_order_customer_id) REFERENCES customer (cust_id);
--
-- ALTER TABLE sales_order
--   ADD CONSTRAINT fk_sales_order_salesperson_salesperson_id FOREIGN KEY (sales_order_salesperson_id) REFERENCES salesperson (salesperson_id);

CREATE TABLE IF NOT EXISTS
sales_order_detail (sales_order_detail_id BIGSERIAL NOT NULL,
                     sales_order_detail_sales_order_id BIGSERIAL NOT NULL, --fk
                     sales_order_detail_car_serial_num VARCHAR(255) NOT NULL, -- fk
                     sales_order_detail_car_unit_price NUMERIC(10,2) NOT NULL,
                     sales_order_detail_qty INT NOT NULL,
                     PRIMARY KEY (sales_order_detail_id),
                     CONSTRAINT fk_sales_order_detail_sales_order_sales_order_id FOREIGN KEY (sales_order_detail_sales_order_id) REFERENCES sales_order (sales_order_id),
                     CONSTRAINT fk_sales_order_detail_car_car_serial_num FOREIGN KEY (sales_order_detail_car_serial_num) REFERENCES car (car_serial_num)
                   );

 --ALTER TABLE sales_order_detail
   --RENAME COLUMN Quantity TO sales_order_detail_qty;

--ALTER TABLE sales_order_detail
--DROP COLUMN sales_order_detail_sub_total;

-- ALTER TABLE sales_order_detail
--   ADD CONSTRAINT fk_sales_order_detail_sales_order_sales_order_id FOREIGN KEY (sales_order_detail_sales_order_id) REFERENCES sales_order (sales_order_id);
--
-- ALTER TABLE sales_order_detail
--   ADD CONSTRAINT fk_sales_order_detail_car_car_serial_num FOREIGN KEY (sales_order_detail_car_serial_num) REFERENCES car (car_serial_num);

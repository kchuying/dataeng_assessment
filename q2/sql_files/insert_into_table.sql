COPY customer(cust_id, cust_name, cust_birth_date, cust_gender_code, cust_phone_num, cust_address, cust_postal_code)
FROM '/store_files_psql/customer.csv'
DELIMITER ','
CSV HEADER;

COPY salesperson(salesperson_id, salesperson_name, salesperson_phone_num)
FROM '/store_files_psql/salesperson.csv'
DELIMITER ','
CSV HEADER;

COPY manufacturer(manufacturer_code, manufacturer_name, manufacturer_location)
FROM '/store_files_psql/manufacturer.csv'
DELIMITER ','
CSV HEADER;

COPY car (car_serial_num, car_manufacturer_code, car_model_name, car_weight_in_kg, car_colour, car_unit_price)
FROM '/store_files_psql/car.csv'
DELIMITER ','
CSV HEADER;

COPY sales_order (sales_order_customer_id, sales_order_salesperson_id, sales_order_total_amt)
FROM '/store_files_psql/sales_order.csv'
DELIMITER ','
CSV HEADER;

COPY sales_order_detail (sales_order_detail_sales_order_id, sales_order_detail_car_serial_num, sales_order_detail_car_unit_price, sales_order_detail_qty)
FROM '/store_files_psql/sales_order_detail.csv'
DELIMITER ','
CSV HEADER;

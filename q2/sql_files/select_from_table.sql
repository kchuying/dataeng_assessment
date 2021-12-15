SELECT c.cust_id,c.cust_name, sum(d.sales_order_detail_car_unit_price) as total_spending
FROM sales_order_detail d
LEFT JOIN sales_order o
ON d.sales_order_detail_sales_order_id = o.sales_order_id
LEFT JOIN customer c
ON c.cust_id = o.sales_order_customer_id
GROUP BY c.cust_id;

SELECT c.cust_id, c.cust_name, sum(o.sales_order_total_amt) as total_spending
FROM sales_order o
LEFT JOIN customer c
ON c.cust_id = o.sales_order_customer_id
GROUP BY c.cust_id;

----

SELECT m.manufacturer_name, SUM(d.sales_order_detail_qty) as qty_sold
FROM sales_order_detail d
LEFT JOIN sales_order o
ON d.sales_order_detail_sales_order_id = o.sales_order_id
LEFT JOIN car c
ON c.car_serial_num = d.sales_order_detail_car_serial_num
LEFT JOIN manufacturer m
ON m.manufacturer_code = c.car_manufacturer_code
WHERE extract(year from o.sales_order_date) = extract(year from CURRENT_DATE)
AND extract(month from o.sales_order_date) = extract(month from CURRENT_DATE)
GROUP BY m.manufacturer_name
ORDER BY SUM(d.sales_order_detail_qty) DESC
LIMIT 3;

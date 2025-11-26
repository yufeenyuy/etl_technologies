set search_path to etl;

create table if not exists customer (
	customer_id varchar,
	first_name varchar,
	last_name varchar,
	birth_date varchar,
	street_name varchar,
	house_number int4,
	zip_code int4,
	city varchar,
	state varchar
);


create table if not exists inventory (
	supplier_product_id int4,
	supplier_product_category varchar,
	supplier_product_subcategory varchar,
	supplier_product_quantity int4,
	supplier_product_price float4,
	supplier_id varchar,
	product_id varchar,
	product_name varchar,
	product_category varchar,
	product_subcategory varchar,
	quantity int4,
	price float4
);



create table if not exists sales (
	transaction_id varchar,
	customer_id varchar,
	product_id varchar,
	transaction_time varchar,
	order_quantity int4,
	price float4,
	sale_amount float4
);



create table if not exists supplier (
	supplier_id varchar,
	company_name varchar,
	street varchar,
	house_number int4,
	zip_code int4,
	state varchar,
	company_type varchar,
	company_size varchar
);



create table if not exists user_interactions(
session varchar,
logtime timestamp,
customer_id varchar,
page_visit varchar,
user_action varchar,
session_duration_sec integer,
search_query varchar
);


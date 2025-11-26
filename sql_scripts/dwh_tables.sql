set search_path to coredwh;

create table if not exists customer(
customer_id varchar primary key,
first_name varchar not null,
last_name varchar not null,
birth_date date not null,
street_name varchar,
house_number varchar,
zip_code varchar,
city varchar,
state varchar
);


create table if not exists supplier(
supplier_id varchar primary key,
company_name varchar not null,
street varchar not null,
house_number varchar null,
zip_code varchar null,
state varchar null,
company_type varchar not null,
company_size varchar
);


create table if not exists supplier_product(
supplier_product_id int4 primary key,
supplier_id varchar not null,
product_category varchar,
product_subcategory varchar,
product_name varchar,
quantity integer check(quantity >= 0),
price float,
foreign key(supplier_id) references supplier on delete set null on update cascade
);


create table if not exists product(
product_id varchar primary key,
product_name varchar not null,
product_category varchar not null,
product_subcategory varchar not null,
quantity integer check(quantity >= 0),
price float check(price >= 0),
supplier_id varchar not null,
supplier_product_id int4 not null,
foreign key(supplier_id) references supplier on delete set null on update cascade,
foreign key(supplier_product_id) references supplier_product on delete set null on update cascade 
);


create table if not exists sales(
transaction_id varchar primary key,
customer_id varchar not null,
product_id varchar not null,
transaction_time timestamp,
order_quantity integer check(order_quantity >= 0),
product_price float check(product_price >= 0),
sale_amount float check(sale_amount >= 0),
foreign key(customer_id) references customer on delete set null on update cascade,
foreign key(product_id) references product on delete set null on update cascade
);


create table if not exists customer_interactions(
session varchar primary key,
logtime timestamp not null,
customer_id varchar not null,
page_visit varchar,
user_action varchar,
session_duration_sec integer,
search_query varchar,
foreign key(customer_id) references customer on delete set null on update cascade
);




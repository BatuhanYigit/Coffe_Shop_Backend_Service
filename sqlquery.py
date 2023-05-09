create_table_users = """CREATE TABLE IF NOT EXISTS "users" (
	id serial PRIMARY KEY,
	email VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR NOT NULL,
	role VARCHAR (50) NOT NULL,
	token VARCHAR,
	expire_time VARCHAR,
	register_date VARCHAR
);  
"""

# register_user = """INSERT INTO "public"."users" (email,password,register_date,role) VALUES ('{email}', '{password}', '{register_date}','{role}')"""

# login_control = """SELECT * FROM users WHERE email='{email}' AND password='{password}' """

orders_create = """INSERT INTO orders (email,orders,order_date) VALUES ('{email}', '{orders}', '{order_date}')"""

getproducts_sql = """SELECT * FROM product"""

item_create = """INSERT INTO item (item_code,item_name,price) VALUES ('{itemcode}','{itemname}', '{price}')"""

country_create = """INSERT INTO country (country) VALUES ('{country}')"""

district_create = """INSERT INTO district (district) VALUES ('{district}')"""

city_create = """INSERT INTO city (city) VALUES ('{city}')"""

address_create = """INSERT INTO address (contry_id,cit_yid,district_id,postalcode,adress_text,user_id) VALUES ('{countryid}','{cityid}','{districtid}','{postalcode}','{adresstext}','{userid}')"""

get_address = """select u.username_,u.email,a.adress_text,c.city,d.district,postalcode
from users u
join address a  on u.id=a.user_id
join city c on c.id = a.city_id
join district d on d.id=district_id
where u.id={userid}"""

get_basket_detail = """select bd.basket_id,bd.totalprice,i.item_name,i.price,s.sugar_type,s.sugar_price,m.milk_type,m.milk_price,sy.syrup_type,sy.syrup_price,sz.size,sz.size_price,bd.id
from basketdetail bd
right join item i  on i.id=bd.item_id
right join milk m on m.id = bd.milk_id
right join syrup sy on sy.id = bd.syrup_id
right join  sugar s on s.id = bd.sugar_id
right join size sz on sz.id = bd.size_id
where bd.basket_id={basket_id}"""

get_item = """SELECT * FROM item"""

total_price = """UPDATE basketdetail SET totalprice = {totalprice} WHERE id = {basket_id} """

set_basket_total_price = """UPDATE basket SET totalprice = {totalprice} WHERE id = {basket_id} """

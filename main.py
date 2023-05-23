from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import pandas as pd
import hashlib
import psycopg2
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlquery
import datetime
import sqlalchemy as sa
from sqlalchemy import create_engine, event
from sqlalchemy.engine.url import URL
load_dotenv()

app = FastAPI()

conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
)

app = FastAPI()

origins = [
    "http://localhost/*",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8000/test",
    "http://localhost:8000/user_table",
    "http://localhost:3000",
    "file:///home/batuhan/Documents/GitHub/html_table/index.html",
    "file:///home/batuhan/Documents/GitHub/html_table/index.html",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5173/test",


]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Country_Create(BaseModel):
    country: str


class Item_Create(BaseModel):
    itemcode: str
    itemname: str
    price: int


class Payment(BaseModel):
    title: str
    count: int
    price: int


class Orders_Create(BaseModel):
    email: str
    orders: str


class City_Create(BaseModel):
    city: str


class District_Create(BaseModel):
    district: str


class Address_Create(BaseModel):
    countryid: int
    cityid: int
    districtid: int
    postalcode: int
    addresstext: str
    userid: int


class Create_Basket(BaseModel):
    basket_id: int
    user_id: str
    create_date: str
    item_count: int
    item_id: int
    amount: int
    sugar_id: int
    syrup_id: int
    size_id: int


class Create_Syrup(BaseModel):
    syrup_type: str
    syrup_price: int


class Create_Size(BaseModel):
    size: str
    size_price: int


class Create_Sugar(BaseModel):
    sugar_type: str
    sugar_price: int


def item_price(id, data, index_df):
    for i in index_df:
        # print(f"for döngüsü {i} ")
        syrup_price = data.iloc[i]['syrup_price']
        # print(syrup_price)
        item_price = data.iloc[i]['item_price']
        # print(item_price)
        size_price = data.iloc[i]['size_price']
        # print(size_price)
        sugar_price = data.iloc[i]['sugar_price']
        # print(sugar_price)
        # print(milk_price)
        item_total_id = data.iloc[i]['id']
        total_price = syrup_price+item_price+size_price+sugar_price
        # print(total_price)
        check_total_price(item_total_id, total_price)


def basket_total_price(id, data, index_df):
    cur = conn.cursor()
    sum = 0
    for i in index_df:
        total_price = data.iloc[i]['totalprice']
        sum = total_price + sum
    info = {
        "basket_id": id,
        "total_price": sum

    }
    cur.execute(sqlquery.set_basket_total_price.format(**info))
    conn.commit()


def check_total_price(id, totalprice):
    cur = conn.cursor()
    info = {
        "basket_id": id,
        "totalprice": totalprice
    }
    cur.execute(sqlquery.total_price.format(**info))
    conn.commit()


def create_date():
    date = datetime.datetime.today()
    return date


@app.post("/create-syrup")
async def create_syrup(create_syrup: Create_Syrup):
    cur = conn.cursor()
    syrup = create_syrup.syrup_type
    syrup_price = create_syrup.syrup_price
    info = {
        "syrup": syrup,
        "syrup_price": syrup_price
    }
    cur.execute(sqlquery.syrup_create.format(**info))
    conn.commit()
    return "Şurup Girilmiştir"


@app.post("/create-size")
async def create_size(create_size: Create_Size):
    cur = conn.cursor()
    size = create_size.size
    size_price = create_size.size_price
    info = {
        "size": size,
        "size_price": size_price
    }
    cur.execute(sqlquery.size_create.format(**info))
    conn.commit()
    return "Boyut Girilmiştir"


@app.post("/create-sugar")
async def create_sugar(create_sugar: Create_Sugar):
    cur = conn.cursor()
    sugar = create_sugar.sugar_type
    sugar_price = create_sugar.sugar_price
    info = {
        "sugar": sugar,
        "sugar_price": sugar_price
    }
    cur.execute(sqlquery.sugar_create.format(**info))
    conn.commit()
    return "Boyut Girilmiştir"


@app.post("/district-create")
async def district_create(district_create: District_Create):
    cur = conn.cursor()
    district = district_create.district
    info = {
        "district": district
    }
    cur.execute(sqlquery.district_create.format(**info))
    conn.commit()
    return "İlçe girilmiştir"


@app.post("/address-create")
async def address_create(address_create: Address_Create):
    cur = conn.cursor()
    countryid = address_create.countryid
    cityid = address_create.cityid
    districtid = address_create.districtid
    postalcode = address_create.postalcode
    adresstext = address_create.addresstext
    userid = address_create.userid
    info = {
        "countryid": countryid,
        "cityid": cityid,
        "districtid": districtid,
        "postalcode": postalcode,
        "adresstext": adresstext,
        "userid": userid
    }
    cur.execute(sqlquery.address_create.format(**info))
    conn.commit()
    return "Adres Girilmiştir"


@app.get("/address-get/{id}")
async def address_get(id=int):
    info = {
        "userid": id
    }
    data = pd.read_sql_query(sqlquery.get_address.format(**info), conn)
    print(data.to_dict("records"))
    return JSONResponse(
        content={
            "data": data.to_dict("records"),
            "success": True
        }
    )


@app.get("/basket-detail-get/{id}")
async def basket_detail_get(id=str):
    info = {
        "basket_id": id,
    }

    data = pd.read_sql_query(sqlquery.get_basket_detail.format(**info), conn)
    index_df = data.index.values

    item_price(id, data, index_df)
    # basket_total_price(id, data, index_df)

    return JSONResponse(
        content={
            "data": data.to_dict("records"),
            "success": True
        }
    )


@ app.post("/country-create")
async def country_create(country_create: Country_Create):
    cur = conn.cursor()
    country = country_create.country
    info = {
        "country": country
    }
    cur.execute(sqlquery.country_create.format(**info))
    conn.commit()
    return "Ülke girilmiştir"


@ app.post("/city-create")
async def city_create(city_create: City_Create):
    cur = conn.cursor()
    city = city_create.city
    info = {
        "city": city
    }
    cur.execute(sqlquery.city_create.format(**info))
    conn.commit()
    return "Şehir Girilmiştir."


@ app.post("/item-create")
async def item_create(item_create: Item_Create):
    cur = conn.cursor()
    itemcode = item_create.itemcode
    itemname = item_create.itemname
    price = item_create.price
    info = {
        "itemcode": itemcode,
        "itemname": itemname,
        "price": price
    }
    print(itemcode)
    cur.execute(sqlquery.item_create.format(**info))
    conn.commit()
    return "Ürün oluşturuldu"


@ app.get("/syrup")
async def get_item():
    data = pd.read_sql_query("SELECT * FROM syrup", conn)

    return JSONResponse(

        content={
            "data": data.to_dict("records"),
            "success": True
        }

    )


@ app.get("/sugar")
async def get_item():
    data = pd.read_sql_query("SELECT * FROM sugar", conn)

    return JSONResponse(

        content={
            "data": data.to_dict("records"),
            "success": True
        }

    )


@ app.get("/size")
async def get_item():
    data = pd.read_sql_query("SELECT * FROM size", conn)

    return JSONResponse(

        content={
            "data": data.to_dict("records"),
            "success": True
        }

    )


@ app.get("/item")
async def get_item():
    data = pd.read_sql_query("SELECT * FROM item", conn)

    return JSONResponse(

        content={
            "data": data.to_dict("records"),
            "success": True
        }

    )


@ app.post("/orders")
async def orders(orders_create: Orders_Create):
    try:
        cur = conn.cursor()
        email = orders_create.email
        orders = orders_create.orders
        order_date = create_date()
        info = {
            "email": email,
            "orders": orders,
            "order_date": order_date,
        }
        cur.execute(sqlquery.orders_create.format(**info))
        conn.commit()
        # order_results = cur.fetchall()
        return "Sipariş Oluşturuldu"
    except:
        print(create_date())
        return "Hata oluştu", status.HTTP_400_BAD_REQUEST


@app.post("/create-basket")
async def create_basket(create_basket: Create_Basket):
    cur = conn.cursor()
    user_id = create_basket.user_id
    create_date = create_basket.create_date
    item_count = create_basket.item_count
    item_id = create_basket.item_id
    amount = create_basket.amount
    sugar_id = create_basket.sugar_id
    syrup_id = create_basket.syrup_id
    size_id = create_basket.size_id
    basket_id = create_basket.basket_id

    info_basket = {
        "user_id": user_id,
        "create_date": create_date,
        "item_count": item_count
    }

    cur.execute(sqlquery.set_basket.format(**info_basket))
    conn.commit()

    # basket_id = pd.read_sql_query(
    #     "select id from basket where user_id = {} ".format(user_id), conn)

    info_basket_detail = {
        "basket_id": basket_id,
        "item_id": item_id,
        "amount": amount,
        "sugar_id": sugar_id,
        "syrup_id": syrup_id,
        "size_id": size_id
    }

    cur.execute(sqlquery.set_basket_detail.format(**info_basket_detail))
    conn.commit


@app.post("/json-test/{basketId}")
async def jsontest(info: Request, basketId=str):

    cur = conn.cursor()
    req_info = await info.json()
    print("Basket IIIIIIIIID", basketId),

    print(req_info['dataCart'], "Deneme data cart")
    print(req_info, "Address Detail")
    print(len(req_info))
    print(req_info['address_detail']['name'])
    print(req_info['address_detail']['surname'])
    name = req_info['address_detail']['name']
    surname = req_info['address_detail']['surname']
    address_name = req_info['address_detail']['address_name']
    email = req_info['address_detail']['email']
    phone = req_info['address_detail']['phone']
    address_detail = req_info['address_detail']['address_detail']
    for data in req_info['dataCart']:

        cur.execute(sqlquery.set_basket_detail.format(
            **data, **{"basketid": basketId, "name": name, "surname": surname, "address_name": address_name, "email": email, "phone": phone, "address_detail": address_detail}))
        conn.commit()

    return {
        "status": "SUCCESS",
        "data": req_info,
        "denemeeeeeeee": "denemeee"

    }

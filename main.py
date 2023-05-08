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


def check_total_price(id, totalprice):
    cur = conn.cursor()
    info = {
        "basket_id": id,
        "totalprice": totalprice
    }
    cur.execute(sqlquery.total_price.format(**info))


def create_date():
    date = datetime.datetime.today()
    return date


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
async def basket_detail_get(id=int):
    info = {
        "basket_id": id,
    }
    data = pd.read_sql_query(sqlquery.get_basket_detail.format(**info), conn)

    print(data.to_dict("records"))
    syrup_price = data.iloc[0]['syrup_price']
    item_price = data.iloc[0]['price']
    size_price = data.iloc[0]['size_price']
    sugar_price = data.iloc[0]['sugar_price']
    total_price = syrup_price+item_price+size_price+sugar_price
    check_total_price(id, total_price)

    print("typeeeeeee : ", data.iloc[0]['syrup_price'])
    print("aaaaaaaaaaaaaa", type(data))
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


@ app.get("/item")
async def get_item():
    data = pd.read_sql_query("SELECT * FROM item", conn)

    return JSONResponse(

        content={
            "data": data.to_dict("records"),
            "success": True
        }

    )


@ app.post("/c")
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

from fastapi import FastAPI
import random

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Mouse", "price": 25},
    {"id": 3, "name": "Keyboard", "price": 75},
]


@app.get("/products")
def get_products():
    return products


@app.post("/products")
def create_products(name: str, price: int):
    produc_obj = {"id": random.randint(6, 100), "name": name, "price": price}
    products.append(produc_obj)
    return {"result": produc_obj}


@app.get("/products/search")
def search_product(name: str):
    for product in products:
        if product["name"] == name:
            return product

    return {"message": "product not found"}


@app.get("/products/{product_id}")
def get_one_products(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"message": "products not found"}


@app.put("/products/{product_id}")
def update_products(product_id: int, product_name: str, product_price: int):
    for product in products:
        if product["id"] == product_id:
            product["name"] = product_name
            product["price"] = product_price

    return {"deatail": "product not found"}


@app.delete("/products/{product_id}")
def remove_products(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"detail": "product remove"}
    return {"deatail": "product not found"}


@app.get("/")
def well_come():
    return {"message": "	 Welcome to Store API"}

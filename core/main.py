from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse, Response

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Mouse", "price": 25},
    {"id": 3, "name": "Keyboard", "price": 75},
    {"id": 4, "name": "Keyboard", "price": 750},
    {"id": 5, "name": "Keyboard", "price": 7500},
]


def not_found():
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "product not found"},
    )


@app.get("/")
def well_come():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Welcome to Store API"},
    )


@app.get("/products")
def get_products(q: str | None = Query(default=None, max_length=50)):
    if q:
        result = [p for p in products if p["name"].lower() == q.lower()]
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    return JSONResponse(status_code=status.HTTP_200_OK, content=products)


@app.post("/products")
def create_products(name: str, price: int):
    if price < 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "price must be positive"},
        )

    new_id = max((p["id"] for p in products), default=0) + 1
    product_obj = {"id": new_id, "name": name, "price": price}
    products.append(product_obj)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"result": product_obj},
    )


@app.get("/products/{product_id}")
def get_one_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return JSONResponse(status_code=status.HTTP_200_OK, content=product)

    return not_found()


@app.put("/products/{product_id}")
def update_product(product_id: int, product_name: str, product_price: int):
    for product in products:
        if product["id"] == product_id:
            product["name"] = product_name
            product["price"] = product_price
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"result": product},
            )

    return not_found()


@app.delete("/products/{product_id}")
def remove_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    return not_found()

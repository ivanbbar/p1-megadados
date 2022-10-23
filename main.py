from fastapi import FastAPI, Query, Path, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Optional
from pydantic import BaseModel, Field

from utils import *

app = FastAPI()

### CLASSES

class ProductsInterface(BaseModel):
    product_id: Optional[int] = Field(None, ge=1)
    name: str = Field(..., max_length=45)
    price: float
    description: Optional[str] = Field(None, max_length=150)

class ProductsInterfaceSecondary(BaseModel):
    product_id: Optional[int] = Field(None, ge=1)
    name: Optional[str] = Field(None, max_length=45)
    price: Optional[float]
    description: Optional[str] = Field(None, max_length=150)

class InventoryProductInterface(BaseModel):
    fk_inventory_id: Optional[int] = Field(None, ge=1)
    fk_product_id: Optional[int] = Field(None, ge=1)
    quantity: int = Field(..., ge=1)

### METHODS

#get all products
@app.get("/products/", tags=["Product"])
async def get_all_products():
    return {"products": read_data("product")}

#get product
@app.get("/products/{product_id}", tags=["Product"])
async def get_product(
    *,
    product_id: int = Path(..., title="The product ID", ge=1)):

    if check_id("product", "product_id", product_id):
        return {"product": list(
            filter(lambda x: x["product_id"] == product_id, read_data("product")))[0]}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# Create product
@app.post("/products/", tags=["Product"])
async def create_product(product: ProductsInterface = Body(...)):

    idmax = 0
    for data in read_data("product"):
        if data["product_id"] > idmax:
            idmax = data["product_id"]
    
    product.product_id = idmax + 1

    with open('data.json', 'r+', encoding='utf-8') as f:
        file = json.load(f)
        file["product"].append(jsonable_encoder(product))  
        json.dump(file, f.truncate(0).seek(0), indent=4)

    return {"message": "success"}

# Update product
@app.put("/products/{product_id}", tags=["Product"])
async def update_product(
    *,
    product_id: int = Path(..., title="The product ID", ge=1),
    product: ProductsInterfaceSecondary = Body(...)):

    if check_id("product", "product_id", product_id):
        update_element = list(
            filter(lambda x: x["product_id"] == product_id, read_data("product")))[0]

        for key, value in jsonable_encoder(product).items():
            if value != None:
                jsonable_encoder(update_element)[key] = value
        update_data("product", ["product_id"], [product_id], jsonable_encoder(update_element))
        return {"message": "success"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# get all inventories
@app.get("/inventory/", tags=["Inventory"])
async def get_all_inventories():
    return {"inventory": read_data("inventory")}

#get inventory
@app.get("/inventory/{inventory_id}", tags=["Inventory Product"])
async def get_inventory_products(
    *,
    inventory_id: int = Path(..., title="The inventory ID", ge=1)):

    if check_id("inventory", "inventory_id", inventory_id):
        return {"inventory_product": list(
            filter(lambda x: x["fk_inventory_id"] == inventory_id, read_data("inventory_product")))}
    else:
        raise HTTPException(status_code=404, detail="Inventory not found")

# update product in inventory
@app.put("/inventory/{inventory_id}/{product_id}", tags=["Inventory Product"])
async def update_inventory_product(
    *,
    inventory_id: int = Path(..., title="The inventory ID", ge=1),
    product_id: int = Path(..., title="The product ID", ge=1),
    inventory: InventoryProductInterface = Body(...)):

    if check_id("inventory", "inventory_id", inventory_id):
        for element in list(filter(lambda x: x["fk_inventory_id"] == inventory_id, read_data("inventory_product"))):
            if element["fk_product_id"] == product_id:
                for key, value in jsonable_encoder(inventory).items():
                    if value != None:
                        element[key] = value
                        update_data("inventory_product", ["fk_inventory_id", "fk_product_id"], [inventory_id, product_id], element)
        return {"message": "success"}
    else:
        raise HTTPException(status_code=404, detail="Inventory not found")

# delete product from inventory
@app.delete("/inventory/{inventory_id}/{product_id}", tags=["Inventory Product"])
async def delete_inventory_product(
    *,
    inventory_id: int = Path(..., title="The inventory ID", ge=1),
    product_id: int = Path(..., title="The product ID", ge=1)):

    if check_id("inventory", "inventory_id", inventory_id):
        delete_data("inventory_product", ["fk_inventory_id", "fk_product_id"], [
                    inventory_id, product_id])
        return {"message": "success"}
    else:
        raise HTTPException(status_code=404, detail="Inventory not found")

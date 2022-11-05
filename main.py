from fastapi import FastAPI, Path, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Optional
from pydantic import BaseModel, Field
from crud import *

crud_products = CrudProducts()
crud_inventory_products = CrudInventoryProducts()

app = FastAPI()

### CLASSES

class ProductsInterface(BaseModel):
    name: str = Field(..., max_length=45)
    price: float
    description: Optional[str] = Field(None, max_length=150)

class ProductsInterfaceSecondary(BaseModel):
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
    return {"products": crud_products.get_all()}

#get product
@app.get("/products/{product_id}", tags=["Product"])
async def get_product(
    *,
    product_id: int = Path(..., title="The product ID", ge=1)):

    try:
        return {"product": crud_products.get(product_id)}
    except:
        raise HTTPException(status_code=404, detail="Product not found")

# Create product
@app.post("/products/", tags=["Product"])
async def create_product(product: ProductsInterface = Body(...)):

    try:
        crud_products.create(jsonable_encoder(product))
        return {"message": "success"}

    except:
        raise HTTPException(status_code=400, detail="Error creating product")

# Update product
@app.put("/products/{product_id}", tags=["Product"])
async def update_product(
    *,
    product_id: int = Path(..., title="The product ID", ge=1),
    product: ProductsInterfaceSecondary = Body(...)):

    try:
        crud_products.update(product_id, jsonable_encoder(product))
        return {"message": "success"}
    except:
        raise HTTPException(status_code=404, detail="Product not found")

# get all inventories
@app.get("/inventory/", tags=["Inventory Product"])
async def get_all_inventories():
    return {"inventory_product": crud_inventory_products.get_all()}

#get inventory
@app.get("/inventory/{inventory_id}", tags=["Inventory Product"])
async def get_inventory_products(
    *,
    inventory_id: int = Path(..., title="The inventory ID", ge=1)):

    try:
        return {"inventory_product": crud_inventory_products.get(inventory_id)}
    except:
        raise HTTPException(status_code=404, detail="Inventory not found")

# update product in inventory
@app.put("/inventory/{inventory_id}/{product_id}", tags=["Inventory Product"])
async def update_inventory_product(
    *,
    inventory_id: int = Path(..., title="The inventory ID", ge=1),
    product_id: int = Path(..., title="The product ID", ge=1),
    inventory: InventoryProductInterface = Body(...)):

    try:
        crud_inventory_products.update(inventory_id, product_id, jsonable_encoder(inventory)["quantity"])
        return {"message": "success"}
    except:
        raise HTTPException(
            status_code=404, detail="Error in updating products in inventory")

# delete product from inventory
@app.delete("/inventory/{inventory_id}/{product_id}", tags=["Inventory Product"])
async def delete_inventory_product(
    *,
    inventory_id: int = Path(..., title="The inventory ID", ge=1),
    product_id: int = Path(..., title="The product ID", ge=1)):

    try:
        crud_inventory_products.delete(inventory_id, product_id)
        return {"message": "success"}
    except:
        raise HTTPException(
            status_code=404, detail="Error in deleting product from inventory")

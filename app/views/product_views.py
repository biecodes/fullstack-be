from fastapi import APIRouter, HTTPException
from app.models.product_models import ProductModel
from app.controllers import product_controller
from app.models.product_filter_models import ProductFilterModel

router = APIRouter()


@router.post("/product/get-all")
def list_products(filters: ProductFilterModel):
    return product_controller.get_products(filters)
    

@router.post("/product/add")
def create_product(product: ProductModel):
    new_product = product_controller.create_product(product)
    return {"message": "Product created", "data": new_product}


@router.get("/product/get-one/{product_id}")
def get_product(product_id: str):
    product = product_controller.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/product/update/{product_id}")
def update_product(product_id: str, product: ProductModel):
    updated_product = product_controller.update_product(product_id, product.dict())
    if not updated_product:
        raise HTTPException(
            status_code=404, detail="Product not found or no changes made"
        )
    return {"message": "Product updated", "data": updated_product}


@router.delete("/product/delete/{product_id}")
def delete_product(product_id: str):
    success = product_controller.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}

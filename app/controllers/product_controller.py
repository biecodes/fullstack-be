from app.database import db
from app.models.product_models import ProductModel
from app.models.product_filter_models import ProductFilterModel
from bson import ObjectId
from pymongo import DESCENDING, ASCENDING
from datetime import datetime


products_collection = db["product"]


def get_products(filters: ProductFilterModel):
    query = {}

    # 🔍 Search handling
    search = (filters.search or "").strip()
    search_by = filters.searchBy or []
    operator = (filters.operator or "or").lower()

    if search and search_by:
        conditions = []
        for field in search_by:
            conditions.append({field: {"$regex": search, "$options": "i"}})

        if operator == "or":
            query["$or"] = conditions
        else:
            query["$and"] = conditions

    # 🔽 Sorting
    order_by = filters.orderBy or "created_at"
    order = (filters.order or "asc").lower()
    sort_order = DESCENDING if order == "desc" else ASCENDING

    # 📄 Pagination
    page = filters.page or 1
    limit = filters.limit or 10
    skip = (page - 1) * limit

    cursor = (
        products_collection.find(query)
        .sort(order_by, sort_order)
        .skip(skip)
        .limit(limit)
    )

    products = []
    for product in cursor:
        product["_id"] = str(product["_id"])
        products.append(product)

    total = products_collection.count_documents(query)

    return {
        "data": products,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit,
        },
    }


def create_product(product: ProductModel):
    product_dict = product.dict()
    result = products_collection.insert_one(product_dict)
    inserted_id = result.inserted_id
    new_product = products_collection.find_one({"_id": inserted_id})
    new_product["_id"] = str(new_product["_id"])
    return new_product


def get_product_by_id(product_id: str):
    try:
        obj_id = ObjectId(product_id)
    except Exception:
        return {"status": False, "data": None, "message": "Invalid product ID format."}

    product = products_collection.find_one({"_id": obj_id})

    if product:
        product["_id"] = str(product["_id"])
        return {
            "status": True,
            "data": product,
            "message": "Product found successfully.",
        }
    else:
        return {"status": False, "data": None, "message": "Product not found."}


def update_product(product_id: str, product_data: dict):
    try:
        obj_id = ObjectId(product_id)
    except:
        return None

    update_data = {k: v for k, v in product_data.items() if v is not None}
    update_data["updatedAt"] = datetime.utcnow()

    result = products_collection.update_one({"_id": obj_id}, {"$set": update_data})
    if result.modified_count == 0:
        return None

    updated_product = products_collection.find_one({"_id": obj_id})
    updated_product["_id"] = str(updated_product["_id"])
    return updated_product


def delete_product(product_id: str):
    try:
        obj_id = ObjectId(product_id)
    except:
        return False
    result = products_collection.delete_one({"_id": obj_id})
    return result.deleted_count > 0

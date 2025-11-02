from app.database import db
from app.models.user_models import UserModel
from bson import ObjectId
from passlib.context import CryptContext
from app.core.security import create_access_token
from icecream import ic

# from datetime import timedelta
from app.models.user_filter_models import UserFilterModel
from pymongo import DESCENDING, ASCENDING
from datetime import timedelta
from datetime import datetime


users_collection = db["user"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    ic(password)
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_users(filters: UserFilterModel):
    query = {}

    # 🔍 Search handling
    if filters.search and filters.search_by:
        conditions = []
        for field in filters.search_by:
            conditions.append({field: {"$regex": filters.search, "$options": "i"}})
        if filters.operator == "or":
            query["$or"] = conditions
        else:
            query["$and"] = conditions

    # 🔽 Sorting
    sort_order = DESCENDING if filters.order.lower() == "desc" else ASCENDING

    # 📄 Pagination
    skip = (filters.page - 1) * filters.size
    cursor = (
        users_collection.find(query)
        .sort(filters.orderBy, sort_order)
        .skip(skip)
        .limit(filters.size)
    )

    users = []
    for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)

    total = users_collection.count_documents(query)

    return {
        "data": users,
        "pagination": {
            "page": filters.page,
            "size": filters.size,
            "total": total,
            "pages": (total + filters.size - 1) // filters.size,
        },
    }


def create_user(user: UserModel):
    user_dict = user.dict()

    # Isi created_at kalau belum ada
    ic("create")
    if not user_dict.get("created_at"):
        user_dict["created_at"] = datetime.utcnow()
    user_dict["password"] = hash_password(user.password)
    result = users_collection.insert_one(user_dict)
    inserted_id = result.inserted_id
    new_user = users_collection.find_one({"_id": inserted_id})
    new_user["_id"] = str(new_user["_id"])
    new_user.pop("password", None)
    return new_user


def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0


def login_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user:
        # user tidak ditemukan
        return {"status": False, "message": "User not found or invalid credentials"}

    if not verify_password(password, user["password"]):
        # password salah
        return {"status": False, "message": "User not found or invalid credentials"}

    # buat JWT token
    token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": str(user["_id"]), "email": user["email"]},
        expires_delta=token_expires,
    )

    # bersihkan password sebelum dikirim
    user["_id"] = str(user["_id"])
    user.pop("password", None)

    return {
        "status": True,
        "message": "Login successful",
        "data": user,
        "access_token": access_token,
        "token_type": "bearer",
    }


def get_user_by_id(user_id: str):
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        return {"status": False, "data": None, "message": "Invalid user ID format."}

    user = users_collection.find_one({"_id": obj_id})

    if user:
        user["_id"] = str(user["_id"])
        return {
            "status": True,
            "data": user,
            "message": "User found successfully.",
        }
    else:
        return {"status": False, "data": None, "message": "User not found."}


def update_users(user_id: str, user_data: dict):
    try:
        obj_id = ObjectId(user_id)
    except:
        return None

    update_data = {k: v for k, v in user_data.items() if v is not None}
    update_data["updatedAt"] = datetime.utcnow()

    result = users_collection.update_one({"_id": obj_id}, {"$set": update_data})
    if result.modified_count == 0:
        return None

    updated_user = users_collection.find_one({"_id": obj_id})
    updated_user["_id"] = str(updated_user["_id"])
    return updated_user

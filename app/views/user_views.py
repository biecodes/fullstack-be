from fastapi import APIRouter, HTTPException
from app.models.user_models import UserModel
from app.controllers import user_controllers
from pydantic import BaseModel
from app.models.user_filter_models import UserFilterModel


router = APIRouter()


class LoginSchema(BaseModel):
    email: str
    password: str


@router.post("/users/get-all")
def list_products(filters: UserFilterModel):
    return user_controllers.get_users(filters)


@router.post("/users/add")
def create_user(user: UserModel):
    user_id = user_controllers.create_user(user)
    return {"message": "User created", "user_id": user_id}


@router.get("/users/get-one/{user_id}")
def get_user(user_id: str):
    product = user_controllers.get_user_by_id(user_id)
    if not product:
        raise HTTPException(status_code=404, detail="User not found")
    return product


@router.put("/users/update/{user_id}")
def update_users(user_id: str, user: UserModel):
    updated_user = user_controllers.update_users(user_id, user.dict())
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    return {"message": "User updated", "user": updated_user}


@router.delete("/users/delete/{user_id}")
def delete_user(user_id: str):
    success = user_controllers.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


@router.post("/users/login")
def login(request: LoginSchema):
    result = user_controllers.login_user(request.email, request.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return result

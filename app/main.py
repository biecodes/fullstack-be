from fastapi import FastAPI
from app.views import user_views
from app.views import product_views
from app.views import upload_views
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Ecommerce Management API",
    version="1.0.0",
)

app.include_router(user_views.router, prefix="/api/v1", tags=["Users"])
app.include_router(product_views.router, prefix="/api/v1", tags=["Products"])
app.include_router(upload_views.router, prefix="/api/v1", tags=["Files"])
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

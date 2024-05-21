from fastapi import FastAPI
from app.routes import category, product, user, venta, oauth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(category.router, prefix="/categories", tags=["categories"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(venta.router, prefix="/ventas", tags=["ventas"])
app.include_router(oauth.router, prefix="/oauth", tags=["ventas"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

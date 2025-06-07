from fastapi import FastAPI
from api.routers import GoalRouters, LimitRouters, UserRouters, TransactionRouters, CategoryRouters
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://easy-finance-ten.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(UserRouters.router, prefix="/user", tags=["Usuario"])
app.include_router(TransactionRouters.router, prefix="/transaction", tags=["Transaction"])
app.include_router(LimitRouters.router, prefix="/limit", tags=["Limit"])
app.include_router(GoalRouters.router, prefix="/goal", tags=["Goal"])
app.include_router(CategoryRouters.router, prefix="/category", tags=["Category"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="EasyFinanceAPI",
        version="1.0.0",
        description="API com autenticação JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

handler = Mangum(app)

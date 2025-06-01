from fastapi import FastAPI
from api.routers import UserRouters, TransactionRouters, GoalRouters, PiggyRouters
from fastapi.openapi.utils import get_openapi

app = FastAPI()


app.include_router(UserRouters.router, prefix="/usuario", tags=["Usuario"])
app.include_router(TransactionRouters.router, prefix="/Transaction", tags=["Transaction"])
app.include_router(GoalRouters.router, prefix="/Goal", tags=["Goal"])
app.include_router(PiggyRouters.router, prefix="/PiggyBank", tags=["PiggyBank"])

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

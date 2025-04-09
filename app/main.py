from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import reservations
from fastapi.openapi.utils import get_openapi


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
@app.get("/")
def root():
    return {"message": "Welcome to the Reservations Microservice!"}
app.include_router(reservations.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Reservations Microservice",
        version="1.0.0",
        description="Handles flight reservations",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for op in path.values():
            op["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi
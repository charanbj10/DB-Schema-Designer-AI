from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import requirement_routes, schema_routes, mongo_routes, mcp_routes

app = FastAPI(
    title="DB Schema Designer AI",
    description="AI-powered MongoDB schema designer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(requirement_routes.router)
app.include_router(schema_routes.router)
app.include_router(mongo_routes.router)
app.include_router(mcp_routes.router)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok", "message": "DB Schema Designer AI is running"}
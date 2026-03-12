# api/routes/mcp_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mcp.mcp_server import MCPServer
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/mcp", tags=["MCP - Prompt Based CRUD"])

mcp = MCPServer(
    mongo_uri=os.getenv("MONGO_URI"),
    db_name=os.getenv("DB_NAME"),
)


class PromptRequest(BaseModel):
    prompt: str


@router.post("/query")
def mcp_query(req: PromptRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt cannot be empty")
    return mcp.handle(req.prompt)
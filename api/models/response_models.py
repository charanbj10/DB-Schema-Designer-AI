from pydantic import BaseModel
from typing import Optional, Any


class RequirementResponse(BaseModel):
    status: str
    formatted_requirement: Optional[str] = None
    message: str


class SchemaResponse(BaseModel):
    status: str
    final_schema: Optional[str] = None
    message: str


class InsertResponse(BaseModel):
    status: str
    message: str
    results: Optional[Any] = None
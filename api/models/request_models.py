from pydantic import BaseModel


class RequirementRequest(BaseModel):
    user_input: str


class ReviewRequest(BaseModel):
    action: str  # "CONFIRM" or modification text


class InsertRequest(BaseModel):
    confirm: str  # "yes" or "no"
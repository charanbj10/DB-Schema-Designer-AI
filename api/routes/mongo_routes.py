from fastapi import APIRouter, HTTPException
from api.models.request_models import InsertRequest
from api.models.response_models import InsertResponse
from api.session.session_store import session_store
import api.services.schema_service as service

router = APIRouter(prefix="/mongo", tags=["MongoDB"])


@router.post("/insert", response_model=InsertResponse)
def insert_to_mongo(req: InsertRequest):
    if not session_store.schema_confirmed:
        raise HTTPException(
            status_code=400,
            detail="Schema not confirmed. Call /schema/confirm with CONFIRM first."
        )

    if req.confirm.strip().lower() != "yes":
        return InsertResponse(
            status="cancelled",
            message="Insertion cancelled."
        )

    results = service.insert_to_mongo()

    return InsertResponse(
        status="done",
        message="Schema successfully inserted into MongoDB.",
        results=results
    )
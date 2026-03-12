from fastapi import APIRouter, HTTPException
from api.models.request_models import ReviewRequest
from api.models.response_models import SchemaResponse
from api.session.session_store import session_store
import api.services.schema_service as service

router = APIRouter(prefix="/schema", tags=["Schema"])


@router.post("/get", response_model=SchemaResponse)
def get_schema():
    if not session_store.req_confirmed:
        raise HTTPException(
            status_code=400,
            detail="Requirement not confirmed. Call /requirement/confirm with CONFIRM first."
        )

    output = service.generate_schema()

    return SchemaResponse(
        status="pending_confirmation",
        final_schema=output,
        message="Review the schema. POST to /schema/confirm with CONFIRM or modification."
    )


@router.post("/confirm", response_model=SchemaResponse)
def confirm_schema(req: ReviewRequest):
    if not session_store.schema:
        raise HTTPException(
            status_code=400,
            detail="No schema found. Call /schema/get first."
        )

    if req.action.strip().upper() == "CONFIRM":
        service.confirm_schema()
        return SchemaResponse(
            status="confirmed",
            message="Schema confirmed. POST to /mongo/insert to insert into MongoDB."
        )

    updated = service.modify_schema(req.action)

    return SchemaResponse(
        status="updated",
        final_schema=updated,
        message="Schema updated. Review and POST to /schema/confirm again."
    )
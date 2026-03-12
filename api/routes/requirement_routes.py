from fastapi import APIRouter, HTTPException
from api.models.request_models import RequirementRequest, ReviewRequest
from api.models.response_models import RequirementResponse
from api.session.session_store import session_store
import api.services.requirement_service as service

router = APIRouter(prefix="/requirement", tags=["Requirement"])


@router.post("/get", response_model=RequirementResponse)
def get_requirement(req: RequirementRequest):
    if not req.user_input.strip():
        raise HTTPException(status_code=400, detail="user_input cannot be empty")

    print(req)
    output = service.get_formatted_requirement(req.user_input)

    return RequirementResponse(
        status="pending_confirmation",
        formatted_requirement=output,
        message="Review the requirement. POST to /requirement/confirm with CONFIRM or modification."
    )


@router.post("/confirm", response_model=RequirementResponse)
def confirm_requirement(req: ReviewRequest):
    if not session_store.format_requirement:
        raise HTTPException(
            status_code=400,
            detail="No requirement found. Call /requirement/get first."
        )

    if req.action.strip().upper() == "CONFIRM":
        service.confirm_requirement()
        return RequirementResponse(
            status="confirmed",
            message="Requirement confirmed. POST to /schema/get to generate schema."
        )

    updated = service.modify_requirement(req.action)

    return RequirementResponse(
        status="updated",
        formatted_requirement=updated,
        message="Requirement updated. Review and POST to /requirement/confirm again."
    )
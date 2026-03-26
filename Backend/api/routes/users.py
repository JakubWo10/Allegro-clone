from fastapi import APIRouter










user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/user_info")
async def user_informations():
    return {"message": "xd"}
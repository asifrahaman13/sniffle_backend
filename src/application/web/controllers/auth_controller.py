from fastapi import APIRouter, Depends, HTTPException
from src.internal.entities.auth import Token
from src.internal.interfaces.database_interface import DatabaseInterface
from src.internal.interfaces.auth_interface import AuthInterface
from exports.exports import auth_service, database_service

auth_router = APIRouter()


@auth_router.post("/google")
async def google_sign_in(
    token: Token,
    auth_interface: AuthInterface = Depends(auth_service),
    database_interface: DatabaseInterface = Depends(database_service),
):
    id_info = auth_interface.verify_google_access_token(token.token)
    if not id_info:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = database_interface.find_one("googleId", id_info["sub"], "users")

    if not user:
        user = {
            "googleId": id_info["sub"],
            "email": id_info["email"],
            "name": id_info.get("name", ""),
        }
        database_interface.insert_one(user, "users")

    access_token = auth_interface.create_access_token(
        data={"sub": id_info["email"], "name": id_info["name"]}
    )

    return {"token": access_token, "user": id_info}


@auth_router.post("/decode_token", response_model=dict)
async def decode_token(
    token: Token, auth_interface: AuthInterface = Depends(auth_service)
):
    try:
        id_info = auth_interface.decode_access_token(token.token)
        return id_info
    except Exception as e:
        return {"error": "Invalid token"}

from fastapi import APIRouter, Depends, HTTPException
from src.internal.entities.auth import Token
from src.infastructure.repositories.database_repository import DatabaseRepository
from src.infastructure.repositories.auth_repository import AuthRepository
from src.internal.use_cases.auth_service import AuthService
from src.internal.use_cases.database_service import DatabaseService
from src.internal.interfaces.database_interface import DatabaseInterface
from src.internal.interfaces.auth_interface import AuthInterface

database_repository = DatabaseRepository()
database_service = DatabaseService(database_repository)
auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

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

    # Find or create the user in your database
    # user = await users_collection.find_one({'googleId': id_info['sub']})

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
async def decode_token(token: Token, auth_interface: AuthInterface = Depends(auth_service)):
    try:
        id_info = auth_interface.decode_access_token(token.token)
        return id_info
    except Exception as e:
        return {"error": "Invalid token"}

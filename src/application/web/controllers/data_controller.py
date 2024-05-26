from fastapi import APIRouter, Depends, HTTPException
from src.infastructure.repositories.auth_repository import AuthRepository
from src.internal.use_cases.auth_service import AuthService
from src.internal.interfaces.auth_interface import AuthInterface
from src.internal.interfaces.data_interface import DataInterface
from src.internal.use_cases.data_service import DataService
from src.internal.entities.auth import Token


# Create a new router
data_router = APIRouter()

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

data_service = DataService()

@data_router.get("/general_metrics/{token}")
async def get_general_metrics(
    token: str,
    auth_interface: AuthInterface = Depends(auth_service),
    data_interface: DataInterface = Depends(data_service),
):
    try:
        # Decode the token
        id_info = auth_interface.decode_access_token(token)

        # Check if the token is valid
        if id_info is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Get the general metrics for the user
        general_metrics = data_interface.get_general_metrics(id_info["sub"])

        # Return the general metrics
        return general_metrics

    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get general metrics")

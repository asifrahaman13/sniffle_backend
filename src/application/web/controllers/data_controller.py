from fastapi import APIRouter, Depends, HTTPException, Header
from src.internal.use_cases.export_service import ExportService
from src.infastructure.repositories.export_repository import ExportRepository
from src.infastructure.repositories.database_repository import DatabaseRepository
from src.internal.interfaces.export_interface import ExportInterface
from src.internal.use_cases.search_service import SearchService
from src.infastructure.repositories.auth_repository import AuthRepository
from src.internal.use_cases.auth_service import AuthService
from src.internal.interfaces.auth_interface import AuthInterface
from src.internal.interfaces.data_interface import DataInterface
from src.internal.use_cases.data_service import DataService
from src.internal.entities.health_model import GeneralParameters
from src.internal.interfaces.search_interface import SearchInterface
from src.infastructure.repositories.search_repository import search_repository

# Create a new router
data_router = APIRouter()

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)


search_service = SearchService(search_repository)
data_service = DataService()

export_repository = ExportRepository()
database_repository=DatabaseRepository()
export_service = ExportService(database_repository, export_repository)


@data_router.get("/quantitative_metrics/{token}")
async def get_quantitative_metrics(
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
        general_metrics = data_interface.get_quantitative_metrics(id_info["sub"])

        if general_metrics is None:
            raise HTTPException(status_code=404, detail="General metrics not found")

        # Return the general metrics
        return general_metrics

    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get general metrics")


@data_router.get("/assessment_metrics/{token}")
async def get_assessment_metrics(
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

        # Get the assessment metrics for the user
        assessment_metrics = data_interface.get_assessment_metrics(id_info["sub"])

        if assessment_metrics is None:
            raise HTTPException(status_code=404, detail="Assessment metrics not found")

        # Return the assessment metrics
        return assessment_metrics
    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get assessment metrics")


@data_router.get("/recommendations/{token}")
async def get_recommendations(
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

        # Get the recommendations for the user
        recommendations = data_interface.get_recommendations(id_info["sub"])

        # Return the recommendations
        return recommendations
    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get recommendations")


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

        if general_metrics is None:
            raise HTTPException(status_code=404, detail="General metrics not found")

        # Return the general metrics
        return general_metrics

    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get general metrics")


@data_router.put("/general_metrics/{token}")
async def update_general_metrics(
    token: str,
    data: GeneralParameters,
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
        general_metrics = data_interface.update_general_metrics(
            "email", id_info["sub"], data.model_dump(), "general_metrics"
        )

        # Return the general metrics
        return {"message": general_metrics}

    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get general metrics")


from pydantic import BaseModel


class QueryResponse(BaseModel):
    query: str


@data_router.post("/search")
async def search_result(
    query_text: QueryResponse, search_interface: SearchInterface = Depends(search_service)
):
    try:
        # Get the search results
        response = search_interface.search(query_text.query)

        # Return the search results
        return response

    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get search results")


from pydantic import BaseModel

class ExportData(BaseModel):
    export_type: str

@data_router.post("/export-data")
async def export_data(
    export_data: ExportData,
    auth_interface: AuthInterface = Depends(auth_service),
    export_interface: ExportInterface= Depends(export_service),
    token: str = Header(..., alias="Authorization"),
):
    try:
        # Decode the token
        id_info = auth_interface.decode_access_token(token.split(" ")[1])

        # Check if the token is valid
        if id_info is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        print(id_info)

        # Get the general metrics for the user
        export_data = export_interface.export_data(id_info["sub"], export_data.export_type)

        if export_data is None:
            raise HTTPException(status_code=404, detail="Export data not found")

        # Return the general metrics
        return export_data

    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get export data")

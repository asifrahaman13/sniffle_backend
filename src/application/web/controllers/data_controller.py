from src.internal.entities.search import QueryResponse
from src.internal.entities.export import ExportData
from fastapi import APIRouter, Depends, HTTPException, Header
from src.internal.interfaces.export_interface import ExportInterface
from src.internal.interfaces.auth_interface import AuthInterface
from src.internal.interfaces.data_interface import DataInterface
from src.internal.entities.health_model import GeneralParameters
from src.internal.interfaces.search_interface import SearchInterface
from exports.exports import auth_service, data_service, search_service, export_service

# Create a new router
data_router = APIRouter()

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


@data_router.post("/search")
async def search_result(
    query_text: QueryResponse,
    search_interface: SearchInterface = Depends(search_service),
):
    try:
        # Get the search results
        response = search_interface.search(query_text.query)

        # Return the search results
        return response

    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get search results")


@data_router.post("/export-data")
async def export_data(
    export_data: ExportData,
    auth_interface: AuthInterface = Depends(auth_service),
    export_interface: ExportInterface = Depends(export_service),
    token: str = Header(..., alias="Authorization"),
):
    try:
        # Decode the token
        id_info = auth_interface.decode_access_token(token.split(" ")[1])

        # Check if the token is valid
        if id_info is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Get the general metrics for the user
        export_data = export_interface.export_data(
            id_info["sub"], export_data.export_type
        )

        if export_data is None:
            raise HTTPException(status_code=404, detail="Export data not found")

        # Return the general metrics
        return {"message": export_data}

    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail="Failed to get export data")

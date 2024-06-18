from pydantic import BaseModel

class ExportData(BaseModel):
    export_type: str
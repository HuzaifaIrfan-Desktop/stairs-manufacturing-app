



from pydantic import BaseModel, Field
from typing import Union

class CutListParams(BaseModel):
    job_name: str = Field(..., description="Name of the Job")
    assembly_name: str = Field(..., description="Name of the assembly")
    builder_name: str = Field(..., description="Name of the builder")

    summary_items: list[tuple[str, Union[str, int, float]]] = Field(..., description="Summary items for the cut list")
    cut_list_data: list[list[ Union[str, int, float]]] = Field(..., description="Cut list data for the report")

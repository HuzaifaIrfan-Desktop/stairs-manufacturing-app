


from pydantic import BaseModel, Field

class Material(BaseModel):
    material_name: str = Field(..., description="Name of the material")
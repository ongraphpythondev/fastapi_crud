from pydantic import BaseModel

# Create BookRequest Base Model
class BookRequest(BaseModel):
    title : str
    description : str
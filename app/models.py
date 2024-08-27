from pydantic import BaseModel

class OCRRequest(BaseModel):
  prompt: str = "Describe the content of these images."

class OCRResponse(BaseModel):
    response: str


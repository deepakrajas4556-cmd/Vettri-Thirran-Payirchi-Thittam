from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=120)
    parties: str = Field(min_length=2, max_length=5000)
    terms: str = Field(min_length=2, max_length=10000)
    effective_date: str = Field(min_length=2, max_length=100)
    governing_law: str = Field(default="", max_length=500)
    language: str = Field(default="English", min_length=2, max_length=50)
    additional_instructions: str = Field(default="", max_length=5000)

    @field_validator("document_type", "parties", "terms", "effective_date")
    @classmethod
    def strip_required(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value

    @field_validator("governing_law", "additional_instructions")
    @classmethod
    def strip_optional(cls, value: str) -> str:
        return value.strip()

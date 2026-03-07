from pydantic import BaseModel, Field, model_validator
from typing import Annotated


class gpt_pydantic_model(BaseModel):
    input_text: Annotated[str, Field(..., examples=["How can I assist you?"])]

    @model_validator(mode='after')
    def text_checker(cls, model):
        model.input_text = " ".join(model.input_text.split())
        return model
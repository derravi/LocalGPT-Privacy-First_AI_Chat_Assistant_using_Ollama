from pydantic import BaseModel, Field, model_validator
from typing import Annotated,List


class gpt_pydantic_model(BaseModel):
    input_text: Annotated[List[str],Field(..., examples=[["How can I assist you?", "how are you"]])]

    @model_validator(mode='after')
    def text_checker(cls, model):
        model.input_text =[" ".join(model.input_text.split()) for text in model.input_text]
        return model
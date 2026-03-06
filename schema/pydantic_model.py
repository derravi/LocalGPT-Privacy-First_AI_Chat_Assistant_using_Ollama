from pydantic import BaseModel,Field
from typing import Annotated
from pydantic import model_validator

class gpt_model(BaseModel):
    input_text:Annotated[str,Field(...,examples=["How can i Assist you?"])]

    @model_validator(mode='after')
    def text_checker(cls,model):
        model.input_text = " ".join(model.input_text.split())

        return model

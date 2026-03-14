from pydantic import BaseModel, Field
from typing import List

try:

    class gpt_pydantic_model(BaseModel):

        input_text: List[str] = Field(
            ...,
            examples=[["How can I assist you?", "How are you?"]]
        )

except Exception as e:
    print(f"Error:{e}.")
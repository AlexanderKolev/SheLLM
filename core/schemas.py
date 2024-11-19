from pydantic import BaseModel

class Context(BaseModel):
    entire_context: str = ""
    prior_command: str = ""

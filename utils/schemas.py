from pydantic import BaseModel

class Context(BaseModel):
    command_history: str = "No previous commands."
    prior_command: str = "No previous command."

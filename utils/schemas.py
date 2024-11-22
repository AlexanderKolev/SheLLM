from pydantic import BaseModel


class Context(BaseModel):
    last_command: str = "echo 'Hello, World!'"
    last_output: str = "Hello, World!\n"
    session_history: str = ""

    def update_session_history(self, command: str, output: str) -> None:
        """Updates session_history with the last command and output."""
        self.session_history += f"> {command}\n{output}\n"

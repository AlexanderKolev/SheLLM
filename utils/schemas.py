from pydantic import BaseModel


class Context(BaseModel):
    last_command: str = "echo 'Hello, World!'"
    last_output: str = "Hello, World!\n"
    tui_history: str = ""

    def update_tui_history(self, command: str, output: str) -> None:
        """Updates tui_history with the last command and output."""
        self.tui_history += f"> {command}\n{output}\n"

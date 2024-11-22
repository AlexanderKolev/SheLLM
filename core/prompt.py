import os
import getpass
from datetime import datetime
from colorama import Fore, Style
from .git import get_git_info
from utils.schemas import Context


def get_prompt():
    """Constructs a customized prompt with user, host, path, git and venv info."""
    user = getpass.getuser()
    host = os.uname().nodename
    path = os.getcwd()
    if len(path) > 42:
        path = "../" + os.path.basename(path)
    git_info = get_git_info()
    venv = os.environ.get('VIRTUAL_ENV', '').split('/')[-1] if os.environ.get('VIRTUAL_ENV') else ""
    current_time = datetime.now().strftime('%H:%M:%S')
    prompt_parts = [
        f"{Fore.RED}[SheLLM]{Style.RESET_ALL}",
        f"{Fore.BLUE}[{current_time}]{Style.RESET_ALL}",
        f"{Fore.GREEN}{user}{Style.RESET_ALL}@{host}:",
        f"{Fore.GREEN}{path}{Style.RESET_ALL}"
    ]
    if git_info:
        prompt_parts.append(f"{Fore.CYAN}({git_info}){Style.RESET_ALL}")
    if venv:
        prompt_parts.append(f"{Fore.MAGENTA}(venv:{venv}){Style.RESET_ALL}")
    return ' '.join(prompt_parts) + "\n>"

def get_openai_system_prompt(context:Context) -> str:
    """Generates the system prompt for OpenAI using the dynamic context."""
    return (
        "You are SheLLM, a shell command generator. Your task is to generate "
        "concise and accurate shell commands based on the provided context of the "
        "user's previous commands. Use the context to infer the user's intent and predict "
        "the next logical command. \n\n"
        "The user's command history should be analyzed to understand patterns and goals:\n"
        f"{context.command_history}\n\n"
        "The last command executed by the user is the most critical context and should be "
        "prioritized when determining the next command:\n"
        f"{context.prior_command}\n\n"
        "Your output must be a single shell command, without any explanations or additional information."
    )

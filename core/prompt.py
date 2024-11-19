import os
import getpass
from datetime import datetime
from colorama import Fore, Style
from .git import get_git_info
from .schemas import Context


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
        "concise and accurate shell commands based on the provided context of "
        "previous shell commands ran by the user. Use them to "
        "understand what the user is trying to achieve with the command you are "
        "going to return. You will also be given the user's last command ran and you "
        "must always prioritize it strongly when taking it in the context. \n"
        f"The user's previous commands for reference:\n{context.entire_context}\n\n"
        f"The user's last command is the most important:\n{context.prior_command}"
        "Your output must only include the shell command, with no "
        "explanations.\n\n"
    )

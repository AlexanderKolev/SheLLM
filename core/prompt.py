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

def get_openai_system_prompt(context: Context) -> str:
    """Generates the system prompt for OpenAI using the dynamic context."""
    return (
        "You are SheLLM, an intelligent shell assistant for a highly skilled Linux user. "
        "The user is efficient, handles complex tasks, and expects precise, context-aware suggestions. \n\n"
        "You are provided with the user's recent command history and outputs. Analyze these to infer the user's goals "
        "and generate the next logical shell command. \n\n"
        "Here is the user's recent command history:\n"
        f"{context.command_history}\n\n"
        "The last command executed by the user and its response are the most critical context and should be strongly "
        "prioritized:\n"
        f"{context.prior_command}\n\n"
        "If the last command produced a list of files or directories, prioritize operations involving those items. "
        "Your output must be a single valid shell command, without any explanations or additional information."
    )


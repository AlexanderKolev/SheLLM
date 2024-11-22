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


def generate_openai_shell_prompt(context: Context) -> str:
    """Generates the system prompt for OpenAI using the dynamic context when a shell command is generated."""
    return (
        "You are SheLLM, a shell command generator. Your task is to generate "
        "accurate shell commands for a highly skilled Linux user. The user expects precise, context-aware suggestions"
        "The user's history of commands and their outputs from their current linux terminal session are given to you "
        f"below and should be analyzed to understand their patterns and goals:\n{context.tui_history}\n\n"
        "The user's most recent command and its output are given to you below -  prioritize them as the primary basis "
        "for inference, while still considering the broader context of the given Shell Session history for "
        "additional insights."        
        f"Most prior command from user:\n{context.last_command}\n"
        f"Response to the most prior command:\n{context.last_command}\n\n"
        "Your output must consist solely of shell commands, with no explanations, additional information, comments, "
        "or symbols not part of the command syntax."
    )


def generate_openai_question_prompt(context: Context) -> str:
    """Generates the user prompt for OpenAI using the dynamic context when a question is asked."""
    return (
        "You are SheLLM, a shell command specialist. Your task is to not discuss other topics, provide short, accurate,"
        " extremely concise, and context-aware shell commands and shell scripting related topics knowledge to a highly "
        f"skilled Linux user. Use for context the user's current terminal session history:\n{context.tui_history}\n\n"
    )

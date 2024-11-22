import os
import logging
from groq import Groq
from dotenv import load_dotenv
from config.logger_setup import setup_logging
from core import prompts
from utils.sanitizer import remove_code_block
from utils.schemas import Context

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

class GroqModel:
    def __init__(self):
        logger.debug("Initializing GroqModel...")
        load_dotenv()
        self.api_key = os.getenv('GROQ_API_KEY')
        logger.debug(f"GROQ_API_KEY: {self.api_key}")
        self.client = Groq(api_key=self.api_key)
        logger.debug("GroqModel initialized.")

    def validate_command(self, command):
        """Validates the command to ensure it is safe and valid to execute."""
        logger.debug(f"Validating command: {command}")
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a senior system administrator who must validate shell commands if there are any errors or not and return the proper/fixed version. Also if the input contains anything other than a pure command (e.g., comments, flags, etc.), you must remove them. If the command is already correct, you must return it as is. If the command is in a code block, you must remove the code block. Use simple commands and avoid using complex commands for fewer errors unless required. Anticipate the user's needs and provide the best possible solution."
                },
                {
                    "role": "user",
                    "content": "ls -d */"
                },
                {
                    "role": "assistant",
                    "content": "ls -d */"
                },
                {
                    "role": "user",
                    "content": """```sh
docker system df | awk '/VOLUME/{getline; while($1 ~ /^[[:alnum:]]/){print $2, $3, $4;s+=($3~/GB/?$2*1024:($3~/kB/?$2/1024:$2));getline}} END{print "Total Size: " s"MB"}' | sort -k1,1rn
```"""
                },
                {
                    "role": "assistant",
                    "content": """sudo docker volume ls -q | xargs -I {} docker volume inspect {} --format='{{ .Name }}{{ printf "\t" }}{{ .Mountpoint }}' | sudo awk '{ system("sudo du -hs " $2) }' | sort -rh"""
                },
                {
                    "role": "user",
                    "content": command
                }
            ]
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages
            )
            logger.debug(f"Response: {response}")
            if response.choices:
                validated_command = response.choices[0].message.content.strip()
                output = remove_code_block(validated_command)
                logger.debug(f"Validated command: {output}")
                return output
            logger.warning("No choices in response.")
            return None
        except Exception as e:
            logger.error(f"Error fetching suggestion from Groq: {e}")
            return None

    def get_command_suggestion(
        self,
        context: Context,
        prompt: str
    ):
        """Generates shell commands based on context and a prompt."""
        logger.debug(f"Generating command suggestion from {self.__class__.__name__} and for prompt: {prompt}")  # noqa
        try:
            messages = [
                {
                    "role": "system",
                    "content": prompts.generate_shell_system_prompt(context)
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages
            )
            logger.debug(f"Response: {response}")
            if response.choices:
                suggested_command = response.choices[0].message.content.strip()
                suggested_command = self.validate_command(suggested_command)
                logger.debug(f"Suggested command: {suggested_command}")
                return suggested_command
            logger.warning("No choices in response.")
            return None
        except Exception as e:
            logger.error(f"Error fetching suggestion from Groq: {e}")
            return None

    def answer_question(
        self,
        context: Context,
        question: str
    ) -> str | None:
        """Generates answers to semantic questions."""
        logger.debug(f"Answering question for context: {context.session_history} and question: {question}")  # noqa
        try:
            messages = [
                {
                    "role": "system",
                    "content": prompts.generate_qa_system_prompt(context)
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages
            )
            logger.debug(f"Response: {response}")
            if response.choices:
                answer = response.choices[0].message.content.strip()
                logger.debug(f"Answer: {answer}")
                return answer
            logger.warning("No choices in response.")
            return None
        except Exception as e:
            logger.error(f"Error fetching answer from Groq: {e}")
            return None

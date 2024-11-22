import openai
import os
import logging
from dotenv import load_dotenv
from core import prompts
from config.logger_setup import setup_logging
from utils.schemas import Context
from utils.sanitizer import remove_code_block

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)


class OpenAIModel:
    def __init__(self):
        logger.debug("Initializing OpenAIModel...")
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI(api_key=self.api_key)
        logger.debug("OpenAIModel initialized.")

    def validate_command(self, command):
        """Validates the command to ensure it is safe and valid to execute."""
        logger.debug(f"Validating command: {command}")
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a senior system administrator who must validate shell commands if there are any errors or not and return the proper/fixed version. Also if the input contains anything other than a pure command (e.g., comments, flags, etc.), you must remove them. If the command is already correct, you must return it as is. If the command is in a code block, you must remove the code block. Use simple commands and avoid using complex commands for fewer errors. Anticipate the user's needs and provide the best possible solution."
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
                model="gpt-4o",
                messages=messages,
                max_tokens=600,
                temperature=0.8
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
            logger.error(f"Error fetching suggestion from OpenAI: {e}")
            return None

    def get_command_suggestion(
        self,
        context: Context,
        prompt: str
    ) -> str | None:
        """Generates shell commands based on context and a prompt."""
        logger.debug(f"Generating command suggestion from {self.__class__.__name__} and prompt: {prompt}")  # noqa
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

            logger.debug(f"Messages sent to API: {messages}")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=4000
            )
            logger.debug(f"Response: {response}")
            if response.choices:
                suggested_command = response.choices[0].message.content.strip()
                logger.debug(f"Suggested command before validation: {suggested_command}")
                suggested_command = self.validate_command(suggested_command)
                logger.debug(f"Suggested command after validation: {suggested_command}")
                return suggested_command
            logger.warning("No choices in response.")
            return None
        except Exception as e:
            logger.error(f"Error fetching suggestion from OpenAI: {e}")
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
            logger.debug(f"Messages sent to API: {messages}")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=4000
            )
            logger.debug(f"Response: {response}")
            if response.choices:
                answer = response.choices[0].message.content.strip()
                logger.debug(f"Answer: {answer}")
                return answer
            logger.warning("No choices in response.")
            return None
        except Exception as e:
            logger.error(f"Error fetching answer from OpenAI: {e}")
            return None

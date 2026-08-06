from dotenv import load_dotenv

from .agents import create_agent, create_character


def main() -> None:
    load_dotenv()  # Load environment variables from .env file

    agent = create_agent()
    character = create_character(agent)
    print(character)

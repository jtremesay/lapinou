import profile

from dotenv import load_dotenv
from pydantic_ai import Agent

load_dotenv()  # Load environment variables from .env file

agent = Agent("ollama:gemma4:cloud")


def main() -> None:
    o = agent.run_sync("What is the capital of France?")
    print(o.output)

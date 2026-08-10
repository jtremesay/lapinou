from pathlib import Path
from typing import Self

from pydantic import BaseModel


class Settings(BaseModel):
    llm_model: str
    google_api_key: str | None = None
    ollama_url: str | None = None
    ollama_api_key: str | None = None

    @classmethod
    def load_from_file(cls, file_path: Path) -> Self:
        with file_path.open("r") as f:
            return cls.model_validate_json(f.read())

    def save_to_file(self, file_path: Path) -> None:
        with file_path.open("w") as f:
            f.write(self.model_dump_json(indent=4))

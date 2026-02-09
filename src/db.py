# database
import json
from pathlib import Path
from typing import List, Literal, Union
from pydantic import BaseModel


class RealFile(BaseModel):
    type: Literal["real"] = "real"
    extension: str
    size: int
    downloaded: bool = False


class Attempts(BaseModel):
    type: Literal["attempts"] = "attempts"
    extensions: List[str] = []


Progress = Union[RealFile, Attempts]


class File(BaseModel):
    dataset: str
    name: str
    url: str
    progress: Progress


def save_db(files: list[File]):
    db_path = Path("db.json")

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump([f.model_dump() for f in files], f, indent=2)


def load_db():
    db_path = Path("db.json")

    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [File.model_validate(item) for item in data]

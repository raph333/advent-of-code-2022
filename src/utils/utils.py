from pathlib import Path
from typing import Union

Int_Convertible = Union[str, int, float]


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def get_file_path(day_number: int, filename: str) -> Path:
    return Path(get_project_root(), 'data', f'day{day_number}', filename)

# def read_file(day_number: int, filename: str) -> str:
#     with open(get_file_path(day_number, filename)) as infile:
#         return infile.read

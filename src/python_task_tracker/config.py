# contains configuration

PRIORITIES = ["low", "medium", "high"]

# database related configuration

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent # resolve method help in understanding symbols in the path
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True) # creates a directory at the path stored in DATA_DIR

# If the directory already exists, exist_ok=True prevents Python from raising an error.

DB_PATH = DATA_DIR / "task.db" # database path

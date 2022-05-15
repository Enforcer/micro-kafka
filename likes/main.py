from pathlib import Path

this_directory = Path(__file__).parent
db_file = this_directory / "likes.db"
DB_URI = f"sqlite:///{db_file}"

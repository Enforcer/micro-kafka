from pathlib import Path
from socket import gethostname

running_in_docker = gethostname() == "docker-transactions"  # set in docker-compose.yml

this_directory = Path(__file__).parent
db_file = this_directory / "transactions.db"
DB_URI = f"sqlite:///{db_file}"

BROKER_URL = "broker:29092" if running_in_docker else "localhost:9092"

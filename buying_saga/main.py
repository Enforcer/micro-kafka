from socket import gethostname

running_in_docker = gethostname() == "docker-catalog"  # set in docker-compose.yml
db_host = "postgres" if running_in_docker else "localhost"

DB_URI = f"postgresql://catalog:catalog@{db_host}:5432/catalog"
BROKER_URL = "broker:29092" if running_in_docker else "localhost:9092"

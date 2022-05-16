from socket import gethostname

running_in_docker = gethostname() == "docker-saga"  # set in docker-compose.yml
db_host = "postgres" if running_in_docker else "localhost"

BROKER_URL = "broker:29092" if running_in_docker else "localhost:9092"

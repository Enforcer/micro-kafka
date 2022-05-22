# Setting up
Build image, download dependencies
```bash
docker-compose build
```

Start zookeeper, broker and UI separately (used by all services)
```bash
docker-compose up broker zookeeper kafka_ui
```

Starting consumers
```bash
docker-compose run --rm saga python consumer.py
```

# FastAPI quick examples
See `examples/fastapi_endpoints_example.py`

# Services
## Kafka UI
`http://localhost:8080/`

## Products
`http://localhost:8100/docs`

## Likes
`http://localhost:8200/docs`

## Catalog
`http://localhost:8300/docs`

## Price estimator
`http://localhost:8400/docs`

## Transactions
`http://localhost:8500/docs`

## Zipkin
`http://localhost:9411`

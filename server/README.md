# Simple server

## Build the image

```
docker image build --no-cache . -t db-archive-server:latest -f ./Dockerfile
```

## Run the container

```
docker compose --file ./docker-compose.yml --env-file ./default.env --project-name db-archive-server up --detach
```

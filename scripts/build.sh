export DOCKER_BUILDKIT=1
docker build --ssh default -t ministerio/tickets-api:latest -f Dockerfile.dev .
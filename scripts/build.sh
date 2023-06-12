export DOCKER_BUILDKIT=1
docker build --ssh default -t localhost:5000/tickets-api:latest -f Dockerfile.dev .
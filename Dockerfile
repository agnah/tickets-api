FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Create destination directory
RUN mkdir -p /app/tickets-api
WORKDIR /app/tickets-api
COPY ./ .
COPY ./prestart.sh ../

# Update sources and install binary requirements
RUN apt-get update && \
    apt-get install curl git -y && \
    pip install --upgrade pip

# Install requirements
RUN pip install -r requirements.txt

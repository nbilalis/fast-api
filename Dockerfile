FROM python:3.10-slim-buster

COPY ./requirements-docker.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# Remove any existing container with same name (--force: if it's running, kill it)
# docker rm fast-api-container --force

# Remove any existing image with same name
# docker rmi fast-api
# docker image rm fast-api

# Build an image from current directry (.) and name it as `fast-api`
# docker build -t fast-api .

# Run the 'fast-api' image in a container. Map 80 port to 8080.
# docker run -d --name fast-api-container -p 8080:80 fast-api

# Maybe run another instance/container
# docker run -d --name fast-api-container-2 -p 8081:80 fast-api

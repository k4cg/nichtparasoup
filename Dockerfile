FROM jfloff/alpine-python:3.8

# Install App
RUN pip install nichtparasoup
WORKDIR /app

# Run nichtparasoup
CMD [ "nichtparasoup", "run", "-c", "/app/config.yml" ]

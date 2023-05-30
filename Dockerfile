FROM python:alpine3.17 

# Install App
RUN apk add build-base git
COPY . /app
WORKDIR /app
RUN pip install .

# Run nichtparasoup
CMD [ "nichtparasoup", "run", "-c", "/app/config/sfw.yaml" ]

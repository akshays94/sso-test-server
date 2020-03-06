FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libxmlsec1-dev

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - piedpiper.wsgi:application

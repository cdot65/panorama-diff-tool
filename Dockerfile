# pull base image
FROM python:3.11.2-slim-bullseye

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN groupadd app && useradd -g app -d /home/app app

# set work directory
WORKDIR /code

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# change to the app user
USER app

# default command to execute
ENTRYPOINT ["python", "./app.py"]

FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the contents of the src/ directory to the /app directory in the image
COPY src/ /app/

# Install dependencies from the Pipfile
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

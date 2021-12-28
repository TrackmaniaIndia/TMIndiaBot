FROM python:3.9-slim

# Set pip to have no saved cache
ENV PIP_NO_CACHE_DIR=false \
    POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN pip install -U poetry

# Working Directory
WORKDIR /TMIBot 

# Install Project Dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy the Source Code
COPY . .

ENTRYPOINT [ "python" ]
CMD [ "-m", "TMIBot"]
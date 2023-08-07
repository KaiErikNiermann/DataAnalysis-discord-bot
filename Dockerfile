FROM python:3.11-bookworm

# Install poetry 
RUN pip install poetry
RUN pip install PEP517

WORKDIR /app

# Copy poetry.lock and pyproject.toml
COPY poetry.lock pyproject.toml /app/

# Initialize project 
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app

# Run the application
CMD ["poetry", "run", "python", "src/main.py"]
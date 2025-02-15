# Use official Python image as base
FROM python:3.12

# Environment variables for Poetry
ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Install Poetry inside the container
RUN pip install poetry==2.1.0

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copy only the dependency files first (for better caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies via Poetry
RUN poetry install

# Copy the rest of the application
COPY . .

# Expose Django's default port (8000)
EXPOSE 8000

# Start Django server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

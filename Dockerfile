FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data
COPY .env .env

# This line sets the default command for the Docker container.
# When the container starts, it will execute:
#   python -m src.main
# - "python": invokes the Python interpreter.
# - "-m src.main": runs the module 'src.main' as a script.
# This means the 'main()' function in src/main.py will trigger,
# launching the ETL pipeline automatically when the container runs.
CMD ["python", "-m", "src.main"]
FROM python:3.12-slim

# Avoid Python creating .pyc files and buffering output, which is useful for debugging in Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establish the working directory in the container
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies of the system required if needed
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code
COPY . .

# Expose the port that the FastAPI will run on
EXPOSE 8000

# Command to start the API (adjusted for Docker)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
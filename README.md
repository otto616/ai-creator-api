# AI Creator API

This repository contains the backend service for the AI features integrated into my personal portfolio. It acts as a secure proxy between the frontend and Hugging Face's inference models, ensuring API keys remain protected and traffic is managed effectively.

The API is built with **FastAPI**, fully **Dockerized**, and designed to be **stateless**.

## Tech Stack

* **Framework:** FastAPI (Python 3.12)
* **AI Engine:** Hugging Face Hub API
* **Security:** `slowapi` for Rate Limiting (IP-based)
* **Infrastructure:** Docker (Debian-slim image)
* **Deployment:** Render

## Key Features

* **Token Security:** All AI model interactions happen server-side to keep secrets hidden.
* **Rate Limiting:** Restricted to 8 requests per minute per IP to prevent abuse and manage Hugging Face usage limits.
* **Automatic Docs:** Interactive Swagger UI available at `/docs`.
* **CORS Ready:** Configured to accept requests from specific frontend domains and localhost.

## Local Development

You can run this API locally without needing to install Python or dependencies, provided you have Docker installed.

### 1. Clone the repository
```bash
git clone [https://github.com/otto616/ai-creator-api.git](https://github.com/otto616/ai-creator-api.git)
cd ai-creator-api

### 2. Set Env Variables
Create a .env file in the root directory. You will need a Hugging Face Access Token:
HUGGINGFACE_TOKEN=your_hf_token_here

### 3. Run With Docker
docker-compose up -d --build
Once the container is up, visit http://localhost:8000/docs to test the endpoints.

## Production Note
This API is currently hosted on Render's Free Tier.
Note on Latency: Free instances on Render "spin down" after 15 minutes of inactivity. If you are the first person to use the API after a period of silence, the first request will trigger a "Cold Start", which can take about 50 seconds while the container reboots. Subsequent requests will be processed instantly. 

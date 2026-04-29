# Document Intelligence Platform

A focused, real-world backend service designed for document intelligence, built as a technical interview task. This platform provides an API to process document text and uses an LLM (OpenAI) to extract a summary and key entities.

## Tech Stack
- **Python 3.11**
- **FastAPI**
- **OpenAI (gpt-3.5-turbo)**
- **Docker & Docker Compose**

## Features
- **`/api/v1/documents/analyze`**: Endpoint to analyze raw document text. Returns a structured JSON containing a summary and a list of identified entities (with their text and label).
- **Centralized Logging**: Well-structured logging to quickly identify OpenAI errors, validation failures, and runtime issues.
- **Robust Exception Handling**: Custom responses for invalid inputs (400 Bad Request) and upstream LLM provider failures (502 Bad Gateway).
- **Dockerized**: Fully containerized for easy and consistent deployment.

## Getting Started

### Prerequisites
- Docker and Docker Compose installed.
- An OpenAI API Key.

### Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository_url>
   cd printdeed
   ```

2. Configure environment variables:
   Copy the example environment file and provide your OpenAI API key.
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to include your actual API key:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

3. Build and run the services using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

### Usage
Once the container is running, the API will be available at `http://localhost:8000`.

- **Health Check**: `GET http://localhost:8000/health`
- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`

#### Example Request

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/documents/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Google is headquartered in Mountain View, California, and was founded by Larry Page and Sergey Brin."
}'
```

#### Example Response

```json
{
  "summary": "Google is a company headquartered in Mountain View, California, founded by Larry Page and Sergey Brin.",
  "entities": [
    {
      "text": "Google",
      "label": "Organization"
    },
    {
      "text": "Mountain View",
      "label": "Location"
    },
    {
      "text": "California",
      "label": "Location"
    },
    {
      "text": "Larry Page",
      "label": "Person"
    },
    {
      "text": "Sergey Brin",
      "label": "Person"
    }
  ]
}
```

## Project Structure
```text
app/
├── api/             # API routing
├── core/            # Configuration and centralized logging setup
├── models/          # Pydantic schema definitions
├── services/        # Business logic and external API integrations (OpenAI)
└── main.py          # FastAPI application initialization
```

# Document Intelligence Platform

A focused, real-world backend service designed for document intelligence, built as a technical interview task. This platform provides an API to process actual document files (.txt, .pdf, .doc, .docx) and uses an LLM (OpenAI) to extract a precise summary and key entities.

## Tech Stack
- **Python 3.11**
- **FastAPI**
- **OpenAI (gpt-3.5-turbo)**
- **MongoDB** with Motor async driver
- **PyPDF** & **python-docx** (Document parsing)
- **antiword** (Legacy .doc extraction)
- **Docker & Docker Compose**

## Features
- **File Upload Parsing**: The `/api/v1/documents/analyze` endpoint seamlessly accepts `.txt`, `.pdf`, `.docx`, and `.doc` file uploads using `multipart/form-data`.
- **OCR Readiness**: The architecture is built with scale in mind. Placeholders and comments are securely prepared in the parser layer to swap in robust binaries like `xpdf` (`pdftotext`) for high-speed PDF extraction, and Tesseract for Image OCR.
- **Structured Data Extraction**: Leverages the official OpenAI SDK and JSON mode constraints to return guaranteed, strongly-typed JSON outputs containing document summaries and distinct entity lists.
- **MongoDB Persistence**: Stores every document analysis result with the uploaded filename and creation timestamp for later retrieval or audit workflows.
- **Centralized Logging**: Well-structured `stdout` logging across the application to quickly identify validation failures, parse issues, and runtime LLM errors.
- **Robust Exception Handling**: Custom HTTP exception mappings ensure clients receive 400s for bad documents and 502s if the upstream LLM service experiences an outage.
- **Dockerized Foundation**: Securely packaged with optimized `Dockerfile`, pinned requirements (like `httpx`), `.dockerignore`, and `.gitignore` to keep container layers fast and slim.

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
   Edit the `.env` file to include your actual API key and optionally the model:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo-1106
   MONGODB_URL=mongodb://localhost:27018
   MONGODB_DATABASE=printdeed
   MONGODB_PORT=27018
   ```

3. Build and run the services using Make:
   ```bash
   make up
   ```

   Useful local commands:
   ```bash
   make build        # Build backend image
   make up           # Build and run API + MongoDB
   make down         # Stop services
   make logs         # Follow service logs
   make local        # Run MongoDB in Docker and API with local uvicorn reload
   make mongo-shell  # Open mongosh inside the MongoDB container
   ```

   Or run Docker Compose directly:
   ```bash
   docker compose up --build -d
   ```

### Usage
Once the container is running, the API will be available at `http://localhost:8000`.

- **Health Check**: `GET http://localhost:8000/health`
- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`

#### Example Request

```bash
# Create a sample document locally
echo "Google is headquartered in Mountain View, California, and was founded by Larry Page and Sergey Brin." > sample.txt

# Upload the document for intelligence extraction
curl -X 'POST' \
  'http://localhost:8000/api/v1/documents/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample.txt'
```

#### Example Response

```json
{
  "document_type": "Article",
  "language": "English",
  "summary": "Google is a company headquartered in Mountain View, California, founded by Larry Page and Sergey Brin.",
  "key_themes": [
    "Corporate History",
    "Technology Companies",
    "Founders"
  ],
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
  ],
  "sentiment": "Neutral",
  "action_items": []
}
```

## Project Structure
```text
app/
├── api/             # API routing mapping
├── core/            # Configuration logic and centralized logger 
├── models/          # Pydantic schema validation definitions
├── services/        # File parsing, OCR integration, and OpenAI bindings
└── main.py          # FastAPI application initialization
```

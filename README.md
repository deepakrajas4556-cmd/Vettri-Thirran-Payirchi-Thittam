# LegalEase — AI-Powered Legal Document Generator

LegalEase is a local-first FastAPI + Streamlit application for generating editable legal-document drafts with Google Gemini and exporting them to TXT, DOCX, and PDF.

> **Important:** LegalEase generates drafts for informational and workflow purposes. It is not a lawyer, does not provide legal advice, and generated text should be reviewed by a qualified legal professional before use.

## Architecture

```text
Streamlit UI
   │
   │ POST /generate
   ▼
FastAPI backend
   │
   ▼
GeminiDocumentGenerator
   │
   ▼
Google Gemini API

Generated text
   ├── TXT
   ├── DOCX
   └── PDF
```

The supplied project document specifies Streamlit + FastAPI + Gemini, with editable previews and TXT/DOCX/PDF export. This implementation keeps that architecture while using Google's current `google-genai` Python SDK rather than the older `google-generativeai` package.

## Project structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── document_utils/
│   ├── __init__.py
│   ├── sanitize.py
│   └── exporters.py
├── frontend/
│   └── app.py
├── assets/
│   └── README.md
├── tests/
│   ├── test_api.py
│   ├── test_exporters.py
│   └── test_sanitize.py
├── .env.example
├── .gitignore
├── Dockerfile
├── Procfile
├── requirements.txt
└── README.md
```

## 1. Requirements

- Python 3.10+
- A Google Gemini API key
- VS Code recommended

The original project document asks for Python 3.10+, FastAPI, Uvicorn, Streamlit, document/PDF libraries, Pillow, requests and environment-variable support.

## 2. Create the environment

### Windows PowerShell

```powershell
cd LegalEase
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows CMD

```cmd
cd LegalEase
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux

```bash
cd LegalEase
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env`:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000
REQUEST_TIMEOUT=120
```

Keep `.env` private. It is excluded by `.gitignore`.

The model can be changed without editing Python code. For example, `gemini-2.5-flash` is also a stable Gemini API model, subject to account availability.

## 4. Start the backend

Open terminal 1:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 5. Start the Streamlit frontend

Open terminal 2:

```bash
streamlit run frontend/app.py
```

Open the URL shown by Streamlit, normally:

```text
http://localhost:8501
```

## 6. Using the application

1. Select or type a document type.
2. Enter the parties.
3. Enter terms separated by semicolons.
4. Enter the effective date.
5. Optionally enter governing law, language and additional instructions.
6. Click **Generate Document**.
7. Review the generated draft.
8. Edit the text if required.
9. Download TXT, DOCX or PDF.

## 7. API example

```bash
curl -X POST "http://127.0.0.1:8000/generate" ^
  -H "Content-Type: application/json" ^
  -d "{\"document_type\":\"NDA\",\"parties\":\"Jane Doe (Disclosing Party); TechNova Inc. (Receiving Party)\",\"terms\":\"Confidentiality; 2-year term; Return confidential information\",\"effective_date\":\"2026-09-25\"}"
```

The API returns:

```json
{
  "document_type": "NDA",
  "content": "...generated draft...",
  "model": "gemini-3.8-flash"
}
```

## 8. Run tests

```bash
pytest -q
```

The tests cover validation, health endpoints, text sanitization and document export.

## 9. Docker

Build:

```bash
docker build -t legalease .
```

Run:

```bash
docker run --rm -p 8000:8000 --env-file .env legalease
```

For Streamlit in Docker, run the frontend separately or extend the image/compose setup for your deployment environment.

## Notes

- The application does not store generated documents on the server.
- Export files are created in memory and returned to the browser.
- A logo can be supplied through the Streamlit interface; if no logo is supplied, exports use a text brand header.
- The backend validates required fields and limits input size.
- Gemini output is treated as untrusted generated text and is not presented as verified legal advice.

## Docker Compose

For a complete two-container local run:

```bash
docker compose up --build
```

Then open `http://localhost:8501`. The frontend connects to the backend service automatically.

Stop everything with:

```bash
docker compose down
```

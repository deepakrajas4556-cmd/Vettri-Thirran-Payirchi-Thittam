import os

from dotenv import load_dotenv
from backend.schemas import DocumentRequest

load_dotenv()


class GeminiDocumentGenerator:
    """Gemini-backed legal document draft generator."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

        if not self.api_key:
            self.client = None
        else:
            try:
                from google import genai
            except ImportError as exc:
                raise RuntimeError(
                    "The google-genai package is required. Run: pip install -r requirements.txt"
                ) from exc
            self.client = genai.Client(api_key=self.api_key)

    def build_prompt(self, request: DocumentRequest) -> str:
        return f"""
You are the drafting engine for LegalEase, an AI-assisted legal-document
drafting application.

Create a professional DRAFT legal document from the supplied facts.

SAFETY AND ACCURACY RULES:
- Do not claim the document is legally valid, attorney-reviewed, jurisdiction-compliant,
  or guaranteed accurate.
- Do not invent names, dates, addresses, amounts, statutes, citations, signatures,
  or other material facts.
- If a material fact is missing, use a clear placeholder such as [INSERT AMOUNT]
  instead of inventing it.
- Preserve user-supplied facts exactly where possible.
- Use neutral professional legal language.
- Structure the draft with a title, introductory/recital section where appropriate,
  numbered sections, and signature blocks.
- Include the requested terms.
- Add common boilerplate only when it is appropriate to the document type, and mark
  jurisdiction-sensitive language for professional review.
- End with a short "Review Notice" stating that the draft should be reviewed by
  a qualified legal professional before execution.
- Output plain text only. Do not use Markdown fences.

DOCUMENT TYPE:
{request.document_type}

PARTIES:
{request.parties}

TERMS / CONDITIONS:
{request.terms}

EFFECTIVE DATE:
{request.effective_date}

GOVERNING LAW:
{request.governing_law or "[NOT SPECIFIED]"}

LANGUAGE:
{request.language}

ADDITIONAL INSTRUCTIONS:
{request.additional_instructions or "[NONE]"}

Generate the complete draft now.
""".strip()

    def generate_document(self, request: DocumentRequest) -> str:
        if self.client is None:
            raise ValueError(
                "GEMINI_API_KEY is not configured. Copy .env.example to .env "
                "and add a valid Gemini API key."
            )

        prompt = self.build_prompt(request)

        from google.genai import types

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.25,
                max_output_tokens=8192,
            ),
        )

        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise ValueError("Gemini returned an empty response.")

        return text.strip()

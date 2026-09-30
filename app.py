import html
import os

import requests
import streamlit as st
from dotenv import load_dotenv

from document_utils.exporters import format_docx, format_pdf, format_txt
from document_utils.sanitize import sanitize_text

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "120"))

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1200px; padding-top: 2rem; }
    .legal-card {
        border: 1px solid #333;
        border-radius: 12px;
        padding: 24px;
        background: #111827;
        color: #f3f4f6;
        max-height: 620px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.65;
    }
    .small-note { color: #6b7280; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚖️ LegalEase")
st.caption("AI-powered legal document drafting with editable preview and TXT / DOCX / PDF export.")

with st.sidebar:
    st.header("Document Settings")
    document_type = st.selectbox(
        "Document type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "General Agreement",
            "Custom",
        ],
    )
    if document_type == "Custom":
        document_type = st.text_input("Custom document type", "Legal Agreement")

    language = st.selectbox("Language", ["English", "Tamil", "Hindi", "Telugu", "Kannada", "Malayalam"])
    governing_law = st.text_input("Governing law / jurisdiction", "")
    effective_date = st.text_input("Effective date", "25/09/2026")
    logo = st.file_uploader("Optional logo", type=["png", "jpg", "jpeg"])

left, right = st.columns(2)

with left:
    st.subheader("Parties")
    parties = st.text_area(
        "Names and roles",
        placeholder="Jane Doe (Service Provider); TechNova Inc. (Client)",
        height=140,
    )

    st.subheader("Terms & Conditions")
    terms = st.text_area(
        "Use semicolons to separate terms",
        placeholder=(
            "Payment within 30 days of invoice; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=180,
    )

    additional = st.text_area(
        "Additional instructions",
        placeholder="Add any special drafting instructions or placeholders.",
        height=120,
    )

    generate = st.button("✨ Generate Document", type="primary", use_container_width=True)

with right:
    st.subheader("Document Preview")
    if "document" not in st.session_state:
        st.info("Your generated document will appear here.")

    if generate:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
            "governing_law": governing_law,
            "language": language,
            "additional_instructions": additional,
        }

        try:
            with st.spinner("Generating your draft..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=REQUEST_TIMEOUT,
                )
            if response.ok:
                st.session_state.document = sanitize_text(response.json()["content"])
                st.session_state.document_type = document_type
                st.session_state.terms = terms
                st.success("Draft generated.")
            else:
                detail = response.json().get("detail", response.text)
                st.error(f"Backend error: {detail}")
        except requests.RequestException as exc:
            st.error(
                "Could not reach the FastAPI backend. Start it with "
                "`uvicorn backend.main:app --reload --port 8000`."
            )
            st.caption(str(exc))

if "document" in st.session_state:
    edited = st.text_area(
        "Editable document",
        value=st.session_state.document,
        height=520,
        key="editable_document",
    )
    st.session_state.document = edited

    preview = html.escape(edited).replace("\n", "<br>")
    st.markdown("#### Styled Preview")
    st.markdown(f'<div class="legal-card">{preview}</div>', unsafe_allow_html=True)

    st.markdown("#### Download")
    logo_bytes = logo.getvalue() if logo is not None else None

    txt_bytes = format_txt(edited)
    docx_bytes, docx_name = format_docx(
        edited,
        st.session_state.document_type,
        logo_bytes=logo_bytes,
        terms=st.session_state.get("terms", ""),
    )
    pdf_bytes, pdf_name = format_pdf(
        edited,
        st.session_state.document_type,
        logo_bytes=logo_bytes,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "Download TXT",
            data=txt_bytes,
            file_name=f"{st.session_state.document_type.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name=docx_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=pdf_name,
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.markdown(
    '<p class="small-note">LegalEase is an AI-assisted drafting tool, not a substitute for qualified legal advice. '
    'Review generated documents for jurisdiction, facts, dates, obligations and signatures before use.</p>',
    unsafe_allow_html=True,
)

from document_utils.exporters import format_docx, format_pdf, format_txt


def test_txt_export():
    data = format_txt("Test document")
    assert data == b"Test document"


def test_docx_export():
    data, filename = format_docx(
        "AGREEMENT\nThis is a test.",
        "Test Agreement",
        terms="Payment;Confidentiality",
    )
    assert filename.endswith(".docx")
    assert data.startswith(b"PK")


def test_pdf_export():
    data, filename = format_pdf("AGREEMENT\nThis is a test.", "Test Agreement")
    assert filename.endswith(".pdf")
    assert data.startswith(b"%PDF")

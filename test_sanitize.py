from document_utils.sanitize import sanitize_text


def test_sanitize_normalizes_quotes_and_spacing():
    text = "Hello\u2019s   world\n\n\nNext"
    assert sanitize_text(text) == "Hello's   world\n\nNext"

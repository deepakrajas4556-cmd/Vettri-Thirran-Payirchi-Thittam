import re


def sanitize_text(text: str) -> str:
    """Normalize generated text without changing its substantive wording."""
    if not text:
        return ""

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\ufeff": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

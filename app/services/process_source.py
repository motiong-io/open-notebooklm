
from pathlib import Path
from pypdf import PdfReader
from app.constants import ERROR_MESSAGE_NOT_PDF, ERROR_MESSAGE_READING_PDF
import time
import requests
from app.constants import JINA_READER_URL, JINA_RETRY_ATTEMPTS, JINA_RETRY_DELAY

def process_pdf(file: str) -> str:
    """Extract text from the PDF file."""
    if not file.lower().endswith(".pdf"):
        return ERROR_MESSAGE_NOT_PDF

    try:
        text = ""
        with Path(file).open("rb") as f:
            reader = PdfReader(f)
            text += "\n\n".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        return f"{ERROR_MESSAGE_READING_PDF}: {str(e)}"
    return text



def process_url(url: str) -> str:
    """Extract text from the URL."""
    try:
        text = ""
        url_text = parse_url(url)
        text += "\n\n" + url_text
    except ValueError as e:
        return str(e)
    return text
    


def parse_url(url: str) -> str:
    """Parse the given URL and return the text content."""
    for attempt in range(JINA_RETRY_ATTEMPTS):
        try:
            full_url = f"{JINA_READER_URL}{url}"
            response = requests.get(full_url, timeout=60)
            response.raise_for_status()  # Raise an exception for bad status codes
            break
        except requests.RequestException as e:
            if attempt == JINA_RETRY_ATTEMPTS - 1:  # Last attempt
                raise ValueError(
                    f"Failed to fetch URL after {JINA_RETRY_ATTEMPTS} attempts: {e}"
                ) from e
            time.sleep(JINA_RETRY_DELAY)  # Wait for X second before retrying
    return response.text

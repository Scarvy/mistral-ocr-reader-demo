import json
import os
import requests
from pathlib import Path

from mistralai import Mistral, DocumentURLChunk
from mistralai.models import OCRResponse
import markdown2
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(
            f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})"
        )
    return markdown_str


def get_combined_markdown(ocr_response: OCRResponse) -> str:
    markdowns: list[str] = []
    for page in ocr_response.pages:
        image_data = {}
        for img in page.images:
            image_data[img.id] = img.image_base64
        markdowns.append(replace_images_in_markdown(page.markdown, image_data))

    return "\n\n".join(markdowns)

def write_to_file(filename: str, content: str) -> None:
    with open(filename, "w") as f:
        f.write(content)

for pdf_file in Path("important").glob("*.pdf"):
    assert pdf_file.is_file(), "File not found"

    print(f"Uploading {pdf_file.stem} to Mistral AI for OCR...")

    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
    )

    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

    pdf_response = client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url),
        model="mistral-ocr-latest",
        include_image_base64=True,
        image_min_size=100,
    )

    response_dict = json.loads(pdf_response.model_dump_json())
    json_string = json.dumps(response_dict, indent=4)

    markdown = get_combined_markdown(pdf_response)

    Path("output").mkdir(exist_ok=True)

    write_to_file(f"output/{uploaded_file.id}.json", json_string)
    write_to_file(f"output/{uploaded_file.id}.md", markdown)
    
    html = markdown2.markdown(markdown)
    write_to_file(f"output/{uploaded_file.id}.html", html)

    response = requests.post(
        url="https://readwise.io/api/v3/save/",
        headers={"Authorization": f"Token {os.getenv('READWISE_API_KEY')}"},
        json={
            "url": f"https://example.com/article/{uploaded_file.filename}",
            "title": uploaded_file.filename,
            # "should_clean_html": False,
            "html": html,
            "tags": ["mistral-ai", "ocr", "pdf"]
        }
    )

    response.raise_for_status()
    print("Readwise saved successfully!", response.json())

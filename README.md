# Mistral OCR Demo

Use [Mistral's OCR](https://docs.mistral.ai/capabilities/document/#are-there-any-limits-regarding-the-ocr-api) processor to extract text and structured content from PDF documents. Upload converted markdown to html to Reader for testing.

## Usage

> [!NOTE]
> Set your [Reader](https://readwise.io/access_token) and [Mistral](https://console.mistral.ai/api-keys) API keys before running.

```.env
MISTRAL_API_KEY = ""
READER_API_KEY = ""
```

```
uv run index.py
```

## Example

Attention is All You Need

Public Example - https://readwise.io/reader/shared/01jp417tzaqy5b830hg8jamp4v

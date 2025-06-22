# Prompter API

This project provides a simple prompt management system with an optional API for interacting with stored prompts.

## Requirements

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/)

Install dependencies:

```bash
pip install fastapi uvicorn
```

## Running the API

Start the API server with:

```bash
python api.py
```

The server will listen on `http://0.0.0.0:8000` by default. FastAPI automatically provides interactive documentation at `/docs`.

Make sure to set the `OPENAI_API_KEY` environment variable if you plan to use the `regenerate` endpoint.

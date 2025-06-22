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

### Web frontend

This repository includes a small static frontend located in `frontend/`. When the
API server is running you can open `http://localhost:8000/` in your browser to
interact with prompts. The interface supports creating new prompts, viewing all
stored prompts, voting, commenting and regenerating prompts via the API.

Make sure to set the `OPENAI_API_KEY` environment variable if you plan to use the `regenerate` endpoint.

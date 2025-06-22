# Prompter API

This project provides a simple prompt management system with an optional API for interacting with stored prompts.

## Requirements

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/)

Install dependencies:

```bash
pip install fastapi uvicorn openai
```

## Running the API

Start the API server with:

```bash
python api.py
```

The server will listen on `http://0.0.0.0:8000` by default. FastAPI automatically provides interactive documentation at `/docs`.

### Web frontend

This repository includes a small static frontend located in `frontend/`. When the API server is running you can open `http://localhost:8000/` in your browser to interact with prompts. The interface sports a playful neobrutalist design that makes browsing prompt history and jumping back into previous prompts easy. You can create new prompts, view stored prompts, vote, comment and regenerate responses via the API.

Make sure to set the `OPENAI_API_KEY` environment variable if you plan to use the `regenerate` endpoint.

## Generating KQL queries

A helper script `generate_kql.py` has been added to turn natural language requests into Kusto Query Language queries. Provide the question on the command line and the script will output the KQL query produced by OpenAI:

```bash
python generate_kql.py "Find all IPs related to a specific user's sign ins"
```

The script stores the question in the prompt history and then calls the OpenAI API with a system prompt instructing the model to respond only with KQL. Ensure that `OPENAI_API_KEY` is set before running the script.

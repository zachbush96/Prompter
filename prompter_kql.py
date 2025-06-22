# prompter_kql.py
# Combined prompt management and KQL generator script

import json
import uuid
import datetime
import os
import sys
from typing import List, Dict, Any

# Optional: import openai only if needed
try:
    import openai
except ImportError:
    openai = None

# Configure your OpenAI key
env_key = os.getenv("OPENAI_API_KEY")
if not env_key:
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")
if openai:
    openai.api_key = env_key

DB_PATH = "prompts_db.json"

DEFAULT_KQL_SYSTEM_PROMPT = (
    "You are an assistant that generates Kusto Query Language (KQL) queries. "
    "Given a natural language description of a question about security or log data, "
    "respond only with the corresponding KQL query."
)

class PromptManager:
    def __init__(self, db_path: str = DB_PATH, default_system_prompt: str = ""):
        self.db_path = db_path
        self.default_system_prompt = default_system_prompt
        self._ensure_db()
        self._load()

    def _ensure_db(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({"prompts": [], "system_prompt": self.default_system_prompt}, f, indent=4)

    def _load(self):
        with open(self.db_path, 'r') as f:
            self.db = json.load(f)
        if "system_prompt" not in self.db:
            self.db["system_prompt"] = self.default_system_prompt
            self._save()
        elif self.default_system_prompt and not self.db.get("system_prompt"):
            self.db["system_prompt"] = self.default_system_prompt
            self._save()

    def _save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.db, f, indent=4)

    def get_system_prompt(self) -> str:
        return self.db.get("system_prompt", "")

    def set_system_prompt(self, text: str):
        self.db["system_prompt"] = text
        self._save()

    def create_prompt(self, text: str) -> str:
        entry = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.datetime.utcnow().isoformat() + 'Z',
            "iterations": [ {"text": text, "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'} ],
            "thumbs_up": 0,
            "thumbs_down": 0,
            "comments": []
        }
        self.db["prompts"].append(entry)
        self._save()
        return entry["id"]

    def list_prompts(self) -> List[Dict[str, Any]]:
        return self.db.get("prompts", [])

    def rate_prompt(self, prompt_id: str, up: bool = True):
        for p in self.db["prompts"]:
            if p["id"] == prompt_id:
                if up:
                    p["thumbs_up"] += 1
                else:
                    p["thumbs_down"] += 1
                self._save()
                return True
        return False

    def comment(self, prompt_id: str, comment_text: str):
        for p in self.db["prompts"]:
            if p["id"] == prompt_id:
                p["comments"].append({
                    "text": comment_text,
                    "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
                })
                self._save()
                return True
        return False

    def regenerate(self, prompt_id: str, system_prompt: str = None) -> str:
        if not openai:
            raise ImportError("openai package is required for regeneration.")
        for p in self.db["prompts"]:
            if p["id"] == prompt_id:
                last = p["iterations"][-1]["text"]
                messages = []
                stored_system = self.get_system_prompt()
                if stored_system:
                    messages.append({"role": "system", "content": stored_system})
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": last})
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages,
                )
                new_text = response.choices[0].message.content.strip()
                p["iterations"].append({
                    "text": new_text,
                    "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
                })
                self._save()
                return new_text
        raise KeyError(f"Prompt ID {prompt_id} not found")

# Default action: generate KQL from user request
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prompter_kql.py 'your question'")
        sys.exit(1)
    question = " ".join(sys.argv[1:])
    pm = PromptManager()
    pid = pm.create_prompt(question)
    query = pm.regenerate(pid, system_prompt=DEFAULT_KQL_SYSTEM_PROMPT)
    print(query)

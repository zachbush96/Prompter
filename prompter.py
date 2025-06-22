# prom pter.py
# A simple prompt management system: stores history, ratings, comments, and regenerates via OpenAI

import json
import uuid
import datetime
import os
import openai
from typing import List, Dict, Any

# Configure your OpenAI key
env_key = os.getenv("OPENAI_API_KEY")
if not env_key:
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")
openai.api_key = env_key

DB_PATH = "prompts_db.json"

class PromptManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_db()
        self._load()

    def _ensure_db(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({"prompts": [], "system_prompt": ""}, f, indent=4)

    def _load(self):
        with open(self.db_path, 'r') as f:
            self.db = json.load(f)
        if "system_prompt" not in self.db:
            self.db["system_prompt"] = ""
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
        # Use the last iteration as the base
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

# Sample usage
if __name__ == "__main__":
    pm = PromptManager()
    print("Existing prompts:")
    for p in pm.list_prompts():
        print(f"- {p['id']}: {p['iterations'][-1]['text'][:40]}... (👍{p['thumbs_up']} 👎{p['thumbs_down']})")

# Sample prompts_db.json content
# -----------------------------
# {
#     "prompts": [
#         {
#             "id": "11111111-1111-1111-1111-111111111111",
#             "created_at": "2025-06-22T13:00:00Z",
#             "iterations": [
#                 {"text": "Write a friendly greeting message for a chatbot.", "timestamp": "2025-06-22T13:00:00Z"},
#                 {"text": "Write a warm, friendly greeting for a chatbot that welcomes the user by name and offers help.", "timestamp": "2025-06-22T13:05:00Z"}
#             ],
#             "thumbs_up": 1,
#             "thumbs_down": 0,
#             "comments": [
#                 {"text": "Make it more concise.", "timestamp": "2025-06-22T13:06:00Z"}
#             ]
#         },
#         {
#             "id": "22222222-2222-2222-2222-222222222222",
#             "created_at": "2025-06-22T14:00:00Z",
#             "iterations": [
#                 {"text": "Generate a brief summary of today's weather in New York.", "timestamp": "2025-06-22T14:00:00Z"}
#             ],
#             "thumbs_up": 0,
#             "thumbs_down": 0,
#             "comments": []
#         }
#     ]
# }

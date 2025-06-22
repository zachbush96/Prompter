import sys
from prompter import PromptManager

DEFAULT_KQL_SYSTEM_PROMPT = (
    "You are an assistant that generates Kusto Query Language (KQL) queries. "
    "Given a natural language description of a question about security or log data, "
    "respond only with the corresponding KQL query."
)


def generate_kql(question: str) -> str:
    pm = PromptManager()
    # Store the user's question as a prompt and generate a KQL query
    pid = pm.create_prompt(question)
    return pm.regenerate(pid, system_prompt=DEFAULT_KQL_SYSTEM_PROMPT)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_kql.py 'your question'")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    query = generate_kql(question)
    print(query)

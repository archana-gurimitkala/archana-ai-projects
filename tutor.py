import os
import argparse

from dotenv import load_dotenv

# Optional imports are loaded lazily inside functions


def detect_backend() -> str:
    preferred = os.getenv("TUTOR_BACKEND", "").strip().lower()
    if preferred in {"openai", "ollama"}:
        return preferred
    # Auto-detect: prefer OpenAI if API key set
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return "ollama"


def call_openai(system: str, user: str, require_json: bool = False) -> str:
    from openai import OpenAI
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content


def call_ollama(system: str, user: str, require_json: bool = False) -> str:
    import requests
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct")
    prompt = f"<|system|>" + system + "\n<|user|>" + user
    data = {"model": model, "prompt": prompt, "stream": False}
    r = requests.post(f"{host}/api/generate", json=data, timeout=120)
    r.raise_for_status()
    out = r.json().get("response", "").strip()
    return out


def ask_model(system: str, user: str, require_json: bool = False) -> str:
    backend = detect_backend()
    if backend == "openai":
        return call_openai(system, user, require_json=False)
    return call_ollama(system, user, require_json=False)


QA_SYSTEM = (
    "You are a patient AI tutor explaining AI/ML concepts to beginners. Answer the question "
    "clearly with simple language, short paragraphs, and one concrete example. Keep the answer concise."
)

"""
Quiz functionality removed. This project is Q&A-only.
"""


def main():
    load_dotenv(override=True)

    parser = argparse.ArgumentParser(description="AI Tutor (Q&A only)")
    parser.add_argument("--mode", default="qa", choices=["qa"], help="qa: ask your own AI question")
    parser.add_argument("--chat", action="store_true", help="Stay in Q&A mode and answer multiple questions in a loop")
    args = parser.parse_args()

    # Freeform Q&A about AI for beginners (single or chat loop)
    if args.chat:
        print("Type your AI questions (type 'exit' to quit):")
        while True:
            user_q = input("\nYou: ").strip()
            if not user_q or user_q.lower() in {"exit", "quit"}:
                break
            answer = ask_model(QA_SYSTEM, user_q)
            print("\nTutor:")
            print(answer)
        return
    else:
        user_q = input("Ask your AI question: ").strip()
        answer = ask_model(QA_SYSTEM, user_q)
        print("\n--- Answer ---")
        print(answer)
        return


if __name__ == "__main__":
    main()
# 
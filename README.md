# AI Tutor 

A minimal CLI AI Tutor inspired by Week 1 principles: simple prompts, API calls, and structured outputs. Uses OpenAI if `OPENAI_API_KEY` is set; otherwise can fall back to local Ollama.

## Quickstart

```bash
cd /Users/archana/ai_tutor
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit as needed
python tutor.py --mode qa              # single AI question
python tutor.py --mode qa --chat       # open-ended AI Q&A chat
```

## Live Demo (No Terminal)
- Open the Colab notebook `colab_demo.ipynb` in this repo and run it in your browser.
- If this is on GitHub, you can also open via Colab by replacing `<user>` and `<repo>` in the link below after you push:

`https://colab.research.google.com/github/<user>/<repo>/blob/main/colab_demo.ipynb`

Colab steps:
- Run the first cell (installs dependencies)
- Enter your OpenAI API key when prompted
- Ask questions in the last cell; type `exit` to stop

## Backends
- OpenAI: requires `OPENAI_API_KEY` in `.env`
- Ollama: requires `ollama` running locally; set `TUTOR_BACKEND=ollama` and `OLLAMA_MODEL=llama3.1:8b-instruct` (or similar)

## Notes
- This CLI answers students' AI questions in plain language (single or chat mode).
- Keep sessions short and iterative.

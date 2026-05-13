# Blog Writing Crew

A multi-agent AI crew that researches, writes, edits, and creates social media content for blog posts — powered by CrewAI and Groq (llama-3.3-70b-versatile).

## Agents

| Agent                          | Role                                                             |
| ------------------------------ | ---------------------------------------------------------------- |
| **Researcher**           | Investigates the topic with data, incidents, and policy analysis |
| **Writer**               | Turns research into a compelling advocacy blog post              |
| **Editor**               | Polishes the post to publication-ready quality                   |
| **Social Media Manager** | Creates Twitter/X threads and LinkedIn posts from the blog       |

## Output

After running, check the `output/` folder:

- `output/blog_post.md` — Final edited blog post
- `output/social_posts.md` — Twitter thread + LinkedIn post

---

## Setup & Running (Windows)

### Prerequisites

- Python 3.10–3.12 (NOT 3.13 — crewai doesn't support it yet)
- `uv` installed: `pip install uv`

### Quick Start

**Step 1 — Run setup (one time only):**

```
setup.bat
```

**Step 2 — Run the crew:**

```
run.bat
```

That's it. The crew will take 2–5 minutes to complete all four tasks.

---

## Why not `crewai run`?

`crewai run` uses `uv` internally to manage a `.venv` and reinstalls packages each time. This breaks `litellm` (which Groq needs) because of a version conflict between `litellm` and `crewai`'s `openai` dependency.

The fix is to use `python run.py` directly (which `run.bat` does), with the venv set up manually via `setup.bat`. This gives you full control and avoids the conflict.

---

## Changing the Topic

Edit `run.py` and change the `topic` value:

```python
inputs = {
    "topic": "Your new topic here",
    ...
}
```

---

## Project Structure

```
blog_writing_crew/
├── .env                        # Your API keys (keep private!)
├── pyproject.toml              # Project config
├── run.py                      # Main entry point
├── run.bat                     # Windows one-click runner
├── setup.bat                   # Windows one-click setup
├── output/
│   ├── blog_post.md            # Generated blog post
│   └── social_posts.md         # Generated social content
└── src/blog_writing_crew/
    ├── crew.py                 # Crew definition
    ├── main.py                 # CLI entry points
    └── config/
        ├── agents.yaml         # Agent definitions
        └── tasks.yaml          # Task definitions
```

## Environment Variables (`.env`)

```
MODEL=groq/llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_api_key_here
CREWAI_TRACING_ENABLED=false
```

Get a free Groq API key at: https://console.groq.com

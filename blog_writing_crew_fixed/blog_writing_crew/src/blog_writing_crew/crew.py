from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
import time
import litellm

# ── Rate-limit retry patch ────────────────────────────────────────────────────
# Groq free tier: 12,000 TPM. We catch 429s and wait before retrying.
_original_completion = litellm.completion

def _completion_with_retry(*args, **kwargs):
    max_retries = 6
    for attempt in range(max_retries):
        try:
            return _original_completion(*args, **kwargs)
        except litellm.RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            # Parse wait time from error message if available, else back off
            wait = 15 * (attempt + 1)
            err_str = str(e)
            if "Please try again in" in err_str:
                try:
                    wait = float(err_str.split("try again in")[1].split("s")[0].strip()) + 2
                except Exception:
                    pass
            print(f"\n⏳ Groq rate limit hit. Waiting {wait:.0f}s before retry "
                  f"(attempt {attempt + 1}/{max_retries})...\n")
            time.sleep(wait)

litellm.completion = _completion_with_retry
# ─────────────────────────────────────────────────────────────────────────────

# Primary LLM — used for research & writing (token-heavy tasks)
groq_llm = LLM(
    model=os.environ["MODEL"],
    api_key=os.environ["GROQ_API_KEY"]
)

# Light LLM — used for editing & social media (same model, but we add a delay
# between tasks via the crew config to stay under the TPM limit)
groq_llm_light = LLM(
    model=os.environ.get("MODEL_LIGHT", os.environ["MODEL"]),
    api_key=os.environ["GROQ_API_KEY"]
)

@CrewBase
class BlogWritingCrew():
    """Blog Writing Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],  # type: ignore[index]
            llm=groq_llm,
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],  # type: ignore[index]
            llm=groq_llm,
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],  # type: ignore[index]
            llm=groq_llm_light,
            verbose=True
        )

    @agent
    def social_media_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_manager'],  # type: ignore[index]
            llm=groq_llm_light,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])  # type: ignore[index]

    @task
    def writing_task(self) -> Task:
        return Task(config=self.tasks_config['writing_task'])  # type: ignore[index]

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task'],  # type: ignore[index]
            output_file='output/blog_post.md'
        )

    @task
    def social_media_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_media_task'],  # type: ignore[index]
            output_file='output/social_posts.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
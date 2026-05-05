from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

groq_llm = LLM(
    model=os.environ["MODEL"],
    api_key=os.environ["GROQ_API_KEY"]
)

@CrewBase
class BlogWritingCrew():
    """Blog Writing Crew"""

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            llm=groq_llm,
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            llm=groq_llm,
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            llm=groq_llm,
            verbose=True
        )
    @agent
    def social_media_manager(self) -> Agent:
        return Agent(
        config=self.agents_config['social_media_manager'],
        verbose=True
    )


    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def writing_task(self) -> Task:
        return Task(config=self.tasks_config['writing_task'])

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task'],
            output_file='output/blog_post.md'
        )
    @task
    def social_media_task(self) -> Task:
        return Task(
        config=self.tasks_config['social_media_task']
    )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
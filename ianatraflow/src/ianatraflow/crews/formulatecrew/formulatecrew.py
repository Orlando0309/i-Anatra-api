from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class Formulatecrew():
    """Formulatecrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ollama_llms = LLM(
            model="ollama/deepseek-r1",
            base_url="http://localhost:11434/api/generate"
        )
    @agent
    def input_formalizer(self) -> Agent:
        return Agent(
            config=self.agents_config['input_formalizer'], # type: ignore[index]
            llm=self.ollama_llms,
            verbose=True
        )

    @task
    def formalize_task(self) -> Task:
        return Task(
            config=self.tasks_config['formalize_task'], # type: ignore[index]
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Formulatecrew crew"""
      

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
           
        )

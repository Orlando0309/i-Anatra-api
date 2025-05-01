from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import PDFSearchTool
from typing import List

@CrewBase
class Pdfcrew():
    """Pdfcrew crew with decision layer and PDFSearch RAG initialized in __init__"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, pdfFile: str):
        # Initialize the PDFSearch tool with RAG config (OLLAMA bge-m3 embedder)
        self.pdf_tool = PDFSearchTool(
            pdf=pdfFile,
            config=dict(
                llm=dict(
                    provider="ollama",
                    config=dict(
                        model="deepseek-r1",
                        base_url="http://localhost:11434"
                    ),
                ),
                embedder=dict(
                    provider="ollama",
                    config=dict(
                        model="bge-m3",
                        base_url="http://localhost:11434"
                    ),
                ),
            )
        )
        # Shared LLM client for any direct LLM calls
        self.ollama_llms = LLM(
            model="ollama/deepseek-r1",
            base_url="http://localhost:11434/api/generate"
        )

    @agent
    def pdf_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_summarizer'],  # type: ignore[index]
            llm=self.ollama_llms,
            tools=[self.pdf_tool],
            verbose=True
        )

    @agent
    def insight_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['insight_extractor'],  # type: ignore[index]
            llm=self.ollama_llms,
            tools=[self.pdf_tool],
            verbose=True
        )

    @agent
    def educational_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['educational_content_creator'],  # type: ignore[index]
            llm=self.ollama_llms,
            tools=[self.pdf_tool],
            verbose=True
        )

    @agent
    def assessment_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['assessment_specialist'],  # type: ignore[index]
            llm=self.ollama_llms,
            tools=[self.pdf_tool],
            verbose=True
        )

    @agent
    def decider(self) -> Agent:
        return Agent(
            config=self.agents_config['decider'],  # type: ignore[index]
            llm=self.ollama_llms,
            verbose=True
        )

    @task
    def summarize_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_task'],  # type: ignore[index]
            callback=None
        )

    @task
    def key_points_task(self) -> Task:
        return Task(
            config=self.tasks_config['key_points_task'],  # type: ignore[index]
            callback=None
        )

    @task
    def flashcards_task(self) -> Task:
        return Task(
            config=self.tasks_config['flashcards_task'],  # type: ignore[index]
            callback=None
        )

    @task
    def quiz_generator_task(self) -> Task:
        return Task(
            config=self.tasks_config['quiz_generator_task'],  # type: ignore[index]
            callback=None
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Pdfcrew with decider orchestrator, passing PDF path to __init__"""
        # Ensure __init__ has been called with pdfFile
        return Crew(
            agents=[
                self.pdf_summarizer(),
                self.insight_extractor(),
                self.educational_content_creator(),
                self.assessment_specialist(),
                self.decider(),
            ],
            tasks=[
                self.summarize_task(),
                self.key_points_task(),
                self.flashcards_task(),
                self.quiz_generator_task(),
            ],
            manager_agent=self.decider(),
            process=Process.hierarchical,
            verbose=True,
            planning=True,
            knowledge=[self.pdf_tool]
        )

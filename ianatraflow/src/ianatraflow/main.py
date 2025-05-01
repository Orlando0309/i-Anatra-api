#!/usr/bin/env python
from random import randint
from typing import List, Dict, Any
from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from crews.formulatecrew.formulatecrew import Formulatecrew

from crews.pdfcrew.pdfcrew import Pdfcrew

# from crews.poem_crew.poem_crew import PoemCrew

class IanatraFlowState(BaseModel):
    resource: str=""
    content_type: str = "pdf"
    request_type: str=""
    crew_result: str = ""
    validation_passed: bool = False
    retry_count: int = 0
    task:str=""
    max_retries: int = 3
    theme:str=""
    error: str = ""
    context: Dict[str, Any] = {}


class IanatraFlow(Flow[IanatraFlowState]):
    pass
    @start()
    def validate_input(self):
        """Initial validation of input parameters"""
        valid_requests = ['summarize', 'key_points', 'flashcards', 'quiz_generator']
        if self.state.request_type not in valid_requests:
            raise ValueError(f"Invalid request type: {self.state.request_type}")
            
        if not self.state.resource.endswith('.pdf'):
            raise ValueError("Only PDF files are supported")
    
    @listen(validate_input)
    def setup_crew(self):
        """Dynamically configure crew based on request type"""
        try:
          
            # Initialize validation crew
            self.validation_crew = Pdfcrew(self.state.resource)
            
        except Exception as e:
            self.state.error = str(e)
            raise
    @listen(setup_crew)
    def formulize_request(self):
        result = Formulatecrew().crew().kickoff(inputs = {'request':self.state.request_type,'context':self.state.theme})
        self.state.task = result.raw
    @listen(formulize_request)
    def kickoff_test(self):
        if self.validation_crew is not None:
            result = self.validation_crew.crew().kickoff(inputs = {'task':self.state.task})
            print(result.raw)
            return result
        return ""
# class PoemState(BaseModel):
#     sentence_count: int = 1
#     poem: str = ""




# def kickoff():
#     poem_flow = PoemFlow()
#     poem_flow.kickoff()


# def plot():
#     poem_flow = PoemFlow()
#     poem_flow.plot()


# if __name__ == "__main__":
#     kickoff()

def kickoff():
    flow = IanatraFlow()
    flow.state.resource = "D:/github/i-Anatra/i-Anatra-api/Unit-6.pdf"
    flow.state.theme = "World war II"
    flow.state.request_type = "key_points"
    flow.kickoff()


def plot():
    flow = IanatraFlow()
    flow.state.resource = "D:/github/i-Anatra/i-Anatra-api/Unit-6.pdf"
    flow.state.theme = "World war II"
    flow.state.request_type = "key_points"
    flow.plot()


if __name__ == "__main__":
    kickoff()


from langgraph.graph import StateGraph
from nodes import Nodes
from states import IanatraState

class IanatraWorkFlow():
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(IanatraState)
        
        # Add all nodes
        workflow.add_node("decider", nodes.decider)
        workflow.add_node("i_anatra_flow", nodes.i_anatra_flow)
        workflow.add_node("video_flow", nodes.video_flow)
        workflow.add_node("simple_request", nodes.simple_request)
        workflow.add_node("outputer", nodes.outputer)
        
        # Set entry and finish points
        workflow.set_entry_point("decider")
        workflow.set_finish_point("outputer")
        
        # Conditional edges from decider
        workflow.add_conditional_edges(
            "decider",
            nodes.decide_path,
            {
                "pdf": "i_anatra_flow",
                "video": "video_flow",
                "simple": "simple_request"
            }
        )
        
        # Edges to outputer
        workflow.add_edge("i_anatra_flow", "outputer")
        workflow.add_edge("video_flow", "outputer")
        workflow.add_edge("simple_request", "outputer")
        
        self.app = workflow.compile()
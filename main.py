# Initialize state
from graph import IanatraWorkFlow
from states import IanatraState


initial_state = IanatraState(contentType='pdf', done=False, request='get everything to remember')

# Create workflow
workflow = IanatraWorkFlow()

# Run
result = workflow.app.invoke(initial_state)
class Nodes():
    def decider(self, state):
        # Simply pass the state to the condition function
        return state
    
    def decide_path(self, state):
        # Decide the next node based on contentType
        content_type = state.get('contentType', '')
        if content_type in ['pdf', 'text']:
            return 'pdf'
        elif content_type == 'video':
            return 'video'
        else:
            return 'simple'
    
    def i_anatra_flow(self, state):
        # Placeholder for PDF/text processing (e.g., RAG crew)
        state['done'] = True  # Mark as processed
        return state
    
    def video_flow(self, state):
        # Placeholder for video processing crew
        state['done'] = True  # Mark as processed
        return state
    
    def simple_request(self, state):
        # Handle simple requests
        state['done'] = True  # Mark as processed
        return state
    
    def outputer(self, state):
        # Final output (placeholder)
        print("vita tompoko")  # Could be replaced with actual output logic
        return state
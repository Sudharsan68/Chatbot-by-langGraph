class SessionStore:
    def __init__(self):
        self.sessions = {}

    def get_history(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str):
        history = self.get_history(session_id)
        history.append({"role": role, "content": content})

session_store = SessionStore()

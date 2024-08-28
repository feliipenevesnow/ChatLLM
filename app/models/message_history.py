class MessageHistory:
    def __init__(self):
        self.history = []

    def update_history(self, user_message, ai_response):
        self.history.append(("human", user_message))
        self.history.append(("ai", ai_response))

        if len(self.history) > 6:
            self.history = self.history[-6:]

    def format_history_for_prompt(self):
        return [(source, message) for source, message in self.history]

    def clear_history(self):
        self.history = []

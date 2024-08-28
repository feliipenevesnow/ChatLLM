class MessageHistory:
    def __init__(self):
        self.history = []

    def update_history(self, sender_type, message):
        if sender_type in "user":
            self.history.append(("user", message))
        else:
            self.history.append(("ai", message))

        if len(self.history) > 6:
            self.history = self.history[-6:]

    def format_history_for_prompt(self):
        return [(sender_type, message) for sender_type, message in self.history]

    def clear_history(self):
        self.history = []

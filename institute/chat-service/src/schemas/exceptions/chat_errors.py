class ChatNotFoundError(Exception):
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        super().__init__(f"Chat with id '{chat_id}' not found.")
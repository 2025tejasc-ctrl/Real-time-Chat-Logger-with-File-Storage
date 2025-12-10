# logger.py

import os
from datetime import datetime
from chat_class import Message

# Decorator to show "[MESSAGE SENT] - Saved to log"
def message_sent_tag(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("[MESSAGE SENT] - Saved to log")
        return result
    return wrapper


class ChatLogger:
    """
    Handles file operations:
    - master chat_log.txt
    - separate log file for each conversation
    """
    def __init__(self, base_log_file: str = "chat_log.txt", logs_dir: str = "logs"):
        self.base_log_file = base_log_file
        self.logs_dir = logs_dir

        # Make sure logs directory exists
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    def _get_conversation_filename(self, conversation_name: str) -> str:
        safe_name = conversation_name.replace(" ", "_")
        return os.path.join(self.logs_dir, f"{safe_name}.txt")

    @message_sent_tag
    def log_message(self, conversation_name: str, message: Message):
        """
        Append message to:
        - main chat_log.txt
        - separate conversation file
        Format: ISO_TIMESTAMP|conversation|sender|text
        """
        line = f"{message.timestamp.isoformat()}|{conversation_name}|{message.sender.username}|{message.text}\n"

        # Append to main log
        with open(self.base_log_file, "a", encoding="utf-8") as f:
            f.write(line)

        # Append to conversation specific log
        conversation_file = self._get_conversation_filename(conversation_name)
        with open(conversation_file, "a", encoding="utf-8") as f:
            f.write(line)

    def load_conversation_history(self, conversation_name: str) -> list[str]:
        """
        Load raw lines of a specific conversation log.
        """
        conversation_file = self._get_conversation_filename(conversation_name)
        if not os.path.exists(conversation_file):
            return []
        with open(conversation_file, "r", encoding="utf-8") as f:
            return f.readlines()

    def load_full_history(self) -> list[str]:
        """
        Load raw lines of full history from chat_log.txt.
        """
        if not os.path.exists(self.base_log_file):
            return []
        with open(self.base_log_file, "r", encoding="utf-8") as f:
            return f.readlines()

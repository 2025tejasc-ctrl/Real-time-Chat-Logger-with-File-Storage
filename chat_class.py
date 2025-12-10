# chat_class.py

from datetime import datetime

class User:
    """
    Represents a chat user.
    """
    def __init__(self, username: str):
        self.username = username

    def __repr__(self):
        return f"User(username='{self.username}')"


class Message:
    """
    Represents a single chat message.
    """
    def __init__(self, text: str, sender: User, timestamp: datetime | None = None):
        self.text = text
        self.sender = sender
        # If no timestamp provided, use current time
        self.timestamp = timestamp or datetime.now()

    def __str__(self):
        # Lambda for timestamp formatting
        format_time = lambda dt: dt.strftime("%H:%M:%S")
        time_str = format_time(self.timestamp)
        return f"{self.sender.username}: {self.text} ({time_str})"


class Chat:
    """
    Manages a conversation between multiple users.
    """
    def __init__(self, conversation_name: str, users: list[User]):
        self.conversation_name = conversation_name
        self.users = users          # list of User objects
        self.messages: list[Message] = []

    def add_message(self, sender: User, text: str, logger=None):
        """
        Create Message object, store in history and log to file (if logger given).
        """
        msg = Message(text=text, sender=sender)
        self.messages.append(msg)

        # Print to screen in proper format
        print(str(msg))

        # Log to file if logger provided
        if logger is not None:
            logger.log_message(self.conversation_name, msg)

    def get_last_n_messages(self, n: int) -> list[Message]:
        """
        Return last N messages.
        """
        return self.messages[-n:]

    def search_messages(self, keyword: str) -> list[Message]:
        """
        Search in message text (case-insensitive).
        """
        keyword_lower = keyword.lower()
        return [m for m in self.messages if keyword_lower in m.text.lower()]

    def get_stats(self):
        """
        Returns basic statistics for this chat:
        - total messages
        - messages per user
        - chat duration
        """
        total_messages = len(self.messages)

        # Count per user
        per_user = {}
        for msg in self.messages:
            per_user[msg.sender.username] = per_user.get(msg.sender.username, 0) + 1

        # Chat duration
        if total_messages >= 2:
            start_time = self.messages[0].timestamp
            end_time = self.messages[-1].timestamp
            duration_seconds = (end_time - start_time).total_seconds()
        else:
            duration_seconds = 0

        return {
            "total_messages": total_messages,
            "per_user": per_user,
            "duration_seconds": duration_seconds
        }

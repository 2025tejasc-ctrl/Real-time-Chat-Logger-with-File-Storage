# chat_main.py

import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from chat_class import User, Chat
from logger import ChatLogger


def create_default_users():
    """
    You can modify or extend this to add more users.
    """
    alice = User("Alice")
    bob = User("Bob")
    return [alice, bob]


def choose_sender(users: list[User]) -> User:
    print("\nAvailable users:")
    for idx, u in enumerate(users, start=1):
        print(f"{idx}. {u.username}")
    while True:
        try:
            choice = int(input("Choose sender (number): "))
            if 1 <= choice <= len(users):
                return users[choice - 1]
            else:
                print("Invalid choice, try again.")
        except ValueError:
            print("Enter a valid number.")


def display_last_n(chat: Chat):
    try:
        n = int(input("How many last messages do you want to see? "))
    except ValueError:
        print("Invalid number.")
        return

    messages = chat.get_last_n_messages(n)
    if not messages:
        print("No messages found.")
        return

    print(f"\nLast {len(messages)} messages in conversation '{chat.conversation_name}':")
    for m in messages:
        print(str(m))


def search_messages(chat: Chat):
    keyword = input("Enter keyword to search: ").strip()
    results = chat.search_messages(keyword)
    if not results:
        print("No messages found with that keyword.")
        return

    print(f"\nMessages containing '{keyword}':")
    for m in results:
        print(str(m))


def show_chat_stats(chat: Chat):
    stats = chat.get_stats()
    print("\nCHAT STATISTICS:")
    print(f"Total Messages: {stats['total_messages']}")
    for username, count in stats["per_user"].items():
        print(f"{username}: {count} messages")
    print(f"Chat Duration: {int(stats['duration_seconds'])} seconds")


def show_pandas_statistics(log_file: str = "chat_log.txt"):
    """
    Data Analysis & Visualization using Pandas & Matplotlib.
    - Display full history table
    - Message frequency per user
    - Activity timeline chart
    """
    if not os.path.exists(log_file):
        print("\nNo log file found yet. Send some messages first.")
        return

    print("\n=== CHAT HISTORY (Pandas DataFrame) ===")
    df = pd.read_csv(
        log_file,
        sep="|",
        header=None,
        names=["timestamp", "conversation", "sender", "text"],
        parse_dates=["timestamp"]
    )

    print(df)

    # Message frequency per user
    print("\n=== MESSAGE FREQUENCY PER USER ===")
    freq = df["sender"].value_counts()
    print(freq)

    # Save frequency bar chart
    plt.figure()
    freq.plot(kind="bar")
    plt.title("Message Frequency per User")
    plt.xlabel("User")
    plt.ylabel("Number of Messages")
    plt.tight_layout()
    freq_chart_path = "message_frequency.png"
    plt.savefig(freq_chart_path)
    plt.close()
    print(f"\nMessage frequency chart saved as: {freq_chart_path}")

    # Activity timeline (cumulative messages over time)
    df_sorted = df.sort_values("timestamp").copy()
    df_sorted["message_count"] = range(1, len(df_sorted) + 1)

    plt.figure()
    plt.plot(df_sorted["timestamp"], df_sorted["message_count"])
    plt.title("Activity Timeline")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Messages")
    plt.xticks(rotation=45)
    plt.tight_layout()
    timeline_chart_path = "activity_timeline.png"
    plt.savefig(timeline_chart_path)
    plt.close()
    print(f"Activity timeline chart saved as: {timeline_chart_path}")


def main():
    print("CHAT APPLICATION")
    print("B.Tech CSE 25-29 - Python Case Study - ITM Skills University")
    print("-" * 50)

    # Setup users, chat and logger
    users = create_default_users()
    conversation_name = "Alice - Bob"   # You can change this if needed
    chat = Chat(conversation_name=conversation_name, users=users)
    logger = ChatLogger()

    print(f"Conversation: {conversation_name}")
    print(f"Date: {datetime.now().date()}")
    print("-" * 50)

    # Main loop
    while True:
        print("\nMENU:")
        print("1. Send a message")
        print("2. Show last N messages")
        print("3. Search messages")
        print("4. Show chat statistics (current run)")
        print("5. Show full statistics with Pandas")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            sender = choose_sender(users)
            text = input("Enter your message: ").strip()
            if text:
                chat.add_message(sender, text, logger=logger)
            else:
                print("Empty message, not sent.")

        elif choice == "2":
            display_last_n(chat)

        elif choice == "3":
            search_messages(chat)

        elif choice == "4":
            show_chat_stats(chat)

        elif choice == "5":
            show_pandas_statistics()

        elif choice == "6":
            print("Exiting chat application. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()

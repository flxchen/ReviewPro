from google import genai
from os import environ
from dotenv import load_dotenv
from time import time
from model import *

load_dotenv()

def db_write(add_db:User | Feedback | Review):
    """
    Writes a User, Feedback, or Review object to the database.

    Args:
        add_db: The object to be added to the database. Must be one of the specified types.
    """
    db.session.add(add_db)
    db.session.commit()

def isReview(text):
    """
    check if review is authentic to save api call to ai reply
    """
    keywords = ["service", "experience", "product", "team", "staff", "price", "work", "job","review","use"]
    return any(word in text.lower() for word in keywords)

def getClient():
    key=environ.get('GEMNI')
    return genai.Client(api_key=key)


user_activity = {}

MAX_REVIEWS = 6
TIME_WINDOW = 60  # seconds

#limit review per user
def is_rate_limited(user_id: str) -> bool:
    """
    Check if a user is rate-limited.
    user_id can be IP address or logged-in user ID.
    """
    now = time()
    timestamps = user_activity.get(user_id, [])
    # Keep only timestamps within the time window
    timestamps = [t for t in timestamps if now - t < TIME_WINDOW]
    
    if len(timestamps) >= MAX_REVIEWS:
        return True
    
    # Save updated timestamps
    timestamps.append(now)
    user_activity[user_id] = timestamps
    return False
import time
import random
import string

# Generate a timestamp-based session ID with random characters
timestamp = int(time.time())
random_chars = ''.join(random.choices(
    string.ascii_uppercase + string.digits, k=3))
session_id = f"{timestamp}_{random_chars}"

print(session_id)

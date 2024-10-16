from datetime import datetime
import os

def is_iso_8601(timestamp: str) -> bool:
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False
    
def format_headers():
    return {'token': os.getenv('ACCESS_TOKEN')}
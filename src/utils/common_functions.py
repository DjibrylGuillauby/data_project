import os
import time

def is_cache_valid(filepath: str, ttl_seconds: int) -> bool:
    """Retourne True si le fichier existe et est plus récent que ttl_seconds."""
    if not os.path.exists(filepath):
        return False
    age_seconds = time.time() - os.path.getmtime(filepath)
    return age_seconds < ttl_seconds

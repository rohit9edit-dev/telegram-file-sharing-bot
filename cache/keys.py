"""Redis cache key patterns"""

def user_key(user_id: int) -> str:
    """User cache key"""
    return f"user:{user_id}"

def file_key(file_id: str) -> str:
    """File cache key"""
    return f"file:{file_id}"

def link_key(link_id: str) -> str:
    """Link cache key"""
    return f"link:{link_id}"

def rate_limit_key(user_id: int, action: str) -> str:
    """Rate limit key"""
    return f"ratelimit:{user_id}:{action}"

def session_key(user_id: int) -> str:
    """User session key"""
    return f"session:{user_id}"

def stats_key(user_id: int) -> str:
    """User stats cache key"""
    return f"stats:{user_id}"

def global_stats_key() -> str:
    """Global stats cache key"""
    return "stats:global"
from datetime import datetime
from typing import Optional

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')

def format_duration(seconds: int) -> str:
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours}h"
    else:
        days = seconds // 86400
        return f"{days}d"

def format_time_remaining(expiry: datetime) -> str:
    """Format time remaining until expiry"""
    now = datetime.utcnow()
    if expiry < now:
        return "Expired"
    
    delta = expiry - now
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    
    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def format_link(link_id: str, bot_username: str) -> str:
    """Format shareable download link"""
    return f"https://t.me/{bot_username}?start=dl_{link_id}"

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_stats(stats: dict) -> str:
    """Format statistics for display"""
    return f"""📊 Statistics:

📁 Total Files: {stats.get('total_files', 0)}
💾 Total Size: {format_file_size(stats.get('total_size', 0))}
🔗 Active Links: {stats.get('active_links', 0)}
📥 Total Downloads: {stats.get('total_downloads', 0)}
👥 Total Users: {stats.get('total_users', 0)}"""
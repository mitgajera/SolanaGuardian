"""
Utility functions for the RugGuard bot
"""

import time
import logging
from datetime import datetime, timedelta
from functools import wraps

logger = logging.getLogger(__name__)

def rate_limit(max_calls=100, period=3600):
    """Rate limiting decorator"""
    def decorator(func):
        func.calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove calls older than the period
            func.calls = [call_time for call_time in func.calls if now - call_time < period]
            
            if len(func.calls) >= max_calls:
                sleep_time = period - (now - func.calls[0])
                logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                func.calls = []
            
            func.calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

def retry_on_failure(max_retries=3, delay=1, backoff=2):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {str(e)}")
                        raise
                    
                    logger.warning(f"Function {func.__name__} failed (attempt {retries}/{max_retries}): {str(e)}")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            return None
        
        return wrapper
    return decorator

def format_large_number(num):
    """Format large numbers with appropriate suffixes (K, M, B)"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)

def calculate_time_ago(timestamp):
    """Calculate human-readable time difference"""
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    
    now = datetime.now(timestamp.tzinfo)
    diff = now - timestamp
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "just now"

def sanitize_username(username):
    """Sanitize username for safe processing"""
    if not username:
        return ""
    
    # Remove @ symbol if present
    username = username.lstrip('@')
    
    # Remove any non-alphanumeric characters except underscore
    import re
    username = re.sub(r'[^a-zA-Z0-9_]', '', username)
    
    return username.lower()

def validate_tweet_text(text):
    """Validate and clean tweet text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    import re
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Truncate if too long
    if len(text) > 280:
        text = text[:277] + "..."
    
    return text

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers, returning default if denominator is zero"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def extract_mentions(text):
    """Extract Twitter mentions from text"""
    import re
    mentions = re.findall(r'@(\w+)', text)
    return [mention.lower() for mention in mentions]

def extract_hashtags(text):
    """Extract hashtags from text"""
    import re
    hashtags = re.findall(r'#(\w+)', text)
    return [hashtag.lower() for hashtag in hashtags]

def is_suspicious_text(text):
    """Check if text contains suspicious patterns"""
    suspicious_patterns = [
        r'\b(guaranteed|100%|risk-free)\b',
        r'\b(moon|lambo|diamond hands)\b',
        r'\b(pump|dump|rug pull)\b',
        r'\b(buy now|urgent|last chance)\b',
        r'🚨+',  # Multiple alarm emojis
        r'\$\d+k|\$\d+m',  # Dollar amounts
    ]
    
    import re
    text_lower = text.lower()
    
    for pattern in suspicious_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    
    return False

def clean_bio(bio):
    """Clean and normalize bio text"""
    if not bio:
        return ""
    
    import re
    
    # Remove excessive emojis
    bio = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]{3,}', '', bio)
    
    # Remove excessive punctuation
    bio = re.sub(r'[!?]{3,}', '!!!', bio)
    
    # Clean whitespace
    bio = re.sub(r'\s+', ' ', bio.strip())
    
    return bio

def get_engagement_level(engagement_rate):
    """Categorize engagement rate"""
    if engagement_rate >= 5:
        return "Very High"
    elif engagement_rate >= 2:
        return "High"
    elif engagement_rate >= 1:
        return "Medium"
    elif engagement_rate >= 0.1:
        return "Low"
    else:
        return "Very Low"

def log_performance(func):
    """Decorator to log function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds: {str(e)}")
            raise
    
    return wrapper

"""
Configuration Module
Manages application configuration and environment variables
"""

import os
from dotenv import load_dotenv

class Config:
    """Configuration class for the RugGuard bot"""
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        load_dotenv()
        
        # Twitter API Configuration
        self.TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
        self.TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
        self.TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
        self.TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
        
        # Bot Configuration
        self.MONITOR_SPECIFIC_ACCOUNT = os.getenv('MONITOR_SPECIFIC_ACCOUNT', 'false').lower() == 'true'
        self.MONITOR_USERNAME = os.getenv('MONITOR_USERNAME', 'projectrugguard')
        
        # Rate Limiting
        self.CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))  # seconds
        self.MAX_REQUESTS_PER_HOUR = int(os.getenv('MAX_REQUESTS_PER_HOUR', '100'))
        
        # Trust List Configuration
        self.TRUST_LIST_URL = os.getenv('TRUST_LIST_URL', 'https://raw.githubusercontent.com/devsyrem/turst-list/main/list')
        self.TRUST_LIST_UPDATE_INTERVAL = int(os.getenv('TRUST_LIST_UPDATE_INTERVAL', '3600'))  # seconds
        
        # Logging Configuration
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', 'rugguard_bot.log')
        
        # Analysis Configuration
        self.MAX_RECENT_TWEETS = int(os.getenv('MAX_RECENT_TWEETS', '20'))
        self.MIN_ACCOUNT_AGE_DAYS = int(os.getenv('MIN_ACCOUNT_AGE_DAYS', '30'))
        self.MIN_FOLLOWERS = int(os.getenv('MIN_FOLLOWERS', '10'))
        
        # Validate required configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate that required configuration is present"""
        required_keys = [
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET',
            'TWITTER_ACCESS_TOKEN',
            'TWITTER_ACCESS_TOKEN_SECRET',
            'TWITTER_BEARER_TOKEN'
        ]
        
        missing_keys = []
        for key in required_keys:
            if not getattr(self, key):
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
    
    def get_twitter_auth(self):
        """Get Twitter API authentication credentials"""
        return {
            'consumer_key': self.TWITTER_API_KEY,
            'consumer_secret': self.TWITTER_API_SECRET,
            'access_token': self.TWITTER_ACCESS_TOKEN,
            'access_token_secret': self.TWITTER_ACCESS_TOKEN_SECRET,
            'bearer_token': self.TWITTER_BEARER_TOKEN
        }
    
    def __str__(self):
        """String representation of configuration (excluding secrets)"""
        return f"""RugGuard Bot Configuration:
- Monitor specific account: {self.MONITOR_SPECIFIC_ACCOUNT}
- Monitor username: {self.MONITOR_USERNAME}
- Check interval: {self.CHECK_INTERVAL}s
- Max requests/hour: {self.MAX_REQUESTS_PER_HOUR}
- Log level: {self.LOG_LEVEL}
- Max recent tweets: {self.MAX_RECENT_TWEETS}
"""

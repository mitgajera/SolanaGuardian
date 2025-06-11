"""
Trust List Checker Module
Checks users against the public trust list from GitHub
"""

import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TrustListChecker:
    """Checks users against the public trust list and analyzes their followers"""
    
    def __init__(self, config):
        """Initialize the trust list checker"""
        self.config = config
        self.trust_list_url = "https://raw.githubusercontent.com/devsyrem/turst-list/main/list"
        self.trust_list = None
        self.last_update = None
        self.cache_duration = timedelta(hours=1)  # Update trust list hourly
        
        # Initialize Twitter API client for follower checking
        try:
            import tweepy
            client = tweepy.Client(
                bearer_token=config.TWITTER_BEARER_TOKEN,
                consumer_key=config.TWITTER_API_KEY,
                consumer_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            self.client = client
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API client for trust checker: {str(e)}")
            raise
    
    def check_trust_list(self, username):
        """Check if user has connections to trusted users"""
        try:
            # Update trust list if needed
            if not self._is_trust_list_current():
                self._update_trust_list()
            
            if not self.trust_list:
                logger.warning("Trust list not available")
                return 0
            
            # Check if user is directly in trust list
            if username.lower() in [user.lower() for user in self.trust_list]:
                logger.info(f"User {username} found in trust list")
                return 100
            
            # Check follower connections to trust list
            trust_connections = self._check_follower_connections(username)
            
            # Score based on trust connections
            if trust_connections >= 5:
                score = 100
            elif trust_connections >= 3:
                score = 80
            elif trust_connections >= 2:
                score = 60
            elif trust_connections >= 1:
                score = 40
            else:
                score = 0
            
            logger.info(f"User {username} has {trust_connections} trust connections, score: {score}")
            return score
            
        except Exception as e:
            logger.error(f"Error checking trust list for {username}: {str(e)}")
            return 0
    
    def _is_trust_list_current(self):
        """Check if trust list needs updating"""
        if not self.trust_list or not self.last_update:
            return False
        
        return datetime.utcnow() - self.last_update < self.cache_duration
    
    def _update_trust_list(self):
        """Update trust list from GitHub"""
        try:
            logger.info("Updating trust list from GitHub")
            
            response = requests.get(self.trust_list_url, timeout=10)
            response.raise_for_status()
            
            # Parse the trust list (assuming it's a text file with usernames)
            content = response.text.strip()
            
            # Handle different possible formats
            if content.startswith('[') and content.endswith(']'):
                # JSON format
                import json
                self.trust_list = json.loads(content)
            else:
                # Text format - one username per line
                self.trust_list = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Remove @ symbols if present
            self.trust_list = [username.lstrip('@') for username in self.trust_list]
            
            self.last_update = datetime.utcnow()
            logger.info(f"Trust list updated with {len(self.trust_list)} users")
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch trust list: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing trust list: {str(e)}")
    
    def _check_follower_connections(self, username):
        """Check how many trusted users follow the given user"""
        try:
            if not self.trust_list:
                return 0
            
            # Get user ID
            user_info = self.client.get_user(username=username)
            if not user_info.data:
                return 0
            
            user_id = user_info.data.id
            
            # Get followers of the user (limited sample due to rate limits)
            followers = self.client.get_users_followers(
                id=user_id,
                max_results=100,  # Limited sample
                user_fields=['username']
            )
            
            if not followers.data:
                return 0
            
            # Count connections to trust list
            follower_usernames = [follower.username.lower() for follower in followers.data]
            trust_connections = 0
            
            for trusted_user in self.trust_list:
                if trusted_user.lower() in follower_usernames:
                    trust_connections += 1
                    logger.debug(f"Found trust connection: {trusted_user}")
            
            return trust_connections
            
        except Exception as e:
            logger.error(f"Error checking follower connections for {username}: {str(e)}")
            return 0
    
    def get_trust_list_info(self):
        """Get information about the current trust list"""
        if not self._is_trust_list_current():
            self._update_trust_list()
        
        return {
            'count': len(self.trust_list) if self.trust_list else 0,
            'last_update': self.last_update,
            'is_current': self._is_trust_list_current()
        }

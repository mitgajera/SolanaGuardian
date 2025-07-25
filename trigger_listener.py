"""
Trigger Listener Module
Monitors Twitter for the "riddle me this" trigger phrase
"""

import tweepy
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TriggerListener:
    """Listens for trigger phrases in Twitter replies"""
    
    def __init__(self, config):
        """Initialize the trigger listener with Twitter API client"""
        self.config = config
        self.trigger_phrase = "riddle me this"
        self.last_check_time = datetime.utcnow() - timedelta(minutes=1)
        
        # Initialize Twitter API client
        try:
            client = tweepy.Client(
                bearer_token=config.TWITTER_BEARER_TOKEN,
                consumer_key=config.TWITTER_API_KEY,
                consumer_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            self.client = client
            logger.info("Twitter API client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API client: {str(e)}")
            raise
    
    def check_for_triggers(self):
        """Check for new replies containing the trigger phrase"""
        triggers = []
        
        try:
            # Search for recent tweets containing the trigger phrase
            current_time = datetime.utcnow()
            
            # Build search query - focus on replies only, more efficient
            query = f'"{self.trigger_phrase}" -is:retweet is:reply -is:quote'
            
            # Don't limit to specific account - monitor all "riddle me this" replies
            # This ensures we catch all triggers regardless of who they're replying to
            
            # Search for tweets with better rate limit handling
            try:
                tweets = self.client.search_recent_tweets(
                    query=query,
                    max_results=10,
                    tweet_fields=['created_at', 'author_id', 'in_reply_to_user_id', 'conversation_id', 'text'],
                    expansions=['author_id', 'in_reply_to_user_id'],
                    start_time=self.last_check_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                )
            except tweepy.TooManyRequests:
                logger.warning("Rate limit hit - will retry in next cycle")
                # Don't update last_check_time so we can retry these tweets
                return triggers
            except Exception as e:
                logger.error(f"Error searching tweets: {str(e)}")
                self.last_check_time = current_time
                return triggers
            
            if not tweets or not hasattr(tweets, 'data') or not tweets.data:
                logger.debug("No new triggers found")
                self.last_check_time = current_time
                return triggers
            
            # Process each tweet
            for tweet in tweets.data:
                try:
                    # Check if it's a reply and contains exact trigger phrase
                    if (hasattr(tweet, 'in_reply_to_user_id') and tweet.in_reply_to_user_id and 
                        self.trigger_phrase.lower() in tweet.text.lower()):
                        
                        print(f"🔍 Processing reply tweet: {tweet.id}")
                        print(f"   Reply text: {tweet.text[:100]}...")
                        print(f"   In reply to user ID: {tweet.in_reply_to_user_id}")
                        
                        # Get original tweet author info
                        original_author_id = tweet.in_reply_to_user_id
                        
                        # Get original author username
                        original_author_username = None
                        if hasattr(tweets, 'includes') and tweets.includes and 'users' in tweets.includes:
                            for user in tweets.includes['users']:
                                if user.id == original_author_id:
                                    original_author_username = user.username
                                    break
                        
                        if not original_author_username:
                            # Fallback: get user info separately
                            try:
                                user_info = self.client.get_user(id=original_author_id)
                                if user_info and hasattr(user_info, 'data') and user_info.data:
                                    original_author_username = user_info.data.username
                            except Exception as e:
                                logger.error(f"Failed to get username for user {original_author_id}: {str(e)}")
                                continue
                        
                        trigger_data = {
                            'reply_tweet_id': tweet.id,
                            'reply_author_id': tweet.author_id,
                            'original_author_id': original_author_id,
                            'original_author_username': original_author_username,
                            'conversation_id': tweet.conversation_id,
                            'created_at': tweet.created_at,
                            'trigger_text': tweet.text
                        }
                        
                        triggers.append(trigger_data)
                        print(f"🔔 TRIGGER FOUND!")
                        print(f"   Tweet ID: {tweet.id}")
                        print(f"   Original Author: @{original_author_username}")
                        logger.info(f"Found trigger: {tweet.id} -> analyzing user {original_author_id}")
                        
                except Exception as e:
                    logger.error(f"Error processing tweet {tweet.id}: {str(e)}")
                    continue
            
            self.last_check_time = current_time
            logger.info(f"Found {len(triggers)} new triggers")
            
        except tweepy.TooManyRequests:
            logger.warning("Rate limit exceeded, waiting...")
            time.sleep(900)  # Wait 15 minutes
        except Exception as e:
            logger.error(f"Error checking for triggers: {str(e)}")
        
        return triggers
    
    def get_conversation_context(self, conversation_id):
        """Get additional context from the conversation"""
        try:
            # Get conversation tweets
            tweets = self.client.get_tweets(
                ids=[conversation_id],
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations'],
                expansions=['author_id']
            )
            
            if tweets and hasattr(tweets, 'data') and tweets.data:
                return tweets.data[0]
            
        except Exception as e:
            logger.error(f"Error getting conversation context: {str(e)}")
        
        return None

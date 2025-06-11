"""
Reply Bot Module
Posts automated replies with trustworthiness analysis results
"""

import tweepy
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class ReplyBot:
    """Posts automated replies with analysis results"""
    
    def __init__(self, config):
        """Initialize the reply bot with Twitter API client"""
        self.config = config
        
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
            
            # Verify credentials
            me = self.client.get_me()
            if me.data:
                logger.info(f"Reply bot initialized as @{me.data.username}")
            else:
                raise Exception("Failed to verify Twitter credentials")
                
        except Exception as e:
            logger.error(f"Failed to initialize reply bot: {str(e)}")
            raise
    
    def post_reply(self, reply_to_tweet_id, message):
        """Post a reply to a specific tweet"""
        try:
            # Validate message length (Twitter limit is 280 characters)
            if len(message) > 280:
                message = self._truncate_message(message)
            
            print(f"📤 Attempting to post reply...")
            print(f"   Target Tweet ID: {reply_to_tweet_id}")
            print(f"   Message Length: {len(message)} characters")
            
            # Post the reply
            response = self.client.create_tweet(
                text=message,
                in_reply_to_tweet_id=reply_to_tweet_id
            )
            
            if response and hasattr(response, 'data') and response.data:
                tweet_id = response.data['id']
                print(f"✅ REPLY POSTED SUCCESSFULLY!")
                print(f"   New Tweet ID: {tweet_id}")
                logger.info(f"Successfully posted reply: {tweet_id}")
                return True
            else:
                print(f"❌ Failed to post reply - no response data")
                logger.error("Failed to post reply - no response data")
                return False
                
        except tweepy.TooManyRequests:
            print(f"⏳ Rate limit exceeded when posting reply")
            logger.warning("Rate limit exceeded when posting reply")
            return False
        except tweepy.Forbidden as e:
            print(f"🚫 Forbidden to post reply: {str(e)}")
            logger.error(f"Forbidden to post reply: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error posting reply: {str(e)}")
            logger.error(f"Error posting reply: {str(e)}")
            return False
    
    def _truncate_message(self, message):
        """Truncate message to fit Twitter's character limit"""
        if len(message) <= 280:
            return message
        
        # Try to truncate at a natural break point
        truncated = message[:270]
        
        # Find the last complete word
        last_space = truncated.rfind(' ')
        if last_space > 200:  # Only truncate at word boundary if reasonable
            truncated = truncated[:last_space]
        
        truncated += "... (1/2)"
        
        logger.warning(f"Message truncated from {len(message)} to {len(truncated)} characters")
        return truncated
    
    def post_thread(self, messages, reply_to_tweet_id=None):
        """Post a thread of messages"""
        try:
            tweet_ids = []
            
            for i, message in enumerate(messages):
                if i == 0 and reply_to_tweet_id:
                    # First tweet is a reply
                    response = self.client.create_tweet(
                        text=message,
                        in_reply_to_tweet_id=reply_to_tweet_id
                    )
                elif i > 0:
                    # Subsequent tweets reply to the previous tweet
                    response = self.client.create_tweet(
                        text=message,
                        in_reply_to_tweet_id=tweet_ids[-1]
                    )
                else:
                    # Standalone tweet
                    response = self.client.create_tweet(text=message)
                
                if response.data:
                    tweet_ids.append(response.data['id'])
                    logger.info(f"Posted tweet {i+1}/{len(messages)}: {response.data['id']}")
                    
                    # Small delay between tweets
                    if i < len(messages) - 1:
                        time.sleep(2)
                else:
                    logger.error(f"Failed to post tweet {i+1}/{len(messages)}")
                    break
            
            return len(tweet_ids) == len(messages)
            
        except Exception as e:
            logger.error(f"Error posting thread: {str(e)}")
            return False
    
    def get_tweet_metrics(self, tweet_id):
        """Get metrics for a posted tweet"""
        try:
            tweet = self.client.get_tweet(
                id=tweet_id,
                tweet_fields=['public_metrics', 'created_at']
            )
            
            if tweet.data:
                return {
                    'id': tweet.data.id,
                    'created_at': tweet.data.created_at,
                    'metrics': tweet.data.public_metrics
                }
            
        except Exception as e:
            logger.error(f"Error getting tweet metrics: {str(e)}")
        
        return None
    
    def delete_tweet(self, tweet_id):
        """Delete a tweet (if needed for cleanup)"""
        try:
            response = self.client.delete_tweet(id=tweet_id)
            if response.data and response.data['deleted']:
                logger.info(f"Successfully deleted tweet: {tweet_id}")
                return True
            else:
                logger.error(f"Failed to delete tweet: {tweet_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting tweet {tweet_id}: {str(e)}")
            return False

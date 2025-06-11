#!/usr/bin/env python3
"""
Test specific tweet detection and relationship mapping
"""

import tweepy
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_specific_tweet(tweet_id):
    """Test detection of a specific tweet and its relationships"""
    try:
        config = Config()
        
        client = tweepy.Client(
            bearer_token=config.TWITTER_BEARER_TOKEN,
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        
        print(f"Testing tweet ID: {tweet_id}")
        
        # Get the specific tweet
        tweet = client.get_tweet(
            id=tweet_id,
            tweet_fields=['created_at', 'author_id', 'in_reply_to_user_id', 'conversation_id', 'referenced_tweets'],
            expansions=['author_id', 'in_reply_to_user_id', 'referenced_tweets.id']
        )
        
        if not tweet or not hasattr(tweet, 'data') or not tweet.data:
            print(f"Could not fetch tweet {tweet_id}")
            return
        
        tweet_data = tweet.data
        print(f"\nTweet Analysis:")
        print(f"ID: {tweet_data.id}")
        print(f"Text: {tweet_data.text}")
        print(f"Author ID: {tweet_data.author_id}")
        print(f"In reply to user ID: {getattr(tweet_data, 'in_reply_to_user_id', 'None')}")
        print(f"Conversation ID: {getattr(tweet_data, 'conversation_id', 'None')}")
        
        # Check if this is a reply
        if hasattr(tweet_data, 'in_reply_to_user_id') and tweet_data.in_reply_to_user_id:
            print(f"\nThis IS a reply to user ID: {tweet_data.in_reply_to_user_id}")
            
            # Get the original author's info
            try:
                original_user = client.get_user(id=tweet_data.in_reply_to_user_id)
                if original_user and hasattr(original_user, 'data') and original_user.data:
                    print(f"Original author: @{original_user.data.username}")
                    print(f"Original author name: {original_user.data.name}")
                else:
                    print("Could not get original author info")
            except Exception as e:
                print(f"Error getting original author: {e}")
        else:
            print("\nThis is NOT a reply")
        
        # Check if it contains the trigger phrase
        if "riddle me this" in tweet_data.text.lower():
            print(f"\nContains trigger phrase: YES")
        else:
            print(f"\nContains trigger phrase: NO")
        
        # Show includes data
        if hasattr(tweet, 'includes') and tweet.includes:
            print(f"\nIncludes data available:")
            if hasattr(tweet.includes, 'users') and tweet.includes.users:
                print(f"Users: {len(tweet.includes.users)}")
                for user in tweet.includes.users:
                    print(f"  - @{user.username} (ID: {user.id})")
        
    except Exception as e:
        print(f"Error testing tweet: {e}")

if __name__ == "__main__":
    # Test the specific tweet ID you mentioned
    test_specific_tweet("1932847635825897540")
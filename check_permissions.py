#!/usr/bin/env python3
"""
Check Twitter API permissions and test posting capability
"""

import tweepy
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_twitter_permissions():
    """Check Twitter API permissions and capabilities"""
    try:
        config = Config()
        
        # Initialize Twitter API client
        client = tweepy.Client(
            bearer_token=config.TWITTER_BEARER_TOKEN,
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        
        # Test 1: Get authenticated user info
        print("🔍 Testing authenticated user access...")
        me = client.get_me()
        if me and me.data:
            print(f"✅ Successfully authenticated as: @{me.data.username}")
            print(f"   User ID: {me.data.id}")
            print(f"   Name: {me.data.name}")
        else:
            print("❌ Failed to get authenticated user info")
            return False
        
        # Test 2: Check if we can read tweets
        print("\n🔍 Testing tweet reading capability...")
        try:
            tweets = client.search_recent_tweets(
                query="hello",
                max_results=10,
                tweet_fields=['created_at', 'author_id']
            )
            if tweets and hasattr(tweets, 'data') and tweets.data:
                print(f"✅ Successfully read {len(tweets.data)} tweets")
            else:
                print("⚠️ Could not read tweets (may be rate limited)")
        except Exception as e:
            print(f"❌ Error reading tweets: {str(e)}")
        
        # Test 3: Try to create a test tweet (will help identify permission issues)
        print("\n🔍 Testing tweet creation capability...")
        try:
            test_tweet = "RugGuard Bot Test - API Permission Check"
            response = client.create_tweet(text=test_tweet)
            if response and hasattr(response, 'data') and response.data:
                tweet_id = response.data['id']
                print(f"✅ Successfully created test tweet: {tweet_id}")
                
                # Delete the test tweet
                print("🧹 Cleaning up test tweet...")
                client.delete_tweet(id=tweet_id)
                print("✅ Test tweet deleted")
                return True
            else:
                print("❌ Failed to create tweet - no response data")
                return False
                
        except tweepy.Forbidden as e:
            print(f"🚫 PERMISSION ERROR: {str(e)}")
            print("❌ Your Twitter app does not have write permissions")
            print("\n🔧 SOLUTION:")
            print("1. Go to https://developer.twitter.com/en/portal/dashboard")
            print("2. Select your app")
            print("3. Go to Settings > User authentication settings")
            print("4. Set App permissions to 'Read and write'")
            print("5. Regenerate your Access Token and Secret")
            return False
            
        except Exception as e:
            print(f"❌ Error creating tweet: {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 CHECKING TWITTER API PERMISSIONS")
    print("=" * 50)
    
    success = check_twitter_permissions()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ALL TESTS PASSED - Bot can post replies!")
    else:
        print("❌ PERMISSION ISSUES DETECTED - Fix required")
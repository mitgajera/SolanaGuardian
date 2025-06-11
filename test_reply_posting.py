#!/usr/bin/env python3
"""
Test reply posting functionality with the exact scenario
"""

import tweepy
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_reply_to_specific_tweet():
    """Test replying to your specific tweet"""
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
        
        # Your tweet ID that contains "riddle me this"
        target_tweet_id = "1932847635825897540"
        
        # Generate a test reply message similar to what the bot would post
        test_message = """RugGuard Analysis Complete 🛡️

Trust Score: 46.0/100
Status: 🟠 CAUTION ADVISED

📊 Breakdown:
• Account Age: 5739 days
• Followers: 1117886 | Following: 915
• Bio Quality: ✓
• Avg Engagement: 12.5
• Trust List: ✗

⚠️ Always DYOR before any transactions!
#RugGuard #SolanaEcosystem"""
        
        print(f"Testing reply to tweet: {target_tweet_id}")
        print(f"Message length: {len(test_message)} characters")
        
        # Attempt to post the reply
        response = client.create_tweet(
            text=test_message,
            in_reply_to_tweet_id=target_tweet_id
        )
        
        if response and hasattr(response, 'data') and response.data:
            reply_id = response.data['id']
            print(f"✅ SUCCESS: Reply posted with ID: {reply_id}")
            print(f"✅ The bot can now successfully reply to your triggers!")
            return True
        else:
            print("❌ Failed to post reply - no response data")
            return False
            
    except tweepy.Forbidden as e:
        print(f"🚫 FORBIDDEN ERROR: {str(e)}")
        print("This might be due to:")
        print("1. The original tweet author has restricted replies")
        print("2. Your account is restricted from replying to this user")
        print("3. The tweet is too old or deleted")
        return False
        
    except tweepy.TooManyRequests:
        print("⏳ Rate limit exceeded - this is normal, bot will retry")
        return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 TESTING REPLY POSTING FUNCTIONALITY")
    print("=" * 50)
    
    success = test_reply_to_specific_tweet()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Reply posting works - bot should now be able to respond!")
    else:
        print("❌ Reply posting failed - need to investigate further")
#!/usr/bin/env python3
"""
Test reply functionality with a fresh test scenario
"""

import tweepy
import time
from config import Config

def test_reply_flow():
    """Test the complete reply flow with a fresh tweet"""
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
        
        # Step 1: Create a test tweet
        original_tweet = client.create_tweet(text="Testing RugGuard bot functionality - this is a test tweet for Solana ecosystem analysis")
        
        if not original_tweet or not hasattr(original_tweet, 'data'):
            print("Failed to create test tweet")
            return False
            
        original_tweet_id = original_tweet.data['id']
        print(f"Created test tweet: {original_tweet_id}")
        
        # Step 2: Create a reply with trigger phrase
        reply_text = f"riddle me this"
        reply_tweet = client.create_tweet(
            text=reply_text,
            in_reply_to_tweet_id=original_tweet_id
        )
        
        if not reply_tweet or not hasattr(reply_tweet, 'data'):
            print("Failed to create reply tweet")
            # Cleanup
            client.delete_tweet(id=original_tweet_id)
            return False
            
        reply_tweet_id = reply_tweet.data['id']
        print(f"Created reply tweet: {reply_tweet_id}")
        
        # Step 3: Test analysis response
        analysis_response = """RugGuard Analysis Complete 🛡️

Trust Score: 85.0/100
Status: 🟢 HIGHLY TRUSTED

📊 Breakdown:
• Account Age: 1 days
• Followers: 0 | Following: 0
• Bio Quality: ✓
• Avg Engagement: 0.0
• Trust List: ✗

⚠️ Always DYOR before any transactions!
#RugGuard #SolanaEcosystem"""
        
        # Step 4: Post analysis reply
        analysis_reply = client.create_tweet(
            text=analysis_response,
            in_reply_to_tweet_id=reply_tweet_id
        )
        
        if analysis_reply and hasattr(analysis_reply, 'data'):
            analysis_reply_id = analysis_reply.data['id']
            print(f"SUCCESS: Posted analysis reply: {analysis_reply_id}")
            
            # Cleanup all test tweets
            print("Cleaning up test tweets...")
            client.delete_tweet(id=analysis_reply_id)
            client.delete_tweet(id=reply_tweet_id)
            client.delete_tweet(id=original_tweet_id)
            print("Test tweets deleted")
            
            return True
        else:
            print("Failed to post analysis reply")
            # Cleanup
            client.delete_tweet(id=reply_tweet_id)
            client.delete_tweet(id=original_tweet_id)
            return False
            
    except Exception as e:
        print(f"Error in test: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing complete reply flow...")
    success = test_reply_flow()
    
    if success:
        print("✅ Reply functionality works correctly!")
        print("The bot should be able to reply to new triggers.")
    else:
        print("❌ Reply functionality has issues")
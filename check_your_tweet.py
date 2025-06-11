#!/usr/bin/env python3
"""
Simple script to check your specific tweet
"""

import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Twitter client
client = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    wait_on_rate_limit=True
)

tweet_id = "1932849961299026096"

try:
    print(f"Checking tweet: {tweet_id}")
    
    # Get tweet details
    tweet = client.get_tweet(
        tweet_id,
        tweet_fields=['text', 'author_id', 'created_at', 'conversation_id', 'in_reply_to_user_id'],
        expansions=['author_id', 'in_reply_to_user_id'],
        user_fields=['username', 'name', 'public_metrics']
    )
    
    if tweet.data:
        print(f"✅ Tweet found")
        print(f"Text: {tweet.data.text}")
        print(f"Author ID: {tweet.data.author_id}")
        print(f"In reply to: {tweet.data.in_reply_to_user_id}")
        
        # Check for trigger phrase
        if "riddle me this" in tweet.data.text.lower():
            print(f"✅ Contains trigger phrase")
            
            if tweet.data.in_reply_to_user_id:
                print(f"✅ Is a reply to user: {tweet.data.in_reply_to_user_id}")
                
                # Get the original author info
                if hasattr(tweet, 'includes') and tweet.includes and 'users' in tweet.includes:
                    for user in tweet.includes['users']:
                        if str(user.id) == str(tweet.data.in_reply_to_user_id):
                            print(f"✅ Original author: @{user.username}")
                            break
            else:
                print("❌ Not a reply")
        else:
            print("❌ No trigger phrase found")
    else:
        print("❌ Tweet not found")
        
except Exception as e:
    print(f"Error: {e}")
#!/usr/bin/env python3
"""
Test script to check your specific tweet and trigger detection
"""

import os
from dotenv import load_dotenv
import tweepy
from config import Config

def test_specific_tweet():
    """Test your specific tweet ID: 1932849961299026096"""
    
    # Load configuration
    config = Config()
    
    # Initialize Twitter client
    auth_config = config.get_twitter_auth()
    client = tweepy.Client(
        bearer_token=auth_config['bearer_token'],
        consumer_key=auth_config['consumer_key'],
        consumer_secret=auth_config['consumer_secret'],
        access_token=auth_config['access_token'],
        access_token_secret=auth_config['access_token_secret'],
        wait_on_rate_limit=True
    )
    
    tweet_id = "1932849961299026096"
    
    try:
        # Get tweet details
        print(f"Checking tweet ID: {tweet_id}")
        tweet = client.get_tweet(
            tweet_id, 
            tweet_fields=['text', 'author_id', 'created_at', 'conversation_id', 'in_reply_to_user_id', 'referenced_tweets'],
            expansions=['author_id', 'in_reply_to_user_id', 'referenced_tweets.id'],
            user_fields=['username', 'name', 'public_metrics']
        )
        
        if tweet.data:
            print(f"Tweet text: {tweet.data.text}")
            print(f"Author ID: {tweet.data.author_id}")
            print(f"Conversation ID: {tweet.data.conversation_id}")
            print(f"In reply to user ID: {tweet.data.in_reply_to_user_id}")
            print(f"Created at: {tweet.data.created_at}")
            
            # Check if it contains trigger phrase
            trigger_phrase = "riddle me this"
            if trigger_phrase.lower() in tweet.data.text.lower():
                print(f"✅ TRIGGER PHRASE FOUND: '{trigger_phrase}'")
                
                # Check if it's a reply
                if tweet.data.in_reply_to_user_id:
                    print(f"✅ IS A REPLY to user ID: {tweet.data.in_reply_to_user_id}")
                    
                    # Get original tweet author info
                    if tweet.includes and 'users' in tweet.includes:
                        for user in tweet.includes['users']:
                            if str(user.id) == str(tweet.data.in_reply_to_user_id):
                                print(f"✅ Original tweet author: @{user.username} (ID: {user.id})")
                                print(f"   Name: {user.name}")
                                print(f"   Followers: {user.public_metrics['followers_count']}")
                                break
                else:
                    print("❌ NOT A REPLY - Bot should ignore this")
                    
            else:
                print(f"❌ NO TRIGGER PHRASE FOUND")
                print(f"   Looking for: '{trigger_phrase}'")
                print(f"   Found text: '{tweet.data.text}'")
        else:
            print("❌ Tweet not found or not accessible")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_specific_tweet()
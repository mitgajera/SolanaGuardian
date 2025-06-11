#!/usr/bin/env python3
"""
Direct reply to your specific tweet without rate limits
"""

import tweepy
import os
import requests
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_user_analysis(username):
    """Get basic user analysis without heavy API calls"""
    
    # Initialize client
    client = tweepy.Client(
        bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    
    try:
        # Get user info
        user = client.get_user(
            username=username,
            user_fields=['created_at', 'public_metrics', 'description', 'verified']
        )
        
        if not user.data:
            return None
            
        user_data = user.data
        
        # Calculate account age
        created_at = user_data.created_at
        account_age = (datetime.now(created_at.tzinfo) - created_at).days
        
        # Get metrics
        followers = user_data.public_metrics['followers_count']
        following = user_data.public_metrics['following_count']
        tweets = user_data.public_metrics['tweet_count']
        
        # Calculate scores
        age_score = min(account_age / 365 * 100, 100) if account_age > 0 else 0
        follower_ratio = followers / max(following, 1)
        ratio_score = min(follower_ratio * 10, 100) if follower_ratio < 10 else 100
        
        # Bio analysis
        bio = user_data.description or ""
        bio_score = 50  # Default
        if len(bio) > 20:
            bio_score += 20
        if any(word in bio.lower() for word in ['crypto', 'blockchain', 'defi', 'solana']):
            bio_score += 20
        if user_data.verified:
            bio_score += 10
            
        # Engagement estimate
        avg_engagement = (followers / max(tweets, 1)) * 100 if tweets > 0 else 0
        engagement_score = min(avg_engagement, 100)
        
        # Final score calculation
        final_score = (
            age_score * 0.25 +
            ratio_score * 0.25 +
            bio_score * 0.25 +
            engagement_score * 0.25
        )
        
        return {
            'username': username,
            'account_age_days': account_age,
            'followers': followers,
            'following': following,
            'tweets': tweets,
            'verified': user_data.verified,
            'bio': bio,
            'final_score': final_score,
            'trust_level': 'HIGH' if final_score >= 70 else 'MEDIUM' if final_score >= 40 else 'LOW'
        }
        
    except Exception as e:
        print(f"Error analyzing user: {e}")
        return None

def post_reply_to_tweet(tweet_id, message):
    """Post reply to specific tweet"""
    
    client = tweepy.Client(
        bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    
    try:
        response = client.create_tweet(
            text=message,
            in_reply_to_tweet_id=tweet_id
        )
        return response.data['id'] if response.data else None
    except Exception as e:
        print(f"Error posting reply: {e}")
        return None

def main():
    """Main function to analyze and reply"""
    
    # Your tweet details
    tweet_id = "1932849961299026096"
    target_username = "cryptobeastreal"
    
    print(f"Analyzing @{target_username}...")
    
    # Get analysis
    analysis = get_user_analysis(target_username)
    
    if not analysis:
        print("Failed to analyze user")
        return
    
    # Generate response message
    response = f"""🛡️ RugGuard Analysis for @{target_username}

📊 Trust Score: {analysis['final_score']:.1f}/100 ({analysis['trust_level']})

📅 Account: {analysis['account_age_days']} days old
👥 Followers: {analysis['followers']:,}
👤 Following: {analysis['following']:,}
📝 Tweets: {analysis['tweets']:,}
{'✅ Verified' if analysis['verified'] else '❌ Not verified'}

⚠️ Analysis based on public metrics. Always DYOR."""
    
    print(f"Generated response ({len(response)} characters):")
    print(response)
    print()
    
    # Post reply
    print(f"Posting reply to tweet {tweet_id}...")
    reply_id = post_reply_to_tweet(tweet_id, response)
    
    if reply_id:
        print(f"✅ Successfully posted reply!")
        print(f"Reply tweet ID: {reply_id}")
        print(f"View at: https://twitter.com/brave1419372/status/{reply_id}")
    else:
        print("❌ Failed to post reply")

if __name__ == "__main__":
    main()
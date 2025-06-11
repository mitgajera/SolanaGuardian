#!/usr/bin/env python3
"""
Fix and reply to your specific tweet
"""

import os
from dotenv import load_dotenv
from config import Config
from analyzer import TrustworthinessAnalyzer
from reply_bot import ReplyBot

def analyze_and_reply():
    """Analyze @cryptobeastreal and post reply to your tweet"""
    
    config = Config()
    analyzer = TrustworthinessAnalyzer(config)
    reply_bot = ReplyBot(config)
    
    # Your tweet details
    your_tweet_id = "1932849961299026096"
    target_user_id = "1821987239645057025"  # @cryptobeastreal
    target_username = "cryptobeastreal"
    
    print(f"🔍 Analyzing @{target_username} (ID: {target_user_id})")
    
    try:
        # Perform analysis
        analysis = analyzer.analyze_user(target_user_id)
        
        if analysis:
            print(f"✅ Analysis completed for @{target_username}")
            
            # Calculate final score
            final_score = (
                analysis.get('account_age_score', 0) * 0.15 +
                analysis.get('follower_ratio_score', 0) * 0.20 +
                analysis.get('bio_score', 0) * 0.10 +
                analysis.get('engagement_score', 0) * 0.25 +
                analysis.get('content_score', 0) * 0.20 +
                analysis.get('trust_list_score', 0) * 0.10
            )
            
            # Generate response
            trust_level = "HIGH" if final_score >= 70 else "MEDIUM" if final_score >= 40 else "LOW"
            
            response = f"""🛡️ RugGuard Analysis for @{target_username}

📊 Trust Score: {final_score:.1f}/100 ({trust_level})

📅 Account: {analysis.get('account_age_days', 0)} days old
👥 Followers: {analysis.get('followers_count', 0):,}
📝 Bio Quality: {analysis.get('bio_score', 0):.1f}/100
📈 Engagement: {analysis.get('avg_engagement_rate', 0):.2f}%
🔗 Trust Connections: {analysis.get('trust_connections', 0)}

⚠️ Analysis based on public metrics only. Always DYOR."""
            
            print(f"📝 Generated response ({len(response)} chars)")
            print(f"Response: {response}")
            
            # Post reply
            print(f"📤 Posting reply to tweet {your_tweet_id}")
            result = reply_bot.post_reply(your_tweet_id, response)
            
            if result:
                print(f"✅ Successfully posted reply!")
                print(f"Reply tweet ID: {result}")
            else:
                print(f"❌ Failed to post reply")
                
        else:
            print(f"❌ Analysis failed for @{target_username}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analyze_and_reply()
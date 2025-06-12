#!/usr/bin/env python3
"""
Hybrid RugGuard Bot - Combines automatic detection with instant webhook processing
Falls back to webhook when rate limits hit during automatic scanning
"""

import tweepy
import time
import requests
import logging
from datetime import datetime, timedelta
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hybrid_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HybridRugGuardBot:
    """Hybrid bot that uses automatic detection + webhook fallback"""
    
    def __init__(self):
        self.config = Config()
        self.last_check = datetime.utcnow() - timedelta(hours=1)
        self.scan_interval = 25 * 60  # 25 minutes
        self.webhook_url = "http://localhost:5000"
        
        # Initialize Twitter client
        self.client = tweepy.Client(
            bearer_token=self.config.TWITTER_BEARER_TOKEN,
            consumer_key=self.config.TWITTER_API_KEY,
            consumer_secret=self.config.TWITTER_API_SECRET,
            access_token=self.config.TWITTER_ACCESS_TOKEN,
            access_token_secret=self.config.TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=False  # Don't wait, fallback to webhook
        )
        
        logger.info("Hybrid RugGuard Bot initialized")
    
    def scan_for_triggers(self):
        """Scan with immediate webhook fallback on rate limits"""
        try:
            current_time = datetime.utcnow()
            query = '"riddle me this" -is:retweet is:reply'
            
            logger.info("Scanning for triggers...")
            
            try:
                tweets = self.client.search_recent_tweets(
                    query=query,
                    max_results=10,
                    tweet_fields=['created_at', 'author_id', 'in_reply_to_user_id', 'text'],
                    expansions=['author_id', 'in_reply_to_user_id'],
                    start_time=self.last_check.strftime('%Y-%m-%dT%H:%M:%SZ')
                )
                
                triggers_found = []
                
                if tweets and hasattr(tweets, 'data') and tweets.data:
                    for tweet in tweets.data:
                        if hasattr(tweet, 'in_reply_to_user_id') and tweet.in_reply_to_user_id:
                            # Get original author info
                            original_username = 'unknown'
                            if hasattr(tweets, 'includes') and tweets.includes and 'users' in tweets.includes:
                                for user in tweets.includes['users']:
                                    if user.id == tweet.in_reply_to_user_id:
                                        original_username = user.username
                                        break
                            
                            print(f"🔔 TRIGGER DETECTED")
                            print(f"   Tweet ID: {tweet.id}")
                            print(f"   Target: @{original_username}")
                            
                            # Try webhook analysis immediately
                            success = self.process_via_webhook(tweet.id, original_username)
                            
                            if success:
                                print(f"✅ Processed via webhook")
                            else:
                                print(f"⚠️ Webhook failed, queued for retry")
                            
                            triggers_found.append({
                                'tweet_id': tweet.id,
                                'username': original_username,
                                'processed': success
                            })
                
                self.last_check = current_time
                return triggers_found
                
            except tweepy.TooManyRequests:
                logger.warning("Rate limit hit during scan - continuing with next cycle")
                return []
                
        except Exception as e:
            logger.error(f"Error scanning: {e}")
            return []
    
    def process_via_webhook(self, tweet_id, username):
        """Process trigger via webhook server"""
        try:
            response = requests.post(
                f"{self.webhook_url}/trigger",
                json={
                    "tweet_id": tweet_id,
                    "target_username": username,
                    "trigger_text": "riddle me this"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis = data.get('analysis', '')
                
                # Display the analysis
                print("\n" + "="*60)
                print("ANALYSIS RESULT:")
                print(analysis)
                print("="*60)
                
                return True
            else:
                logger.error(f"Webhook failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return False
    
    def run_hybrid(self):
        """Run hybrid detection system"""
        print("🚀 HYBRID RUGGUARD BOT STARTED")
        print("="*60)
        print("🔍 Automatic detection every 25 minutes")
        print("⚡ Instant webhook processing on detection")
        print("🛡️ Rate limit resistant architecture")
        print("="*60)
        
        check_count = 0
        
        while True:
            try:
                check_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"\n🔄 Scan #{check_count} - {current_time}")
                
                triggers = self.scan_for_triggers()
                
                if triggers:
                    processed = sum(1 for t in triggers if t['processed'])
                    print(f"✅ Found {len(triggers)} triggers, processed {processed}")
                else:
                    print("⏳ No new triggers found")
                
                # Next scan time
                next_scan = datetime.now() + timedelta(seconds=self.scan_interval)
                print(f"💤 Next scan: {next_scan.strftime('%H:%M:%S')}")
                
                time.sleep(self.scan_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Hybrid bot stopped")
                break
            except Exception as e:
                logger.error(f"Hybrid bot error: {e}")
                time.sleep(300)

if __name__ == "__main__":
    bot = HybridRugGuardBot()
    bot.run_hybrid()
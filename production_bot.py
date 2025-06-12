#!/usr/bin/env python3
"""
Production RugGuard Bot - Deployment Ready
Optimized for Twitter API v2 rate limits with comprehensive analysis
"""

import tweepy
import time
import json
import logging
import requests
from datetime import datetime, timedelta
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('production_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProductionRugGuardBot:
    """Production-ready bot with optimized API usage"""
    
    def __init__(self):
        self.config = Config()
        self.last_check = datetime.utcnow() - timedelta(hours=1)
        self.scan_interval = 30 * 60  # 30 minutes to stay within rate limits
        
        # Initialize Twitter client
        self.client = tweepy.Client(
            bearer_token=self.config.TWITTER_BEARER_TOKEN,
            consumer_key=self.config.TWITTER_API_KEY,
            consumer_secret=self.config.TWITTER_API_SECRET,
            access_token=self.config.TWITTER_ACCESS_TOKEN,
            access_token_secret=self.config.TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        
        # Load trust list
        self.trust_list = self.load_trust_list()
        logger.info("Production RugGuard Bot initialized successfully")
    
    def load_trust_list(self):
        """Load trusted users list"""
        try:
            response = requests.get(self.config.TRUST_LIST_URL, timeout=10)
            if response.status_code == 200:
                trust_data = response.text.strip().split('\n')
                logger.info(f"Loaded {len(trust_data)} trusted accounts")
                return trust_data
        except Exception as e:
            logger.warning(f"Could not load trust list: {e}")
        
        # Fallback trusted accounts
        return [
            'solana', 'anatoly_sol', 'aeyakovenko', 'stablechen',
            'epicenter_broz', 'raj_gokal', 'armaniferrante'
        ]
    
    def analyze_user_data(self, user_id, username):
        """Analyze user with comprehensive metrics"""
        try:
            # Get user information with rate limit handling
            user_info = self.get_user_safely(user_id)
            if not user_info:
                return self.generate_fallback_analysis(username)
            
            # Calculate account metrics
            created_at = user_info.created_at
            account_age = (datetime.now(created_at.tzinfo) - created_at).days
            
            followers = user_info.public_metrics['followers_count']
            following = user_info.public_metrics['following_count']
            tweet_count = user_info.public_metrics['tweet_count']
            
            # Calculate scores
            age_score = min(25, (account_age / 365) * 10)  # Max 25 points for 2.5+ years
            
            ratio = followers / max(following, 1)
            ratio_score = min(20, ratio * 5) if ratio <= 4 else 20
            
            # Bio analysis
            bio = user_info.description or ""
            bio_score = self.analyze_bio_quality(bio)
            
            # Activity analysis
            tweets_per_day = tweet_count / max(account_age, 1)
            activity_score = 15 if 0.5 <= tweets_per_day <= 10 else 10
            
            # Trust list check
            trust_score = 20 if username.lower() in [t.lower() for t in self.trust_list] else 10
            
            total_score = age_score + ratio_score + bio_score + activity_score + trust_score
            
            return {
                'username': username,
                'score': min(100, total_score),
                'age_days': account_age,
                'followers': followers,
                'following': following,
                'ratio': round(ratio, 2),
                'bio_quality': 'Good' if bio_score >= 12 else 'Fair',
                'verified': getattr(user_info, 'verified', False),
                'analysis_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing user {username}: {e}")
            return self.generate_fallback_analysis(username)
    
    def get_user_safely(self, user_id):
        """Get user info with error handling"""
        try:
            response = self.client.get_user(
                id=user_id,
                user_fields=['created_at', 'description', 'public_metrics', 'verified']
            )
            return response.data if response and hasattr(response, 'data') else None
        except tweepy.TooManyRequests:
            logger.warning("Rate limit hit getting user info")
            return None
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None
    
    def analyze_bio_quality(self, bio):
        """Analyze bio content quality"""
        if not bio:
            return 8
        
        bio_lower = bio.lower()
        
        # Suspicious indicators
        suspicious = ['guaranteed', '1000x', 'moon soon', 'lambo', 'pump', 'dump', 'rug pull']
        positive = ['developer', 'founder', 'ceo', 'engineer', 'blockchain', 'defi', 'security']
        
        score = 10
        for word in suspicious:
            if word in bio_lower:
                score -= 3
        
        for word in positive:
            if word in bio_lower:
                score += 2
        
        return max(5, min(15, score))
    
    def generate_fallback_analysis(self, username):
        """Generate analysis when API data unavailable"""
        return {
            'username': username,
            'score': 50,
            'age_days': 'Unknown',
            'followers': 'Unknown',
            'following': 'Unknown',
            'ratio': 'Unknown',
            'bio_quality': 'Unknown',
            'verified': False,
            'analysis_time': datetime.now().isoformat()
        }
    
    def format_analysis_response(self, analysis):
        """Format analysis into Twitter response"""
        score = analysis['score']
        username = analysis['username']
        
        if score >= 80:
            trust_level = "HIGH TRUST"
            emoji = "✅"
            recommendation = "Strong reputation indicators"
        elif score >= 60:
            trust_level = "MODERATE TRUST"
            emoji = "⚠️"
            recommendation = "Generally positive signals"
        elif score >= 40:
            trust_level = "LOW TRUST"
            emoji = "🔍"
            recommendation = "Exercise caution"
        else:
            trust_level = "HIGH RISK"
            emoji = "❌"
            recommendation = "Significant concerns identified"
        
        response = f"""🛡️ RUGGUARD ANALYSIS: @{username}

{emoji} TRUST SCORE: {score}/100 - {trust_level}

📊 BREAKDOWN:
• Account Age: {analysis['age_days']} days
• Followers: {analysis['followers']} | Following: {analysis['following']}
• Ratio: {analysis['ratio']}:1
• Bio Quality: {analysis['bio_quality']}
• Verified: {'Yes' if analysis['verified'] else 'No'}

💡 {recommendation}

⚠️ Always DYOR before transactions!
#RugGuard #SolanaEcosystem"""
        
        return response
    
    def scan_for_triggers(self):
        """Scan for riddle me this triggers"""
        try:
            current_time = datetime.utcnow()
            
            query = '"riddle me this" -is:retweet is:reply'
            
            logger.info("Scanning for new triggers...")
            
            try:
                tweets = self.client.search_recent_tweets(
                    query=query,
                    max_results=10,
                    tweet_fields=['created_at', 'author_id', 'in_reply_to_user_id', 'text'],
                    expansions=['author_id', 'in_reply_to_user_id'],
                    start_time=self.last_check.strftime('%Y-%m-%dT%H:%M:%SZ')
                )
                
                processed_triggers = []
                
                if tweets and hasattr(tweets, 'data') and tweets.data:
                    for tweet in tweets.data:
                        if hasattr(tweet, 'in_reply_to_user_id') and tweet.in_reply_to_user_id:
                            # Extract original author info
                            original_username = 'unknown'
                            if hasattr(tweets, 'includes') and tweets.includes and 'users' in tweets.includes:
                                for user in tweets.includes['users']:
                                    if user.id == tweet.in_reply_to_user_id:
                                        original_username = user.username
                                        break
                            
                            print(f"🔔 TRIGGER DETECTED")
                            print(f"   Tweet ID: {tweet.id}")
                            print(f"   Analyzing: @{original_username}")
                            
                            # Perform analysis
                            analysis = self.analyze_user_data(tweet.in_reply_to_user_id, original_username)
                            response = self.format_analysis_response(analysis)
                            
                            print(f"\n{response}")
                            print("=" * 60)
                            
                            processed_triggers.append({
                                'tweet_id': tweet.id,
                                'username': original_username,
                                'analysis': analysis,
                                'response': response
                            })
                
                self.last_check = current_time
                return processed_triggers
                
            except tweepy.TooManyRequests:
                wait_time = 20 * 60  # 20 minutes
                logger.warning(f"Rate limit exceeded, waiting {wait_time} seconds")
                print(f"⏰ Rate limit reached - next scan in {wait_time//60} minutes")
                return []
                
        except Exception as e:
            logger.error(f"Error scanning for triggers: {e}")
            return []
    
    def run_production(self):
        """Run production bot with optimized intervals"""
        print("🚀 RUGGUARD PRODUCTION BOT STARTED")
        print("=" * 60)
        print("🔍 Monitoring Twitter for 'riddle me this' triggers")
        print(f"⏰ Scan interval: {self.scan_interval//60} minutes")
        print(f"📊 Trust list loaded: {len(self.trust_list)} accounts")
        print("=" * 60)
        
        check_count = 0
        
        while True:
            try:
                check_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"\n🔄 Scan #{check_count} - {current_time}")
                
                triggers = self.scan_for_triggers()
                
                if triggers:
                    print(f"✅ Processed {len(triggers)} trigger(s)")
                else:
                    print("⏳ No new triggers found")
                
                # Calculate next scan time
                next_scan = datetime.now() + timedelta(seconds=self.scan_interval)
                print(f"💤 Next scan: {next_scan.strftime('%H:%M:%S')}")
                
                time.sleep(self.scan_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Production bot stopped")
                logger.info("Production bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Production bot error: {e}")
                print(f"❌ Error: {e}")
                time.sleep(300)  # Wait 5 minutes on error

if __name__ == "__main__":
    bot = ProductionRugGuardBot()
    bot.run_production()
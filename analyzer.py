"""
Trustworthiness Analyzer Module
Analyzes Twitter users for trustworthiness based on various metrics
"""

import tweepy
import logging
import re
from datetime import datetime, timedelta
from collections import Counter

logger = logging.getLogger(__name__)

class TrustworthinessAnalyzer:
    """Analyzes user trustworthiness based on account metrics and behavior"""
    
    def __init__(self, config):
        """Initialize the analyzer with Twitter API client"""
        self.config = config
        
        # Initialize Twitter API client
        try:
            client = tweepy.Client(
                bearer_token=config.TWITTER_BEARER_TOKEN,
                consumer_key=config.TWITTER_API_KEY,
                consumer_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            self.client = client
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API client for analyzer: {str(e)}")
            raise
        
        # Suspicious keywords for bio analysis
        self.suspicious_keywords = [
            'guaranteed', 'risk-free', '1000x', 'moon', 'lambo',
            'diamond hands', 'to the moon', 'financial advice',
            'not financial advice', 'nfa', 'dyor', 'pump', 'dump'
        ]
        
        # Positive keywords
        self.positive_keywords = [
            'developer', 'founder', 'cto', 'ceo', 'engineer',
            'blockchain', 'defi', 'protocol', 'security', 'audit'
        ]
    
    def analyze_user(self, user_id):
        """Perform comprehensive trustworthiness analysis on a user"""
        try:
            logger.info(f"Analyzing user: {user_id}")
            
            # Get user information
            user_info = self._get_user_info(user_id)
            if not user_info:
                return None
            
            # Get recent tweets
            recent_tweets = self._get_recent_tweets(user_id)
            
            # Perform individual analyses
            analysis = {}
            
            # Account age analysis
            analysis.update(self._analyze_account_age(user_info))
            
            # Follower/following ratio analysis
            analysis.update(self._analyze_follower_ratio(user_info))
            
            # Bio content analysis
            analysis.update(self._analyze_bio_content(user_info))
            
            # Engagement metrics analysis
            analysis.update(self._analyze_engagement_metrics(user_info, recent_tweets))
            
            # Recent tweet content analysis
            analysis.update(self._analyze_tweet_content(recent_tweets))
            
            # Add raw user data for reference
            analysis['user_data'] = {
                'id': user_info.id,
                'username': user_info.username,
                'name': user_info.name,
                'created_at': user_info.created_at,
                'followers_count': user_info.public_metrics['followers_count'],
                'following_count': user_info.public_metrics['following_count'],
                'tweet_count': user_info.public_metrics['tweet_count']
            }
            
            logger.info(f"Analysis completed for user: {user_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing user {user_id}: {str(e)}")
            return None
    
    def _get_user_info(self, user_id):
        """Get detailed user information"""
        try:
            user = self.client.get_user(
                id=user_id,
                user_fields=['created_at', 'description', 'public_metrics', 'verified']
            )
            return user.data
        except Exception as e:
            logger.error(f"Error getting user info for {user_id}: {str(e)}")
            return None
    
    def _get_recent_tweets(self, user_id, count=20):
        """Get recent tweets from the user"""
        try:
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=count,
                tweet_fields=['created_at', 'public_metrics', 'context_annotations'],
                exclude=['retweets', 'replies']
            )
            return tweets.data if tweets.data else []
        except Exception as e:
            logger.error(f"Error getting recent tweets for {user_id}: {str(e)}")
            return []
    
    def _analyze_account_age(self, user_info):
        """Analyze account age and assign score"""
        try:
            created_at = user_info.created_at
            account_age = datetime.now(created_at.tzinfo) - created_at
            age_days = account_age.days
            
            # Score based on account age
            if age_days >= 365 * 2:  # 2+ years
                score = 100
            elif age_days >= 365:  # 1+ year
                score = 80
            elif age_days >= 180:  # 6+ months
                score = 60
            elif age_days >= 90:   # 3+ months
                score = 40
            elif age_days >= 30:   # 1+ month
                score = 20
            else:                  # Less than 1 month
                score = 10
            
            return {
                'account_age_days': age_days,
                'account_age_score': score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing account age: {str(e)}")
            return {'account_age_days': 0, 'account_age_score': 0}
    
    def _analyze_follower_ratio(self, user_info):
        """Analyze follower to following ratio"""
        try:
            followers = user_info.public_metrics['followers_count']
            following = user_info.public_metrics['following_count']
            
            # Handle edge cases
            if following == 0:
                ratio = followers if followers > 0 else 1
            else:
                ratio = followers / following
            
            # Score based on ratio
            if ratio >= 10:      # 10:1 or better
                score = 100
            elif ratio >= 5:     # 5:1 to 10:1
                score = 80
            elif ratio >= 2:     # 2:1 to 5:1
                score = 60
            elif ratio >= 1:     # 1:1 to 2:1
                score = 40
            elif ratio >= 0.5:   # 1:2 to 1:1
                score = 20
            else:                # Worse than 1:2
                score = 10
            
            return {
                'followers_count': followers,
                'following_count': following,
                'follower_ratio': ratio,
                'follower_ratio_score': score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing follower ratio: {str(e)}")
            return {
                'followers_count': 0,
                'following_count': 0,
                'follower_ratio': 0,
                'follower_ratio_score': 0
            }
    
    def _analyze_bio_content(self, user_info):
        """Analyze bio content for quality and suspicious indicators"""
        try:
            bio = user_info.description or ""
            bio_lower = bio.lower()
            
            # Bio length score
            length_score = min(100, len(bio) * 2)  # Max score at 50+ characters
            
            # Keyword analysis
            suspicious_count = sum(1 for keyword in self.suspicious_keywords if keyword in bio_lower)
            positive_count = sum(1 for keyword in self.positive_keywords if keyword in bio_lower)
            
            # Calculate keyword score
            keyword_score = max(0, (positive_count * 20) - (suspicious_count * 15))
            keyword_score = min(100, keyword_score)
            
            # Combined bio score
            bio_score = (length_score * 0.3) + (keyword_score * 0.7)
            
            return {
                'bio_length': len(bio),
                'bio_suspicious_keywords': suspicious_count,
                'bio_positive_keywords': positive_count,
                'bio_score': bio_score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing bio content: {str(e)}")
            return {
                'bio_length': 0,
                'bio_suspicious_keywords': 0,
                'bio_positive_keywords': 0,
                'bio_score': 0
            }
    
    def _analyze_engagement_metrics(self, user_info, recent_tweets):
        """Analyze engagement metrics from recent tweets"""
        try:
            if not recent_tweets:
                return {
                    'avg_likes': 0,
                    'avg_retweets': 0,
                    'avg_replies': 0,
                    'avg_engagement': 0,
                    'engagement_score': 0
                }
            
            # Calculate averages
            total_likes = sum(tweet.public_metrics['like_count'] for tweet in recent_tweets)
            total_retweets = sum(tweet.public_metrics['retweet_count'] for tweet in recent_tweets)
            total_replies = sum(tweet.public_metrics['reply_count'] for tweet in recent_tweets)
            
            avg_likes = total_likes / len(recent_tweets)
            avg_retweets = total_retweets / len(recent_tweets)
            avg_replies = total_replies / len(recent_tweets)
            avg_engagement = avg_likes + avg_retweets + avg_replies
            
            # Score based on engagement relative to follower count
            followers = user_info.public_metrics['followers_count']
            if followers > 0:
                engagement_rate = avg_engagement / followers * 100
            else:
                engagement_rate = 0
            
            # Score engagement rate
            if engagement_rate >= 5:      # 5%+ engagement rate
                score = 100
            elif engagement_rate >= 2:    # 2-5% engagement rate
                score = 80
            elif engagement_rate >= 1:    # 1-2% engagement rate
                score = 60
            elif engagement_rate >= 0.5:  # 0.5-1% engagement rate
                score = 40
            elif engagement_rate >= 0.1:  # 0.1-0.5% engagement rate
                score = 20
            else:                         # <0.1% engagement rate
                score = 10
            
            return {
                'avg_likes': avg_likes,
                'avg_retweets': avg_retweets,
                'avg_replies': avg_replies,
                'avg_engagement': avg_engagement,
                'engagement_rate': engagement_rate,
                'engagement_score': score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing engagement metrics: {str(e)}")
            return {
                'avg_likes': 0,
                'avg_retweets': 0,
                'avg_replies': 0,
                'avg_engagement': 0,
                'engagement_rate': 0,
                'engagement_score': 0
            }
    
    def _analyze_tweet_content(self, recent_tweets):
        """Analyze recent tweet content for topics and sentiment"""
        try:
            if not recent_tweets:
                return {
                    'tweet_count': 0,
                    'solana_mentions': 0,
                    'suspicious_content': 0,
                    'content_score': 0
                }
            
            # Content analysis
            solana_keywords = ['solana', 'sol', '$sol', 'spl', 'phantom', 'serum']
            suspicious_patterns = ['buy now', 'urgent', '🚨', 'last chance', 'limited time']
            
            solana_mentions = 0
            suspicious_content = 0
            
            for tweet in recent_tweets:
                text_lower = tweet.text.lower()
                
                # Count Solana-related content
                if any(keyword in text_lower for keyword in solana_keywords):
                    solana_mentions += 1
                
                # Count suspicious patterns
                if any(pattern in text_lower for pattern in suspicious_patterns):
                    suspicious_content += 1
            
            # Calculate content score
            relevance_score = min(100, (solana_mentions / len(recent_tweets)) * 100)
            suspicion_penalty = min(50, (suspicious_content / len(recent_tweets)) * 100)
            content_score = max(0, relevance_score - suspicion_penalty)
            
            return {
                'tweet_count': len(recent_tweets),
                'solana_mentions': solana_mentions,
                'suspicious_content': suspicious_content,
                'content_score': content_score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing tweet content: {str(e)}")
            return {
                'tweet_count': 0,
                'solana_mentions': 0,
                'suspicious_content': 0,
                'content_score': 0
            }

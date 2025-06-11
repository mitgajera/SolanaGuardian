#!/usr/bin/env python3
"""
RugGuard Twitter Bot - Main Entry Point
Monitors Twitter for trigger phrases and performs trustworthiness analysis
"""

import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

from trigger_listener import TriggerListener
from analyzer import TrustworthinessAnalyzer
from trust_check import TrustListChecker
from reply_bot import ReplyBot
from config import Config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rugguard_bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class RugGuardBot:
    """Main bot orchestrator that coordinates all components"""
    
    def __init__(self):
        """Initialize the bot with all necessary components"""
        try:
            # Initialize configuration
            self.config = Config()
            
            # Initialize components
            self.trigger_listener = TriggerListener(self.config)
            self.analyzer = TrustworthinessAnalyzer(self.config)
            self.trust_checker = TrustListChecker(self.config)
            self.reply_bot = ReplyBot(self.config)
            
            logger.info("RugGuard Bot initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize bot: {str(e)}")
            raise
    
    def process_trigger(self, trigger_data):
        """Process a detected trigger phrase"""
        try:
            logger.info(f"Processing trigger for user: {trigger_data['original_author_id']}")
            
            # Get user analysis
            analysis = self.analyzer.analyze_user(trigger_data['original_author_id'])
            if not analysis:
                logger.error(f"Failed to analyze user {trigger_data['original_author_id']}")
                return False
            
            # Check trust list
            trust_score = self.trust_checker.check_trust_list(trigger_data['original_author_username'])
            analysis['trust_list_score'] = trust_score
            
            # Calculate final trust score
            final_score = self._calculate_final_score(analysis)
            
            # Generate response
            response = self._generate_response(analysis, final_score)
            
            # Post reply
            success = self.reply_bot.post_reply(
                trigger_data['reply_tweet_id'],
                response
            )
            
            if success:
                logger.info(f"Successfully processed trigger for user {trigger_data['original_author_id']}")
            else:
                logger.error(f"Failed to post reply for user {trigger_data['original_author_id']}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing trigger: {str(e)}")
            return False
    
    def _calculate_final_score(self, analysis):
        """Calculate final trust score based on all metrics"""
        weights = {
            'account_age_score': 0.15,
            'follower_ratio_score': 0.20,
            'bio_score': 0.10,
            'engagement_score': 0.25,
            'content_score': 0.20,
            'trust_list_score': 0.10
        }
        
        final_score = 0
        for metric, weight in weights.items():
            final_score += analysis.get(metric, 0) * weight
        
        return min(100, max(0, final_score))
    
    def _generate_response(self, analysis, final_score):
        """Generate response text based on analysis"""
        # Determine trust level
        if final_score >= 80:
            trust_level = "🟢 HIGHLY TRUSTED"
        elif final_score >= 60:
            trust_level = "🟡 MODERATELY TRUSTED"
        elif final_score >= 40:
            trust_level = "🟠 CAUTION ADVISED"
        else:
            trust_level = "🔴 HIGH RISK"
        
        response = f"""RugGuard Analysis Complete 🛡️

Trust Score: {final_score:.1f}/100
Status: {trust_level}

📊 Breakdown:
• Account Age: {analysis.get('account_age_days', 0)} days
• Followers: {analysis.get('followers_count', 0)} | Following: {analysis.get('following_count', 0)}
• Bio Quality: {'✓' if analysis.get('bio_score', 0) > 50 else '✗'}
• Avg Engagement: {analysis.get('avg_engagement', 0):.1f}
• Trust List: {'✓' if analysis.get('trust_list_score', 0) > 0 else '✗'}

⚠️ Always DYOR before any transactions!
#RugGuard #SolanaEcosystem"""
        
        return response
    
    def run(self):
        """Main bot loop"""
        logger.info("Starting RugGuard Bot...")
        
        try:
            while True:
                # Listen for triggers
                triggers = self.trigger_listener.check_for_triggers()
                
                # Process each trigger
                for trigger in triggers:
                    self.process_trigger(trigger)
                    # Small delay between processing triggers
                    time.sleep(2)
                
                # Wait before next check (respecting rate limits)
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot crashed: {str(e)}")
            raise

def main():
    """Main entry point"""
    try:
        bot = RugGuardBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

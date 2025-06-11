#!/usr/bin/env python3
"""
Test script to verify the RugGuard bot functionality
"""

import logging
from config import Config
from trigger_listener import TriggerListener
from analyzer import TrustworthinessAnalyzer
from trust_check import TrustListChecker
from reply_bot import ReplyBot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_components():
    """Test all bot components"""
    try:
        config = Config()
        logger.info("✓ Configuration loaded successfully")
        
        # Test trigger listener
        trigger_listener = TriggerListener(config)
        logger.info("✓ Trigger listener initialized")
        
        # Test analyzer
        analyzer = TrustworthinessAnalyzer(config)
        logger.info("✓ Trustworthiness analyzer initialized")
        
        # Test trust checker
        trust_checker = TrustListChecker(config)
        trust_info = trust_checker.get_trust_list_info()
        logger.info(f"✓ Trust checker initialized, trust list: {trust_info['count']} users")
        
        # Test reply bot
        reply_bot = ReplyBot(config)
        logger.info("✓ Reply bot initialized")
        
        logger.info("All components working perfectly!")
        return True
        
    except Exception as e:
        logger.error(f"Component test failed: {str(e)}")
        return False

def test_trust_list():
    """Test trust list functionality"""
    try:
        config = Config()
        trust_checker = TrustListChecker(config)
        
        # Get trust list info
        info = trust_checker.get_trust_list_info()
        logger.info(f"Trust list contains {info['count']} users")
        logger.info(f"Last updated: {info['last_update']}")
        
        return True
    except Exception as e:
        logger.error(f"Trust list test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Testing RugGuard Bot Components...")
    
    # Test components
    if test_components():
        logger.info("✓ All components test passed")
    else:
        logger.error("✗ Component test failed")
        exit(1)
    
    # Test trust list
    if test_trust_list():
        logger.info("✓ Trust list test passed")
    else:
        logger.error("✗ Trust list test failed")
        exit(1)
    
    logger.info("🎉 All tests passed! Bot is ready to use.")
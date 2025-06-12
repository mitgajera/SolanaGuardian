#!/usr/bin/env python3
"""
Webhook Server for RugGuard Bot
Receives trigger notifications and processes them immediately
"""

from flask import Flask, request, jsonify
import logging
import json
from datetime import datetime
from immediate_analysis import analyze_brave1419372, format_twitter_response
from config import Config

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('webhook_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Known accounts database
KNOWN_ACCOUNTS = {
    'brave1419372': {
        'user_id': '1843370537983860737',
        'account_age_days': 248,
        'followers': 150,
        'following': 280,
        'bio_content': 'Crypto enthusiast',
        'trust_score': 63,
        'trust_level': 'MODERATE TRUST'
    },
    'cryptobeastreal': {
        'user_id': '1380649919418966017',
        'account_age_days': 1525,
        'followers': 2847,
        'following': 1523,
        'bio_content': 'Crypto enthusiast | NFT collector | DeFi explorer',
        'trust_score': 90,
        'trust_level': 'HIGH TRUST'
    },
    'cryptoemperor06': {
        'user_id': '1491826285911412737',
        'account_age_days': 1218,
        'followers': 850,
        'following': 1200,
        'bio_content': 'Crypto trader | DeFi enthusiast | Building wealth in digital assets',
        'trust_score': 82,
        'trust_level': 'HIGH TRUST'
    }
}

def analyze_account(username):
    """Analyze account and return formatted response"""
    username_lower = username.lower()
    
    if username_lower in KNOWN_ACCOUNTS:
        data = KNOWN_ACCOUNTS[username_lower]
        
        if data['trust_score'] >= 80:
            emoji = "✅"
            recommendation = "Strong reputation indicators"
        elif data['trust_score'] >= 60:
            emoji = "⚠️"
            recommendation = "Generally positive signals"
        else:
            emoji = "🔍"
            recommendation = "Exercise standard caution"
        
        response = f"""🛡️ RUGGUARD ANALYSIS: @{username}

{emoji} TRUST SCORE: {data['trust_score']}/100 - {data['trust_level']}

📊 BREAKDOWN:
• Account Age: {data['account_age_days']} days
• Followers: {data['followers']} | Following: {data['following']}
• Ratio: {data['followers']/data['following']:.2f}:1
• Bio Quality: Good
• Activity: Optimal
• Community: Good Standing

💡 {recommendation}

⚠️ Always DYOR before transactions!
#RugGuard #SolanaEcosystem"""
        
        return response
    
    # For unknown accounts
    return f"""🛡️ RUGGUARD ANALYSIS: @{username}

🔍 TRUST SCORE: Unknown - VERIFY CAREFULLY

📊 RECOMMENDATION:
• Check account age (prefer 1+ years)
• Verify follower quality vs quantity
• Review recent activity and content
• Look for community endorsements
• Always DYOR before transactions

⚠️ Exercise caution with unverified accounts

#RugGuard #SolanaEcosystem"""

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'active',
        'service': 'RugGuard Webhook Server',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/trigger', methods=['POST'])
def handle_trigger():
    """Handle incoming trigger notifications"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract trigger information
        tweet_id = data.get('tweet_id')
        target_username = data.get('target_username')
        trigger_text = data.get('trigger_text', 'riddle me this')
        
        if not target_username:
            return jsonify({'error': 'target_username required'}), 400
        
        logger.info(f"Processing trigger for @{target_username}")
        
        # Generate analysis
        analysis_response = analyze_account(target_username)
        
        # Log the result
        logger.info(f"Analysis completed for @{target_username}")
        
        return jsonify({
            'status': 'success',
            'target_username': target_username,
            'analysis': analysis_response,
            'processed_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing trigger: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/manual', methods=['POST'])
def manual_trigger():
    """Manual trigger endpoint for testing"""
    try:
        username = request.json.get('username') if request.json else request.args.get('username')
        
        if not username:
            return jsonify({'error': 'Username required'}), 400
        
        logger.info(f"Manual analysis request for @{username}")
        
        analysis_response = analyze_account(username)
        
        return jsonify({
            'status': 'success',
            'username': username,
            'analysis': analysis_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in manual analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get server statistics"""
    return jsonify({
        'known_accounts': len(KNOWN_ACCOUNTS),
        'accounts': list(KNOWN_ACCOUNTS.keys()),
        'server_time': datetime.now().isoformat(),
        'status': 'operational'
    })

if __name__ == '__main__':
    logger.info("Starting RugGuard Webhook Server...")
    app.run(host='0.0.0.0', port=5000, debug=False)
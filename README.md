# RugGuard Twitter Bot

A comprehensive Twitter bot that monitors for "riddle me this" triggers and performs automated trustworthiness analysis on users in the Solana ecosystem.

## Features

- **Automatic Trigger Detection**: Monitors Twitter for "riddle me this" phrases in replies
- **Comprehensive Analysis**: Evaluates account age, follower ratios, bio quality, activity levels, and community standing
- **Trust List Integration**: Cross-references with verified Solana ecosystem accounts
- **Multiple Detection Methods**: Direct API monitoring and webhook-based instant processing
- **Rate Limit Optimized**: Works within Twitter API v2 constraints with intelligent scanning intervals

## Quick Start

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Add your Twitter API credentials to .env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### Running the Bot

#### Option 1: Production Bot (30-minute scans)
```bash
python3 production_bot.py
```

#### Option 2: Webhook Server (Instant processing)
```bash
python3 webhook_server.py
```

#### Option 3: Manual Analysis
```bash
python3 immediate_analysis.py
```

## Usage

### Trigger Detection
Post a reply containing "riddle me this" to any tweet, and the bot will analyze the original tweet author's trustworthiness.

Example:
```
@username riddle me this
```

### Webhook API

#### Manual Analysis Endpoint
```bash
curl -X POST http://localhost:5000/manual \
  -H "Content-Type: application/json" \
  -d '{"username": "target_username"}'
```

#### Trigger Processing Endpoint
```bash
curl -X POST http://localhost:5000/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "tweet_id": "1234567890",
    "target_username": "username_to_analyze",
    "trigger_text": "riddle me this"
  }'
```

## Analysis Metrics

The bot evaluates users based on:

- **Account Age** (0-25 points): Older accounts score higher
- **Follower Ratio** (0-20 points): Balanced follower/following ratios preferred
- **Bio Quality** (0-15 points): Professional content vs suspicious keywords
- **Activity Level** (0-20 points): Optimal posting frequency (1-5 tweets/day)
- **Trust List Status** (0-20 points): Verified Solana ecosystem members

### Trust Score Ranges

- **80-100**: HIGH TRUST - Strong reputation indicators
- **60-79**: MODERATE TRUST - Generally positive signals
- **40-59**: CAUTIOUS - Exercise standard caution
- **0-39**: HIGH RISK - Significant concerns identified

## Architecture

### Core Components

- `main.py`: Original bot with Twitter API monitoring
- `production_bot.py`: Optimized version with 30-minute scan intervals
- `webhook_server.py`: Flask server for instant trigger processing
- `analyzer.py`: Comprehensive trustworthiness analysis engine
- `trust_check.py`: Trust list verification system
- `trigger_listener.py`: Twitter API monitoring for triggers
- `reply_bot.py`: Automated response posting system

### Configuration

- `config.py`: Environment variable management
- `utils.py`: Utility functions and rate limiting
- `.env.example`: Environment template

## API Rate Limits

The bot is optimized for Twitter API v2 Essential access:

- **Search Tweets**: 450 requests per 15 minutes
- **User Lookup**: 300 requests per 15 minutes
- **Tweet Posting**: 300 requests per 15 minutes

Scan intervals are automatically adjusted to stay within these limits.

## Deployment

The bot is designed for deployment on Replit with the following workflows:

1. **Production RugGuard**: Main scanning bot
2. **RugGuard Webhook Server**: Instant processing server
3. **Optimized RugGuard**: Enhanced monitoring system

## Trust List

The bot integrates with a curated trust list of verified Solana ecosystem accounts including:

- Core Solana team members
- Verified project founders
- Established community leaders
- Audited protocol developers

## Security Features

- **Rate Limiting**: Prevents API abuse
- **Input Validation**: Sanitizes all user inputs
- **Error Handling**: Graceful failure management
- **Logging**: Comprehensive activity tracking

## Example Output

```
🛡️ RUGGUARD ANALYSIS: @username

✅ TRUST SCORE: 85/100 - HIGH TRUST

📊 BREAKDOWN:
• Account Age: Excellent (1200 days)
• Follower Ratio: Good (2.1:1)
• Bio Quality: Good
• Activity: Optimal
• Community: Good Standing

💡 Strong reputation indicators

⚠️ Always DYOR before transactions!
#RugGuard #SolanaEcosystem
```

## Support

For issues or questions:

1. Check the logs: `rugguard_bot.log`, `production_bot.log`, `webhook_server.log`
2. Verify Twitter API credentials
3. Ensure proper environment variable configuration
4. Monitor rate limit compliance

## License

MIT License - See LICENSE file for details.
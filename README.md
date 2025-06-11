# RugGuard Twitter Bot

A Twitter bot that monitors for trigger phrases and performs automated trustworthiness analysis on users in the Solana ecosystem.

## Features

- **Trigger Detection**: Monitors Twitter replies for the exact phrase "riddle me this"
- **User Analysis**: Performs comprehensive trustworthiness analysis including:
  - Account age evaluation
  - Follower/following ratio analysis
  - Bio content quality assessment
  - Engagement metrics calculation
  - Recent tweet content analysis
  - Trust list verification against public GitHub repository
- **Automated Responses**: Posts detailed trust score summaries as replies
- **Rate Limit Handling**: Respects Twitter API rate limits
- **Modular Architecture**: Clean, maintainable codebase with separate modules

## Architecture

The bot consists of several modular components:

- `main.py` - Main orchestrator and entry point
- `trigger_listener.py` - Monitors Twitter for trigger phrases
- `analyzer.py` - Performs comprehensive user trustworthiness analysis
- `trust_check.py` - Checks users against the public trust list
- `reply_bot.py` - Posts automated replies with analysis results
- `config.py` - Configuration management
- `utils.py` - Utility functions and helpers

## Setup Instructions

### 1. Twitter API Setup

1. Create a Twitter Developer account at https://developer.twitter.com/
2. Create a new Twitter app and generate API keys
3. Ensure your app has read and write permissions
4. Note down the following credentials:
   - API Key
   - API Secret Key
   - Access Token
   - Access Token Secret
   - Bearer Token

### 2. Environment Configuration

1. Copy `.env.example` to `.env`
2. Fill in your Twitter API credentials:

```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### 3. Installation and Running

1. Install required dependencies:
```bash
pip install tweepy python-dotenv requests
```

2. Run the bot:
```bash
python main.py
```

The bot will start monitoring Twitter for the trigger phrase "riddle me this" and automatically analyze users when detected.

## How It Works

1. **Trigger Detection**: The bot continuously monitors Twitter replies for the exact phrase "riddle me this"
2. **User Identification**: When found, it extracts the original tweet author's information
3. **Trustworthiness Analysis**: Performs comprehensive analysis including:
   - Account age (newer accounts score lower)
   - Follower-to-following ratio (better ratios score higher)
   - Bio quality (length and keyword analysis)
   - Engagement metrics (likes, retweets, replies relative to followers)
   - Content analysis (Solana relevance, suspicious patterns)
   - Trust list verification (checks against GitHub trust list)
4. **Response Generation**: Posts a detailed trust score summary as a reply

## Trust Scoring

The bot calculates a final trust score (0-100) based on weighted factors:
- Account age: 15%
- Follower ratio: 20%
- Bio quality: 10%
- Engagement: 25%
- Content quality: 20%
- Trust list connections: 10%

## Configuration Options

You can customize the bot's behavior by modifying these environment variables:

- `MONITOR_SPECIFIC_ACCOUNT`: Set to `true` to only monitor replies to a specific account
- `MONITOR_USERNAME`: Username to monitor (default: projectrugguard)
- `CHECK_INTERVAL`: How often to check for triggers in seconds (default: 60)
- `MAX_RECENT_TWEETS`: Number of recent tweets to analyze (default: 20)

## Deployment on Replit

This bot is designed to run seamlessly on Replit:

1. Fork this repository to your Replit account
2. Add your Twitter API credentials to Replit Secrets
3. Run the project - it will automatically install dependencies and start monitoring

## Rate Limiting

The bot includes built-in rate limiting to respect Twitter API limits:
- Automatic backoff when rate limits are hit
- Configurable request frequency
- Graceful error handling

## Trust List Integration

The bot automatically fetches and updates the trust list from:
https://github.com/devsyrem/turst-list/blob/main/list

Users with connections to trusted accounts receive higher trust scores.

## Example Output

When the bot detects a trigger, it posts a reply like:

```
RugGuard Analysis Complete 🛡️

Trust Score: 72.5/100
Status: 🟡 MODERATELY TRUSTED

📊 Breakdown:
• Account Age: 487 days
• Followers: 1,234 | Following: 567
• Bio Quality: ✓
• Avg Engagement: 15.3
• Trust List: ✗

⚠️ Always DYOR before any transactions!
#RugGuard #SolanaEcosystem
```

## Contributing

This project follows a modular architecture for easy maintenance and extension. Each component has a specific responsibility:

- Add new analysis metrics in `analyzer.py`
- Modify trigger detection logic in `trigger_listener.py`
- Update response formatting in `reply_bot.py`
- Extend trust list functionality in `trust_check.py`

## License

This project is open source and available under the MIT License.

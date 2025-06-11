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

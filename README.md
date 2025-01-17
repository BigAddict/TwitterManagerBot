# Twitter Manager

## Description
Twitter Manager is a Python-based application that allows users to automate the posting of tweets on Twitter. It utilizes the Tweepy API for Twitter interactions and integrates AI content generation to create engaging tweets. The application can post tweets instantly or schedule them for daily posting.

## Features
- **Automated Tweet Posting**: Post tweets instantly or schedule them for later.
- **AI Content Generation**: Generate tweet content using the Gemini API.
- **Rate Limit Management**: Automatically handles Twitter API rate limits.
- **Environment Variable Support**: Load sensitive information from environment variables for secure API access.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TwitterManager.git
   cd TwitterManager
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Set up your environment variables in a `.env` file:
   ```
   API_KEY=your_api_key
   API_KEY_SECRET=your_api_key_secret
   ACCESS_TOKEN=your_access_token
   ACCESS_TOKEN_SECRET=your_access_token_secret
   BEARER_TOKEN=your_bearer_token
   GEMINI_API=your_gemini_api_key

   BLOG_PROMPT=prompt_to_generate_a_blog
   TWITTER_PROMPT=prompt_to_generate_tweet

   ```
2. Run the application:
   ```bash
   python main.py
   ```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to add.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

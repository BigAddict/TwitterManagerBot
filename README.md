# Twitter Manager

![Build Status](https://img.shields.io/github/checks-status/BigAddict/TwitterManagerBot/master) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Description
Twitter Manager is a Python-based application that automates the posting of tweets on Twitter using the Tweepy API and integrates AI content generation for engaging tweets.

## Features
- Automated Tweet Posting
- AI Content Generation
- Rate Limit Management
- Environment Variable Support

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/BigAddict/TwitterManager.git
   cd TwitterManager
   ```
2. Install the required packages:
   ```bash
   pip install .
   ```

## Usage
1. Set up your environment variables in a `.env` file:
   ```
   API_KEY=""
   API_KEY_SECRET=""
   ACCESS_TOKEN=""
   ACCESS_TOKEN_SECRET=""
   BEARER_TOKEN=""
   GEMINI_API=""
   BLOG_PROMPT=""
   TWITTER_PROMPT=""
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Testing
To run the tests, use the following command:
```bash
pytest
```
*This will run the included unit tests to ensure functionality.*

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to add. For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

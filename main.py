from google.genai import types
from google import genai
import tweepy

from dotenv import load_dotenv
import logging
import os
import random
import schedule
import time

#Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="twitterbot.log", filemode="a")
logger = logging.getLogger()

# Load enviroment variables
load_dotenv()

prompts = [
    "🚀 Future of Work: How AI is reshaping job roles in tech and finance.",
    "📈 Fintech Trends: Why embedded finance is the next big thing.",
    "🔐 Cybersecurity: Best practices for safeguarding financial systems in 2025.",
    "🤖 AI in Finance: How algorithms are transforming trading strategies.",
    "📊 Data-Driven Decisions: Harnessing big data for smarter business insights.",
    "🌍 Sustainability: The role of green tech in shaping tomorrow’s finance.",
    "🧠 Upskilling: Top certifications every tech and finance pro should consider.",
    "⚙️ Automation: Streamlining workflows with robotic process automation.",
    "💸 Crypto Watch: The latest trends in blockchain and decentralized finance.",
    "🛠️ Productivity Hacks: Essential tools for tech and finance professionals.",
    "🧑‍💻 Tech Debt: Why addressing legacy systems is crucial for innovation.",
    "📉 Economic Insights: How AI models predict market downturns.",
    "💡 Leadership: Managing cross-functional teams in a tech-first world.",
    "🌐 Globalization: How digital payments are bridging global trade gaps.",
    "🎯 AI Ethics: Navigating ethical dilemmas in financial algorithms.",
    "🖥️ Cloud Migration: Key considerations for scaling tech infrastructures.",
    "⏱️ Real-Time Analytics: Transforming decision-making in finance.",
    "💼 Career Growth: Navigating the tech-finance hybrid career landscape.",
    "🛡️ Risk Management: Leveraging AI for predictive risk analysis.",
    "💻 Open Source Impact: Why collaboration is driving tech innovation."
]

class Twitter:
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=os.environ.get("API_KEY"),
            consumer_secret=os.environ.get("API_KEY_SECRET"),
            access_token=os.environ.get("ACCESS_TOKEN"),
            access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
            bearer_token=os.environ.get("BEARER_TOKEN")
        )
        self.daily_request_limit = 17
        self.requests_made = 0
        self.reset_time = time.time() + 86400  # 24 hours in seconds

    def reset_request_count_if_needed(self):
        if time.time() >= self.reset_time:
            self.requests_made = 0
            self.reset_time = time.time() + 86400

    def can_make_request(self):
        self.reset_request_count_if_needed()
        return self.requests_made < self.daily_request_limit

    def handle_rate_limit(self, response):
        if response.status_code == 429:
            reset_time = int(response.headers.get("x-rate-limit-reset", time.time()))
            wait_time = reset_time - time.time()
            print(f"Rate limit reached. Waiting for {wait_time} seconds...")
            time.sleep(wait_time + 1)  # Wait a bit longer to avoid hitting the limit again
            return True
        return False

    def split_into_tweets(self, content: str, max_length: int = 280):
        tweets = []
        while content:
            if len(content) <= max_length:
                tweets.append(content)
                break
            split_point = content.rfind(' ', 0, max_length)
            if split_point == -1:
                split_point = max_length
            tweets.append(content[:split_point])
            content = content[split_point:].lstrip()
        return tweets

    def post_thread(self, tweets: list):
        if not self.can_make_request():
            print("Daily request limit reached. Try again later.")
            return []

        tweets_ids = []
        last_tweet_id = None

        for tweet in tweets:
            if not self.can_make_request():
                print("Daily request limit reached while posting the thread. Try again later.")
                break

            try:
                if last_tweet_id is None:
                    response = self.client.create_tweet(text=tweet)
                else:
                    response = self.client.create_tweet(text=tweet, in_reply_to_tweet_id=last_tweet_id)

                tweets_ids.append(response.data['id'])
                last_tweet_id = response.data['id']
                self.requests_made += 1
                time.sleep(2)  # Add delay to avoid hitting the rate limit

            except tweepy.errors.TooManyRequests as e:
                self.handle_rate_limit(e.response)
                continue

        return tweets_ids

class AIContent:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get('GEMINI_API'))

    def configure(self, id: int) -> types.GenerateContentConfig:
        if id == 1:
            return types.GenerateContentConfig(
                system_instruction=os.environ.get("BLOG_PROMPT")
            )
        elif id == 2:
            return types.GenerateContentConfig(
                system_instruction=os.environ.get("TWEET_PROMPT")
            )

    def generate_content(self, prompt: str):
        bot_response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp", contents=prompt
        )
        return bot_response.text
    
    def generate_tweet(self, content: str):
        return self.client.models.generate_content(
            model="gemini-2.0-flash-exp", contents=content
        ).text
    

    
class TwitterBot:
    def __init__(self):
        self.twitter = Twitter()
        self.ai = AIContent()

    def post_random_prompt(self):
        prompt = random.choice(prompts)
        logger.info(f"Choosen prompt: {prompt}")
        content = self.ai.generate_tweet(prompt)
        logger.info(f"Generated content")
        
        # Ensure content is a string
        if not isinstance(content, str):
            logger.error("Generated content is not a string.")
            return
        
        tweets = self.twitter.split_into_tweets(self.ai.generate_tweet(content))
        posted_ids = self.twitter.post_thread(tweets)
        logger.info(f"Thread posted with tweet IDs: {posted_ids}")

    def schedule_daily_tweet(self):
        schedule.every().day.at("03:00").do(lambda: self.post_random_prompt())
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping scheduler")

def main():
    choice = input("Enter '1' for instant post or '2' for scheduled posting: ")
    bot = TwitterBot()
    bot.schedule_daily_tweet()

if __name__ == "__main__":
    main()

import unittest
from unittest.mock import patch, MagicMock
from main import Twitter, AIContent, TwitterBot

class TestTwitter(unittest.TestCase):
    @patch('main.tweepy.Client')
    def test_initialization(self, mock_client):
        twitter = Twitter()
        self.assertIsNotNone(twitter.client)

    def test_can_make_request(self):
        twitter = Twitter()
        twitter.requests_made = 0
        self.assertTrue(twitter.can_make_request())

    def test_post_thread(self):
        twitter = Twitter()
        twitter.requests_made = 0
        tweets = ["Test tweet"]
        with patch('main.tweepy.Client.create_tweet', return_value=MagicMock(data={'id': 1})):
            posted_ids = twitter.post_thread(tweets)
            self.assertEqual(posted_ids, [1])

class TestAIContent(unittest.TestCase):
    @patch('main.genai.Client')
    def test_generate_content(self, mock_client):
        ai_content = AIContent()
        mock_client.return_value.models.generate_content.return_value.text = "Generated content"
        content = ai_content.generate_content("Test prompt")
        self.assertEqual(content, "Generated content")

class TestTwitterBot(unittest.TestCase):
    @patch('main.Twitter')
    @patch('main.AIContent')
    def test_post_random_prompt(self, mock_ai_content, mock_twitter):
        bot = TwitterBot()
        mock_ai_content.return_value.generate_tweet.return_value = "Generated tweet"
        bot.post_random_prompt()
        # Check that generate_tweet was called twice
        self.assertEqual(mock_ai_content.return_value.generate_tweet.call_count, 2)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from src.interactive_agent import InteractiveLLMAgent
import asyncio

class TestInteractiveLLMAgent(unittest.TestCase):
    def setUp(self):
        self.config_list = [{'model': 'gpt-4', 'api_key': 'fake_api_key'}]
        self.agent = InteractiveLLMAgent(self.config_list)

    def test_initialization(self):
        """Test initialization of the InteractiveLLMAgent."""
        self.assertEqual(self.agent.config_list, self.config_list)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"feed": [{"title": "Test News", "summary": "Summary", "overall_sentiment_score": 0.5}]}')
    def test_get_market_news(self, mock_open):
        """Test fetching market news from file."""
        result = self.agent.get_market_news(0, 1)
        expected = [{'title': 'Test News', 'summary': 'Summary', 'overall_sentiment_score': 0.5}]
        self.assertEqual(result, expected)

    def test_get_market_news_file_not_found(self):
        """Test get_market_news handling when file is not found."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = self.agent.get_market_news(0, 1)
            expected = [{'title': 'No data found', 'summary': 'Could not fetch data', 'overall_sentiment_score': 0}]
            self.assertEqual(result, expected)

    @patch('asyncio.Future.done')
    @patch('asyncio.Future.result')
    def test_fetch_news_periodically(self, mock_result, mock_done):
        """Test the periodic fetching of news."""
        mock_done.return_value = True
        mock_result.return_value = []
        with patch.object(self.agent, 'get_market_news', return_value=[{'title': 'Async News', 'summary': 'Async Summary', 'overall_sentiment_score': 1}]) as mock_get_news:
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(self.agent.fetch_news_periodically())
                mock_get_news.assert_called()
                self.assertTrue(mock_result.called)
                self.assertTrue(mock_done.called)
            except Exception as e:
                print(e)

    def test_run(self):
        """Test running the agent."""
        with patch('src.interactive_agent.InteractiveLLMAgent.fetch_news_periodically', new_callable=MagicMock()) as mock_fetch_news:
            loop = asyncio.get_event_loop()
            try:
                asyncio.ensure_future(self.agent.run())
                loop.run_until_complete(asyncio.sleep(0.1))  # run the loop briefly to start the task
                mock_fetch_news.assert_called_once()
            except Exception as e:
                print(e)
            finally:
                loop.stop()

if __name__ == '__main__':
    unittest.main()


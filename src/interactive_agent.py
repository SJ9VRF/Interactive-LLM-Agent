import asyncio
import json
import requests

class InteractiveLLMAgent:
    def __init__(self, config_list):
        self.config_list = config_list
        self.data = asyncio.Future()

    def get_market_news(self, ind, ind_upper):
        """Fetches market news within a given index range from a local JSON for simulation.
        In a real application, replace this with a function to fetch data from a web API.
        """
        try:
            with open('data/market_news_sample.json', 'r') as file:
                data = json.load(file)
            feeds = data["feed"][ind:ind_upper]
            return feeds
        except FileNotFoundError:
            return [{"title": "No data found", "summary": "Could not fetch data", "overall_sentiment_score": 0}]

    async def fetch_news_periodically(self):
        """Simulates the periodic fetching of market news data."""
        index = 0
        while True:
            if index >= len(self.config_list):  # Reset index to simulate continuous cycle
                index = 0
            feeds = self.get_market_news(index, index + 1)
            if self.data.done():
                self.data.result().extend(feeds)
            else:
                self.data.set_result(feeds)
            await asyncio.sleep(5)  # Wait for 5 seconds before fetching next news item
            index += 1

    async def run(self):
        """Runs the agent to continuously fetch and process data."""
        print("Agent started. Fetching market news...")
        task = asyncio.create_task(self.fetch_news_periodically())
        try:
            while True:
                if self.data.done():
                    latest_data = self.data.result()
                    self.data = asyncio.Future()  # Reset future for the next data
                    print("Latest market news:")
                    for news in latest_data:
                        print(f"Title: {news['title']}, Summary: {news['summary']}, Sentiment: {news['overall_sentiment_score']}")
                await asyncio.sleep(10)  # Check every 10 seconds if there's new data
        except asyncio.CancelledError:
            task.cancel()
            print("Agent stopped.")

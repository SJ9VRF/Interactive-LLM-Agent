from interactive_agent import InteractiveLLMAgent

def main():
    config_list = [{'model': 'gpt-4', 'api_key': 'your_api_key_here'}]
    agent = InteractiveLLMAgent(config_list)
    agent.run()

if __name__ == "__main__":
    main()


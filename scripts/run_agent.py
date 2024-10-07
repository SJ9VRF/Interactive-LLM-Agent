import sys
import os

# Add the project src directory to the Python path to enable imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from interactive_agent import InteractiveLLMAgent

def run_agent():
    # Define the configuration list for the agent; this should ideally be secured or dynamically retrieved
    config_list = [
        {
            'model': 'gpt-4', 
            'api_key': 'your_openai_api_key_here'
        }
    ]

    # Create an instance of the agent with the configuration
    agent = InteractiveLLMAgent(config_list)

    # Run the agent
    try:
        agent.run()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping the agent.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    run_agent()


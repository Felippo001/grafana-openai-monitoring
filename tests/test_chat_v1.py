
"""
Test module for chat_v1 function.
"""

import os
import openai
from grafana_openai_monitoring import chat_v1

def test_chat_v1():
    """
    Test the chat_v1 functionality with OpenAI API.

    This test function sets up the OpenAI API with monitoring using the chat_v1 decorator,
    sends a sample chat message, and asserts the response.

    Make sure you have the required environment variables set:
    - OPENAI_API_KEY
    - PROMETHEUS_URL
    - LOKI_URL
    - PROMETHEUS_USERNAME
    - LOKI_USERNAME
    - GRAFANA_CLOUD_ACCESS_TOKEN
    """

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Apply the custom decorator to the OpenAI API function
    openai.Completion.create = chat_v1.monitor(
        openai.Completion.create,
        metrics_url=os.getenv("PROMETHEUS_URL"),
        logs_url=os.getenv("LOKI_URL"),
        metrics_username=os.getenv("PROMETHEUS_USERNAME"),
        logs_username=os.getenv("LOKI_USERNAME"),
        access_token=os.getenv("GRAFANA_CLOUD_ACCESS_TOKEN")
    )

    # Now any call to openai.Completion.create will be automatically tracked
    response = openai.Completion.create(model="davinci", prompt="Hello world", max_tokens=10)

    assert response['object'] == 'text_completion'

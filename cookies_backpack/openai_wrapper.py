"""
OpenAI API を叩きます。
※ あらかじめ .env に以下を記入しておく必要があります。
OPENAI_API_ORG="******"
OPENAI_API_KEY="******"
"""
import openai
from dotenv import load_dotenv
import os


class OpenAIWrapper:
    def __init__(self):
        load_dotenv()
        openai.organization = os.getenv('OPENAI_API_ORG')
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI()
    def request(self, prompt):
        res = self.client.responses.create(model='gpt-4o', input=prompt)
        return res.output_text

import g4f
from g4f.client import Client

class GroqClient:
    def __init__(self):
        self.client = None

    def initialize(self, api_key):
        # g4f does not require API key initialization, so this is a placeholder
        self.client = Client()

    def generate_completion(self, prompt, model="gpt-4o"):  # Model name is symbolic for g4f
        if not self.client:
            raise ValueError("Client not initialized.")

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Error generating completion: {str(e)}")
from litellm import completion
import logging

class HuggingFaceAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.validate_api_key()

    def validate_api_key(self):
        if not self.api_key:
            logging.error("Hugging Face API key is missing.")
            raise ValueError("Hugging Face API key is missing.")
        logging.info("Hugging Face API key is valid.")

    def generate_comment(self, code):
        response = completion(
            model="huggingface/model-name",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a comment for the following code:\n{code}"}
            ],
            api_key=self.api_key
        )
        return response['choices'][0]['message']['content']

    def generate_documentation(self, code):
        response = completion(
            model="huggingface/model-name",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate documentation for the following code:\n{code}"}
            ],
            api_key=self.api_key
        )
        return response['choices'][0]['message']['content']

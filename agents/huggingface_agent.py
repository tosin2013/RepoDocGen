from litellm import completion

class HuggingFaceAgent:
    def __init__(self, api_key):
        self.api_key = api_key

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

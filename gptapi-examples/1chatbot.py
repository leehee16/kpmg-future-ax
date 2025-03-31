import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv('open_api_key')

if api_key is None:
    raise ValueError("API key is not set. Check your .env file.")

# Initialize OpenAI client with the API key
openai.api_key = api_key

print("Authentication successful")

# Send a message to the GPT model
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a chatbot specialized in recommending movies in the romance, melodrama, comedy, and superhero genres."},
        {"role": "user", "content": "I like Iron Man. Can you recommend similar movies?"}
    ]
)

# Print the response content
print(response['choices'][0]['message']['content'])

# Keep the conversation going until the user decides to quit
while True:
    user_input = input("Enter your message (or 'q' to quit): ")
    if user_input.lower() == 'q':
        print("Ending conversation.")
        break
    
    # Send user's message to the GPT model
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    # Print the response content
    print("AI:", response['choices'][0]['message']['content'])

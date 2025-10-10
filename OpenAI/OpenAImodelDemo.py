import openai
openai.api_key = "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"
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful writing assistant."},
        {"role": "user", "content": "Write a short poem about the ocean."}
    ],
    temperature=0.7,
    max_tokens=300
)
print(response['choices'][0]['message']['content'])
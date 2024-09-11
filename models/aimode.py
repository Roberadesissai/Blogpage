# models/aimode.py

from openai import OpenAI

YOUR_API_KEY = "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"


def get_ai_response(user_message):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    try:
        # chat completion without streaming
        response = client.chat.completions.create(
            model="llama-3-sonar-large-32k-online",
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in AI response generation: {str(e)}")
        return f"An error occurred: {str(e)}"


# Uncomment this if you want to use streaming
# def get_ai_response_stream(user_message):
#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "You are an artificial intelligence assistant and you need to "
#                 "engage in a helpful, detailed, polite conversation with a user."
#             ),
#         },
#         {
#             "role": "user",
#             "content": user_message,
#         },
#     ]
#
#     client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")
#
#     try:
#         # chat completion with streaming
#         response_stream = client.chat.completions.create(
#             model="llama-3-sonar-large-32k-online",
#             messages=messages,
#             stream=True,
#         )
#         for response in response_stream:
#             yield response.choices[0].delta.content
#     except Exception as e:
#         print(f"Error in AI response generation: {str(e)}")
#         yield f"An error occurred: {str(e)}"

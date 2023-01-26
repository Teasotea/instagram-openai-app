import openai
import os

# Set up the OpenAI API client
openai.api_key = os.environ.get('OPENAI_API')

# Set up the model and prompt
model_engine = "text-davinci-003"


def generateComment(user, post):
    #Build prompt
    prompt =  f'As {user}, respond to {post}'

    print("Prompt :\n", prompt)

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response


if __name__ == "__main__":
    user = 'Instagram'
    post = 'Thanks for helping with organising event! It was nice to work with you!'#"How you doin?"

    reply = generateComment(user, post)

    print("Reply:\n", reply)
